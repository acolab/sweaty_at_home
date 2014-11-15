sweaty@home
==============

Goal
----
Create a connected thermostat able to pilot a boiler (on/off) and electronic heater (Pilot wire)

Hardware
--------
### Server
Raspberry Pi
433 Mhz receiver

### Thermal sensor
Arduino
Digital Thermometer : DS18B20
433 Mhz emetter

Software
--------
### Arduino
OneWire Library
VirtualWire Library

### Rapsberry
Flask : phyton web framework
SQLite
SQLalchemy
Python
PiGPIO : http://abyz.co.uk/rpi/pigpio/index.html

Requirements
------------
Package      | Version
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
- Read temperature from remote sensor through RF
- Set hysteresis for Temperature regulation
- Pilot boiler through relay
- Pilot Electric heater through optotriac

### Web Interface
- Set Temperature
- Graph logged T°

Install
-------
### Arduino
Download and upload the Arduino sektch into an Arduino board.
10k Pull-up resistor between +5V and Data
Arduino pin out
Thermometer : pin 2
RF Emetter : pin 12

### Raspberry
Install
python-sqlachemy, python-pip, python-flask

PiGPIO : http://abyz.co.uk/rpi/pigpio/download.html
