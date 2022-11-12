# wifi_qrcode

Generate WiFi Access QR Codes

# Installation

```bash
pip install makeqr -U
```

# Usage example

## To test that installation was successful, try:

```bash
makeqr --help
```

or

```
makeqr wifi --help
```

## Command line command

### Command

```bash
makeqr -p wifi --ssid ABC --password Tfsjfklasdjfklasdest -s wpa2
```

### Output

```
DATA MODEL
  {"ssid": "ABC", "security": "wpa2", "password": "Tfsjfklasdjfklasdest", "hidden": false}
ENCODED QR DATA
  WIFI:S:ABC;P:Tfsjfklasdjfklasdest;T:WPA;;
RESULT

  ██████████████        ████  ██████  ██████  ██████████████
  ██          ██    ██  ██████████        ██  ██          ██
  ██  ██████  ██  ██████  ██  ██      ████    ██  ██████  ██
  ██  ██████  ██  ██  ██      ██  ████    ██  ██  ██████  ██
  ██  ██████  ██  ██    ██    ██    ████████  ██  ██████  ██
  ██          ██  ██  ██████    ██  ████  ██  ██          ██
  ██████████████  ██  ██  ██  ██  ██  ██  ██  ██████████████
                  ██  ██████    ████  ██
  ██  ██████████      ██      ████████        ██████████
        ██  ██  ██  ██    ██    ████  ██████  ██  ██  ████
  ██    ██  ████████    ████    ██████      ████  ████
  ██████    ██  ██  ██  ██    ██      ██  ██████  ██    ████
  ██          ██  ████  ██  ██    ████  ██      ████████
        ██  ██    ██████  ██████    ████████    ████  ████
    ██  ████  ████  ██████  ██  ██  ████  ██    ██    ██
    ████  ████          ██    ██████    ██  ██      ██
    ██████    ██  ████████████  ██████  ██      ██  ██  ████
  ██      ████        ██    ████  ██████████████  ██    ██
  ██      ██  ████    ██  ████  ████            ██  ████
  ██  ██████        ██████    ██      ██████████  ██      ██
  ██  ████  ██████      ████    ██████    ██████████████
                  ██  ██    ██    ██  ██  ██      ██  ██
  ██████████████      ██  ██████████  ██████  ██  ██  ██
  ██          ██  ████  ██  ██  ████    ████      ████
  ██  ██████  ██  ██  ██      ████  ██    ██████████    ████
  ██  ██████  ██  ██    ████      ██      ██      ██    ████
  ██  ██████  ██  ██    ██    ████  ████  ██  ████████  ██
  ██          ██    ██  ██    ██████      ████      ██  ██
  ██████████████  ██  ██        ██  ██  ██    ██  ██
```

## Docker container

```bash
docker run ghcr.io/shpaker/makeqr:4.0.1 -p link https://t.me/shpaker

```

## As python module

```bash
from makeqr import MakeQR, QRMailToModel

model = QRMailToModel(
  to='foo@bar.baz',
  subject='Awesome subject!',
)
qr = MakeQR(model)
data: bytes = qr.make_image_data()
```
