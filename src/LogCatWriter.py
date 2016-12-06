class LogCatWriter:
    def __init__(self,package,tagtime,report,dicts,splitdicts):
        f=file(report+"\\logcat.txt",'w')
        f.write("package,tagtime,clicktime,timestamp,pid,tid,infotag,content\n")
        for clicktime in sorted(splitdicts.keys()):
            etimes=splitdicts[clicktime]
            for etime in sorted(etimes):
                for infotag in dicts[etime]:
                    pid = dicts[etime][infotag]["pid"]
                    tid = dicts[etime][infotag]["tid"]
                    content = dicts[etime][infotag]["content"].replace("\"", "'")
                    #print "infotag",infotag
                    if infotag.endswith(":"):
                        infotag=infotag[0:-1]
                    writeline=package+","+str(tagtime)+","+str(clicktime)+','+str(etime)+","+str(pid)+','+str(tid)+','+str(infotag)+','+str(content)
                    f.write(writeline+"\n")
