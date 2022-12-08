import datetime as dt
import configparser
import pytz




if False:
    print("Starting HeatingPI V0.3")


    hpConfig = configparser.ConfigParser()
    hpConfig.read("config.ini")

    pollPeriod = int(hpConfig["control"]['poll_period'])
    MQTTSpamPeriod = int(hpConfig["mqtt"]['tele_period'])
    MQTTSlowSpamPeriod = int(hpConfig["mqtt"]['slow_tele_period'])

    rotate = 0
    lstateCounter = 0
    ltime = 0
    spamltime = 0
    slowspamltime = 0
    t1 = -99  # FB Vorlauf
    t2 = -99  # FB Ruecklauf
    t3 = -99  # Solar Vorlauf
    t4 = -99  # Solar Speicher
    t5 = -99  # Solar Ruecklauf

    FBZuHeiss = 30
    if not hpConfig["control"]['fb_too_hot'] is None:
        FBZuHeiss = int(hpConfig["control"]['fb_too_hot'])
    FBEntwarnung = 25  # Wenn Schlimm ist wird ab dieser Temperature schlimm wieder ausgeschaltet
    FBSchlimm = False  # ist True wenn zu heiss war und noch zurueckgeschraubt werden muss

    onon = True
    print FBZuHeiss

    time = dt.datetime.now().strftime("%H:%M:%S")
    print("time:", time)

    u = dt.datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)  # NOTE: it works only with a fixed utc offset

    localtime = u.astimezone(pytz.timezone("Europe/Madrid"))
    sttime = localtime.strftime("%H:%M:%S")
    print sttime
    #print(pytz.country_timezones['es'])
