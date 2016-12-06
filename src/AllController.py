from glob import glob
from logParsers.Memoryparser import *
from numpy import sort
from logParsers.DumpPageParser import *
import os
from systraceAnalysis.sysTrace import *
from sysTraceAnalysis import *
from logParsers.LogCatAllParser import *
from logParsers.LogCatEventParser import *
from logParsers.NetCapParser import *
from CollectingLogs import *

from analyzers.loadingTimeSolver import *
from analyzers.loadingTimeSolverWithPic import *
from logParsers.ScreenCapConverter import *
from logParsers.ScreenShotConverter import *
from logParsers.ScreenShotParser import *
from getLoadingTimeFromScreenshot import *
from sqlhelpers.ConnectToDB import *
from sqlhelpers.queryClicks import *
from sqlhelpers.queryLoadtime import *
from utils.SplitTimestamps import *
from logParsers.StraceParser import *
from netReconstructor.Constructor import*
from MemoryWriter import *
from LogCatWriter import*
from analyzers.loadingTimeSolver import *
from analyzers.loadingTimeSolverWithPic import *
from logParsers.ScreenCapConverter import *
from logParsers.ScreenShotConverter import *
from logParsers.ScreenShotParser import *
from getLoadingTimeFromScreenshot import *


class AllController:
    def __init__(self,dir):
        self.dir = dir
        self.memoryFiles = glob(dir + "\\**\\**.txt")
        self.logcatAlls = glob(dir + "\\logcatAll_**.txt")
        self.logcatEvents = glob(dir + "\\logcatEvent_**.txt")
        self.systraces = glob(dir + "\\**\\**.html")
        self.netcaps = glob(dir + "\\**_network_**.cap")
        self.stracefiles=glob(dir+"\\**strace_**.trace")
        self.dumpPages = glob(dir + "\\dumpPage_**.xml")
        self.screenshots = glob(dir + "\\screenshot_**\\**.png")


        self.screenpngs = glob(dir + "\\screenpng_**\\**.png")

        self.package = dir.split("\\")[-1]
        print self.package

        self.reportdir = "results\\" + self.package
        if os.path.isdir(self.reportdir) == False:
            os.mkdir(self.reportdir)
        self.files = []
        self.files.extend(self.memoryFiles)
        self.files.extend(self.logcatAlls)
        self.files.extend(self.logcatEvents)
        self.files.extend(self.systraces)
        self.files.extend(self.netcaps)
        self.files.extend(self.stracefiles)
        self.files.extend(self.dumpPages)
        self.files.extend(self.screenpngs)
        self.files.extend(self.screenshots)
        self.filedicts = {}

        self.data = {}
        self.dir="results\\"+self.package
        if os.path.isdir(self.dir)==False:
            os.mkdir(self.dir)

        connect = ConnectToDB()
        connect.connect("uilogs")
        self.db = connect.db

        self.filedicts = CollectingLogs(self.files).filedicts
        self.run()
        #self.runNetcap()
        #self.runStrace()


    def getCount(self,mtimes,mdicts):
        values=[]
        for mtime in sorted(mtimes):
            if "SQL" in mdicts[mtime]:
                size = mdicts[mtime]["SQL"]["malloc_size"]
                # print clicktime,mtime,size
            dbcount = 0
            if "DB" in mdicts[mtime]:
                dbcount = len(mdicts[mtime]["DB"].keys())
            values.append(dbcount)
        if len(values)>0:
            return max(values)
        else:
            return 0








    def WriteStrace(self,splitdicts,strace,starttime):

        for clicktime in sorted(splitdicts.keys()):
            totaltime=0
            filecount=0
            stimes=splitdicts[clicktime]
            for stime in stimes:

                for fname in strace[stime]:
                    timespent=strace[stime][fname]["timespent"]
                    filename=strace[stime][fname]["filename"]
                    print filename
                    cursor=self.db.cursor()
                    command="insert into `Strace` (`package`, `tagtime`, `clicktime`,`timestamp`, `function`,`latency`,  `filename`  ) values(\""+self.package+"\",\""+str(starttime)+"\",\""+str(clicktime)+"\",\""+str(stime)+"\",\""
                    command+=fname+"\","+str(timespent)+",\""+filename+"\")"
                    print command
                    cursor.execute(command)
                    self.db.commit()





    def run(self):

        for timestamp in self.filedicts:
            clicks={}
            memory={}
            print self.filedicts[timestamp].keys()
            screenshots={}
            screenpngs={}
            appcreatedtime=-1
            if "memoryInfo" in self.filedicts[timestamp]:
                memoryFiles = self.filedicts[timestamp]["memoryInfo"]
                memoryparser=Memoryparser(memoryFiles)
                memory=memoryparser.dicts
                print "app created time",memoryparser.processCreatedTime
                appcreatedtime=memoryparser.processCreatedTime
                #mdicts = Memoryparser(memoryFiles).dicts  # timestamp: DB:dbname

            if "dumpPage" in self.filedicts[timestamp]:
                dumper = DumpPageParser(self.filedicts[timestamp]["dumpPage"])
                clicks = dumper.clicks
                pids=dumper.pids
                views=dumper.views
                viewdicts=self.GetClickViews(clicks,views,timestamp)


                self.WriteClickToSQL(clicks,viewdicts,timestamp)
                self.WriteApp(pids,timestamp,appcreatedtime)
                splitdicts = SplitTimestamps(list(sort(clicks.keys())), list(sort(memory.keys())), timestamp).dicts
                MemoryWriter(self.package,self.dir,timestamp,memory,splitdicts)
            if "strace" in self.filedicts[timestamp]:
                stracefile = self.filedicts[timestamp]["strace"]
                print stracefile
                strace = StraceParser(stracefile).dicts  # timestamp: functioname: function,filename,timespent
                splitdicts = SplitTimestamps(list(sort(clicks.keys())), list(sort(strace.keys())),
                                                 timestamp).dicts  ##clicktime: []

                #self.WriteStrace(splitdicts, strace, timestamp)
            if "network" in self.filedicts[timestamp]:
                netcapfile = self.filedicts[timestamp]["network"]
                print netcapfile
                netdicts = NetCapParser(netcapfile).frames  # timestamp: tag: request/response
                constructor = Constructor(netdicts, timestamp)
                #self.WriteNetToSql(constructor.timedicts, constructor.sessions, timestamp, clicks)


            if "logcatAll" in self.filedicts[timestamp]:
                logcatAllfile = self.filedicts[timestamp]["logcatAll"]
                logcatalllogs = LogCatAllParsers(logcatAllfile).dicts
                splitdicts = SplitTimestamps(list(sort(clicks.keys())), list(sort(logcatalllogs.keys())), timestamp).dicts
                #self.WriteAll(logcatalllogs, clicks, timestamp)
                LogCatWriter(self.package,timestamp,self.dir,logcatalllogs,splitdicts)
            if "logcatEvent" in self.filedicts[timestamp]:
                logcatEventfile = self.filedicts[timestamp]["logcatEvent"]
                    # print logcatEventfile
                eventdicts = LogCatEventParser(logcatEventfile).dicts
                self.WriteEvent(eventdicts, clicks, timestamp)
            if "screenpng" in self.filedicts[timestamp]:
                print "screenpng here"
                screencaps = self.filedicts[timestamp]["screenpng"]
                screenpngs= ScreenShotParser(screencaps).dicts
            if "screenshot" in self.filedicts[timestamp]:
                screenshots = self.filedicts[timestamp]["screenshot"]
                screenshots= ScreenShotParser(screenshots).dicts
            getLoadingTimeFromScreenshot(self.package, timestamp, screenshots, screenpngs, self.db)


    def WriteAll(self, logcatdicts, clicks, timestamp):
            splitdicts = SplitTimestamps(list(sort(clicks.keys())), list(sort(logcatdicts.keys())), timestamp).dicts
            for clicktime in sorted(splitdicts.keys()):
                etimes = splitdicts[clicktime]
                for etime in sorted(etimes):
                    for infotag in logcatdicts[etime]:
                        pid = logcatdicts[etime][infotag]["pid"]
                        tid = logcatdicts[etime][infotag]["tid"]
                        content = logcatdicts[etime][infotag]["content"].replace("\"", "'")
                        cursor = self.db.cursor()
                        command = "insert into `LogcatAlls` (`package`,`tagtime`,`clicktime`,`timestamp`,`tag`,`pid`,`tid`,`content`) values("
                        command += "\"" + self.package + "\",\"" + str(timestamp) + "\",\"" + str(
                            clicktime) + "\",\"" + str(etime) + "\",\"" + infotag + "\","
                        command += str(pid) + "," + str(tid) + ",\"" + content + "\")"
                        # print command
                        cursor.execute(command)
                        self.db.commit()

    def WriteEvent(self, eventdicts, clicks, timestamp):
            splitdicts = SplitTimestamps(list(sort(clicks.keys())), list(sort(eventdicts.keys())), timestamp).dicts
            # print splitdicts
            for clicktime in sorted(splitdicts.keys()):
                eventtimes = splitdicts[clicktime]
                for etime in sorted(eventtimes):
                    # print clicktime,etime, eventdicts[etime]
                    for infotag in eventdicts[etime]:
                        content = eventdicts[etime][infotag]
                        cursor = self.db.cursor()
                        command = "insert into `LogcatEvents` (`package`,`tagtime`,`clicktime`,`timestamp`,`tag`,`content`) values(" + "\"" + self.package + "\",\"" + str(
                            timestamp) + "\",\"" + str(clicktime) + "\",\"" + str(
                            etime) + "\",\"" + infotag + "\",\"" + content + "\"" + ")"
                        # print command
                        cursor.execute(command)
                        self.db.commit()





                        #print clicks
    def GetClickViews(self,clicks,views,starttime):
        redicts={}
        clicktimes=sorted(clicks.keys())
        viewtimes=sorted(views.keys())
        #print len(clicktimes),len(viewtimes)

        redicts[starttime]=self.getTotal(views[viewtimes[0]])
        index=0
        while index<len(clicktimes):
            clicktime=clicktimes[index]
            if index+1<len(clicktimes):
                viewtime=viewtimes[index+1]
                redicts[clicktime] = self.getTotal(views[viewtime])
            else:
                redicts[clicktime]=0

            index+=1
        return redicts


    def getTotal(self,dicts):
        total=0
        for item in dicts:
            total+=dicts[item]
        return total



    def WriteApp(self,pids,timestamp,applaunchtime):
        value=""
        for pid in pids:
            value+=str(pid)+","
        if value.endswith(","):
            value=value[0:-1]
        cursor=self.db.cursor()
        command="insert into `App` (`package`, `tagtime`,`launchtime` , `pids`) values( \""+self.package+"\",\""+str(timestamp)+"\",\""+str(applaunchtime)+"\",\""+value+"\")"
        print command
        #print command
        cursor.execute(command)
        self.db.commit()

    def WriteClickToSQL(self,clicks,viewdicts,timestamp):
            if timestamp in viewdicts:
                command = "insert into clicktrace (`package`,`tagtime`,`clicktime`,`invoketime`,`element`,   `views`,`resourceid`,`classname`,`text`,`left`,`top`,`right`,`bottom`) values(\"" + self.package + "\",\"" + str(
                    timestamp) + "\","
                command += "\"" + str(timestamp) + "\",\"" + str(timestamp) + "\",\"" + "App Launch"+ "\"," + str(viewdicts[timestamp]) + ","
                command += "\"" + str(-1) + "\",\"" + str(-1) + "\",\"" + str(-1) + "\"," + str(-1) + "," + str(
                    -1) + "," + str(-1) + "," + str(-1)
                command += ")"
                cursor = self.db.cursor()
                cursor.execute(command)
                self.db.commit()
            for clicktime in clicks:
                invoketime=clicks[clicktime]["click"]
                element=clicks[clicktime]["element"]
                command="insert into clicktrace (`package`,`tagtime`,`clicktime`,`invoketime`,`element`,   `views`,`resourceid`,`classname`,`text`,`left`,`top`,`right`,`bottom`) values(\""+self.package+"\",\""+str(timestamp)+"\","
                command+="\""+str(clicktime)+"\",\""+str(invoketime)+"\",\""+element+"\","+str(viewdicts[clicktime])+","

                if element!="pressback":
                    resource=clicks[clicktime]["resource"]
                    classname=clicks[clicktime]["classname"]
                    text=clicks[clicktime]["text"]
                    left=clicks[clicktime]["left"]
                    right=clicks[clicktime]["right"]
                    bottom=clicks[clicktime]["bottom"]
                    top=clicks[clicktime]["top"]
                    command+="\""+resource+"\",\""+classname+"\",\""+text+"\","+str(left)+","+str(top)+","+str(right)+","+str(bottom)

                else:
                    command += "\"" + str(-1) + "\",\"" +  str(-1) + "\",\"" + str(-1) + "\"," +  str(-1)  + "," +  str(-1)  + "," +  str(-1)  + "," +  str(-1)
                command+=")"
                command=command.encode("utf-8")
                print command
                cursor=self.db.cursor()
                cursor.execute(command)
                self.db.commit()







                #self.Write(netdicts,splitdicts)
    def WriteNetToSql(self,timedicts,httpsessions,startime,clicks):
        splitdicts=SplitTimestamps(list(sort(clicks.keys())),list(sort(timedicts.keys())),startime).dicts
        for clicktime in sorted(splitdicts.keys()):
            etimes=splitdicts[clicktime]
            for etime in sorted(etimes):
                seq=timedicts[etime]
                starttime=httpsessions[seq]["starttime"]
                endtime=httpsessions[seq]["endtime"]
                latency=httpsessions[seq]["latency"]
                requestdata=httpsessions[seq]["requestdata"]
                responsedata=httpsessions[seq]["responsedata"]
                content_type=httpsessions[seq]["content-type"]
                if httpsessions[seq]["response"]==[]:
                    tag="only request"
                else:
                    tag="session"

                cursor=self.db.cursor()
                command="insert into `Network` (`package`,`tagtime`,`clicktime`,`timestamp`,`tag`,`contenttype`, `starttime`,      `endtime`,`latency`,`uploadsize`,        `downloadsize`  )values("
                command+="\""+self.package+"\",\""+str(startime)+"\",\""+str(clicktime)+"\",\""+str(etime)+"\",\""+tag+"\",\""+content_type+"\","+str(starttime)+","+str(endtime)+","+str(latency)+","+str(requestdata)+","+str(responsedata)+")"
                print command
                cursor.execute(command)
                self.db.commit()
























