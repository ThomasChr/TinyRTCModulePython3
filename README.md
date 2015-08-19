# TinyRTCModulePython
Python Codes for Access to the DS1307 and AT24C32 I2C ICs which are on the "Tiny RTC Module"

Preperations fpr the Pi to activate I2C-Bus:
Simply start 'raspi-config' (as root) go to "Advanced Options" and enable the automatic load of the I2C-Interface.

Preparations for the module to work with a Raspberry Pi (Pullup Resistors R2 + R3 need to be removed to not fry your Pi) and a CR2032-Battery (loading circuit needs to be removed (CR2032 is not rechargable) and Voltage Divider for powering the DS1307 BAT-Pin need to be removed).
Fix is from this page: http://www.sunspot.co.uk/Projects/Arduino/speaking-vario/tinyRTCfix.html

1. Remove Pullups R2 + R3
2. Remove R4 R5 R6 and D1
3. Short the now free Pads from R6

These Python Codes need the SMBUS Library (for Python3) installed.
How to from here: http://www.linuxcircle.com/2015/05/03/how-to-install-smbus-i2c-module-for-python-3/

- sudo -i
- apt-get install python3-dev
- apt-get install libi2c-dev
- cd /tmp
- wget http://ftp.de.debian.org/debian/pool/main/i/i2c-tools/i2c-tools_3.1.0.orig.tar.bz2 # download Python 2 source
- tar xavf i2c-tools_3.1.0.orig.tar.bz2
- cd i2c-tools-3.1.0/py-smbus
- mv smbusmodule.c smbusmodule.c.orig # backup
- wget https://gist.githubusercontent.com/sebastianludwig/c648a9e06c0dc2264fbd/raw/2b74f9e72bbdffe298ce02214be8ea1c20aa290f/smbusmodule.c # download patched (Python 3) source
- python3 setup.py build
- python3 setup.py install
- exit

These Python Codes are all completly OpenSource and come with no varranty. Use as you wish, but at your own risk.
