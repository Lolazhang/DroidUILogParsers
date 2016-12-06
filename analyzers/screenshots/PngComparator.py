
from PIL import ImageChops,Image
import math
import operator
class PngComparator:
    def __init__(self,png1,png2):
        #print png1.split("\\")[-1],png2.split("\\")[-1]
        h1 = Image.open(png1)
        h2 = Image.open(png2)

        diff = ImageChops.difference(h1, h2)
        #print str(diff.getbbox())
        self.similarity=-1
        diffbox=diff.getbbox()
        if diffbox==None:
            self.similarity=1
        else:
            (left,top,right,bottom)=diffbox
            #print left,top,right,bottom
            self.similarity=1-(right-left )*(bottom-top)/(1440*2560.0)
            #print self.similarity

