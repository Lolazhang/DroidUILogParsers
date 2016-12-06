class MemoryWriter:
    def __init__(self,package,report,tagtime,mdicts,splitdicts):
        self.fw=file(report+"\\memory.csv",'w')
        self.fw.write("package,tagtime,clicktime,timestamp,tag,item,value\n")
        self.keywords=["Native Heap","image mmap","Graphics","GL","TOTAL"]
        for clicktime in sorted(splitdicts.keys()):
            etimes=splitdicts[clicktime]
            for etime in sorted(etimes):
                dicts=mdicts[etime]
                for keyword in dicts:
                    if keyword in self.keywords:
                        totalpss=dicts[keyword]["totalpss"]
                        privatedirty=dicts[keyword]["privatedirty"]
                        writeline=package+","+str(tagtime)+","+str(clicktime)+","+str(etime)+","+keyword+","+"totalpss,"+str(totalpss)
                       # print writeline
                        self.fw.write(writeline+"\n")
                        writeline = package + "," + str(tagtime) + "," + str(clicktime) + "," + str(
                            etime) + "," + keyword + ",privatedirty" + "," + str(privatedirty)
                       # print writeline
                        self.fw.write(writeline+"\n")
                    if keyword=="DB":
                        for dbname in dicts["DB"]:
                            pgsz=dicts["DB"][dbname]["pgsz"]
                            dbsz=dicts["DB"][dbname]["dbsz"]
                            lookaside=dicts["DB"][dbname]["lookaside"]
                            cache=dicts["DB"][dbname]["cache"]
                            writeline=package+","+str(tagtime)+","+str(clicktime)+","+str(etime)+",DB,"+dbname+",pgsz"+str(pgsz)
                            self.fw.write(writeline + "\n")
                            writeline = package + "," + str(tagtime) + "," + str(clicktime) + "," + str(
                                etime) + ",DB," + dbname + ",dbsz" + str(dbsz)
                            self.fw.write(writeline + "\n")
                            writeline = package + "," + str(tagtime) + "," + str(clicktime) + "," + str(
                                etime) + ",DB," + dbname + ",lookaside" + str(lookaside)
                            self.fw.write(writeline + "\n")
                            writeline = package + "," + str(tagtime) + "," + str(clicktime) + "," + str(
                                etime) + ",DB," + dbname + ",cache" +str(cache)
                            self.fw.write(writeline + "\n")
                    if keyword=="OBJECTS":
                        views=dicts["OBJECTS"]["views"]
                        writeline = package + "," + str(tagtime) + "," + str(clicktime) + "," + str(etime) +",views,"+str(views)
                        self.fw.write(writeline+"\n")
                    if keyword=="ASSETALLOC":
                        for name in dicts["ASSETALLOC"]:
                            size=dicts["ASSETALLOC"][name]
                            writeline=  writeline=package+","+str(tagtime)+","+str(clicktime)+","+str(etime)+",ASSETALLOC,"+name+","+str(size)
                            self.fw.write(writeline+"\n")
                    if keyword=="SQL":
                        for key in dicts["SQL"]:
                            value=dicts["SQL"][key]
                            writeline=package+","+str(tagtime)+","+str(clicktime)+","+str(etime)+",SQL,"+key+","+str(value)
                            #print writeline
                            self.fw.write(writeline+"\n")






