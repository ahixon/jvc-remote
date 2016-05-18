# jvc-remote

Remote control library and web server for JVC projectors.

## Dependencies

* pyserial for communication with projector -- `pip install serial`
* (optionally) Flask for web remote -- `pip install flask`

## Usage

You can use the included projector.py as a library. This might end up on pip in the future.

The webserver should be provided with the path to the serial port. It will then host on port 5000.

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
