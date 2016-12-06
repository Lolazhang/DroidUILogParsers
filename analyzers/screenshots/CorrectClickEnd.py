class CorrectClickEnd:
    def __init__(self,dicts):
        keylists=sorted(dicts.keys())
        self.endtime=-1
        index=0
        count=0
        while index<len(keylists):
            timestamp=keylists[index]
            similarity=dicts[timestamp]
            if similarity==1:
                self.endtime=timestamp

                break
            count+=1
            index+=1
        if self.endtime==-1:
            self.endtime=keylists[-1]
        elif count==0:
            self.endtime=-1
