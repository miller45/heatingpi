import tempsensors
import valve
import mqttcom
import configparser
import math
import arduino
import arduino2
import time
import datetime
import os
import repeatedtimer

print("Starting HeatingPI V0.5")

serialp = '/dev/ttyACM0'
if 'OVERRIDE_SERIAL' in os.environ:
    serialp = os.environ['OVERRIDE_SERIAL']
serialp2 = '/dev/ttyAMA0'
if 'OVERRIDE_SERIAL2' in os.environ:
    serialp2 = os.environ['OVERRIDE_SERIAL2']

ard = arduino.Arduino(serialp)

hpConfig = configparser.ConfigParser()
hpConfig.read("config.ini")


# mySens = tempsensors.TempSensors("28-3c01f0964f8c", "28-3c01f0965e56")
alls= [
    hpConfig["sensors"]["T1"],
    hpConfig["sensors"]["T2"],
    hpConfig["sensors"]["T3"],
    hpConfig["sensors"]["T4"],
    "/dummy5",
    hpConfig["sensors"]["T6"]
]
mySens = tempsensors.TempSensors(alls)
ard2 = arduino2.Arduino2(serialp2, alls)

# mySens = tempsensors.TempSensors("28-0317607252ff", "28-051760bdebff")

relayBoard = valve.Valve()
srvaddress = hpConfig["mqtt"]["server_address"]
if 'OVERRIDE_MQTT_HOST' in os.environ:
    srvaddress = os.environ['OVERRIDE_MQTT_HOST']

mqttClient = mqttcom.MQTTComm(srvaddress, hpConfig["mqtt"]["base_topic"])

mqttClient.ping()

pollPeriod = int(hpConfig["control"]['poll_period'])
slow_poll_period = float(int(hpConfig["control"]['slow_poll_period']))
MQTTSpamPeriod = int(hpConfig["mqtt"]['tele_period'])
MQTTSlowSpamPeriod = int(hpConfig["mqtt"]['slow_tele_period'])

do_control_solar = "yes" == hpConfig["control"]['control_solar']
do_time_stats = "yes" == hpConfig["control"]['emit_time_stats']

rotate = 0
lstateCounter = 0
ltime = 0
spamltime = 0
slowspamltime = 0

defval = -99

t1 = defval # FB Vorlauf
t2 = defval # FB Ruecklauf
t3 = defval # Solar Vorlauf
t4 = defval # Solar Speicher
t5 = defval # Solar Ruecklauf
t6 = defval # was auch immer

temps_ready = False # are the temperatur values ready (read at least once)

statread1 = 0  # last amount of time to read local temp sensors
statread2 = 0  # last amount of time to read serially connecte temp sensor

FBZuHeiss = 30
if not hpConfig["control"]['fb_too_hot'] is None:
    FBZuHeiss = int(hpConfig["control"]['fb_too_hot'])

FBEntwarnung = 25  # Wenn Schlimm ist wird ab dieser Temperature schlimm wieder ausgeschaltet
FBSchlimm = False  # ist True wenn zu heiss war und noch zurueckgeschraubt werden muss

onon = True

last_switch_52_time = -1000


def regeln_solar_speicher(currtimems):
    global t1, t2, t3, t4, t5, t6
    global mqttClient, last_switch_52_time
    hysteresis = 6
    offteresis = 3
    SV = t3
    SR = t5
    SS = t4
    if SS < 10:
        mqttClient.switchOnOff("52", "OFF")
        last_switch_52_time = currtimems
    elif (SS + hysteresis) < SR:
        mqttClient.switchOnOff("52", "ON")
        last_switch_52_time = currtimems
    elif (SS + offteresis) >= SR:
        # if the last switch was done less than 10 minutes ago dont switch off yet
        if currtimems - 10 * 60 * 1000 > last_switch_52_time:
            mqttClient.switchOnOff("52", "OFF")
            last_switch_52_time = currtimems


