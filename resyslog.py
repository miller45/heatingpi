import platform

def syslog(message):
    if platform.system()=="Windows":
        pass
    else:
        import syslog
        syslog.syslog(message)
