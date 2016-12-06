import Image
import os
from glob import glob
class ScreenShotConverter:
    def __init__(self,filenames):

        self.Convert(filenames)

    def Convert(self,filenames):
        for filename in filenames:

            img=Image.open(filename)


            #rawData = open(filename, 'rb').read()
           # imgSize = (1440, 2560)
            #img = Image.fromstring('RGBA', imgSize, rawData)
            cropbox = [0, 0, 1440, 70]
            cropbox = [0, 71, 1440, 2560]
            newimg = img.crop(cropbox)
            #newfilename="d:\\test\\data1\\bbc,mobile.news.ww\\"+filename.split("\\")[-1]
            newimg.save(filename)


