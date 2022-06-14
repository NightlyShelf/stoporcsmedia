from enum import Enum
from TextBuilder import *
class Task():
    def __init__(self, form, resource):
        self.form = form
        self.resource = resource

    def SetNick(self, nick):
        self.nick = nick

    def GenerateMessage(self):
        builder = TextBuilder(self.resource, self.form, self.nick)
        self.message = builder.build()
        if (self.form == Report.EMAIL):
            self.header = builder.header
        return self.message
