import serial
import re


class Arduino2:
    def __init__(self, port, wnames):
        self.port = port
        self.last = -98
        self.ser = serial.Serial(port, 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.tbu={}
        self.wnames = ['/dummy0']
        self.wnames.extend(wnames)
        self.reading = False
        for w in wnames:
            self.tbu[w] = "-99"

    def read_all_temperatures(self):
        wasreading = self.reading
        self.reading = True
        if wasreading:
            return
        while self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            if line.startswith("I"):
                ap = line.find("G")
                tp = line.find("T")
                adr = line[ap+1:tp].lower()
                adr = adr[:2]+"-"+adr[2:]
                temp = line[tp+1:]
                if re.match(r"^[0-9.]+$", temp):
                    self.last = float(temp)
                    if adr in self.tbu:
                       # print(adr+":"+temp)
                        self.tbu[adr] = temp
        self.reading = False

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
        adr = self.wnames[num]
        ret = "-1.97"
        if not self.tbu[adr] is None:
            ret = self.tbu[adr]
        return ret
