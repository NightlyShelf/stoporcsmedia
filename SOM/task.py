import random

from SOM.textbuild import *
from SOM.tags import *
import urllib.parse
class Task():

    emailsource = "Email.csv"
    messagesource = "Message.csv"
    nick = "Zhenya"

    def __init__(self, form, resource):
        self.form = form
        self.resource = resource

    def GenerateMessage(self):
        builder = TextBuilder(self.resource, self.form, Task.nick, Task.messagesource, Task.emailsource)
        self.message = builder.build()

        if self.form == Report.EMAIL:
            self.header = builder.header
            if self.resource.tags.network == Network.TG:
                self.recipient = "abuse@telegram.org"
            elif self.resource.tags.network == Network.TT:
                if random.randint(1,2) == 1:
                    self.recipient = "info@tiktok.com"
                else:
                    self.recipient = "legal@tiktok.com"
            elif self.resource.tags.network == Network.FB:
                self.recipient = "support@fb.com"
            elif self.resource.tags.network == Network.IN:
                self.recipient = "support@instagram.com"
            elif self.resource.tags.network == Network.YT:
                self.recipient = "support@google.com"
            else:
                print("Twitter emailing is not supported.")
            return [self.recipient, self.header, self.message]
        else:
            return self.message
