# wifi_qrcode
Generate WiFi Access QR Codes

# Installation

```bash
pip install wifi_qrcode
```

# Usage example

```bash
wifi_qrcode --ssid MYWIRELESSNETWORK --auth WPA --password SECRET
```

# Arguments

## Required

* `--ssid` Network SSID

## Optional

* `--auth` Authentication type; can be WEP or WPA, or 'nopass' for no password
* `--password` Password, ignored if `--auth` is "nopass" 
* `--hidden` True if the network SSID is hidden.
* `--output` QR-code file
