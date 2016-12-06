class CollectingLogs:
    def __init__(self,files):
        self.files=files
        self.filedicts={}


        for filename in self.files:

            if "systrace" in filename:
                timestamp = filename.split("\\")[-2].split("_")[1]
                key = filename.split("\\")[-2].split("_")[0]
                # print key,timestamp
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                if not "systrace" in self.filedicts[timestamp]:
                    self.filedicts[timestamp]["systrace"] = []
                self.filedicts[timestamp]["systrace"].append(filename)
            elif "memoryInfo" in filename:
                timestamp = filename.split("\\")[-2].split("_")[1]
                key = filename.split("\\")[-2].split("_")[0]
                # print key, timestamp
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                if not "memoryInfo" in self.filedicts[timestamp]:
                    self.filedicts[timestamp]["memoryInfo"] = []
                self.filedicts[timestamp]["memoryInfo"].append(filename)
            elif "_network_" in filename:
                timestamp = filename.split("\\")[-1].split("_")[-1].split(".")[0]
                key = "network"
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                self.filedicts[timestamp][key] = filename
            elif "screenpng_" in filename:
                timestamp = filename.split("\\")[-2].split("_")[-1]
                key = "screenpng"
                # print "found screenpnf"
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                if not "screenpng" in self.filedicts[timestamp]:
                    self.filedicts[timestamp]["screenpng"] = []
                self.filedicts[timestamp]["screenpng"].append(filename)
            elif "screenshot_" in filename:
                timestamp = filename.split("\\")[-2].split("_")[-1]
                key = "screenshot"
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                if not "screenshot" in self.filedicts[timestamp]:
                    self.filedicts[timestamp]["screenshot"] = []
                self.filedicts[timestamp]["screenshot"].append(filename)


            else:
                key = filename.split("\\")[-1].split("_")[0]
                timestamp = filename.split("\\")[-1].split("_")[1].split(".")[0]
                print key, timestamp
                if not timestamp in self.filedicts:
                    self.filedicts[timestamp] = {}
                self.filedicts[timestamp][key] = filename
