import paho.mqtt.client as mqtt
import posixpath as path


class MQTTComm:
    relay1State = False
    relay2State = False
    relay3State = False
    stateCounter = 0

    def __init__(self, server_address, base_topic):
        self.server_address = server_address
        self.base_topic = base_topic
        self.actuator_topic = path.join(base_topic, "actuators")
        self.sensors_topic = path.join(base_topic, "sensors")
        print(self.sensors_topic)

        self.client = mqtt.Client()
        self.connect()

    def connect(self):


        # def lcon(client, userdata, flags, rc):
        #     # self.on_connect(client,userdata,flags,rc)
        #     print("Connect with result code " + str(rc))

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.server_address, 1883, 60)
        self.client.loop_start()
        self.client.subscribe(
            path.join(self.actuator_topic, '#')
        )  # the hash symbol means we get all message from sensors*

    def ping(self):
        print("ping from oled")

    def on_connect(self, client, userdata, flags, rc):
        print("Connect with result code " + str(rc))

    def on_message(self, client, userdata, msg):

        (head, tail) = path.split(msg.topic)
        if (tail == "R1"):
            self.relay1State = (msg.payload == "1")
        elif (tail == "R2"):
            self.relay2State = (msg.payload == "1")
        elif (tail == "R3"):
            self.relay3State = (msg.payload == "1")
        elif tail == "VALVE":
            if msg.payload == "HOTTER":
                self.relay2State = True
                self.relay1State = False
            elif msg.payload == "COLDER":
                self.relay2State = True
                self.relay1State = False
            elif msg.payload == "STOP":
                self.relay2State = False
                self.relay1State = False

        self.stateCounter = self.stateCounter + 1
        # if(msg.topic.ends)

        print(msg.topic + " " + str(msg.payload))

    def sendTemperature(self, sensorName, value):
        self.client.publish(path.join(self.sensors_topic, sensorName), value)
