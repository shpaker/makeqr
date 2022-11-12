# wifi_qrcode

Generate WiFi Access QR Codes

# Installation

```bash
pip install makeqr -U
```

# Usage example

To test that installation was successful, try:

```bash
makeqr --help
makeqr wifi --help
```

Usage from the command line:

```bash
makeqr -o 123.jpg wifi --ssid ABC --password Tfsjfklasdjfklasdest -s wpa2
```

... or as python module:

```bash
python -m makeqr wifi --ssid MYWIRELESSNETWORK --auth WPA --password SECRET
python -m makeqr mailto --to user@mail.org --subject "Mail from QR"
```

... or as docker container:

```bash
docker run ghcr.io/shpaker/makeqr wifi --ssid MYWIRELESSNETWORK --auth WPA --password SECRET
```

# Features

- [x] geo
- [x] link
- [x] mailto
- [x] sms
- [x] tel
- [x] wifi
