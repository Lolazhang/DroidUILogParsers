class FrameCollector:
    def __init__(self,frames):
        self.frames=frames
        self.results={}
        self.frags={} #startseq: sequences[], starttime., endtime, tag:
        self.responses=[]
        self.requests=[]

        self.visited=[]
        self.Run()

    def Run(self):
        self.dicts={}
        keys=self.frames.keys()
        for tcpseq in keys:
            #print tcpseq
            if tcpseq not in self.visited:
                self.renodes={}
                self.renodes[0]={}
                self.renodes[0]["node"]=tcpseq
                self.renodes[0]["next"]=""

                self.visited.append(tcpseq)

                self.getSequenced(tcpseq,0)
                #print tcpseq,self.renodes
                self.results[tcpseq]=self.renodes
                self.frags[tcpseq]={}
                self.frags[tcpseq]["sequences"]=[]
                self.frags[tcpseq]["starttime"]=-1
                self.frags[tcpseq]["endtime"]=-1
                self.frags[tcpseq]["tag"]=self.frames[tcpseq]["tag"]
                sequences=[]
                timestamps=[]
                for index in self.renodes:
                    node=self.renodes[index]["node"]
                    sequences.append(node)
                    timestamps.append(self.frames[node]["timestamp"])

                self.frags[tcpseq]["sequences"]=sequences
                self.frags[tcpseq]["starttime"]=min(timestamps)
                self.frags[tcpseq]["endtime"]=max(timestamps)

                if self.frames[tcpseq]["tag"]=="request":
                    self.requests.append(tcpseq)
                if self.frames[tcpseq]["tag"]=="response":
                    #print tcpseq, self.renodes

                    self.responses.append(tcpseq)









    def getSequenced(self,tcpseq,index):
        nextseq=self.frames[tcpseq]["nextseq"]
        if nextseq in self.frames:
            if not index in self.renodes:
                self.renodes[index]={}
            self.renodes[index]["node"]=tcpseq
            self.renodes[index]["next"]=nextseq


            self.visited.append(nextseq)
            self.getSequenced(nextseq,index+1)






