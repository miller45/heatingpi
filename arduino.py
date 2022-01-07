#!/usr/bin/env python3
import serial

class Arduino:
    def __init__(self, port):
        self.port=port
        self.last=-98
        self.ser = serial.Serial(port, 115200, timeout=1) #'/dev/ttyACM0'
        self.ser.reset_input_buffer()
    def readRuecklauf(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            if line.startswith("T"):
                temp=line[1:]
                self.last=float(temp)
                return self.last
            else:
                return self.last



