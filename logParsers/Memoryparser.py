##https://developer.android.com/studio/profile/investigate-ram.html
class Memoryparser:
    def __init__(self,filenames):
        self.dicts={}
        self.processCreatedTime=-1
        for filename in filenames:
            f=file(filename,'r')



            self.timestamp=int(filename.split("\\")[-1].replace(".txt",""))
            self.dicts[self.timestamp]={} # SQL, keyword, DB, ASSETALLOC, OBJECT
            self.startime=-1
            self.sqltag=False
            self.dbtag=False
            self.asserttag=False
            self.viewtag=False
            while True:
                line=f.readline()
                if not line:
                    break
                content=line
                #print content
                self.ParseLine(content)

    def ParseLine(self,content):


        if "Uptime" in content:
            items=content.split(" ")
            #print items
            uptime=int(items[1])
            realtime=int(items[3])
            if self.processCreatedTime==-1:
                self.processCreatedTime=self.timestamp
            #print uptime,realtime
        keywords=["Native Heap","Dalvik Heap","Dalvik Other","Stack","Other dev",".so mmap",".apk mmap",".ttf mmap",".dex mmap","code mmap","image mmap","Other mmap","Graphics","GL",
                  "Unknown","TOTAL"]
        for keyword in keywords:
            if keyword in content:

                dicts=self.parseItem1(keyword,content)

                self.dicts[self.timestamp][keyword]=dicts[keyword]
        databasekeywords=["DATABASES","SQL"]
        if "Objects" in content:
            self.viewtag=True
            self.dicts[self.timestamp]["OBJECTS"]={}
        if "SQL" in content:
            self.sqltag=True
            self.viewtag=False
            self.dicts[self.timestamp]["SQL"]={}
        if self.viewtag==True:
            self.parseObject(content)
        if "DATABASES" in content:
            self.sqltag=False
            self.dbtag=True
        if self.sqltag==True:
            self.parseSQLItem(content)

        if "Asset Allocations" in content:
            self.dbtag=False
            self.asserttag=True
        if self.dbtag==True:
            if not "DB" in self.dicts[self.timestamp]:

                self.dicts[self.timestamp]["DB"]={}
            self.parseDBItem(content)
        if self.asserttag==True:
            self.dicts[self.timestamp]["ASSETALLOC"]={}
            self.parseAssetAllocations(content.strip())

    def parseObject(self,content):
        if "Objects" not in content:
            views=-1
            viewrootimpl=-1
            appcontext=-1
            activities=-1
            assets=-1
            assetsmanagers=-1
            localbinders=-1
            proxybinders=-1
            deathrecipients=-1
            opensslsockets=-1

            if "Views" in content:
                items=content.split()
                views=int(items[1])
                viewrootimp=int(items[3])
                self.dicts[self.timestamp]["OBJECTS"]["views"]=views
                self.dicts[self.timestamp]["OBJECTS"]["viewrootimpl"] = viewrootimp
            if "AppContexts" in content:
                items=content.split()
                appcontext=int(items[1])
                activities=int(items[3])
                self.dicts[self.timestamp]["OBJECTS"]["appcontexts"] =appcontext
                self.dicts[self.timestamp]["OBJECTS"]["activities"] = activities
            if "Assets" in content:
                items=content.split()
                #print items
                assets=int(items[1])
                assetsmanagers=int(items[3])
                self.dicts[self.timestamp]["OBJECTS"]["assets"] = assets
                self.dicts[self.timestamp]["OBJECTS"]["assetsmanagers"] = assetsmanagers
            if "Local Binders" in content:
                line=content.replace("Local Binders","LocalBinders").replace("Proxy Binders","ProxyBinders")
                items=line.split()
                localbinders=int(items[1])
                proxybinders=int(items[3])
                self.dicts[self.timestamp]["OBJECTS"]["localbinders"] = localbinders
                self.dicts[self.timestamp]["OBJECTS"]["proxybinders"] = proxybinders
            if "Death Recipients" in content:
                items=content.split()
                deathrecipients=int(items[2])
                self.dicts[self.timestamp]["OBJECTS"]["deathrecipients"] = deathrecipients
            if "OpenSSL Sockets" in content:
                items=content.split()
                opensslsockets=int(items[2])
                self.dicts[self.timestamp]["OBJECTS"]["opensslsockets"] = opensslsockets




    def parseAssetAllocations(self,content):
        #print content
        if "Asset Allocations" not in content:
            items=content.split(":")
            size=items[-1]
            name=content.split(size)[0]
            self.dicts[self.timestamp]["ASSETALLOC"][name]=size


    def parseDBItem(self,content):
        if "pgsz" not in content and "DATABASES" not in content:
            #print content
            items=content.split()
            #print items
            #print len(items)
            index=0
            count=0
            pgsz=-1
            dbsz=-1
            lookaside=-1
            cache=""
            dbname=""
            if len(items)==5:
                pgsz=int(items[0])
                dbsz=int(items[1])
                lookaside=int(items[2])
                cache=items[3]
                dbname=items[4]
            elif len(items)>0:
                if len(items)==4:
                    dbname=items[3]
                    cache=items[2]
                    lookaside=int(items[1])
                    dbsz=int(items[0])
                if len(items)==3:
                    dbname=items[2]
                    cache=items[1]
                    lookaside=int(items[0])
                if len(items)==2:
                    dbname=items[1]
                    cache=items[0]


            if not dbname in self.dicts[self.timestamp]["DB"]:
                self.dicts[self.timestamp]["DB"][dbname]={}
            #print dbname
            self.dicts[self.timestamp]["DB"][dbname]["pgsz"]=pgsz
            self.dicts[self.timestamp]["DB"][dbname]["dbsz"] = dbsz
            self.dicts[self.timestamp]["DB"][dbname]["lookaside"] =lookaside
            self.dicts[self.timestamp]["DB"][dbname]["cache"] = cache


            #if len(items)>0 and len(items)!=5:
                #print content
                #print items
            '''
            while index<len(items):
                item=items[index]
                if item!="":
                    if count==0:
                        pgsz=int(item)
                    if count==1:
                        dbsz=int(item)
                    if count==2:
                        lookaside=int(item)
                    if count==3:
                        cache=item
                    if count==4:
                        dbname=item


                    count+=1


                index+=1
            print pgsz,dbsz, lookaside,cache,dbname
            '''


    def parseSQLItem(self,content):
        content=content.strip()
        if "MEMORY_USED" in content:
            items= content.split(" ")
            index=1
            value=-1
            while index<len(items):
                item=items[index]
                if item!="":
                    value=int(item)
                    break
                index+=1
            #print value
            self.dicts[self.timestamp]["SQL"]["memory_used"]=value
        if "MALLOC_SIZE" in content:
            items=content.split(" ")
            pagecache_overflow=-1
            malloc_size=-1
            memory_used=-1
            index=1
            count=0

            while index<len(items):
                item=items[index]
                if item!="" and item!="MALLOC_SIZE:":
                    if count==0:
                        pagecache_overflow=int(item)
                    if count==1:
                        malloc_size=int(item)

                    count+=1
                index+=1
            #print pagecache_overflow,malloc_size
            self.dicts[self.timestamp]["SQL"]["pagecache_overflow"]=pagecache_overflow
            self.dicts[self.timestamp]["SQL"]["malloc_size"]=malloc_size





    def parseItem1(self,keyword,content):
        content=content.strip()

        if keyword in content:
            items=content.split(keyword+" ")[-1].split((" "))

            #print items
            index=0
            totalpss=0
            privatedirty=0
            privateclean=0
            swappeddrity=0
            heapsize=-1
            heapalloc=-1
            heapfree=-1
            #print items

            for item in items:
                if item!="" :
                    #print "here",item, ord(item)
                    if index==0:
                        totalpss=int(item)
                    if index==1:
                        privatedirty=int(item)
                    if index==2:
                        privateclean=int(item)
                    if index==3:
                        swappeddrity=int(item)
                    if index==4:
                        heapsize=int(item)
                    if index==5:
                        heapalloc=int(item)
                    if index==6:
                        heapfree=int(item)


                    index+=1
            #print totalpss,privatedirty,privateclean,swappeddrity,heapsize,heapalloc,heapfree
            dicts={}
            dicts[keyword]={}
            dicts[keyword]["totalpss"]=totalpss
            dicts[keyword]["privatedirty"]=privatedirty
            dicts[keyword]["privateclean"]=privateclean
            dicts[keyword]["swappeddirty"]=swappeddrity
            dicts[keyword]["heapsize"]=heapsize
            dicts[keyword]["heapalloc"]=heapalloc
            dicts[keyword]["heapfree"]=heapfree
            return dicts


