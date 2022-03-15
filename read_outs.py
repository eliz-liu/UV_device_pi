#!/usr/bin/python
# -*- coding:UTF-8 -*-

import time
import Si1145 as Sensor

Sensor.Si1145_Init()

try:
    while True:
        print "==================="
        print "Vis: ", Sensor.Si1145_readVisible()
        print "IR: ", Sensor.Si1145_readIR()
    
        UVindex = Sensor.Si1145_readUV()
        UVindex /= 100.0
        print "UV: ", UVindex
        time.sleep(1)

except:
    Sensor.Si1145_close()
