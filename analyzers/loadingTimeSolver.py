from utils.SplitTimestamps import *
from numpy import sort
class loadingTimeSolver:
    def __init__(self,clickdicts, memorydicts,networkdicts,starttime,packageName):
        self.dicts={}
        self.clicks=clickdicts
        self.memorydicts=memorydicts
        self.packageName=packageName
        self.networkdicts=networkdicts
        clicktimes = []
        self.odicts={}
        for timestamp in self.clicks:
            clicktimes.append(self.clicks[timestamp]["click"])
            self.odicts[self.clicks[timestamp]["click"]] = timestamp
        self.clicksplits = SplitTimestamps(list(sort(clicktimes)),
                                           list(sort(self.memorydicts.keys())),starttime).dicts  # click:[]
        #print self.clicksplits
        self.netsplits=SplitTimestamps(list(sort(clicktimes)), list(sort(self.networkdicts.keys())),starttime).dicts
        #print self.netsplits
        self.__run()

    def __run(self):
        keylist=[]
        for clicktime in self.clicksplits:
            keylist.append(clicktime)
        keylist.sort()
        newkeylist=keylist
        print newkeylist
        f=file(self.packageName+"_memory.csv",'w')
        for clicktime in newkeylist:

            mtimes=self.clicksplits[clicktime]
            print clicktime,len(mtimes)
            if clicktime in self.odicts:
                otime=self.odicts[clicktime]
                content=self.clicks[otime]["element"]
            else:
                content="launch app"
            starttime=0
            print str(content.encode("utf-8"))
            f.write(content.encode("utf-8")+"\n")
            if len(mtimes)>0:
                starttime=min(mtimes)
            #print clicktime
            for mtime in mtimes:
                if "TOTAL" in self.memorydicts[mtime]:
                    total=self.memorydicts[mtime]["TOTAL"]["privatedirty"]
                    graphic=0
                    if "Graphics" in self.memorydicts[mtime]:
                        graphics=self.memorydicts[mtime]["Graphics"]["privatedirty"]
                        GL=self.memorydicts[mtime]["GL"]["privatedirty"]
                        graphic=graphics+GL
                    #print mtime, graphic,total

                    writeline=str(clicktime)+","+str(mtime)+","+str(total)+","+str(graphic)+","+str(mtime-starttime)
                    f.write(writeline+"\n")
            f.write("\n")

        f1=file(self.packageName+"_network.csv",'w')
        print "write network"
        for clicktime in newkeylist:
            mtimes=self.netsplits[clicktime]
            print clicktime, len(mtimes)
            if clicktime in self.odicts:
                otime = self.odicts[clicktime]
                content = self.clicks[otime]["element"]
            else:
                content = "launch app"
            starttime = 0
            print str(content.encode("utf-8"))
            f1.write(content.encode("utf-8") + "\n")
            if len(mtimes) > 0:
                starttime = min(mtimes)
            for mtime in mtimes:
                tag=self.networkdicts[mtime]["tag"]
                writeline=str(clicktime)+","+str(mtime)+","+str(tag)+","+str(mtime-starttime)
                f1.write(writeline+"\n")
                print "write netwoirk"
            f1.write("\n")

            #print '\n'



