# SnapRip

SnapRip parses C64 Vice snapshots and extracts koala or hires images, sprites, font and petscii from it.
As of now, this is a commandline-tool.
It runs on 64 bit versions of Linux, MacOS, Windows and other systems supported by Python. 


# Why SnapRip?

reason | description
---|---
open source | easy to modify and to improve, any useful contribution is highly welcome
portable | available on Linux, MacOS, Windows and any other system supported by Python3
simple | easy to use


# Usage

    snaprip v2.00 [27.02.2022] *** by fieserWolF
    usage: snaprip.py [-h] snapshot output

    This script parses C64 Vice snapshots and extracts koala or hires images, sprites, font and petscii from it.

    positional arguments:
      snapshot    snapshot file
      output      output filename

    optional arguments:
      -h, --help  show this help message and exit

    Example: ./snaprip.py snapshot.vsf test


Have a good look in /doc.


# Output file formats


## Koala image

offset|length|data
---|---|---
0|2|start address $6000 (high, low)
2|8000|bitmap
8002|1000|screen
9002|1000|colorram $d800
10002|1|background color $d021


## Hires image

offset|length|data
---|---|---
0|2|start address $6000 (high, low)
2|8000|bitmap
8002|1000|screen
9002|1|border color $d020


## PETSCII image standard ROM font

offset|length|data
---|---|---
0|2|start address $3000 (high, low)
2|1000|screen
1002|1000|colorram $d800
2002|1|background color $d021
2003|1|border color $d020


## PETSCII image with custom font

offset|length|data
---|---|---
0|2|start address $3000 (high, low)
2|2048|font
2050|1000|screen
3050|1000|colorram $d800
4050|1|background color $d021
4051|1|border color $d020


## Spriteset

offset|length|data
---|---|---
0|2|start address $2000 (high, low)
2|64|sprite 1 + 1 byte $00
66|64|sprite 2 + 1 byte $00
130|64|sprite 3 + 1 byte $00
194|64|sprite 4 + 1 byte $00
258|64|sprite 5 + 1 byte $00
322|64|sprite 6 + 1 byte $00
386|64|sprite 7 + 1 byte $00
450|64|sprite 8 + 1 byte $00



# Author

* fieserWolF/Abyss-Connection - *code* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)


# Getting Started

Clone the git-repository to your computer:
```
git clone https://github.com/fieserWolF/snaprip.git
```

Start the python script:
```
python3 snaprip.py --help
```



## Prerequisites

At least this is needed to run the script directly:

- python 3
- argparse

Normally, you would use pip like this:
```
pip3 install argparse
```

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt-get update
apt-get install python3 python3-argh
```
# Changelog

## Future plans

- maybe: implement other exports

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:

[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)


## Changes in 2.00

- complete re-write in python3


## Changes in 1.00

- initial release written in FreePascal

# License

_SnapRip - C64 Vice Emulator Snapshop Parser._

_Copyright (C) 2022 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3 and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


