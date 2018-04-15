import oled
import tempsensors
import relay
import time
import mqttcom
import configparser
import math

print("Starting HeatingPI V0.2")

hpConfig = configparser.ConfigParser()
hpConfig.read("config.ini")

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-0317607252ff", "28-051760bdebff")

myRelay = relay.RelayBoard()

myMQTT = mqttcom.MQTTComm(hpConfig["mqtt"]["server_address"], hpConfig["mqtt"]["base_topic"])

myMQTT.ping()

rotate = 0
lstateCounter = 0
ltime = 0

try:
    while True:
        currtime = math.trunc(time.time() * 1000) # time in microseconds
        if currtime - 1000 > ltime:
            ltime = currtime
            t1 = float(mySens.read_temperature1())
            t2 = float(mySens.read_temperature2())
            myMQTT.sendTemperature("T1", t1)
            myMQTT.sendTemperature("T2", t2)
            myOled.showTemperatures(t1, t2)
        if lstateCounter != myMQTT.stateCounter:
            lstateCounter = myMQTT.stateCounter
            if myMQTT.relay1State:
                myRelay.switchRelay1On()
            else:
                myRelay.switchRelay1Off()
            if myMQTT.relay2State:
                myRelay.switchRelay2On()
            else:
                myRelay.switchRelay2Off()
            if myMQTT.relay3State:
                myRelay.switchRelay3On()
            else:
                myRelay.switchRelay3Off()

except:
    myRelay.cleanup()
