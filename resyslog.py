import platform

def syslog(message):
    if platform.system()=="Windows":
        print(message)
    else:
        import syslog
        syslog.syslog(message)
