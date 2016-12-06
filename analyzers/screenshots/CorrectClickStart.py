class CorrectClickStart:
    def __init__(self,dicts):
        self.dicts={}
        self.starttime=-1
        keylists=sorted(dicts.keys())
        index=0
        count=0
        while index<len(keylists):
            similarity=dicts[keylists[index]]
            if similarity==1:
                count+=1
                self.starttime=keylists[index]
            index+=1
        #print index
        if count==len(keylists):
            self.starttime=-1



