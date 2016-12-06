from xml.sax import ContentHandler
from xml.sax import make_parser
class dumpXmlHandler(ContentHandler):
    def __init__(self):
        self.dicts={}
        self.clicks={}
        self.pids=[]
        self.views={}
        self.viewflag=False
        self.viewtime=-1

    def startElement(self,name, attrs):
        if name=="invokedElement":
            clicktime=int(attrs.get("Clicktime",""))
            timestamp=int(attrs.get("Timestamp",""))
            classname=attrs.get("classname","")
            resource_id=attrs.get("resource-id","")

            left=attrs.get("coord-left","")
            top=attrs.get("coord-top","")
            right=attrs.get("coord-right","")
            bottom=attrs.get("coord-bottom","")


            text=attrs.get("text","")
            if len(text)>80:# if the text length>80 characters, only save the previous 80
                text=text[0:80]

            if not timestamp in self.clicks:
                self.clicks[timestamp]={}
                self.clicks[timestamp]["click"]=clicktime
                self.clicks[timestamp]["element"]=classname+"||"+resource_id+"||"+text
                self.clicks[timestamp]["resource"]=resource_id
                self.clicks[timestamp]["classname"]=classname
                self.clicks[timestamp]["text"]=text
                self.clicks[timestamp]["left"]=left
                self.clicks[timestamp]["right"]=right
                self.clicks[timestamp]["bottom"]=bottom
                self.clicks[timestamp]["top"]=top
        elif name=="pressBack":
            clicktime=int(attrs.get("Clicktime",""))
            timestamp=int(attrs.get("Timestamp",""))
            if not timestamp in self.clicks:
                self.clicks[timestamp]={}
                self.clicks[timestamp]["click"]=clicktime
                self.clicks[timestamp]["element"]="pressback"
        elif name=="Process":
            pid=int(attrs.get("pid",""))
            if not pid in self.pids:
                self.pids.append(pid)
        elif name=="hierarchy":
            timestamp=int(attrs.get("Timestamp",""))
            self.viewflag=True
            self.viewtime=timestamp
            self.views[timestamp]={}
        elif self.viewflag==True:
            #print name
            if not name in self.views[self.viewtime]:
                self.views[self.viewtime][name]=0
            self.views[self.viewtime][name]+=1




    def endElement(self, name):
        if name=="hierarchy":
            self.viewflag=False
        return

class DumpPageParser:
    def __init__(self,filename):
        handler=dumpXmlHandler()
        parser=make_parser()
        parser.setContentHandler(handler)
        parser.parse(open(filename,'r'))
        self.clicks=handler.clicks
        self.pids=handler.pids
        self.views=handler.views

