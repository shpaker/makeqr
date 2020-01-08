from enum import Enum, unique
from os import getcwd
from os import path
from typing import Optional

from fire import Fire

from wifi_qrcode import AuthType, FileFormat, save_wifi_qrcode

DEFAULT_FILE_NAME: str = 'wifi_qrcode'
DEFAULT_FILE_FORMAT: FileFormat = FileFormat.PNG


@unique
class ValidateInputStatus(Enum):
    Success = 0
    UnknownAuthType = 1
    EmptyPassword = 2


def fire_app(ssid: str,
             auth: str = AuthType.nopass.name,
             password: Optional[str] = None,
             hidden: bool = False,
             output: str = DEFAULT_FILE_NAME) -> None:

    status = ValidateInputStatus.Success
    auth_type = AuthType.nopass

    try:
        auth_type = AuthType[auth]

        if auth_type is not AuthType.nopass and not password:
            status = ValidateInputStatus.EmptyPassword
    except KeyError:
        status = ValidateInputStatus.UnknownAuthType

    try:
        file_ext = output.split('.')[-1]
        file_format = FileFormat[file_ext.upper()]
    except KeyError:
        file_format = DEFAULT_FILE_FORMAT
        output = f'{output}.{DEFAULT_FILE_FORMAT.name.lower()}'

    file_path = path.join(getcwd(), output)

    if status is ValidateInputStatus.Success:
        save_wifi_qrcode(ssid=ssid,
                         auth=auth_type,
                         password=password,
                         hidden=hidden,
                         file_format=file_format,
                         file_path=file_path)

    print(f'Format: {file_format.name}')
    print(f'Path: {file_path}')
    print(f'Status: {status.name}')

    exit(status.value)


def main():
    Fire(fire_app)


if __name__ == '__main__':
    main()
