
#creates fake sensor files for testing

import configparser

import os
fakep="/tmp/sys/bus/w1/devices"
print("makeing fake sensor in {}".format(fakep);

hpConfig = configparser.ConfigParser()
hpConfig.read("config.ini")

allsens=(
    hpConfig["sensors"]["T1"],
    hpConfig["sensors"]["T2"],
    hpConfig["sensors"]["T3"],
    hpConfig["sensors"]["T4"],
    hpConfig["sensors"]["T6"]
)