from  WordCleanProcess import WordClean

class invertedIndex:
    def __init__(self):
        # create an empty inverted index
        self.inverted_lists = {}
        self.word_occur = {}
        self.doc_occur = {}
        self.totalDcos = 0
        self.cleaner = WordClean()

    # read doc an fill words in index
    def readFromFile(self, file_name , fileFormat = True , strLine = "" ):
        # construct index from given file

        # assume ids of docs
        doc_id = 0

        # read file
        if fileFormat :
            with open(file_name, encoding="utf8") as file:
                for line in file:
                    doc_id += 1
                    self.word_occur[doc_id] = 0
                    self.workOnLine(line, doc_id)

        # read line of string (query input)
        else:
            doc_id += 1
            self.word_occur[doc_id] = 0
            self.workOnLine(strLine,doc_id)

        self.totalDcos = doc_id



    def workOnLine(self , line , doc_id ):
        words = self.cleaner.Parse(line)

        # print("--> : {}".format(words))
        for word in words:

            if (word != -1):
                # adding keyword (token) to Index ...
                if word not in self.inverted_lists:
                    self.inverted_lists[word] = []
                    self.doc_occur[word] = {}


                    # don't repeat docs id
                if not len(self.inverted_lists[word]) or \
                        self.inverted_lists[word][-1] != doc_id:
                    # first filling for doc with id (doc_id)
                    self.inverted_lists[word].append(doc_id)
                    self.doc_occur[word][doc_id] = 0

                # increase occurrence
                self.doc_occur[word][doc_id] += 1
                self.word_occur[doc_id] += 1
                # print(word)


    def clearIndex(self):
        self.inverted_lists = {}
        self.doc_occur = {}


    # present index
    def presentInvertedIndex(self):
        for word, ids in self.inverted_lists.items():
            print('{} => {}'.format( word , ids ) )


    # present keywords of index
    def presentKeywordsIndex(self):
        for key in self.inverted_lists.keys():
            print(key)

    #present index by (keyword , occurrence)
    def presentKeywordsOccur(self):
        for word, ids in self.inverted_lists.items():
            print('{} => ['.format(word) , end=" " )
            for id in ids :
                print( "#{}({})".format(id , self.doc_occur[word][id] ) , end=", " )

            print("]")

    # comparing key
    def getCmpKey(self , item):
        return  item[0]

    # present index by (keyword , Total occurrence) ordered by occurrence
    def presentIndexOrderByOccur(self):
        List = []
        for word, ids in self.inverted_lists.items():
            total_occur = 0
            for id in ids :
                total_occur += self.doc_occur[word][id]

            List.append( ( total_occur , word ) )

        List.sort(key=self.getCmpKey , reverse=True)
        for occur , word in  List :
            print('{} => {}'.format( word , occur) )




