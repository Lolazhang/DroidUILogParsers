from datetime import datetime
import time
def getTimestampByDatetime(datestr):
    format="%Y %m-%d %H:%M:%S.%f"
    dt=datetime.strptime(datestr,format)
    seconds=time.mktime(dt.timetuple())+28800## +8 hours
    milliseconds=int(datestr.split(".")[-1])
    final=int(seconds*1000+milliseconds)
    #print "final",final
    return final

def getTimestampByDatetime1(datestr):
    format="%Y-%m-%d %H:%M:%S.%f"
    dt=datetime.strptime(datestr,format)
    seconds=time.mktime(dt.timetuple())+28880## +8 hours
    milliseconds=int(datestr.split(".")[-1])
    final=int(seconds*1000+milliseconds)
    #print "final",final
    return final

