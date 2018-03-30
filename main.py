#!/usr/bin/env python
import oled
import tempsensors
import relay
import time

print("Starting HeatingPI")

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-0317607252ff","28-051760bdebff")

myRelay = relay.RelayBoard()

toggle=False

try:
    while True:
        time.sleep(1)
        t1=float(mySens.read_temperature1())
        t2=float(mySens.read_temperature2())
        myOled.showTemperatures(t1,t2)
        if toggle:
            toggle=False
            myRelay.switchRelay1Off()
        else:
            toggle=True
            myRelay.switchRelay1On()
except:
    myRelay.cleanup()
    

