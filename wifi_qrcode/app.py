from enum import Enum, unique
from os import getcwd
from os import path
from typing import Optional, Union

from fire import Fire
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage

from wifi_qrcode import AuthType, ImageFormat
from wifi_qrcode.makers import make_wifi, make_mailto
from wifi_qrcode.utils import make_image

DEFAULT_FILE_NAME: str = 'qrcode'
DEFAULT_FILE_FORMAT: ImageFormat = ImageFormat.PNG

QR_FILL_COLOR: str = 'black'
QR_BACK_COLOR: str = 'white'


@unique
class ValidateInputStatus(Enum):
    SUCCESS = 0
    WIFI_UNKNOWN_AUTH_TYPE = 1
    WIFI_EMPTY_PASSWORD = 2


class App:
    def __init__(self) -> None:
        self.status: ValidateInputStatus = ValidateInputStatus.SUCCESS
        self.file_format: Optional[ImageFormat] = None
        self.file_path: Optional[str] = None

    def _parse_file_name(self, file_name: str) -> str:
        try:
            file_ext = file_name.split('.')[-1]
            self.file_format = ImageFormat[file_ext.upper()]
        except KeyError:
            self.file_format = DEFAULT_FILE_FORMAT
            file_name = f'{file_name}.{DEFAULT_FILE_FORMAT.name.lower()}'

        self.file_path = path.join(getcwd(), file_name)

        print(f'Format: {self.file_format.name}')
        print(f'Path: {self.file_path}')

        return self.file_path

    def _save(self, img: Union[PilImage, SvgImage]) -> None:
        print(f'Status: {self.status.name}')

        with open(self.file_path, 'wb') as file:
            img.save(file)

        exit(self.status.value)

    def wifi(self,
             ssid: Union[str, int],
             auth: str = AuthType.WPA.name,
             password: Optional[Union[str, int]] = None,
             hidden: bool = False,
             output: str = DEFAULT_FILE_NAME) -> None:

        self._parse_file_name(output)

        auth_type = AuthType.nopass

        try:
            auth_type = AuthType[auth.upper()]

            if auth_type is not AuthType.nopass and not password:
                self.status = ValidateInputStatus.WIFI_EMPTY_PASSWORD
        except KeyError:
            self.status = ValidateInputStatus.WIFI_UNKNOWN_AUTH_TYPE

        if self.status is ValidateInputStatus.SUCCESS:
            data = make_wifi(ssid=ssid,
                             auth=auth_type,
                             password=password,
                             hidden=hidden)

            print(f'Data: {data}')

            img = make_image(data=data,
                             file_format=self.file_format,
                             fill_color=QR_FILL_COLOR,
                             back_color=QR_BACK_COLOR)

            self._save(img)

    def mailto(self,
               to: str,
               subject: Optional[str] = None,
               cc: Optional[str] = None,
               bcc: Optional[str] = None,
               body: Optional[str] = None,
               output: str = DEFAULT_FILE_NAME) -> None:

        self._parse_file_name(output)

        if cc:
            cc = cc.split(',')

        if bcc:
            bcc = bcc.split(',')

        data = make_mailto(to=to, subject=subject, cc=cc, bcc=bcc, body=body)

        print(f'Data: {data}')

        img = make_image(data=data,
                         file_format=self.file_format,
                         fill_color=QR_FILL_COLOR,
                         back_color=QR_BACK_COLOR)

        self._save(img)


def main():
    app = App()
    Fire(app)


if __name__ == '__main__':
    main()
