import random
import copy
from SOM.textbuild import *
from SOM.task import *
from SOM.resource import *
from SOM.links import *
from pickle import loads, dumps, UnpicklingError


class API:

    ACTUALVERSION = "1.0"

    def __init__(self, nick, debug=False):
        self.DEBUG = debug
        self.objects = []
        Task.nick = nick

    #Step 1: Set sources

    def SetSourcesFromFile(self, email, message):
        Task.emailsource = email
        Task.messagesource = message
        TextBuilder.LoadSources(email, message)
    def SetSourcesText(self, email, message):
        TextBuilder.emesrc = email
        TextBuilder.mssrc = message

    #Step 2: Set nick

    def SetNick(self, nick):
        Task.nick = nick

    #Step 3: Load objects or use instant values

    def LoadObjectsFromFile(self, filename):
        raw_objects = []
        try:
            if self.DEBUG:
                print("[LoadObjectsFromFile()] INFO: Trying to open the selected file with testing objects...")
            with open(filename, "rb") as f:
                lines = f.readlines()
                for line in lines:
                    raw_objects.append(line.replace(b"\n", b""))
            if self.DEBUG:
                print("Success!")
        except Exception as ex:
            if self.DEBUG:
                print("[LoadObjectsFromFile()] ERROR: unable to read or parse " + filename + ". Check its availability and try again.")
                input()
        self.LoadObjectsFromBytesArray(raw_objects)


    def LoadObjectsFromBytes(self, data):
        raw_objects = data.split(b"\n")
        self.LoadObjectsFromBytesArray(raw_objects)


    def LoadObjectsFromBytesArray(self, data):
        for raw in data:
            try:
                try:
                    obj = loads(raw)
                    if(obj.VERSION != API.ACTUALVERSION):
                        if(self.DEBUG):
                            print("[LoadObjectsFromBytesArray()] ERROR: Version of the objects are not actual. Please, run the Complier with this resource and try again. Skipping...")
                        continue
                except ValueError or AttributeError or NameError:
                    if (self.DEBUG):
                        print(
                            "[LoadObjectsFromBytesArray()] ERROR: Version of the objects are not actual. Please, run the Complier with this resource and try again. Skipping...")
                    continue
                self.objects.append(obj)
            except UnpicklingError:
                if self.DEBUG:
                    print("[LoadObjectsFromBytesArray()] ERROR: unable to decrypt object " + str(raw) + ". Perhaps the object is damaged or inaccessible.")
                    continue

    def AddObject(self, task):
        self.objects.append(task)

    def AddObjectManual(self, type, atype, crimes, network, mainlink, exlinks):
        self.objects.append(Task(type, Resource(Tags(network, atype, crimes), Links(mainlink, exlinks))))

    #Step 4: Allow or not repeating resources in the list

    def RepeatingMode(self, allowRepeating):
        self.objects_cp = copy.deepcopy(self.objects)
        self.allowRepeating = allowRepeating

    #Step 5: Get random object or generate a message/email!

    def GetRandomTask(self):
        if len(self.objects) == 0:
            if not self.objects_cp == []:
                self.objects = copy.deepcopy(self.objects_cp)
            else:
                if self.DEBUG:
                    print("[GetRandomTask()] ERROR: list of the task's is empty. Seems to be RepeatingMode is off or error while loading the objects.")
                return None
        task = random.choice(self.objects)
        if not self.allowRepeating:
            self.objects.remove(task)
        return task

    def GenerateUsingObject(self, object):
        if object:
            return object.GenerateMessage()
        else:
            if self.DEBUG:
                print("[GenerateUsingObject()] ERROR: you provided corrupted object or None value. Please check it.")
            return "Sorry, text is not available right now. Please try again later or contact the support."

    def GenerateRandom(self):
        return self.GenerateUsingObject(self.GetRandomTask())

