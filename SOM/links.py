class Links():
    def __init__(self, Alink, Exlinks=None):
        if Exlinks is None:
            Exlinks = []
        self.alink = Alink
        self.exlinks = Exlinks


class Exlink():
    def __init__(self, crime, link):
        self.crime = crime
        self.link = link
