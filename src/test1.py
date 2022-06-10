from Resource import *
from Tags import *
from Links import *
from Task import *
#Serialization
#import pickle as pc

testres = Resource(Tags(Network.TW, Type.AC, [Crimes.iui, Crimes.dfk, Crimes.hsp, Crimes.ofs]),
                   Links("https:/twitter.com/gazetaru", [Exlink(Crimes.iui,
                                                                "https://twitter.com/GazetaRu/status/1534849682576445440?s=20&t=1ZyTeGS74miMYloG6kep7g"),
                                                         Exlink(Crimes.hsp,
                                                                "https://twitter.com/GazetaRu/status/1534842132388892674?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ"),
                                                         Exlink(Crimes.dfk,
                                                                "https://twitter.com/GazetaRu/status/1534833652508422144?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ"),
                                                         Exlink(Crimes.iui,
                                                                "https://twitter.com/GazetaRu/status/1534823512694833152?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ")]))

#Test example
b = Task(Report.EMAIL, testres)
b.SetNick("Test")
print(b.GenerateMessage()+"\n")
b.form = Report.MESSAGE
print(b.GenerateMessage())