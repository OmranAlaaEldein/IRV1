import xml.sax


class SecondTestDSProcess(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.note = ""
        self.description = ""
        self.summary = ""
        self.counter = 0


    # Call when an element starts
    def startElement(self, tag, attributes):

        self.CurrentData = tag
        if tag == "topic":
            self.counter += 1
            print ("({})  ".format(self.counter))

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "note":
            print("note : {}".format(self.note) )
        elif self.CurrentData == "description":
            print("description : {}".format(self.description) )
        elif self.CurrentData == "summary":
            print("summary : {}".format(self.summary) )

        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "note":
            self.note = content
        elif self.CurrentData == "description":
            self.description = content
        elif self.CurrentData == "summary":
            self.summary = content
            testDSF2.write(self.note + " " +
                           self.description + " " +
                           self.summary + "\n")



# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = SecondTestDSProcess()
parser.setContentHandler(Handler)


testDSF2 = open("dataset/testDS_num2.txt", "a")
parser.parse("dataset/testDS_num2.xml")
testDSF2.close()