def regeln_fussboden_heizung(currtimems):
    global t1, t2, t3, t4, t5, t6
    global mqttClient, relayBoard
    global FBSchlimm, FBZuHeiss, FBEntwarnung
    FBVor = t1
    FBRueck = t2
    SV = t3
    SR = t5
    SS = t4
    if FBSchlimm:
        if FBVor <= FBEntwarnung:
            FBSchlimm = False  # Alarm zuruecksetzen und nicht mehr regeln
            relayBoard.slog("Entwarnung")
            # mqttClient.set_valve("STOP")
    elif FBVor >= FBZuHeiss:
        FBSchlimm = True
        mqttClient.switchOnOff("51", "OFF")  # pumpe fb heizung
        relayBoard.slog("FB zu heiss")

        # mqttClient.set_valve("COLDER")


def read_all_temperatures():
    global ard2
    ard2.read_all_temperatures()


def collect_all_temperatures():
    global ard2, t1, t2, t3, t4, t5, t6
    global statread1, temps_ready
    tic = time.clock()
    t1 = float(ard2.read_temperature1())
    t2 = float(ard2.read_temperature2())
    t3 = float(ard2.read_temperature3())
    t4 = float(ard2.read_temperature4())
    t6 = float(ard2.read_temperature6())
    toc = time.clock()
    statread1 = toc - tic
    temps_ready = True


# read the temperatur in the "background" without hindering the main loop

rtemp_timer1 = repeatedtimer.RepeatedTimer(1, read_all_temperatures)
rtemp_timer2 = repeatedtimer.RepeatedTimer(slow_poll_period / 1000, collect_all_temperatures)

while onon:

    try:
        while True:
            currtime = math.trunc(time.time() * 1000)  # time in milliseconds
            if currtime - pollPeriod > ltime:
                # read this temp here because it breaks in the out func
                tic = time.clock()
                t5 = float(ard.readRuecklauf())
                toc = time.clock()
                statread2 = toc - tic

                # regeln
                if do_control_solar:
                    regeln_solar_speicher(currtime)

                regeln_fussboden_heizung(currtime)

                ltime = currtime

            if currtime - MQTTSpamPeriod > spamltime:
                if temps_ready: # in the first round the tempareture values are not yet there
                    mqttClient.sendTemperature("T1", t1)
                    mqttClient.sendTemperature("T2", t2)
                    mqttClient.sendTemperature("T3", t3)
                    mqttClient.sendTemperature("T4", t4)
                    mqttClient.sendTemperature("T5", t5)
                    mqttClient.sendTemperature("T6", t6)
                    mqttClient.send_state(str(currtime))
                    if do_time_stats:
                        mqttClient.send_stats("S1 %f S2 %f" % (statread1, statread2))
                spamltime = currtime

            # slower updates for homeassisant
            if currtime - MQTTSlowSpamPeriod > slowspamltime:
                slowspamltime = currtime
                if temps_ready: # in the first round the tempareture values are not yet there
                    mqttClient.sendTemperature("SLOWT1", t1)
                    mqttClient.sendTemperature("SLOWT2", t2)
                    mqttClient.sendTemperature("SLOWT3", t3)
                    mqttClient.sendTemperature("SLOWT4", t4)
                    mqttClient.sendTemperature("SLOWT5", t5)
                    mqttClient.sendTemperature("SLOWT6", t6)

            if lstateCounter != mqttClient.stateCounter:
                lstateCounter = mqttClient.stateCounter
                if mqttClient.relay1State:
                    relayBoard.switchRelay1On()
                else:
                    relayBoard.switchRelay1Off()
                if mqttClient.relay2State:
                    relayBoard.switchRelay2On()
                else:
                    relayBoard.switchRelay2Off()
                if mqttClient.relay3State:
                    relayBoard.switchRelay3On()
                else:
                    relayBoard.switchRelay3Off()

                if do_control_solar != mqttClient.control_solar:
                    do_control_solar = mqttClient.control_solar

            time.sleep(0.001)
    except KeyboardInterrupt:
        print('program cancelled by keyboard')
        onon = False
        break

    except BaseException as error:
        relayBoard.cleanup()
        print('An exception occurred: {} {}'.format(type(error), error))
        print("restarting after 5 secs")
        time.sleep(5)
    except:
        relayBoard.cleanup()
        print("exception occurred restarting after 1 secs")
        time.sleep(1)

rtemp_timer1.stop()
rtemp_timer2.stop()
relayBoard.cleanup()

