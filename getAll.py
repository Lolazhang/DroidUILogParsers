from src.AllController import *
import os
from glob import glob
dir="d:\\test\\bbc.mobile.news.ww"
#AllController(dir)
dir="d:\\test\\logs1205"
apps=glob(dir+"\\*")
for app in apps:
     print "app",app
     #AllController(app)
#print glob(dir+"\\*\\")
AllController("D:\\test\\logs1205\\com.andromo.dev22397.app218710")
