# MakeQR

[![PyPI](https://img.shields.io/pypi/v/makeqr.svg)](https://pypi.python.org/pypi/makeqr)
[![Downloads](https://img.shields.io/pypi/dm/makeqr.svg)](https://pypi.python.org/pypi/makeqr)
[![Python](https://img.shields.io/pypi/pyversions/makeqr.svg)](https://pypi.python.org/pypi/makeqr)
[![Test](https://github.com/shpaker/makeqr/actions/workflows/tests.yml/badge.svg)](https://github.com/shpaker/makeqr/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/makeqr.svg)](https://github.com/shpaker/makeqr/blob/main/LICENSE)

Generate QR codes for links, WiFi networks, geo points, e-mail, SMS and plain
text — from the command line or from Python.

## Installation

```bash
pip install makeqr -U
```

Or, with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install makeqr
```

To run it without installing anything:

```bash
uvx makeqr --help
```

## Commands

| Command  | Encodes                | Example                                              |
|----------|------------------------|------------------------------------------------------|
| `link`   | A URL                  | `makeqr link https://example.com`                     |
| `wifi`   | WiFi network access    | `makeqr wifi -s wpa -p s3cret HomeWiFi`               |
| `geo`    | Geographic coordinates | `makeqr geo -lat 55.75 -long 37.61`                   |
| `mailto` | A pre-filled e-mail    | `makeqr mailto -s Hello to@example.com`               |
| `sms`    | A pre-filled SMS       | `makeqr sms -r +79876543210 -b 'on my way'`           |
| `tel`    | A phone number         | `makeqr tel +79876543210`                             |
| `text`   | Arbitrary text         | `makeqr text 'hello world'`                           |

The scheme may be omitted from a link — `makeqr link example.com` encodes
`https://example.com`.

Run `makeqr <command> --help` for the options of a single command.

## Global options

Global options go **before** the command name:

```bash
makeqr -o code.png -e high wifi --security wpa --password s3cret HomeWiFi
```

| Option                    | Default  | Description                                            |
|---------------------------|----------|--------------------------------------------------------|
| `-o`, `--output`          | —        | Write the image here; the extension picks the format   |
| `-e`, `--error-correction`| `medium` | `low`, `medium`, `quartile` or `high`                    |
| `-s`, `--box-size`        | `8`      | Pixel size of a single QR module                       |
| `-b`, `--border`          | `1`      | Width of the quiet zone, in modules                    |
| `-v`, `--verbose`         | off      | Print the model and the encoded payload                |
| `-q`, `--quiet`           | off      | Do not print the QR code to the terminal               |
| `-V`, `--version`         | —        | Show the version and exit                              |

Without `--output` the code is only printed to the terminal. Passwords are
masked in verbose output.

## Usage example

```bash
makeqr -v wifi --password TopSecret --security wpa HomeWiFi
```

```plain
 __   __  _______  ___   _  _______  _______  ______
|  |_|  ||   _   ||   | | ||       ||       ||    _ |
|       ||  |_|  ||   |_| ||    ___||   _   ||   | ||
|       ||       ||      _||   |___ |  | |  ||   |_||_
|       ||       ||     |_ |    ___||  |_|  ||    __  |
| ||_|| ||   _   ||    _  ||   |___ |      | |   |  | |
|_|   |_||__| |__||___| |_||_______||____||_||___|  |_|

Model: {"ssid":"HomeWiFi","security":"wpa","password":"**********","hidden":false}
Encoded: WIFI:S:HomeWiFi;P:***;T:WPA;;
                                                              
  ██████████████  ████    ██████  ██  ██      ██████████████  
  ██          ██    ██████████████      ██    ██          ██  
  ██  ██████  ██      ██      ██    ██████    ██  ██████  ██  
  ██  ██████  ██  ██████          ██  ██  ██  ██  ██████  ██  
  ██  ██████  ██  ██    ████          ████    ██  ██████  ██  
  ██          ██  ██  ████        ██████████  ██          ██  
  ██████████████  ██  ██  ██  ██  ██  ██  ██  ██████████████  
                  ████  ██████    ██████                      
  ██      ██  ██████████    ██  ██████  ██  ██████████    ██  
  ██    ██      ██    ████  ██████            ████████        
    ██████████████      ████    ██        ████    ████    ██  
  ██        ██  ████    ██    ██  ████  ████  ██        ██    
    ██████    ██    ██      ██████████    ████  ████    ██    
  ██    ██        ████    ██    ██    ██        ██████        
  ████████    ████    ████████████  ████      ██      ██  ██  
            ██  ██      ██  ██  ████████  ████      ██    ██  
      ██      ██    ██    ████      ██  ██  ██        ██  ██  
  ██    ██      ██      ████████  ██    ██    ██████████      
      ██    ████  ████  ██      ████████    ██      ████  ██  
        ██████  ████████████  ████████  ██    ██  ██          
  ████    ██  ██  ██      ██████  ██████  ██████████    ██    
                  ██████  ██      ████    ██      ████  ██    
  ██████████████  ██        ██████      ████  ██  ██  ██  ██  
  ██          ██        ██  ██      ████  ██      ████        
  ██  ██████  ██  ██  ██  ████    ██    ████████████████      
  ██  ██████  ██              ██  ██    ████        ██    ██  
  ██  ██████  ██    ██          ████████                ████  
  ██          ██            ████  ████  ██  ██    ████  ████  
  ██████████████  ████████    ██████████  ████████  ██  ██    
                                                              
```

## Docker

```bash
docker run --rm ghcr.io/shpaker/makeqr:latest link https://t.me/shpaker
```

To keep the generated file, mount a directory and write into it:

```bash
docker run --rm -v "$PWD:/out" ghcr.io/shpaker/makeqr:latest -o /out/code.png link https://example.com
```

## As a Python module

```python
from makeqr import MakeQR, QRMailToModel

qr = MakeQR(
    QRMailToModel(
        to="foo@bar.baz",
        subject="Awesome subject!",
    )
)

data: bytes = qr.make_image_data()  # PNG bytes
qr.save("mail.png")                 # or straight to a file
```

Every model exposes the payload it encodes:

```python
>>> from makeqr import QRWiFiModel
>>> QRWiFiModel(ssid="HomeWiFi", security="wpa", password="TopSecret").qr_data
'WIFI:S:HomeWiFi;P:TopSecret;T:WPA;;'
```

## Development

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just).

```bash
uv sync          # create the environment
just lint        # ruff, formatting and ty
just test        # pytest with coverage
just fix         # auto-fix and format
```

Optionally, install the git hooks with [prek](https://github.com/j178/prek):

```bash
uv tool install prek
just hooks
```

## License

[MIT](LICENSE)
