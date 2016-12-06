class queryClicks:
    def __init__(self,db, package,tagtime):
        self.dicts={} # clicktime, invoketime, element
        self.db=db
        cursor=self.db.cursor()
        command="select* from clicktrace where package=\""+package+"\" and tagtime=\""+str(tagtime)+"\""
        print command
        cursor.execute(command)
        results=cursor.fetchall()
        for result in results:
            clicktime=int(result[3])
            invoketime=result[4]
            element=result[5]
            if not clicktime in self.dicts:
                self.dicts[clicktime]={}
            self.dicts[clicktime]["invoketime"]=int(invoketime)
            self.dicts[clicktime]["element"]=element
