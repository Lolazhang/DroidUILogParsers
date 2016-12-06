import dpkt
import socket
class NetCapParser:
    def __init__(self,netfile):
        #print netfile
        f=open(netfile,'rb') ## rb tag is very important, otherwise, memoryerror  captured.
        pcap=dpkt.pcap.Reader(f)
        self.netstats={}#timestamp:tag: request/response
        self.frames={}
        self.httpsession={}
        self.httpsession["request"]=[]
        self.httpsession["response"]=[]
        f1=file("netdata.txt",'w')
        framecounter=0
        for ts, buf in pcap:

            timestamp=int((ts+28800)*1000.0)
            #print timestamp

            eth=dpkt.ethernet.Ethernet(buf)




            if not isinstance(eth.data, dpkt.ip.IP):
                print "NON ip packet type not supported"
                continue
            ip=eth.data


            ip_src=self.inet_to_str(ip.src)
            ip_dst=self.inet_to_str(ip.dst)

            ip1, ip2 = map(socket.inet_ntoa, [ip.src, ip.dst])
            #l7 = ip.data
            #sport, dport = [l7.sport, l7.dport]
            #print 'Ethernet Frame:', self.mac_addr(eth.src), self.mac_addr(eth.dst), eth.type
            #print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' % \
                  #(self.inet_to_str(ip.src), self.inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments,
                  # fragment_offset)


            tcp=ip.data
            tcpseqnumber=ip_src+"_"+ip_dst+"_"+str(tcp.seq)
            nextseq=tcp.seq+len(tcp.data)
            nexttcpseqnumber=ip_src+"_"+ip_dst+"_"+str(nextseq)

            sport,dport=[tcp.sport,tcp.dport]





            if tcp.dport==80 and len(tcp.data)>0:
                tcp=ip.data


                try:
                    request=dpkt.http.Request(tcp.data)
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    continue

                k = (ip2, dport, ip1, sport)
                if not framecounter in self.frames:
                    self.frames[framecounter]={}
                self.frames[framecounter]["timestamp"]=timestamp
                self.frames[framecounter]["seq"]=tcpseqnumber
                self.frames[framecounter]["nextseq"]=nexttcpseqnumber
                self.frames[framecounter]["tag"]="request"
                self.frames[framecounter]["http"]=request
                self.frames[framecounter]["length"]=len(tcp.data)

                self.frames[framecounter]["id"] = k

                if not timestamp in self.netstats:
                    self.netstats[timestamp]={}
                    self.netstats[timestamp]["tag"]=""
                    self.netstats[timestamp]["data"]=""
                self.netstats[timestamp]["tag"]="request"
                self.netstats[timestamp]["data"]=repr(request)
                #print request.method
                #print "request",request.uri
                #for header in request.headers.keys():
                    #print header,request.headers[header]
                # Print out the info
                #print 'Timestamp: Request', timestamp
                #print "http request:", request.body
                #print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' % \
                      #((ip.src), (ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments,
                     #  fragment_offset)
                #print 'HTTP request: %s\n' % repr(request)


               # print "request",k
                #print "tcp legnth",len(tcp.data)
                #print "http",len(request.data),"headers",len(request.headers),"body",len(request.body)
                if not "request" in self.httpsession:
                    self.httpsession["request"]=[]
                self.httpsession["request"].append(k)
                framecounter += 1


            if tcp.sport==80 and len(tcp.data)>0:

                try:
                    #print "seq number", tcp.seq,"next", tcp.seq+length
                    #self.dicts[tcp.seq] = tcp.seq + length

                    response=dpkt.http.Response(tcp.data)
                    k = (ip1, sport, ip2, dport)
                    #print "response",k
                    #print "tcp legnth", len(tcp.data)
                    #print "http", len(response.data), "headers", len(response.headers),"body",len(response.body)
                    if not "response" in self.httpsession:
                        self.httpsession["response"]=[]
                    self.httpsession["response"].append(k)


                    #print "Timestamp response:",timestamp
                    #print "Http response:%s\n"% repr(response)
                    #print "http response", response.body
                    if not timestamp in self.netstats:
                        self.netstats[timestamp] = {}
                        self.netstats[timestamp]["tag"] = ""
                        self.netstats[timestamp]["data"] = ""
                    self.netstats[timestamp]["tag"] = "response"
                    self.netstats[timestamp]["http"]=response

                    if not framecounter in self.frames:
                        self.frames[framecounter] = {}
                    self.frames[framecounter]["timestamp"] = timestamp
                    self.frames[framecounter]["seq"] = tcpseqnumber
                    self.frames[framecounter]["nextseq"] = nexttcpseqnumber
                    self.frames[framecounter]["tag"] = "response"
                    self.frames[framecounter]["http"] = response
                    self.frames[framecounter]["length"] = len(tcp.data)

                    self.frames[framecounter]["id"]=k
                    framecounter += 1

                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                     continue





    def mac_addr(self,address):
        """Convert a MAC address to a readable/printable string

           Args:
               address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
           Returns:
               str: Printable/readable MAC address
        """
        return ':'.join('%02x' % ord(b) for b in address)



    def inet_to_str(self,inet):
        """Convert inet object to a string

            Args:
                inet (inet struct): inet network address
            Returns:
                str: Printable/readable IP address
        """
        # First try ipv4 and then ipv6
        #try:
        return socket.inet_ntoa(inet)
            #return socket.inet_ntop(socket.AF_INET, inet)
        #except ValueError:
            #return socket.inet_ntop(socket.AF_INET6, inet)


