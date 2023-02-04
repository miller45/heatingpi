import re
import os
import time
import syslog


class TempSensors:
    disableSensor1 = False
    disableSensor2 = False
    disableSensor3 = False
    disableSensor4 = False
    disableSensor6 = False  # Five is the arduino temp sensors so we use 6 here to avoid mixup

    last_vals = {}
    sens_states = {}

    def __init__(self, w1name1, w1name2, wlname3, wlname4, wlname6):
        basep = "/sys/bus/w1/devices/"

        if 'OVERRIDE_W1_PATH' in os.environ:
            basep = os.environ['OVERRIDE_W1_PATH']

        self.sensor1path = basep + w1name1 + "/w1_slave"
        self.sensor2path = basep + w1name2 + "/w1_slave"
        self.sensor3path = basep + wlname3 + "/w1_slave"
        self.sensor4path = basep + wlname4 + "/w1_slave"
        self.sensor6path = basep + wlname6 + "/w1_slave"

    def read_temperature1(self):
        ret = "-99"
        if self.disableSensor1:
            return ret
        try: 
            ret = self.read_sensor(self.sensor1path)
        except:
            self.disableSensor1 = True
        return ret

    def read_temperature2(self):
        ret = "-99"
        if self.disableSensor2:
            return ret
        try: 
            ret = self.read_sensor(self.sensor2path)
        except:
            self.disableSensor2 = True
        return ret

    def read_temperature3(self):
        ret = "-99"
        if self.disableSensor3:
            return ret
        try:
            ret = self.read_sensor(self.sensor3path)
        except:
            self.disableSensor3 = True
        return ret

    def read_temperature4(self):
        ret = "-99"
        if self.disableSensor4:
            return ret
        try:
            ret = self.read_sensor(self.sensor4path)
        except:
            self.disableSensor4 = True
        return ret

    def read_temperature6(self):
        ret = "-99"
        if self.disableSensor6:
            return ret
        try:
            ret = self.read_sensor(self.sensor6path)
        except:
            self.disableSensor6 = True
        return ret

    def read_sensor(self,path):
        value = "-1"
        try:
            f = open(path, "r")
            line = f.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                line = f.readline()
                m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
                if m:
                    value = str(float(m.group(2)) / 1000.0)
                    self.last_vals[path] = value
                    self.sens_states[path] = 1
            f.close()
        except IOError as e:
            self.slog("Error reading {}: {}".format(path, e))
            if path in self.last_vals:
                value = self.last_vals[path]
            self.sens_states[path] = 0
        return value

    def slog(self, msg):
        syslog.syslog(msg)
        print(msg)
