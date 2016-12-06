class SplitTimestamps:
    def __init__(self,clicktimes, targets,timestamp):
        self.dicts={} # click: [times]
        self.clicktimes=clicktimes
        self.targets=targets
        self.starttime=int(timestamp)
        self.Run()

    def Run(self):
        index=0
        selected=[]
        targets=self.targets
        #print targets
        #print targets

        while index<len(self.clicktimes):
            target=self.clicktimes[index]
            #print target
            if not target in self.dicts:
                self.dicts[target]=[]
            if index<len(self.clicktimes)-1:
                next=self.clicktimes[index+1]

                for timestamp in targets:
                    #print timestamp, target, next
                    if timestamp>=target and timestamp<=next:
                       # print "fpound"
                        #print timestamp, target,next
                        self.dicts[target].append(timestamp)

                        targets.remove(timestamp)


            else:
                for timestamp in targets:
                    if timestamp>=target :
                        self.dicts[target].append(timestamp)

                        targets.remove(timestamp)
            index+=1
        #print len(selected),len(self.targets)
        if len(targets)>0:
            self.dicts[self.starttime]=targets



