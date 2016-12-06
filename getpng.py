from src.PNGProcessor import *
from glob import glob
dir="d:\\test\\logs1205"
apps=glob(dir+"\\**")
for app in apps:
    print app
    PNGController(app)
