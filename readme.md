# MakeQR

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

```bash
makeqr wifi --help
```

## Command line command

### Command

```bash
makeqr -p wifi --ssid ABC --password Tfsjfklasdjfklasdest -s wpa2
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

DATA MODEL
{"ssid": "ABC", "security": "wpa2", "password": "Tfsjfklasdjfklasdest", "hidden": false}

QR STRING
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

```python
from makeqr import MakeQR, QRMailToModel

model = QRMailToModel(
  to='foo@bar.baz',
  subject='Awesome subject!',
)
qr = MakeQR(model)
data: bytes = qr.make_image_data()
```
