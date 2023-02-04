import paho.mqtt.client as mqtt
import posixpath as path
import syslog

class MQTTComm:
    relay1State = False
    relay2State = False
    relay3State = False
    swState={}
    stateCounter = 0

    control_solar = True
    had_self_state = False

    def __init__(self, server_address, base_topic):
        self.server_address = server_address
        self.base_topic = base_topic
        self.actuator_topic = path.join("cmnd", base_topic, "ACTUATOR")
        self.sensors_topic = path.join("tele", base_topic, "SENSOR")
        self.state_topic = path.join("tele", base_topic, "STATE")
        self.stats_topic = path.join("tele", base_topic, "STATS")
        self.controlstate_topic = path.join("tele", base_topic, "STATS")
        self.result_topic = path.join("stat", base_topic, "RESULT")
        self.lwt_topic = path.join("stat", base_topic, "LWT")
        # self.slog(self.sensors_topic)

        self.client = mqtt.Client()
        self.connect()

    def connect(self):


        #  def lcon(client, userdata, flags, rc):
        #     # self.on_connect(client,userdata,flags,rc)
        #     print("Connect with result code " + str(rc))

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set(self.lwt_topic, payload="Offline", qos=0, retain=True)
        self.client.connect(self.server_address, 1883, 60)
        self.client.loop_start()
        self.client.subscribe(
            path.join(self.actuator_topic, '#')
        )  # the hash symbol means we get all messages
        self.client.subscribe(
            path.join(self.state_topic, 'CONTROLSTATE')
        )  # the hash symbol means we get all message from sensors*

    def ping(self):
        self.slog("ping from mqtt")
        self.client.publish(path.join(self.sensors_topic, "STATUS"), "Ping from heatingpi")

    def switchOnOff(self, which, what, force=False):
        if which in self.swState:
            if (self.swState[which] != what) or force:
                self.client.publish("cmnd/sonoff/" + which + "/POWER", what)
                self.swState[which] = what
                self.slog("switching {} {}".format(which, what))
        else:
            self.client.publish("cmnd/sonoff/" + which + "/POWER", what)
            self.swState[which] = what
            self.slog("switching {} {}".format(which, what))

    def on_connect(self, client, userdata, flags, rc):
        self.slog("Connect with result code {}".format(rc))
        self.client.publish(self.lwt_topic, payload="Online", qos=0, retain=True)

    def on_message(self, client, userdata, msg):

        (head, tail) = path.split(msg.topic)
        if head == self.actuator_topic:
            if tail == "R1":
                self.relay1State = (msg.payload == "1")
                self.client.publish(self.result_topic, '{"RELAY1":"'+("ON" if self.relay1State else "OFF")+'"}')
            elif tail == "R2":
                self.relay2State = (msg.payload == "1")
                self.client.publish(self.result_topic, '{"RELAY2":"' + ("ON" if self.relay2State else "OFF") + '"}')
            elif tail == "R3":
                self.relay3State = (msg.payload == "1")
                self.client.publish(self.result_topic, '{"RELAY3":"' + ("ON" if self.relay3State else "OFF") + '"}')
            elif tail == "VALVE":
                self.set_valve(msg.payload)
            elif tail == "SETCONTROL":
                self.had_self_state = True  # see below at CONTROLSTATE: avoid setting state again if received from retained message
                self.set_control(msg.payload)
            self.slog(msg.topic + " " + str(msg.payload))
            self.stateCounter = self.stateCounter + 1
        if head == self.state_topic:
            if tail == "CONTROLSTATE":
                if not self.had_self_state:
                    self.had_self_state = True
                    self.set_control(msg.payload)
                self.stateCounter = self.stateCounter + 1
                self.set_valve(msg.payload)
            elif tail == "SETCONTROL":
                self.had_self_state = True  # see below at CONTROLSTATE: avoid setting state again if received from retained message
                self.set_control(msg.payload)
            self.slog(msg.topic + " " + str(msg.payload))
            self.stateCounter = self.stateCounter + 1
        if head == self.state_topic:
            if tail == "CONTROLSTATE":
                if not self.had_self_state:
                    self.had_self_state = True
                    self.set_control(msg.payload)
                self.stateCounter = self.stateCounter + 1







    def set_valve(self, towhat):
        if towhat == "HOTTER":
            self.relay2State = True
            self.relay1State = False
        elif towhat == "COLDER":
            self.relay2State = False
            self.relay1State = True
        elif towhat == "STOP":
            self.relay2State = False
            self.relay1State = False
    def set_control(self, towhat):
        if towhat == "OFF":
            self.control_solar = False
            self.client.publish(path.join(self.state_topic, 'CONTROLSTATE'), 'OFF', 0, True)
        elif towhat == "ON":
            self.control_solar = True
            self.client.publish(path.join(self.state_topic, 'CONTROLSTATE'), 'ON', 0, True)

    def sendTemperature(self, sensor_name, value):
        rondvalue = round(value, 1) # dies sensoren sind sowieso nicht so genau ...eine nachkommastelle  reicht
        self.client.publish(path.join(self.sensors_topic, sensor_name), rondvalue)
    def send_state(self, message):
        self.client.publish(self.state_topic, message)

    def send_stats(self, message):
        self.client.publish(self.stats_topic, message)

    def slog(self, msg):
        syslog.syslog(msg)
        print(msg)
