class HttpSession:
    def __init__(self,frames,orderdicts,frags,requests,responses):
        self.frames=frames
        self.orderdicts=orderdicts
        self.frags=frags
        self.requests=requests
        self.timedicts={}
        self.responses=responses
        self.sessions={} # start tcp seqnumber_end tcp number: requests, responses, requesttime, responsetime, latency,
        self.Run()

    def Run(self):
        count=0
        for tcpseq in self.responses:
            responsestart = self.frags[tcpseq]["starttime"]
            requestseq=self.Search(self.frames[tcpseq]["id"],responsestart)
            if requestseq==-1:
                print "not found",tcpseq

            else:
                timestamp=self.frames[requestseq]["timestamp"]
                self.timedicts[timestamp]=requestseq
                if not requestseq in self.sessions:
                    self.sessions[requestseq]={}

                self.sessions[requestseq]["resseq"]=tcpseq
                self.sessions[requestseq]["request"]=self.frags[requestseq]["sequences"]
                self.sessions[requestseq]["response"]=self.frags[tcpseq]["sequences"]
                reqsize,_=self.GetPayloadSize(requestseq,self.frags[requestseq]["sequences"],"request")
                ressize,content_type=self.GetPayloadSize(tcpseq,self.frags[tcpseq]["sequences"],"response")
                self.sessions[requestseq]["requestdata"] = reqsize
                self.sessions[requestseq]["responsedata"] = ressize
                self.sessions[requestseq]["content-type"]=content_type
                self.sessions[requestseq]["starttime"]=self.frags[requestseq]["starttime"]
                self.sessions[requestseq]["endtime"]=self.frags[tcpseq]["endtime"]
                self.sessions[requestseq]["latency"]=self.frags[tcpseq]["endtime"]-self.frags[requestseq]["starttime"]


            count+=1
        for request in self.requests:
            if request not in self.sessions:
                #print "found here"
                timestamp = self.frames[request]["timestamp"]
                self.timedicts[timestamp] = request
                self.sessions[request]={}
                self.sessions[request]["resquest"]=self.frags[request]["sequences"]
                self.sessions[request]["response"]=[]
                self.sessions[request]["resseq"] = request
                reqsize, _ = self.GetPayloadSize(request, self.frags[request]["sequences"], "request")

                self.sessions[request]["requestdata"] = reqsize
                self.sessions[request]["responsedata"] = -1
                self.sessions[request]["content-type"] = ""
                self.sessions[request]["starttime"]=self.frags[request]["starttime"]
                self.sessions[request]["endtime"]=self.frags[request]["endtime"]
                self.sessions[request]["resseq"]=-1
                self.sessions[request]["latency"]=self.frags[request]["endtime"]-self.frags[request]["starttime"]

    def GetPayloadSize(self,tcpseq,sequences,method):
        content_type=""
        size=0
        for order in sorted(self.orderdicts[tcpseq].keys()):
            node=self.orderdicts[tcpseq][order]["node"]
            #print order, node
            http=self.frames[node]["http"]

            if method=="request":
               #print http.headers
               size+=self.frames[node]["length"]
            else:
                #print http.headers
                if "content-type" in http.headers:
                    content_type=http.headers["content-type"]
                size+=self.frames[node]["length"]
        return size, content_type




        #size=len(data)
        #print size



            #print "data",http.data
            #print "body",http.body

    def Search(self,id,responsestart):
        tcpseqs={}
        for tcpseq in self.requests:

                if self.frames[tcpseq]["id"]==id:
                    mystart = self.frags[tcpseq]["starttime"]
                    if mystart<responsestart:
                        tcpseqs[mystart]=tcpseq
        if tcpseqs=={}:
            return -1
        else:
            keys=sorted(tcpseqs.keys())
            return tcpseqs[keys[-1]] ## get the maxium number
