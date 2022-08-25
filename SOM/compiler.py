import pickle as pc
import sys
import urllib.error
import urllib.request
from enum import Enum
import bs4

from SOM.links import *
from SOM.resource import *
from SOM.task import *
from SOM.tags import *

# MANUAL MODE TEST: compiler.exe -mode=manual -wmode=rewrite -datain=rt=email[f=acnt[n=twtr[c=iui,dfk,hsp,
# iui[lnk=https:/twitter.com/gazetaru[exl=iui#https://twitter.com/GazetaRu/status/1534849682576445440?s=20`t
# =1ZyTeGS74miMYloG6kep7g~dfk#https://twitter.com/GazetaRu/status/1534842132388892674?s=20`t=NAKVMpiBdSNDlzlUi1v4NQ
# -dataout=test.pcl
from SOM.textbuild import Report


class CMode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    TESTING = "testing"


class WriteMode(Enum):
    REWRITE = "rewrt"
    ADDTOEXISTING = "add"


class Compiler:
    TASKTYPECOEF = 4

    def __init__(self, mode=None, wmode=None, datain=None, dataout=None):
        self.mode = mode
        self.wmode = wmode
        self.datain = datain
        self.dataout = dataout

    def GenerateManual(self, keys, consolemode=False):
        report_type = None
        content_type = None
        network = None
        content_crimes = None
        content_link = None
        content_clinks = None
        if consolemode:
            print("Analysing input data...")
        for key in keys:
            if "rt=" in key:
                key = key.replace("rt=", "").lower()
                if key == "message":
                    report_type = Report.MESSAGE
                elif key == "email":
                    report_type = Report.EMAIL
                continue
            elif "f=" in key:
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
            elif "n=" in key:
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
            elif "c=" in key:
                crimesn = key.replace("c=", "").lower().split(",")
                crimes = []
                for crime in crimesn:
                    crimes.append(CrimesSwitcher.switcher.get(crime))
                content_crimes = crimes
                continue
            elif "lnk=" in key:
                content_link = key.replace("lnk=", "")
                continue
            # Not obligatory
            elif "exl=" in key:
                links = key.replace("exl=", "").split("~")
                linksfin = []
                for link in links:
                    exkey, exlink = link.split("#")
                    exkey = CrimesSwitcher.switcher.get(exkey)
                    exlink = exlink.replace("`", "&")
                    linksfin.append(Exlink(exkey, exlink))
                content_clinks = linksfin
                continue
            else:
                if consolemode:
                    print(
                        "Error occurred: Invaild key (" + key + ") provided. Check it rightness and restart the program.\nExit code: 2.")
                    input()
                    sys.exit(2)
                return "Invaild key"
        # test: rt=message|f=twet|n=twtr|c=iui,dfk,hsp,iui|lnk=https:/twitter.com/gazetaru|exl=iui#https://twitter.com/GazetaRu/status/1534849682576445440?s=20`t=1ZyTeGS74miMYloG6kep7g~dfk#https://twitter.com/GazetaRu/status/1534842132388892674?s=20`t=NAKVMpiBdSNDlzlUi1v4NQ
        if report_type == None:
            if consolemode:
                print("Error (Missing report type). Seems to be \"rt=\" argument missing or incorrect data provided?")
                input()
                sys.exit(2)
            return "Missing rt"
        if content_type == None:
            if consolemode:
                print("Error (Missing content type). Seems to be \"f=\" argument missing or incorrect data provided?")
                input()
                sys.exit(2)
            return "Missing ct"
        if network == None:
            if consolemode:
                print("Error (Missing network type). Seems to be \"n=\" argument missing or incorrect data provided?")
                input()
                sys.exit(2)
            return "Missing nt"
        if content_crimes == None:
            if consolemode:
                print("Error (Missing content crimes). Seems to be \"c=\" argument missing or incorrect data provided?")
                input()
                sys.exit(2)
            return "Missing cc"
        if content_link == None:
            if consolemode:
                print("Error (Missing link). Seems to be \"l=\" argument missing or incorrect data provided?")
                input()
                sys.exit(2)
            return "Missing lnk"
        if consolemode:
            print("Successful!")
            print("Task object generated successful!")
        return Task(report_type,
                    Resource(Tags(network, content_type, content_crimes), Links(content_link, content_clinks)))

    def GenerateAuto(self, link, consolemode=False):
        if consolemode:
            print("Beginning generation for " + link + "...")
        network = None
        type = None
        crimes = None
        reporttype = None
        exlinks = None
        if not "https://" in link or "http://" in link or "www." in link:
            if consolemode:
                print("Link hasn't got \"https://\" prefix. Adding it...")
            link = link.replace("http://", "")
            link = link.replace("www.", "")
            link = link.replace("https://", "")
            link = "https://" + link
        thelink = link
        # Telegram
        if "t.me/" in link:
            if consolemode:
                print("Network: Telegram")
            network = Network.TG
            if "/s/" in link:
                link = link.replace("/s/","")
            try:
                webpage = urllib.request.urlopen(link)
                source = webpage.read()
                soup = bs4.BeautifulSoup(source, "html.parser")
                if soup.find("a", "tgme_page_context_link") != None or "/s/" in link:
                    type = Type.CH
                    if consolemode:
                        print("Type: Channel")
                    if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                        if consolemode:
                            print("Report type: Email")
                        reporttype = Report.EMAIL
                    else:
                        if consolemode:
                            print("Report type: Message")
                        reporttype = Report.MESSAGE
                elif soup.find("div", "tgme_page_widget") != None:
                    type = Type.GN
                    if consolemode:
                        print("Type: Publication")
                        print("Report type: Message")
                    reporttype = Report.MESSAGE
                else:
                    type = Type.AC
                    if consolemode:
                        print("Type: Account")

                    if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                        if consolemode:
                            print("Report type: Email")
                        reporttype = Report.EMAIL
                    else:
                        if consolemode:
                            print("Report type: Message")
                        reporttype = Report.MESSAGE

            except urllib.error.URLError or urllib.error.HTTPError as error:
                if consolemode:
                    print(
                        "Detected problem while connecting to the " + link + ". Press Enter to skip or write Exit to exit...")
                    a = input()
                    if a.lower() == "exit":
                        print("Exiting...")
                        sys.exit(1)
                else:
                    raise error
            crimes = []
            for i in range(random.randint(6, 8)):
                crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
            if type == Type.CH:
                if consolemode:
                    print("Searching for publications in channel...")
                comlink = link.replace("https://t.me/", "")
                comlink = "https://t.me/s/" + comlink
                try:
                    webpage = urllib.request.urlopen(comlink)
                    soup = bs4.BeautifulSoup(webpage.read(), "html.parser")
                    linksex = []
                    if soup.find_all("a", "tgme_widget_message_date") == []:
                        exlinks = None
                    else:
                        for linkk in soup.find_all("a", "tgme_widget_message_date"):
                            linksex.append(linkk.get("href"))
                        exlinks = []
                        lonks = []
                        for i in range(1, random.randint(1, len(linksex))):
                            lonks.append(random.choice(linksex))
                            for lnk in lonks:
                                exlinks.append(Exlink(random.choice(list((CrimesSwitcher.switcher.values()))), lnk))
                except urllib.error.URLError or urllib.error.HTTPError as error:
                    if consolemode:
                        print(
                            "Detected problem while connecting to the " + link + ". Press Enter to skip or write Exit to exit...")
                        a = input()
                        if a.lower() == "exit":
                            print("Exiting...")
                            sys.exit(1)
                    else:
                        raise error
        # Instagram
        elif "instagram.com/" in link:
            network = Network.IN
            type = Type.AC
            crimes = []
            for i in range(random.randint(4, 8)):
                crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
            if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                reporttype = Report.EMAIL
            else:
                reporttype = Report.MESSAGE
        # Facebook
        elif "facebook.com/" in link or "fb.watch/" in link or "fb.com/" in link:
            network = Network.FB
            if "/posts/" in link:
                type = Type.GN
            elif "fb.watch" in link:
                type = Type.VD
            else:
                type = Type.AC
            crimes = []
            for i in range(random.randint(4, 8)):
                crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
            if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                reporttype = Report.EMAIL
            else:
                reporttype = Report.MESSAGE
        # Twitter
        elif "twitter.com/" in link or "t.co/" in link:
            network = Network.TW
            type = Type.AC
            crimes = []
            for i in range(random.randint(4, 8)):
                crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
            reporttype = Report.MESSAGE
        # TikTok
        elif "tiktok.com/" in link:
            network = Network.TT
            if "@" in link:
                type = Type.AC
                crimes = []
                for i in range(random.randint(4, 8)):
                    crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
                if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                    reporttype = Report.EMAIL
                else:
                    reporttype = Report.MESSAGE
            else:
                crimes = []
                for i in range(random.randint(4, 8)):
                    crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
                reporttype = Report.MESSAGE
        # YouTube
        elif "youtube.com/" in link:
            network = Network.YT
            if "watch?" in link:
                type = Type.VD
                crimes = []
                for i in range(random.randint(4, 8)):
                    crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
                reporttype = Report.MESSAGE
            else:
                type = Type.AC
                crimes = []
                for i in range(random.randint(4, 8)):
                    crimes.append(random.choice(list((CrimesSwitcher.switcher.values()))))
                if random.randint(1, Compiler.TASKTYPECOEF) == 1:
                    reporttype = Report.EMAIL
                else:
                    reporttype = Report.MESSAGE
        if network == None or type == None or crimes == None or thelink == None or reporttype == None:
            if consolemode:
                print(
                    "Problem occurred: Error while creating Ressource object. Seems to be incorrect data provided. Contact the technical administrator. Press Enter to skip or write Exit to exit...")
                a = input()
                if a.lower() == "exit":
                    print("Exiting...")
                    sys.exit(1)
            else:
                raise AttributeError
        if consolemode:
            print("Generated!")
        return Task(reporttype, Resource(Tags(network, type, crimes), Links(thelink, exlinks)))

    def Test(self, obj):
        task = pc.loads(obj)
        text = "TASK OBJECT SUMMARY:\n"
        text += "Type: " + str(task.resource.tags.type.value) + "\n"
        text += "Network: " + str(task.resource.tags.network.value) + "\n"
        text += "Report format: " + str(task.form.value) + "\n"
        text += "Resource link: " + str(task.resource.links.alink) + "\n"
        text += "Crimes: " + str(task.resource.tags.crimes) + "\n"
        text += "Exlinks: " + str(task.resource.links.exlinks) + "\n"
        text += "Report sample: " + str(task.GenerateMessage()) + "\n\n"
        return text

    def Generate(self):
        print("Beginning generation...")
        self.final = None
        if self.mode == CMode.MANUAL:
            print("Mode: Manual")
            self.datain = self.datain.split("[")
            self.final = self.GenerateManual(self.datain, consolemode=True)
            if self.wmode == WriteMode.REWRITE:
                print("Rewriting file...")
                try:
                    with open(self.dataout, "wb") as f:
                        f.write(pc.dumps(self.final))
                        print("Successfully encoded object!")
                        f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception:
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
                    input()
                    sys.exit(1)
            else:
                print("Adding object to existing file...")
                try:
                    with open(self.dataout, "ab") as f:
                        f.write(pc.dumps(self.final))
                        f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception:
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
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
                        self.links.append(line.replace("\n", ""))
                print("Success!")

            except Exception as ex:
                print(
                    "Error occurred: unable to read or parse " + self.datain + ". Check its availability and try again.")
                input()
                sys.exit(1)
            if self.links == []:
                print(
                    "Warning: provided file with input data (" + self.datain + ") is empty or corrupted. Nothing to generate.\nExiting...")
                input()
                sys.exit(1)
            for link in self.links:
                self.final.append(pc.dumps(self.GenerateAuto(link, consolemode=True)))
            if self.wmode == WriteMode.REWRITE:
                print("Rewriting file...")
                try:
                    with open(self.dataout, "wb") as f:
                        for line in self.final:
                            f.write(line)
                            f.write(b"\n")
                    print("Successfully wrote to file!")
                except Exception as ex:
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
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
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
                    input()
                    sys.exit(1)
        elif self.mode == CMode.TESTING:
            print("Mode: Testing")
            finaltext = ""
            objects = []
            try:
                print("Trying to open the selected file with testing objects...")
                with open(self.datain, "rb") as f:
                    lines = f.readlines()
                    for line in lines:
                        objects.append(line.replace(b"\n", b""))
                print("Success!")
            except Exception as ex:
                print(
                    "Error occurred: unable to read or parse " + self.datain + ". Check its availability and try again.")
                input()
                sys.exit(1)
            for obj in objects:
                print("Generating summary for next object...")
                finaltext += self.Test(obj)
            if self.wmode == WriteMode.REWRITE:
                try:
                    print("Finishing with exporting summary...")
                    with open(self.dataout, "w") as f:
                        f.write(finaltext)
                        print("Success!")
                except Exception as ex:
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
                    input()
                    sys.exit(1)
            else:
                try:
                    print("Finishing with exporting summary...")
                    with open(self.dataout, "a") as f:
                        f.write(finaltext)
                        print("Success!")
                except Exception as ex:
                    print(
                        "Error occurred while writing to file: " + self.dataout + ". Try again or choose another file/location.\nExiting...")
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
            arg = arg.replace("-mode=", "").lower()
            if arg == "manual":
                mode = CMode.MANUAL
            elif arg == "auto":
                mode = CMode.AUTO
            elif arg == "testing":
                mode = CMode.TESTING
            else:
                print("Error occurred: Invaild value of the -mode argument ("+ arg +"). Check it rightness and restart the program.\nExit code: 2.")
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
                print("Error occurred: Invaild value of the -wmode argument ("+ arg +"). Check it rightness and restart the program.\nExit code: 2.")
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
            print(f"Unrecognized argument " + arg + ". Check it rightness and restart the program.\nExit code: 2.")
            input()
            sys.exit(2)
    if not mode:
        print("Error (Missing mode). Seems to be \"-mode\" argument missing or incorrect data provided?")
        input()
        sys.exit(2)
    if not wmode:
        print("Error (Missing writing mode). Seems to be \"-wmode\" argument missing or incorrect data provided?")
        input()
        sys.exit(2)
    if not datain:
        print("Error (Missing input data). Seems to be \"-datain\" argument missing or incorrect data provided?")
        input()
        sys.exit(2)
    if not dataout:
        print("Error (Missing output data). Seems to be \"-dataout\" argument missing or incorrect data provided?")
        input()
        sys.exit(2)
    print("Success!")
    compiler = Compiler(mode, wmode, datain, dataout)
    compiler.Generate()
    print("Success! You can see changes in your file. Good luck!")
    input()
