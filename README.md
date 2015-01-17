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
- LCD Screen 2x20 Characters PC2002LRS-A

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

LCD Wiring
----------
```
Connector
16 - 15 [-------------------------------------------]
14 - 13 [                                           ]
12 - 11 [                                           ]
10 - 9  [                                           ]
 8 - 7  [                                           ]
 6 - 5  [                                           ]
 4 - 3  [                                           ]
 2 - 1  [-------------------------------------------]
```
PC2002  |   Signal  |  Couleur    | Rasp
--------|-----------|-------------|--------------
1       |    VSS    |     Marron  |    GND
2       |    VDD    |     Rouge   |    +5V
3       |    Vo     |             |    LCD Contrast
4       |    RS     |     Orange  |    GPIO 7
5       |    R/!W   |             |    GND
6       |    Enable |     Jaune   |    GPIO 8
7       |    DB0    |             |    -
8       |    DB1    |             |    -
9       |    DB2    |             |    -
10      |    DB3    |             |    -
11      |    DB4    |     Vert    |    GPIO 25
12      |    DB5    |     Bleu    |    GPIO 24
13      |    DB6    |     Violet  |    GPIO 23
14      |    DB7    |     Gris    |    GPIO 18
15      |    Anode  |     Blanc   |    +30mA (3V)
16      |    Cathode|             |    GND


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

#### Arduino pin out
10k Pull-up resistor between +5V and Data

DS18B20 (data pin) : pin 2

RF Emetter : pin 12

### Raspberry
On top of a vanilla version of Raspbian, install
```
sudo apt-get update
sudo apt-get install python-sqlalchemy python-flask apache2 libapache2-mod-wsgi git avahi-daemon
```
Download and Install PiGPIO : http://abyz.co.uk/rpi/pigpio/download.html
```
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
cd ..
```

Get sweaty@home and install it:
```
git clone https://github.com/acolab/sweaty_at_home.git
cd sweaty_at_home
sudo cp init.d/pigpiod /etc/init.d/pigpiod
sudo update-rc.d pigpiod defaults
sudo service pigpiod start
sudo cp apache_config /etc/apache2/sites-available/sweaty_at_home
sudo a2ensite sweaty_at_home
sudo a2dissite default default_ssl
sudo service apache2 reload
```

Then connect to http://raspberrypi.local/.

If you use the one wire sensor directly connected to the pi, install the daemon:
```
sudo cp init.d/one_wire_sensor /etc/init.d/
sudo update-rc.d one_wire_sensor defaults
sudo service one_wire_sensor start
```

Enabling MRF24J40 ZigBee support on the Raspberry Pi
----------------------------------------------------

On a Linux system:

Install rpi-build (https://github.com/notro/rpi-build/wiki):

    sudo wget https://raw.githubusercontent.com/notro/rpi-build/master/rpi-build -O /usr/bin/rpi-build && sudo chmod +x /usr/bin/rpi-build
    rpi-build

Prepare a working directory and configure the kernel:

    mkdir rpi_mrf
    cd rpi_mrf
    rpi-build use[stdlib] rpi_linux menuconfig

Activate these options:

```
Networking support
  Networking options
    <M> IEEE Std 802.15.4
      <M> 6lowpan support
      <M> Generic IEEE
Device Drivers
  Network device support
    <M> IEE 802.15.4 drivers
      <M> Microchip MRF24J40 tranceiver driver
```

Build the kernel:

    rpi-build use[stdlib] rpi_linux build

Install it on your Raspberry Pi:

    rpi-build use[stdlib] rpi_linux install SSHIP=<ip of the raspberry pi>

Reboot the Raspberry and you should be able to load the mrf24j40 module (and add it to /etc/modules).

