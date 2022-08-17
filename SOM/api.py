import random

from SOM.textbuild import *
from SOM.task import *
from pickle import loads, dumps, UnpicklingError


class API:
    def __init__(self, nick, debug=False):
        self.DEBUG = debug
        self.objects = []
        self.nick = nick

    def SetSourcesFromFile(self, email, message):
        Task.emailsource = email
        Task.messagesource = message
        TextBuilder.LoadSources(email, message)
    def SetSourcesText(self, email, message):
        TextBuilder.emesrc = email
        TextBuilder.mssrc = message

    def LoadObjectsFromFile(self, filename):
        raw_objects = []
        try:
            if self.DEBUG:
                print("Trying to open the selected file with testing objects...")
            with open(filename, "rb") as f:
                lines = f.readlines()
                for line in lines:
                    raw_objects.append(line.replace(b"\n", b""))
            if self.DEBUG:
                print("Success!")
        except Exception as ex:
            if self.DEBUG:
                print("Error occurred: unable to read or parse " + filename + ". Check its availability and try again.")
                input()
        self.LoadObjectsFromBytesArray(raw_objects)


    def LoadObjectsFromBytes(self, data):
        raw_objects = data.split(b"\n")
        self.LoadObjectsFromBytesArray(raw_objects)


    def LoadObjectsFromBytesArray(self, data):
        for raw in data:
            try:
                obj = dumps(raw)
                self.objects.append(obj)
            except UnpicklingError:
                if self.DEBUG:
                    print("Error occurred: unable to decrypt object " + str(raw) + ". Perhaps the object is damaged or inaccessible.")
                    continue


    def GetRandomTask(self):
        return random.choice(self.objects)

    def GenerateUsingObject(self, object):
        return object.GenerateMessage()

    def GenerateRandom(self):
        self.GenerateUsingObject(self.GetRandomTask())

