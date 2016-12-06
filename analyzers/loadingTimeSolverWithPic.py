from screenshots.PngComparator import*
from screenshots.CorrectClickStart import *
from screenshots.CorrectClickEnd import *
class loadingTimeSolverWithPic:
    def __init__(self,screenpngs, screenshots):
        #self.clicks=clicks
        self.screenpngs=screenpngs
        self.screenshots=screenshots
        self.targetdicts={}
        self.applaunchTime=-1
        self.getTargetPic()
        self.enddicts={}
        self.startdicts={}
        self.CorrectClickTime()

        self.Run()
        print self.enddicts.keys()
        print self.enddicts

    def getTargetPic(self):
        for clicktime in sorted(self.screenpngs.keys()):

            #if clicktime in self.screenshots:
               # targetpngs = self.screenshots[clicktime]
                #targetpng = self.getTargetPngInShots(targetpngs)
            #else:
            targetpng = self.getTargetPngInPngs(self.screenpngs[clicktime])
            self.targetdicts[clicktime]=targetpng


    def CorrectClickTime(self):
        ## last time
        keylist=sorted(self.screenpngs.keys())
        index=1
        while index<len(keylist):
            currenttime=keylist[index]
            print currenttime
            lasttarget=self.targetdicts[keylist[index-1]]
            print "lasttarget",lasttarget
            dicts=self.screenpngs[currenttime]
            #print dicts
            redicts=self.Compare(dicts,lasttarget)
            correctstart=CorrectClickStart(redicts).starttime
            print "correct",correctstart
            self.startdicts[currenttime]=currenttime
            if correctstart!=-1:
                self.startdicts[currenttime]=correctstart
            print '\n'
            index+=1


    def Run(self):
        for clicktime in sorted(self.screenpngs.keys()):
            dicts=self.screenpngs[clicktime]
            targetpng=self.targetdicts[clicktime]
            print clicktime
            self.enddicts[clicktime]=clicktime
            redicts=self.Compare(dicts,targetpng)
            endtime=CorrectClickEnd(redicts).endtime
            print "endtime",endtime
            if endtime!=-1:
                self.enddicts[clicktime]=endtime




    def Compare(self,dicts,targetpng):
        redicts={}
        for timestamp in sorted(dicts.keys()):
            #print timestamp
            capture=dicts[timestamp]

            print capture.split("\\")[-1],targetpng.split("\\")[-1]


            similarity=PngComparator(capture, targetpng).similarity
            print similarity
            redicts[timestamp]=similarity
        return redicts
    def getTargetPngInPngs(self,dicts):
        #keylist=
        #print sorted(dicts.keys())
        value=sorted(dicts.keys())[-1]
        #print value
        return dicts[value]

    def getTargetPngInShots(self,targetpng):
        key= targetpng.keys()[0]
        return targetpng[key]