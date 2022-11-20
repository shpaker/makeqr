# MakeQR

[![PyPI](https://img.shields.io/pypi/v/makeqr.svg)](https://pypi.python.org/pypi/makeqr)
[![PyPI](https://img.shields.io/pypi/dm/makeqr.svg)](https://pypi.python.org/pypi/makeqr)

Generate WiFi Access QR Codes

# Installation

```bash
pip install makeqr -U
```

## To test that installation was successful, try:

```bash
makeqr --help
```

or

```bash
makeqr wifi --help
```

# Usage example

## Command line command

### Command

```bash
makeqr -v wifi --password TopSecret --security wpa2 HomeWiFi
```

### Output

```plain
 __   __  _______  ___   _  _______  _______  ______
|  |_|  ||   _   ||   | | ||       ||       ||    _ |
|       ||  |_|  ||   |_| ||    ___||   _   ||   | ||
|       ||       ||      _||   |___ |  | |  ||   |_||_
|       ||       ||     |_ |    ___||  |_|  ||    __  |
| ||_|| ||   _   ||    _  ||   |___ |      | |   |  | |
|_|   |_||__| |__||___| |_||_______||____||_||___|  |_|

Model: {"ssid": "HomeWiFi", "security": "wpa2", "password": "TopSecret", "hidden": false}
Encoded: WIFI:S:HomeWiFi;P:TopSecret;T:WPA;;
                                                              
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

## Docker container

```bash
docker run ghcr.io/shpaker/makeqr:4.0.1 link https://t.me/shpaker
```

## As python module

```python
from makeqr import MakeQR, QRMailToModel

qr = MakeQR(
  model = QRMailToModel(
    to='foo@bar.baz',
    subject='Awesome subject!',
  )
)
data: bytes = qr.make_image_data()
```
