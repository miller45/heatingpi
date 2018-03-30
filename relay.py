import RPi.GPIO as GPIO


class RelayBoard:
    Relay_Ch1 = 26
    Relay_Ch2 = 20
    Relay_Ch3 = 21

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Relay_Ch1,GPIO.OUT)
        GPIO.setup(self.Relay_Ch2,GPIO.OUT)
        GPIO.setup(self.Relay_Ch3,GPIO.OUT)
        GPIO.output(self.Relay_Ch1,GPIO.HIGH)
        GPIO.output(self.Relay_Ch2,GPIO.HIGH)
        GPIO.output(self.Relay_Ch3,GPIO.HIGH)
    
    def switchRelay1On(self):
        GPIO.output(self.Relay_Ch1,GPIO.LOW)
    def switchRelay1Off(self):
        GPIO.output(self.Relay_Ch1,GPIO.HIGH)
    def cleanup(self):
        GPIO.cleanup()
    def ping(self):
        print("ping")
        
        
        