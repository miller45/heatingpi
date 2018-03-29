import oled
import tempsensors
import time

print("Starting HeatingPI")

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-0317607252ff","28-051760bdebff")

while True:
    time.sleep(1)
    t1=float(mySens.read_temperature1())
    t2=float(mySens.read_temperature2())
    myOled.showTemperatures(t1,t2)


