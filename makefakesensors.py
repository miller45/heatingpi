# creates fake sensor files for testing

import configparser

import os
fakecon="""a0 01 55 05 7f a5 81 66 b2 : crc=b2 YES
a0 01 55 05 7f a5 81 66 b2 t=26000"""
fakep = "/tmp/sys/bus/w1/devices"
print("makeing fake sensor in {}".format(fakep))

hpConfig = configparser.ConfigParser()
hpConfig.read("config.ini")

allsens = (
    hpConfig["sensors"]["T1"],
    hpConfig["sensors"]["T2"],
    hpConfig["sensors"]["T3"],
    hpConfig["sensors"]["T4"],
    hpConfig["sensors"]["T6"]
)
for s in allsens:
    d = os.path.join(fakep, s)
    os.makedirs(d)
    f = open(os.path.join(d, "w1_slave"), "w")
    f.write(fakecon)
    f.close()

