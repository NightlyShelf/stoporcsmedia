from enum import Enum


class Tags():
    def __init__(self, network, type, crimes):
        self.network = network
        self.crimes = crimes
        self.type = type


class Network(Enum):
    IN = "Instagram"
    FB = "Facebook"
    TT = "Tik Tok"
    TG = "Telegram"
    TW = "Twitter"
    YT = "Youtube"


class Crimes(Enum):
    mup = "murdered people"
    aup = "anti-ukranian propaganda"
    hsp = "hate speech to Ukranian people"
    msc = "photos/videos of shelling cities for the Russian propaganda"
    pwr = "propaganda of the war"
    pkp = "propaganda of ruthless killing people"
    iui = "information that undermines the integrity of Ukraine"
    ofs = "offensive speech"
    dfk = "disinformation and distribution fakes"
    dpd = "distribution of personal data and information"


class Type(Enum):
    # Accounts:
    CH = "channel"
    AC = "account"

    # Types of publications:
    VD = "video"
    TW = "tweet"
    GN = "publication"
