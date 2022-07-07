from task import *
from resource import *
from tags import *
from links import *
# Serialization
while True:
    testres = Resource(Tags(Network.TW, Type.AC, [Crimes.iui, Crimes.dfk, Crimes.hsp, Crimes.ofs]),
                       Links("https:/twitter.com/gazetaru", [Exlink(Crimes.iui,
                                                                    "https://twitter.com/GazetaRu/status/1534849682576445440?s=20&t=1ZyTeGS74miMYloG6kep7g"),
                                                             Exlink(Crimes.hsp,
                                                                    "https://twitter.com/GazetaRu/status/1534842132388892674?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ"),
                                                             Exlink(Crimes.dfk,
                                                                    "https://twitter.com/GazetaRu/status/1534833652508422144?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ") ]))#,
                                                             #Exlink(Crimes.iui,
                                                                    #"https://twitter.com/GazetaRu/status/1534823512694833152?s=20&t=NAKVMpiBdSNDlzlUi1v4NQ")]))
    b = Task(Report.EMAIL, testres)
    b.SetNick("Test")
    print("This test shows you how this module works. You can see the email and message to support below, which is almost unique.")
    print("--------------------------------------------------------------")
    print("Email:")
    print("--------------------------------------------------------------")
    b.form = Report.EMAIL
    print(b.GenerateMessage() + "\n")
    print("--------------------------------------------------------------")
    b.form = Report.MESSAGE
    print("Message:")
    print("--------------------------------------------------------------")
    print(b.GenerateMessage())
    print("--------------------------------------------------------------")
    print("Press enter to generate new text")
    input()
