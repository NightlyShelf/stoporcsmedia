from som.api import *
api = API("John Smith") #, debug=True)
api.SetSourcesFromFile("Email.csv", "Message.csv")
api.LoadObjectsFromFile("result.res")
api.RepeatingMode(False)
keep = True
while keep:
    print("-----------------------------------------------------------------------------------------------------------")
    text = api.GenerateRandom()
    if text == "Sorry, text is not available right now. Please try again later or contact the support.":
        keep = False
    if type(text) == str:
        print("Message:", text)
    elif type(text) == list:
        print("Header:", text[1])
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Recipient:", text[0])
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Text:", text[2])

