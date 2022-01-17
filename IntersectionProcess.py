import re

class Intersection:

    def __init__(self):
        self.inrSecLists = []
        self.taked_terms = []

    def matchWords(self , index , query ):

        self.inrSecLists = []
        self.taked_terms = []
        for word in query.inverted_lists.keys():
            print("Check for : " , word)
            if word in index.inverted_lists :
                print("{} is Exist ... ".format(word))
                self.inrSecLists.append(set(index.inverted_lists[word]))
                self.taked_terms.append(word)

            # word is not found in index
            #else :
            #    self.inrSecLists.append(set())

        return self.inrSecLists

    def matchByAnd(self , first , second ):
        self.inrSecLists[second] =  self.inrSecLists[second].\
            intersection(self.inrSecLists[first])
        print("After Intersection =>> {}".format(self.inrSecLists[second]))

    def matchByOr(self, first, second):
        self.inrSecLists[second] = self.inrSecLists[second].\
            union(self.inrSecLists[first])
        print("After Union =>> {}".format(self.inrSecLists[second]))


    def matchByNot(self, first, second):
        self.inrSecLists[second] = self.inrSecLists[first]. \
            difference(self.inrSecLists[second])
        print("After Difference =>> {}".format(self.inrSecLists[second]))



    def matchOperators(self , BiOprt , index ):

        if BiOprt == 'and':
            self.matchByAnd(index, index + 1)

        if BiOprt == 'or':
            self.matchByOr(index, index + 1)

        if BiOprt == 'not':
            self.matchByNot(index, index + 1)


    def intersectMatchedDocs(self):

        length = len(self.inrSecLists)
        if( not length ):
            return -1
        index = 0
        while( index < length-1 ):
            self.matchOperators('and' , index)
            index+=1

        if( not len(self.inrSecLists[-1]) ):
            return -1

        return  self.inrSecLists[-1]



