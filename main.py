import oled
import tempsensors

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-0317607252ff","28-051760bdebff")

print(mySens.read_temperature1())
print(mySens.read_temperature2())