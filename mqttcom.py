import paho.mqtt.client as mqtt


class MQTTComm:

    def __init__(self, serverAddress):
        self.serverAddress = serverAddress
        self.connect()

    def connect(self):
        self.client = mqtt.Client()

        def lcon(client, userdata, flags, rc):
            # self.on_connect(client,userdata,flags,rc)
            print("Connect with result code " + str(rc))

        self.client.on_connect = self.on_connect
        self.client.connect(self.serverAddress, 1883, 60)
        self.client.loop_start()

    def ping(self):
        print("ping from oled")

    def on_connect(self, client, userdata, flags, rc):
        print("Connect with result code " + str(rc))

    def sendTemperature(self, sensorName, value):
        self.client.publish("heatingpi/sensors/" + sensorName, value)
