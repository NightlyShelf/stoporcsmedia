from enum import Enum


class Tags:
    def __init__(self, network, _type, crimes):
        self.network = network
        self.crimes = crimes
        self.type = _type


# IF EDITING, CONSIDER YOU CHANGED IT IN compiler.py (GenerateManual function)
class Network(Enum):
        IN = "Instagram"
        FB = "Facebook"
        TT = "TikTok"
        TG = "Telegram"
        TW = "Twitter"
        YT = "Youtube"


class Crimes(Enum):
    mup = "images/videos murdered people"
    aup = "anti-ukrainian propaganda"
    hsp = "messages of hate speech to Ukrainian people"
    msc = "photos/videos of shelling cities for the Russian propaganda"
    pwr = "propaganda of the war"
    pkp = "propaganda of ruthless killing people"
    iui = "information that undermines the integrity of Ukraine"
    ofs = "offensive speech messages"
    dfk = "disinformation and distribution fakes"
    dpd = "distribution of personal data and information"


class CrimesSwitcher:
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


class Type(Enum):
    # Accounts:
    CH = "channel"
    AC = "account"

    # Types of publications:
    VD = "video"
    TW = "tweet"
    GN = "post"
