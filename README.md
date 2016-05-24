# jvc-remote

Remote control library and tiny web server for JVC projectors that communicate over RS232.

## Dependencies

* pyserial for communication with projector -- `pip install serial`

## Usage

### Python Library
You can use the included `projector.py` as a library. This might end up on pip in the future.

#### Web Remote

It provides both a web interface, as well as a JSON API for interacting with the projector.

![Changing source](/../screens/screens/source.png?raw=true) ![Changing presets](/../screens/screens/adjust.png?raw=true) ![Main remote](/../screens/screens/main.png?raw=true) 

The webserver should be provided with the path to the serial port. It will then host on port `5000`.

#### JSON API

All endpoints are currently GET.

* `/on`, `/off` - turn the projector on and off.
* `/status` - returns current power state, current input source (if any) and model number.
* `/input/<source>` - sets the input source to <source>. You can list the available input sources using:
* `/inputs` - lists available input source types and display names.
* `/press/<button>` - simulate a remote control button press. You can list available button names using:
* `/buttons` - lists available button names for the projector.

Routes will return 200 on success *or* failure (check `success` field in returned JSON objects), 404 if a particular button or input source is unknown, or 501 if the projector is unavailble (disconnected or uncommunicable).

## Running on OpenWRT

This was tested on OpenWrt Chaos Calmer 15.05.1.

Log into SSH, and do:
```
opkg install python-pyserial # auto-installes python-lite
opkg install python-logging # needed for BaseHTTPServer
opkg install python-codecs # needed for JSON - big
```

You'll also want to install the USB serial converter driver that you use. Some common ones:
```
opkg install kmod-usb-serial
opkg install kmod-usb-serial-ftdi
opkg install kmod-usb-serial-cp210x
opkg install kmod-usb-serial-ch341
opkg install kmod-usb-serial-pl2303
```

and finally, `opkg install unzip`. Download the master tarball somewhere that doesn't require HTTPS, then wget it onto the router and unzip. Then just run `server.py /dev/ttyUSB0` as usual.

It might take a while at the start, and you'll get a bunch of `ValueError: unsupported hash type sha512` messages in the meantime, but don't fear.

## Device support

### Tested
* DLA-HD250

### Untested

Should work fine, but possibly missing some additional remote buttons and direct commands):

* DLA-HD350
* DLA-HD750
* DLA-HD550
* DLA-HD950
* DLA-HD990
* DLA-X3
* DLA-X7
* DLA-X9
* DLA-X30
* DLA-X70R
* DLA-X90R
* DLA-RS10
* DLA-RS15
* DLA-RS20
* DLA-RS25
* DLA-RS35
* DLA-RS40
* DLA-RS45
* DLA-RS50
* DLA-RS55
* DLA-RS60
* DLA-RS65

## License

The MIT License (MIT)

Copyright (c) 2016 Alex Hixon alex@alexhixon.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.