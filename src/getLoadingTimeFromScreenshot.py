from analyzers.loadingTimeSolverWithPic import *
class getLoadingTimeFromScreenshot:
    def __init__(self,package,tag,screenshots,screenpngs,db):
        self.db=db
        self.package=package
        self.screenpngs = screenpngs
        self.screenshots =screenshots
        loadingtime = loadingTimeSolverWithPic(screenpngs, screenshots)
        startdicts = loadingtime.startdicts
        enddicts = loadingtime.enddicts


        for click in enddicts:

            end = enddicts[click]
            if click in startdicts:
                start = startdicts[click]
            else:
                start=click
            if start>end:
                start=click
            command="insert into loadingtimescreenshot (`package`,`tagtime`,`clicktime`,`starttime`,`endtime`,`loadtime`) values("+"\""+self.package+"\",\"" +str(tag)+"\",\""+str(click)+"\",\""+str(start)+"\",\""+str(end)+"\"," +str(end-start)   + ")"
            print command
            cursor=self.db.cursor()
            cursor.execute(command)
            self.db.commit()

