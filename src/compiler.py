from resource import *
from tags import *
from task import *
import sys
from links import *
from enum import Enum
import pickle as pc
import base64 as b64
#STATUS: Do the automatic generator (with parser)
#DONE: ManualGenerate
#LATER: args parser and fileIO

#TEST: compiler.exe -mode=manual -wmode=rewrite -datain=rt=email[f=acnt[n=twtr[c=iui,dfk,hsp,iui[lnk=https:/twitter.com/gazetaru[exl=iui#https://twitter.com/GazetaRu/status/1534849682576445440?s=20`t=1ZyTeGS74miMYloG6kep7g~dfk#https://twitter.com/GazetaRu/status/1534842132388892674?s=20`t=NAKVMpiBdSNDlzlUi1v4NQ -dataout=test.pcl


class CMode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
class WriteMode(Enum):
    REWRITE = "rewrt"
    ADDTOEXISTING = "add"

class Compiler:
    def __init__(self, mode, wmode, datain, dataout):
        self.mode = mode
        self.wmode = wmode
        self.datain = datain
        self.dataout = dataout

    def GenerateManual(self, keys):
        report_type = None
        content_type = None
        network = None
        content_crimes = None
        content_link = None
        content_clinks = None
        print("Analysing input data...")
        for key in keys:
            if("rt=" in key):
                key = key.replace("rt=","").lower()
                if(key == "message"):
                    report_type = Report.MESSAGE
                elif(key == "email"):
                    report_type = Report.EMAIL
                continue
            elif ("f=" in key):
                form = key.replace("f=", "").lower()
                switcher = {
                    "chnl": Type.CH,
                    "vdio": Type.VD,
                    "acnt": Type.AC,
                    "twet": Type.TW,
                    "publ": Type.GN
                }
                content_type = switcher.get(form)
                continue
            elif("n=" in key):
                form = key.replace("n=", "").lower()
                switcher = {
                    "twtr": Network.TW,
                    "ytub": Network.YT,
                    "inst": Network.IN,
                    "tlgm": Network.TG,
                    "tktk": Network.TT,
                    "fcbk": Network.FB
                }
                network = switcher.get(form)
                continue
            elif("c=" in key):
                crimesn = key.replace("c=","").lower().split(",")
                crimes = []
                switcher = {
                    "mup": Crimes.mup,
                    "aup": Crimes.aup,
                    "dfk": Crimes.dfk,
                    "dpd": Crimes.dpd,
                    "hsp": Crimes.hsp,

                    "iui": Crimes.iui,
                    "msc": Crimes.msc,
                    "ofs": Crimes.ofs,
                    "pkp": Crimes.pkp,
                    "pwr": Crimes.pwr
                }
                for crime in crimesn:
                    crimes.append(switcher.get(crime))
                content_crimes = crimes
                continue
            elif("lnk=" in key):
                content_link = key.replace("lnk=","")
                continue
            #Not obligatory
            elif("exl=" in key):
                links = key.replace("exl=","").split("~")
                linksfin = []
                for link in links:
                    exkey, exlink = link.split("#")
                    switcher = {
                        "mup": Crimes.mup,
                        "aup": Crimes.aup,
                        "dfk": Crimes.dfk,
                        "dpd": Crimes.dpd,
                        "hsp": Crimes.hsp,

                        "iui": Crimes.iui,
                        "msc": Crimes.msc,
                        "ofs": Crimes.ofs,
                        "pkp": Crimes.pkp,
                        "pwr": Crimes.pwr
                    }
                    exkey = switcher.get(exkey)
                    exlink = exlink.replace("`", "&")
                    linksfin.append(Exlink(exkey, exlink))
                content_clinks = linksfin
                continue
            else:
                print(f"Error occured: Invaild key ("+key+") provided. Check it rightness and restart the program.\nExit code: 2.")
                input()
                sys.exit(2)
        #test: rt=message|f=twet|n=twtr|c=iui,dfk,hsp,iui|lnk=https:/twitter.com/gazetaru|exl=iui#https://twitter.com/GazetaRu/status/1534849682576445440?s=20`t=1ZyTeGS74miMYloG6kep7g~dfk#https://twitter.com/GazetaRu/status/1534842132388892674?s=20`t=NAKVMpiBdSNDlzlUi1v4NQ
        if(report_type == None):
            print("Error (Missing report type). Seems to be \"rt=\" argument missing or incorrect data provided?")
            input()
            sys.exit(2)
        if (content_type == None):
            print("Error (Missing content type). Seems to be \"f=\" argument missing or incorrect data provided?")
            input()
            sys.exit(2)
        if (network == None):
            print("Error (Missing network type). Seems to be \"n=\" argument missing or incorrect data provided?")
            input()
            sys.exit(2)
        if (content_crimes == None):
            print("Error (Missing content crimes). Seems to be \"c=\" argument missing or incorrect data provided?")
            input()
            sys.exit(2)
        if (content_link == None):
            print("Error (Missing link). Seems to be \"l=\" argument missing or incorrect data provided?")
            input()
            sys.exit(2)
        print("Sucessfull!")
        print("Task object generated successful!")
        return Task(report_type, Resource(Tags(network,content_type,content_crimes), Links(content_link, content_clinks)))
    def GenerateAuto(self, link):
        print("Auto generating is not available right now. Exiting...")
        input()
        sys.exit(0)
        pass
    def Generate(self):
        print("Beginning generation...")
        self.final = None
        if self.mode == CMode.MANUAL:
            print("Mode: Manual")
            self.datain = self.datain.split("[")
            self.final = self.GenerateManual(self.datain)
            if self.wmode == WriteMode.REWRITE:
                print("Rewriting file...")
                try:
                    with open(self.dataout, "wb") as f:
                        f.write(pc.dumps(self.final))
                        print("Successfully encoded object!")
                        f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception as ex:
                    print("Error occured: ", ex.args)
                    input()
                    sys.exit(1)
            else:
                print("Adding object to existing file...")
                try:
                    with open(self.dataout, "ab") as f:
                        f.write(pc.dumps(self.final))
                        f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception as ex:
                    print("Error occured: ", ex.args)
                    input()
                    sys.exit(1)
        elif self.mode == CMode.AUTO:
            print("Mode: Auto")
            self.links = []
            self.final = []
            try:
                print("Reading links for autogenerate from file...")
                with open(self.datain) as f:
                    lines = f.readlines()
                    for line in lines:
                        self.links.append(line.replace("\n",""))
                print("Success!")

            except Exception as ex:
                print("Error occured: ", ex.args)
                input()
                sys.exit(1)
            for link in self.links:
                self.final.append(pc.dumps(self.GenerateAuto(link)))
            if self.wmode == WriteMode.REWRITE:
                print("Rewriting file...")
                try:
                    with open(self.dataout, "wb") as f:
                        for line in self.final:
                            f.write(line)
                            f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception as ex:
                    print("Error occured: ", ex.args)
                    input()
                    sys.exit(1)
            else:
                print("Adding object(s) to existing file...")
                try:
                    with open(self.dataout, "ab") as f:
                        for line in self.final:
                            f.write(line)
                            f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception as ex:
                    print("Error occured: ", ex.args)
                    input()
                    sys.exit(1)


