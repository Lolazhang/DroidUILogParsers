from utils import*
import datetime
class StraceParser:
    def __init__(self,filename):
        self.dicts={}
        f=file(filename,'r')
        timestamp=int(filename.split("\\")[-1].split("_")[-1].replace(".trace",""))/1000.0
        #print timestamp
        datestr=  datetime.datetime.fromtimestamp(
               timestamp
            ).strftime('%Y-%m-%d %H:%M:%S.%f')
        print datestr
        hour=datestr.split()[-1].split(":")[0]
        self.date = datestr.split()[0]
        self.correct=True
        if hour.startswith("0"):
            ohour=int(hour[1])
            if ohour<8:
                self.correct=True







        #print self.date


        while True:
            line=f.readline()
            if not line:
                break
            items=line.split()
            #print items
            try:
               self.ParseLine(items)
                #pass
            except:
                pass



    def ParseLine(self,items):

        datetime= self.date+" "+items[0]
        print datetime
        timestamp=getTimestampByDatetime1(datetime)
        if self.correct==True:
            timestamp=timestamp-86400*1000
        print timestamp
        index=1
        function=""
        while index<len(items)-3:
             current=items[index]
             function+=current+" "
             index+=1
        if function.endswith(" "):
            function=function[0:-1]
        functionname=items[1].split("(")[0]
        filename=items[2][1:-2]
        timespent=items[-1]
        timespent=float(timespent.split("<")[-1].split(">")[0])
        print timestamp, functionname,filename, timespent
        if not timestamp in self.dicts:
            self.dicts[timestamp]={}
        if not functionname in self.dicts[timestamp]:
            self.dicts[timestamp][functionname]={}
        self.dicts[timestamp][functionname]["timespent"]=timespent
        self.dicts[timestamp][functionname]["filename"]=filename
        self.dicts[timestamp][functionname]["function"]=function
