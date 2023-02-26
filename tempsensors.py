import re
import os
import time
import syslog


class TempSensors:
                    #  0     1     2     3     4    5     6
                    # Five is the arduino temp sensors so we use 6 here to avoid mixup
    disabledSensors = [True] # we dont want to use number 0 so its a dummy
    sensorpathes = ["/dummy"]

    last_vals = {}
    sens_states = {}

    recycles = 0

    def __init__(self, wnames):
        basep = "/sys/bus/w1/devices/"

        if 'OVERRIDE_W1_PATH' in os.environ:
            basep = os.environ['OVERRIDE_W1_PATH']
        self.sensorpathes = ["/dummy"]

        for n in wnames:
            self.sensorpathes.append(basep + n + "/w1_slave")
            self.disabledSensors.append(n == "/dummy")

    def read_temperature1(self):
        return self.read_temperature_generic(1)

    def read_temperature2(self):
        return self.read_temperature_generic(2)

    def read_temperature3(self):
        return self.read_temperature_generic(3)

    def read_temperature4(self):
        return self.read_temperature_generic(4)

    def read_temperature6(self):
        return self.read_temperature_generic(6)

    def read_temperature_generic(self, num):
        ret = "-2.99"
        if self.disabledSensors[num]:
            return ret

        ret = self.read_sensor(self.sensorpathes[num])
        if ret == "-1.99":
            self.disabledSensors[num] = True
        self.recycles = self.recycles + 1
        if self.recycles > 60:
            self.recycles = 0
            for i in range(1, len(self.disabledSensors)):
                print(i)
                self.disabledSensors[i] = False


        return ret

    def read_sensor(self,path):
        value = "-1.98"
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
