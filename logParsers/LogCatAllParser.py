from utils import*
class LogCatAllParsers:
    def __init__(self,filename):
        f=file(filename,'r')
        starttime=int(filename.split("\\")[-1].split("_")[-1].replace(".txt",""))
        print starttime
        self.dicts={}
        f1=file("logcat.csv",'w')
        f2=file("alltags.csv",'w')
        tags=[]
        self.ignoretags=["libprocessgroup:","PackageManager:","PackageSettings:","PackageParser:","QueryController:","AccessibilityNodeInfoDumper:","AccessibilityCache:","ThermalEngine:"]
        while True:
            line=f.readline()
            if not line:
                break
            if line.strip()!="":
                #print line
                if ":" in line and "." in line:
                    items=line.strip().split(" ")
                #print items

                    datetime="2016 "+items[0]+" "+items[1]
                   #print datetime
                    timestamp=getTimestampByDatetime(datetime)
                    if timestamp>starttime:
                        #print items
                        startindex=2
                        pid,tid,logcattag,infotag,content=self.ParseLine(items,startindex,line)
                        if infotag not in self.ignoretags:
                            if not timestamp in self.dicts:
                                self.dicts[timestamp]={}
                            self.dicts[timestamp][infotag]={}
                            self.dicts[timestamp][infotag]["pid"]=pid
                            self.dicts[timestamp][infotag]["tid"]=tid ## tid!=pid, then it's another thread
                            self.dicts[timestamp][infotag]["content"]=content

                        writeline=str(timestamp)+","+str(pid)+","+str(tid)+","+logcattag+","+infotag+","+content
                        if writeline.endswith("\n")==False:
                            f1.write(writeline+"\n")
                        else:
                            f1.write(writeline)
                        if infotag not in tags:
                            tags.append(infotag)


        for tag in tags:
            f2.write(tag+"\n")



    def ParseLine(self,items,startindex,line):
        pid=-1
        tid=-1
        logcattag=-1
        infotag=-1
        content=""
        count=0
        #print len(items)
        index=startindex
        while index<len(items):
            item=items[index]
            #print "item",item, count
            if item!="":
                if count==0:
                    pid=int(item)
                if count==1:
                    tid=int(item)
                if count==2:
                    logcattag=item
                if count==3:
                    infotag=item

                count+=1
            index+=1
        if infotag!=-1:
            content=line.split(logcattag+" "+infotag)[-1]
        #print line
        #print pid, tid, logcattag, infotag, content
        return pid, tid, logcattag,infotag, content





