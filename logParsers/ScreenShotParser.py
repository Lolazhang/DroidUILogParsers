class ScreenShotParser:
    def __init__(self,filenames):
        self.dicts={}
        for filename in filenames:
            #print filename
            name=filename.split("\\")[-1].replace(".png","")
            clicktime=int(name.split("_")[0])
            capturetime=int(name.split("_")[1])
            if not clicktime in self.dicts:
                self.dicts[clicktime]={}
            self.dicts[clicktime][capturetime]=filename