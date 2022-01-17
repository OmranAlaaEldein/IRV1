from nltk.stem import snowball , porter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from AmbiguousTokenProcess import AmbiguousToken

import re

class WordClean:

    def __init__(self):
        self.Stemmer = porter.PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.StopWords = set(stopwords.words('english'))
        self.AmbToken = AmbiguousToken()

    def dealWithSyntax(self ,word):
        if (len(word) > 0):
            word = word.lower()
            return  (True,word)
        return (False,word)

    def dealWithStemming(self,word):
        return  self.Stemmer.stem(word)

    def dealWithLemmatizing(self,word):
        return  self.lemmatizer.lemmatize(word)

    def Tokenization(self , line):
        DTWords , restOfLine = self.AmbToken.dealWithDateTime(line)
        #print(DTWords)
        #print("rest " + restOfLine)
        words = re.split("[^a-zA-Z0-9]+", restOfLine)
        words.extend(DTWords)

        return words

    def dealWithStopWords(self , word):
        if not word in self.StopWords :
            return word
        else:
            return -1

    def Parse(self,line):
        TokenizedWords = self.Tokenization(line)
        for index, word in enumerate(TokenizedWords):
            #print("\nDeal With Tokenizaing {}".format(word) )
            resSyntx = self.dealWithSyntax(word)
            resStpW = self.dealWithStopWords(word)
            if(resSyntx[0] and resStpW != -1 ):
                #print("Deal With Syntax {}".format(resSyntx[1]))
                Stem = self.dealWithStemming(resSyntx[1])
                #print("Deal With Stemming {}".format(Stem))
                lemma_plus = self.dealWithLemmatizing(Stem)
                #print("(+)Deal With Lemmatizing {}".format(lemma_plus))
                lemma_mynus = self.dealWithLemmatizing(resSyntx[1])
                #print("(-)Deal With Lemmatizing {}".format(lemma_mynus))
                TokenizedWords[index] = lemma_plus
            else :
                TokenizedWords[index] = -1

        return TokenizedWords