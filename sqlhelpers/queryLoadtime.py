class queryLoadtime:
    def __init__(self,db,package,tagtime):
        cursor=db.cursor()
        self.dicts={}
        command="select * from loadingtimescreenshot where package=\""+package+"\" and tagtime=\""+str(tagtime)+"\""
        cursor.execute(command)
        results=cursor.fetchall()
        for result in results:
            clicktime=int(result[3])
            starttime=result[4]
            endtime=result[5]
            if not clicktime in self.dicts:
                self.dicts[clicktime]={}
            self.dicts[clicktime]["start"]=int(starttime)
            self.dicts[clicktime]["end"]=int(endtime)

