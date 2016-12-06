import Image
import os
from glob import glob
class ScreenCapConverter:
    def __init__(self,filenames):

        self.Convert(filenames)

    def Convert(self,filenames):
        for filename in filenames:
            picname=filename.split("\\")[-1]
            dir=filename.split(picname)[0].replace("screencap_","screenpng_")

            if os.path.isdir(dir)==False:
                os.mkdir(dir)
            rawData = open(filename, 'rb').read()
            imgSize = (1440, 2560)
            img = Image.fromstring('RGBA', imgSize, rawData)
            newfilename=filename.replace(".raw",".png").replace("screencap_","screenpng_")
            cropbox=[0,0,1440,70]
            cropbox=[0,71,1440,2560]
            newimg=img.crop(cropbox)
            newimg.save(newfilename)

            #mg.save(newfilename)

        def CropPicture(self,newfilename):
            cropbox=[]
            #im=Image.open()


