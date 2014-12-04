#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, struct
import urllib
import sys

if len(sys.argv) != 2:
    print "usage: python one_wire_daemon.py <sensor file>"
    print "example: python one_wire_daemon.py /sys/bus/w1/devices/28-000005fbb5db/w1_slave"
    sys.exit(1)

sensor_path = sys.argv[1]

while True:
    f = open(sensor_path)
    lines = f.readlines()
    f.close()

    if lines[0].strip()[-3:] == 'YES':
        t_start = lines[1].find('t=')
        if t_start != -1:
            string = lines[1].strip()[t_start+2:]
            temperature = float(string) / 1000.0

            if temperature < 85.0: # the sensor sometimes report 85000 or values > 120000
                print "Temperature: {temp}".format(temp=temperature)

                try:
                    params = urllib.urlencode({'value': temperature})
                    f = urllib.urlopen("http://localhost:5000/new-temperature", params)
                    print "Server response: {response}".format(response=f.read())
                except Exception,e:
                    print str(e)

    time.sleep(10)
