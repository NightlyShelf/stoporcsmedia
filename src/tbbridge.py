import sys

from links import *
from resource import *
from tags import *
from task import *
import  base64 as b64
import pickle as pk
class Bridge():
    def __init__(self):
        self.args = sys.argv
        self.task = None
        # default variables
        self.mode = None
        self.form = None
        self.net = None
        self.crimes = None
        self.link = None
        self.exlink = None
        self.reporttype = None
        self.cryptedtext = None
        for arg in self.args:
            self.ProceedArg(arg)

    def ProceedArg(self, key):
        if ("-m=" in key):
            self.mode = key.replace("-m=", "")
        if("-rt=" in key):
            key = key.replace("-rt=","")
            if(key == "message"):
                self.reporttype = Report.MESSAGE
            elif(key == "email"):
                self.reporttype = Report.EMAIL
        if ("-f=" in key):
            form = key.replace("-f=", "")
            switcher = {
                Type.CH.value: Type.CH,
                Type.VD.value: Type.VD,
                Type.AC.value: Type.AC,
                Type.TW.value: Type.TW,
                Type.GN.value: Type.GN
            }
            self.form = switcher.get(form)
        if("-n=" in key):
            form = key.replace("-n=", "")
            switcher = {
                Network.TW.value: Network.TW,
                Network.YT.value: Network.YT,
                Network.IN.value: Network.IN,
                Network.TG.value: Network.TG,
                Network.TT.value: Network.TT,
                Network.FB.value: Network.FB

            }
            self.net = switcher.get(form)
        if("-c=" in key):
            crimesn = key.replace("-c=","").split(",")
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
            self.crimes = crimes
        if("-l=" in key):
            self.link = key.replace("-l=","")
        if("-crypted=" in key):
            self.cryptedtext = key.replace("-crypted=","")
        if("-exl=" in key):
            links = key.replace("-exl=","").split("~")
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
                exlink = exlink.replace("`and`", "&")
                linksfin.append(Exlink(exkey,exlink))
            self.exlink = linksfin
    def PrintParam(self):
        print("Mode: ", self.mode)
        print("Form: ", self.form)
        print("Network: ", self.net)
        print("Crimes: ", self.crimes)
        print("Link: ", self.link)
        for link in self.exlink:
            print(link.crime, link.link)
        print("Report type: ", self.reporttype)

    #Generates and writes serialized object to file. Chat-bot will decrypt and display it.
    def CreateResourceObject(self):
        self.task = Task(self.form, Resource(Tags(self.net, self.form, self.crimes), Links(self.link, self.exlink)))
        self.task.form = self.reporttype
        task = pk.dumps(self.task)
        with open("buffer.tmp","wb") as b:
            b.write(task)

#Test
if __name__ == "__main__":
    bridge = Bridge()
    if(bridge.mode == "gnrt"):

        bridge.PrintParam()

        print(bridge.CreateResourceObject())
    if(bridge.mode == "decrypt"):
        with open(bridge.cryptedtext, "rb") as b:
            txt = b.read()
        obj = pk.loads(txt)
        obj.SetNick("Test")
        print(obj.GenerateMessage())

