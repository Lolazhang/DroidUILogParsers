from FrameCollector import *
from HttpSession import *
class Constructor:
    def __init__(self,frames,starttime):
        self.frames=frames
        self.latency={}
        self.size={}
        self.objects={}
        self.images={}
        self.dicts={}
        self.packets={}
        self.sessions={}
        self.timedicts={}
        self.Init()
        self.Run()

    def Run(self):
        selected=[]
        framecollector=FrameCollector(self.dicts)

        #self.fragments=FrameCollector(self.dicts).results#tcpseq, orders: order: node: next
        httpSession=HttpSession(self.dicts,framecollector.results,framecollector.frags,framecollector.requests,framecollector.responses)
        self.sessions=httpSession.sessions
        self.timedicts=httpSession.timedicts




    def Init(self):
        frames=self.frames
        for framenum in frames:
            timestamp=frames[framenum]["timestamp"]
            tcpseq=frames[framenum]["seq"]
            nextseq=frames[framenum]["nextseq"]
            tag=frames[framenum]["tag"]
            http=frames[framenum]["http"]
            self.dicts[tcpseq]={}
            self.dicts[tcpseq]["timestamp"]=timestamp
            self.dicts[tcpseq]["nextseq"]=nextseq
            self.dicts[tcpseq]["tag"]=tag
            self.dicts[tcpseq]["http"]=http
            self.dicts[tcpseq]["length"]=frames[framenum]["length"]
            self.dicts[tcpseq]["id"]=frames[framenum]["id"]# request: dst_ip, dst_port, src_ip, src_port; response: src_ip, src_port, dst_ip, dst_port




