import random
class Task():

    emailsource = "Email.csv"
    messagesource = "Message.csv"
    nick = "Zhenya"

    def __init__(self, form, resource):
        self.form = form
        self.resource = resource
        self.VERSION = "1.0"

    def GenerateMessage(self):
        from SOM.textbuild import TextBuilder, Report
        from SOM.tags import Network
        builder = TextBuilder(self.resource, self.form, Task.nick)
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
                self.recipient = "support@twitter.com"
            return [self.recipient, self.header, self.message]
        else:
            return self.message
