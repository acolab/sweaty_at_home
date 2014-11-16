sweaty@home
==============

Goal
----
Create a connected thermostat able to pilot a boiler (on/off) and electronic heater (Pilot wire)

Hardware
--------
### Server
- Raspberry Pi
- 433 Mhz receiver
- LCD Screen 2x20 Characters

### Thermal sensor
- Arduino Uno
- Digital Thermometer : DS18B20
- 433 Mhz emetter

Software
--------
### Arduino
- OneWire Library
- VirtualWire Library

### Rapsberry
- Flask : phyton web framework
- SQLite
- SQLalchemy
- Python
- [PiGPIO](http://abyz.co.uk/rpi/pigpio/index.html)
- Custom LCD Lib from [zem.fr](http://www.zem.fr/raspberry-pi-et-afficheur-lcd-hitachi-hd44780-1602-part-2/)

Requirements
------------
Package      | Version
-------------|---------
Flask        | 0.10.1
Jinja2       | 2.7.3
MarkupSafe   | 0.23
SQLAlchemy   | 0.9.8
Werkzeug     | 0.9.6
argparse     | 1.2.1
distribute   | 0.6.24
itsdangerous | 0.24
wsgiref      | 0.1.2


Functionnality
--------------
- [x] Read temperature from remote sensor through RF
- [x] Set hysteresis for Temperature regulation
- [x] Display current temperature on LCD
- [ ] Pilot boiler through relay
- [ ] Pilot Electric heater through optotriac

### Web Interface
- [ ] Set Temperature
- [ ] Graph logged T°

Install
-------
### Arduino
Download and upload the Arduino sektch into an Arduino board.
10k Pull-up resistor between +5V and Data
Arduino pin out
Thermometer : pin 2
RF Emetter : pin 12

### Raspberry
On top of a vanilla version of Raspbian, install
```
sudo apt-get update
sudo apt-get install python-sqlachemy python-pip python-flask
```
Download and Install PiGPIO : http://abyz.co.uk/rpi/pigpio/download.html
```
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
make install
```
