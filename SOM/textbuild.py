import csv
import random as rn
from enum import Enum

from SOM.task import *
from SOM.tags import *
import copy as cp

# Now we don't use nltk in connection with bugs :(

# import nltk
# from nltk.corpus import wordnet as wn

class Report(Enum):
    EMAIL = 1
    MESSAGE = 2


class TextBuilder:
    def __init__(self, resource, complainttype, nick, message_source, email_source):
        self.resource = resource
        self.complainttype = complainttype
        self.linkscopy = []
        self.nick = nick
        self.header = ""
        self.message_source = message_source
        self.email_source = email_source

        # NLTK import part
        '''
        try:
            nltk.word_tokenize('foobar')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.pos_tag(nltk.word_tokenize('foobar'))
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        try:
            wn.synsets("have")
        except LookupError:
            nltk.download("omw-1.4")
        '''

    def build(self):
        message = ""
        crimeslist = []
        self.linkscopy = None

        if (self.resource.links.exlinks != None and self.resource.links.exlinks != []):
            self.linkscopy =  cp.deepcopy(self.resource.links.exlinks)
            self.linkscopy2 = cp.deepcopy(self.resource.links.exlinks)
        for crime in self.resource.tags.crimes:
            crimeslist.append(crime.value)
        if (self.complainttype == Report.EMAIL):
            generatorlist = []
            try:
                f = open(self.email_source, "r")
                csvr = csv.reader(f, dialect="excel")
                for row in csvr:
                    network, crime, content, key = row[0], row[1], row[2], row[3]
                    if (network == "Any" or network == self.resource.tags.network.value) and (
                            crime == "Any" or crime in crimeslist):
                        generatorlist.append(row)
                self.generatorlist = generatorlist
                f.close()
                message = self.GetRandomVariant("TXT", 2, generatorlist, crimeslist)
                message = message.replace("GRRR", self.GetRandomVariant("GRRR", 2, self.generatorlist, crimeslist))
                message = message.replace("APPP", self.GetRandomVariant("APPP", 2, self.generatorlist, crimeslist))
                message = message.replace("RSSS", self.GetRandomVariant("RSSS", 2, self.generatorlist, crimeslist))
                message = message.replace("GBBB", self.GetRandomVariant("GBBB", 2, self.generatorlist, crimeslist))
                message = message.replace("BLLL", self.GetRandomVariant("BLLL", 2, self.generatorlist, crimeslist))
                message = message.replace("ENDD", self.GetRandomVariant("ENDD", 2, self.generatorlist, crimeslist))
                message = message.replace("GREET", self.GetRandomVariant("GREET", 2, self.generatorlist, crimeslist))
                message = message.replace("PREV", self.GetRandomVariant("PREV", 2, self.generatorlist, crimeslist))
                message = message.replace("FACT", self.GetRandomVariant("FACT", 2, self.generatorlist, crimeslist))
                message = message.replace("EXPL", self.GetRandomVariant("EXPL", 2, self.generatorlist, crimeslist))
                message = message.replace("DEMD", self.GetRandomVariant("DEMD", 2, self.generatorlist, crimeslist))
                if (self.resource.tags.type == Type.AC or self.resource.tags.type == Type.CH) and self.linkscopy != None and self.linkscopy != []:

                    message = message.replace("RSIN", self.GetRandomVariant("RSIN", 2, self.generatorlist, crimeslist))
                    message = message.replace("RES1", self.GetRandomVariant("RES", 2, self.generatorlist, crimeslist))
                    message = message.replace("RES2", self.GetRandomVariant("RES", 2, self.generatorlist, crimeslist))
                    message = message.replace("RES3", self.GetRandomVariant("RES", 2, self.generatorlist, crimeslist))
                    message = message.replace("RES4", self.GetRandomVariant("RES", 2, self.generatorlist, crimeslist))
                    message = message.replace("GBIN", self.GetRandomVariant("GBIN", 2, self.generatorlist, crimeslist))
                    message = message.replace("VR1", self.GetRandomVariant("VR", 2, self.generatorlist, crimeslist))
                    message = message.replace("VR2", self.GetRandomVariant("VR", 2, self.generatorlist, crimeslist))
                    message = message.replace("VR3", self.GetRandomVariant("VR", 2, self.generatorlist, crimeslist))
                    message = message.replace("VR4", self.GetRandomVariant("VR", 2, self.generatorlist, crimeslist))
                    message = message.replace("VR5", self.GetRandomVariant("VR", 2, self.generatorlist, crimeslist))
                else:
                    message = message.replace("RSIN", "")
                    message = message.replace("RES1", "")
                    message = message.replace("RES2", "")
                    message = message.replace("RES3", "")
                    message = message.replace("RES4", "")
                    message = message.replace("GBIN", "")
                    message = message.replace("VR1", "")
                    message = message.replace("VR2", "")
                    message = message.replace("VR3", "")
                    message = message.replace("VR4", "")
                    message = message.replace("VR5", "")
                    message = message.replace("*dn*", "\n")
                    message = message.replace("*n*", "\n")
                    for i in range(2,11):
                        m = ""
                        for j in range(0,i):
                            m+="\n"
                        message = message.replace(m, "\n")
                message = message.replace("PREN", self.GetRandomVariant("PREN", 2, self.generatorlist, crimeslist))
                message = message.replace("RQOF", self.GetRandomVariant("RQOF", 2, self.generatorlist, crimeslist))
                message = message.replace("FDEM", self.GetRandomVariant("FDEM", 2, self.generatorlist, crimeslist))
                message = message.replace("LSWD", self.GetRandomVariant("LSWD", 2, self.generatorlist, crimeslist))
                message = message.replace("SIGN", self.GetRandomVariant("SIGN", 2, self.generatorlist, crimeslist))
                message = message.replace("{NTWRK}", self.resource.tags.network.value)
                message = message.replace("{TYPE}", self.resource.tags.type.value)
                message = message.replace("{ALINK}", self.resource.links.alink)
                message = message.replace("{NICK}", self.nick)
                message = message.replace("*dn*", " \n\n ")
                message = message.replace("*n*", " \n ")

                # DON'T UNCOMMENT!
                # message = self.NLProcessing(message)

                self.header = self.GetRandomVariant("HEADER", 2, generatorlist, crimeslist)
                self.header = self.header.replace("{NTWRK}", self.resource.tags.network.value)
                self.header = self.header.replace("{TYPE}", self.resource.tags.type.value)
            except FileNotFoundError:
                raise FileNotFoundError
        else:
            generatorlist = []
            try:
                f = open(self.message_source, "r")
                csvr = csv.reader(f, dialect="excel")
                for row in csvr:
                    key, network, type, content = row[0], row[1], row[2], row[3]
                    if (network == "Any" or network == self.resource.tags.network.value) and (
                            type == "Any" or type == self.resource.tags.type):
                        generatorlist.append(row)
                f.close()
                message = self.GetRandomVariant("TXT", 3, generatorlist, crimeslist)
                message = message.replace("INTR", self.GetRandomVariant("INTR", 3, generatorlist, crimeslist))
                message = message.replace("MAIN", self.GetRandomVariant("MAIN", 3, generatorlist, crimeslist))
                message = message.replace("BLCK", self.GetRandomVariant("BLCK", 3, generatorlist, crimeslist))
                message = message.replace("{TYPE}", self.resource.tags.type.value)
                message = message.replace("{NTWRK}", self.resource.tags.network.value)
                message = message.replace("*n*", "\n")
            except FileNotFoundError:
                raise FileNotFoundError
        return message

    def GetRandomVariant(self, key, contentkey, variantslist, crimes):
        self.variants= []
        if (contentkey == 2):
            for line in variantslist:
                if (line[3] == key and (line[1] == "Any" or line[1] in crimes)):
                    self.variants.append(line)
        else:
            for line in variantslist:

                if (line[0] == key and (line[1] == "Any" or line[1] in crimes)):
                    self.variants.append(line)
        if ("RES" == key):
            r = rn.choice(self.variants)
            res = r[contentkey]
            self.variants.remove(r)
            if(self.linkscopy == []):

                #print("Using again;" , self.linkscopy)
                exlink = rn.choice(self.linkscopy2)
                res = res.replace("{LINK}", exlink.link)
                res = res.replace("{CTNT}", exlink.crime.value)
                return res
            #print(rn.choice(self.linkscopy))
            exlink = rn.choice(self.linkscopy)
            res = res.replace("{LINK}", exlink.link)
            res = res.replace("{CTNT}", exlink.crime.value)
            self.linkscopy.remove(exlink)
            return res
        elif ("VR" == key):
            r = rn.choice(self.variants)
            vr = r[contentkey]
            self.variants.remove(r)
            return vr
        elif ("MAIN" == key):
            r = rn.choice(self.variants)[contentkey]
            for i in range(1, 5):
                crime = rn.choice(crimes)
                r = r.replace("{CTNT" + str(i) + "}", crime)
                crimes.remove(crime)
            return r
        else:
            return rn.choice(self.variants)[contentkey]
    # NOT WORKING, corrupts text with incorrect synonymous (is it a bug of AI?)
    # EDIT: Tested, it is a bug of AI of using incorrect words. Let's don't use it, maybe we should use file with synonyms instead?
    """
    def NLProcessing(self, text):
        final = text
        words = nltk.word_tokenize(text, "english")
        print(words)
        for word in words:
            if(word in ".,/?<>|\\\"\';:{[}]+=_-)(*&^%$#@!~`" or "(" in word or ")" in word or "[" in word or "]" in word or "{" in word or "}" in word or "*" in word or len(word) <= 1): continue
            else:
                if(rn.randint(1,4) == 3):
                    wordlower = word.lower()
                    s = wn.synsets(wordlower)
                    if(s == []): continue
                    a = rn.choice(s).lemma_names()
                    if(a == []): continue
                    print(a)
                    x = True
                    while x:
                        syn = rn.choice(a)
                        if(a == wordlower and len(a) >= 2):
                            continue
                        if(len(a) == 1):
                            break
                        else:
                            break
                    final = final.replace(word, syn)
                    print("Word: ", word)
                    print("Synonym: ", syn)
        return final
        """