if __name__ == "__main__":
    print("Compiler version 0.8")
    print("Part of StopRussia - Mriya Project")
    print("Learn how to use in README")
    print("--------------------------------------------------------")
    args = sys.argv
    print("Parsing arguments...")
    mode, wmode, datain, dataout = None, None, None, None
    for arg in args:
        if "-mode=" in arg:
            arg = arg.replace("-mode=","").lower()
            if arg == "manual":
                mode = CMode.MANUAL
            elif arg == "auto":
                mode = CMode.AUTO
            else:
                print(f"Error occured: Invaild value of the -mode argument ({0}). Check it and restart the program.\nExit code: 2", arg)
                input()
                sys.exit(2)
            continue
        elif "-wmode=" in arg:
            arg = arg.replace("-wmode=", "").lower()
            if arg == "rewrite":
                wmode = WriteMode.REWRITE
            elif arg == "add":
                wmode = WriteMode.ADDTOEXISTING
            else:
                print(f"Error occured: Invaild value of the -wmode argument ({0}). Check it rightness and restart the program.\nExit code: 2.", arg)
                input()
                sys.exit(2)
            continue
        elif "-datain=" in arg:
            arg = arg.replace("-datain=", "")
            datain = arg
            continue
        elif "-dataout=" in arg:
            arg = arg.replace("-dataout=", "")
            dataout = arg
            continue
        elif ".exe" in arg:
            continue
        else:
            print(f"Unrecognized argument "+arg+". Check it rightness and restart the program.\nExit code: 2.")
            input()
            sys.exit(2)
    print("Success!")
    compiler = Compiler(mode, wmode, datain, dataout)
    compiler.Generate()
    print("Success! You can see changes in your file. Good luck!")
    input()
    #test
    #compiler = Compiler(CMode.MANUAL, WriteMode.REWRITE, "rt=email|f=acnt|n=twtr|c=iui,dfk,hsp,iui|lnk=https:/twitter.com/gazetaru|exl=iui#https://twitter.com/GazetaRu/status/1534849682576445440?s=20`t=1ZyTeGS74miMYloG6kep7g~dfk#https://twitter.com/GazetaRu/status/1534842132388892674?s=20`t=NAKVMpiBdSNDlzlUi1v4NQ")
    #argstest = .split("|")
    #task = GenerateManual(argstest)
    #task.SetNick("Test")
    #print(task.GenerateMessage())

