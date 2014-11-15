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
