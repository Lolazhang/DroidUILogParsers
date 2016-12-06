from glob import glob
from logParsers.Memoryparser import *
from numpy import sort
from logParsers.DumpPageParser import *
import os
from systraceAnalysis.sysTrace import *
from sysTraceAnalysis import *
from logParsers.LogCatAllParser import *
from logParsers.LogCatEventParser import *
from logParsers.NetCapParser import *
from CollectingLogs import *

from analyzers.loadingTimeSolver import *
from analyzers.loadingTimeSolverWithPic import *
from logParsers.ScreenCapConverter import *
from logParsers.ScreenShotConverter import *
from logParsers.ScreenShotParser import *
from getLoadingTimeFromScreenshot import *
from sqlhelpers.ConnectToDB import *


class PNGController:
    def __init__(self, dir):
        self.dir = dir
        self.memoryFiles = glob(dir + "\\**\\**.txt")

        self.dumpPages = glob(dir + "\\dumpPage_**.xml")
        # print self.dumpPages
        self.logcatAlls = glob(dir + "\\logcatAll_**.txt")
        self.logcatEvents = glob(dir + "\\logcatEvent_**.txt")
        self.systraces = glob(dir + "\\**\\**.html")
        self.netcaps = glob(dir + "\\**_network_**.cap")
        self.screendraw = glob(dir + "\\**\\**.raw")

        self.screenshots = glob(dir + "\\screenshot_**\\**.png")
        ScreenCapConverter(self.screendraw)
        ScreenShotConverter(self.screenshots)