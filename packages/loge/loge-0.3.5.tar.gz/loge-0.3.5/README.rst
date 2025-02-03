
Loge - Easy and fast generation of interactive reports with Python
------------------------------------------------------------------


Changelog
---------
Loge 0.3.5 (beta stage)

- tested / updated for python 3.12 compatibility

Loge 0.3.4 (beta stage)

- dxf file graphics displaying
- anastruct support added
- embedding image from clipboard

Loge 0.3.3 (beta stage)

- Greek letters added to code editor
- updated to current pyqt5 version
- mistune v1 version required - mistune 0.8.4 version specified in setup.py

Loge 0.3.1 (beta stage)

- synchronize scrolling option
- saving scrolls positions
- ask to save job when file is closing
- don't need save file to start
- file browser added

Loge 0.2.3 (beta stage)

- editor added

- user interface updated

Loge 0.1.9 (alpha stage)

- first public release

Description
-----------

Loge is a tool for crating dynamic reports with Python. Report source is written in python with some additional special syntax where you can define report content and format.

Installation
------------

Minimal Loge requirements:

1. Python 3
2. pyqt5
3. mistune
4. pillow

Optional Loge dependencies (to make all Loge features available):

1. unum
2. matplotlib
3. svgvrite
4. pillow
5. tabulate
6. dxf2svg
7. anastruct

Loge is available through PyPI and can be install with pip command. To install Loge with minimal requirements use pip by typing ::

    pip install loge

You can install optional dependencies by taping: ::

    pip install unum matplotlib svgwrite pillow tabulate dxf2svg anastruct

To run Loge use command: ::

    loge

Please find more information about installing process at project website.

Tested python versions 3.11, 3.12 (tested on January 2025). Python versions 3.9, 3.10 should work as well.

License
-------

Copyright (C) 2017-2025, the Loge development team

Loge is distributed under the terms of GNU General Public License

The full license can be found in 'license.txt'

Loge development team can be found in 'development.txt'

About us
--------

The development of Loge is coordinated by Lukasz Laba. See development.txt file for a complete list of people who helped develop Loge.

Contributions
-------------

If you want to help out, create a pull request or start a discussion in our group forum.

More information
----------------

Project website: https://loge.readthedocs.io

Google group forum: https://groups.google.com/d/forum/python_loge

Code repository: https://bitbucket.org/lukaszlaba/loge

Contact: Lukasz Laba <lukaszlaba@gmail.com>