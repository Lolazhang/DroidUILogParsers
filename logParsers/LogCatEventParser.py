from utils import*
class LogCatEventParser:
    def __init__(self,filename):
        self.dicts={}
        f=file(filename,'r')
        starttime=int(filename.split("\\")[-1].split("_")[-1].replace(".txt",""))
        #f1=file("events.txt",'w')
        self.ignoretags=["notification_cancel:","notification_cancel_all:","backup_data_changed:","netstats_mobile_sample:","netstats_wifi_sample:"]
        while True:
            line=f.readline()
            if not line:
                break
            content=line.strip()
            if content!="" and ":" in content and "." in content:
                #print content
                items=content.split(" ")
                #print items
                datastr="2016 "+items[0]+" "+items[1]
                timestamp=getTimestampByDatetime(datastr)
                if timestamp>=starttime:
                    #print content
                    pid,tid,logcattag,infotag,da=self.ParseLine(content,items)
                    if infotag not in self.ignoretags:
                        if not timestamp in self.dicts:
                            self.dicts[timestamp]={}
                        self.dicts[timestamp][infotag]=da
                    writeline=str(timestamp)+","+str(pid)+","+str(tid)+","+logcattag+","+infotag+","+da
                    #print writeline
                    #f1.write(writeline+"\n")



    def ParseLine(self,content,items):
        index=2
        count=0
        pid=-1
        tid=-1
        logcattag=-1
        infotag=-1
        content1=""
        while index<len(items):
            item=items[index]
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
            content1=content.split(logcattag+" "+infotag)[-1]
            print content1
            print pid,tid,logcattag,infotag,content1

        return pid,tid,logcattag,infotag,content1

