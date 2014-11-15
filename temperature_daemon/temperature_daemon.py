#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, pigpio, vw, struct
import urllib

RX=11
BPS=2000
pi = pigpio.pi() # Connect to local Pi.
rx = vw.rx(pi, RX, BPS) # Specify Pi, rx gpio, and baud.

print "Waiting for temperature on pin #{rx} at {bps} bps".format(rx=RX, bps=BPS)

while True:
   if not rx.ready():
      time.sleep(0.1)
   else:
      msg = "".join(chr (c) for c in rx.get())
      # print ":".join("{:02x}".format(ord(c)) for c in msg)
      
      value = struct.unpack(">h", msg)[0]
      value = value / 100.0

      print "Received temperature: {temp}".format(temp=value)

      try:
        params = urllib.urlencode({'value': value})
        f = urllib.urlopen("http://localhost:5000/new-temperature", params)
        print "Server response: {response}".format(response=f.read())
      except Exception,e:
        print str(e)
