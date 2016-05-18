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

## License

The MIT License (MIT)

Copyright (c) 2016 Alex Hixon alex@alexhixon.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.