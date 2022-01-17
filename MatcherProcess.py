from  invertedIndexProcess import invertedIndex
from IntersectionProcess import Intersection
from RankerProcess import Ranker
from os import path
baseUrl = path.dirname(__file__) + '\\'

# it's changeable according to __file__ directory
#print(baseUrl)



class Matcher :

    def __init__(self , BasicIX , QgramIX):
        self.BSC_IX = BasicIX
        self.Q_gramIX = QgramIX
        self.QUR_IX = invertedIndex()
        self.intersectionHandler = Intersection()
        self.taked_terms = []

        # ranker
        self.ranker = Ranker(BasicIX)



    def queryBuildIX(self , fileFormat = True , strLine = "" ):
        self.QUR_IX.clearIndex()
        self.QUR_IX.readFromFile('dataset/query.txt' , fileFormat , strLine)

    def getResultByBasicIX(self):
        self.taked_terms = []
        # check for words exist in index
        temp = self.intersectionHandler.matchWords(self.BSC_IX, self.QUR_IX )
        print("Existing Words ...")
        print(temp)
        self.taked_terms = self.intersectionHandler.taked_terms
        print('------------ taken terms ---------------')
        print(self.taked_terms)


        # intersection matched docsuments
        queryResult = self.intersectionHandler.intersectMatchedDocs()
        combinedPropDocs = -1


        if (queryResult != -1):
            combinedPropDocs = {"sum_tf_idf": [], "vs_freq": [], "vs_tf_idf": []}
            # ranking
            self.ranker.ranking(queryResult , self.taked_terms , combinedPropDocs)

        return combinedPropDocs


    def getResultByQgramIX(self):
        self.taked_terms = []
        self.Q_gramIX.clearForNewQuery()
        # foreach term in Query create n-grams
        for term in self.QUR_IX.inverted_lists.keys():
            print("==> ( ", term, " ) ")
            ngrams = self.Q_gramIX.Ngrams(term)

            print('------------------- Matches ------------------')
            self.Q_gramIX.QgramMatches(ngrams)
            # no match ( term does not exist even after correct spelling )
            if( not len(self.Q_gramIX.grams_matche.items()) ) :
                continue;
            self.Q_gramIX.QgramFrequence()

            for word_id, freq in self.Q_gramIX.gram_frequences:
                print(f"{self.Q_gramIX.word_ids[word_id]} => {freq}")

            print("-------------------- TOP K --------------------")

            result = self.Q_gramIX.Top_k_words(self.BSC_IX, 3)

            for word, ids in result.items():
                print(f"{word}=>{ids}")

            print("-------------- After Edit Distance -------------")
            result = self.Q_gramIX.matchTermCadediates(result, term)
            print(result)
            self.Q_gramIX.proposalTermsArr.append(result)
            print("----------------- End Iteration -----------------")
            print("-------------------------------------------------")

        self.Q_gramIX.max_propTermArr = len(self.Q_gramIX.proposalTermsArr)
        print("-------Prposal Array --------- ")
        print(self.Q_gramIX.proposalTermsArr)

        self.Q_gramIX.permutation([] ,[], 0 ,self)

        if(not len(self.Q_gramIX.combinedPropDocs['sum_tf_idf'])) :
            return -1

        return  self.Q_gramIX.combinedPropDocs


    def writeOnFile(self , file_name , headerMsg , queryResult ):
        with open(baseUrl + file_name, 'a+' , encoding="utf8") as file:
            if(headerMsg != "") :
                file.write(headerMsg + "\t\n")
            file.write(str(queryResult)+ "\t\n")

    def clearFile(self , file_name ):
        # must be checked whether there is reading
        # process or not from any Client
        open(baseUrl + file_name, 'w').close()


    def recordQueryResult(self , queryResult ):
        self.writeOnFile('OutPut.txt', "Ranked by (Sum Of TF-IDF) Method?", queryResult['sum_tf_idf'])
        self.writeOnFile('OutPut.txt', "Ranked by (Frequency Using Vector Space) Method?", queryResult['vs_freq'])
        self.writeOnFile('OutPut.txt', "Ranked by (TF-IDF Using Vector Space) Method?", queryResult['vs_tf_idf'])




    def parse(self, fileFormat = True , strLine = "" ):

        print("\n------------ Start fetching ------------\n")
        self.clearFile('OutPut.txt')
        self.queryBuildIX(fileFormat , strLine)


        # parse query using direct intersection
        queryResult = self.getResultByBasicIX()

        msg = "By Basic Index ...."
        print("\n" + msg + "\n")
        if (queryResult == -1):
            self.writeOnFile('OutPut.txt',msg, "Unfortunately! no selected document(s) ...")
            print("Unfortunately! no selected document(s) ...")
        else:
            self.writeOnFile('OutPut.txt', msg , "")
            self.recordQueryResult(queryResult)



        # parse query using undirect intersection (correct spelling)
        queryResult = self.getResultByQgramIX()

        msg = "\nBy Qgram Index ...."
        print(""+msg+"\n")
        if (queryResult == -1):
            self.writeOnFile('OutPut.txt',msg, "Unfortunately! no selected document(s) ...")
            print("Unfortunately! no selected document(s) ...")
        else:
            self.writeOnFile('OutPut.txt', msg , "")
            self.recordQueryResult(queryResult)
            print(queryResult)




