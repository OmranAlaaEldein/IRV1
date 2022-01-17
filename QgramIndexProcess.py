
class QgramIndex:

    def __init__(self , q):

        self.q= q
        self.padding = ""
        self.inverted_lists = {}
        self.word_ids = {}
        self.grams_matche = {}
        self.gram_frequences = {}
        self.proposalTermsArr = []
        self.max_propTermArr = 0
        self.combinedPropDocs = {"sum_tf_idf": [], "vs_freq": [], "vs_tf_idf": []}
        self.taken_term = []

        index = 1
        while index < q :
            self.padding += "?"
            index+=1


    def clearForNewQuery(self):
        self.proposalTermsArr = []
        self.max_propTermArr = 0
        self.combinedPropDocs = {"sum_tf_idf": [], "vs_freq": [], "vs_tf_idf": []}
        self.taken_term = []


    #computing n-gram for padded ,normalized version of given string
    def Ngrams(self , word ):
        subStrs = []
        word = self.padding + word + self.padding
        index = 0
        length = len(word) - self.q + 1
        while index < length :
            gram = word[index:index+self.q]
            # delete gram of form like :
            # ( $$a , $$$a , a$$$ , a$$ , ..... etc.)
            # and keep that like
            # ( $a , a$ only )
            if( gram.count('?') <= 1 ):
                subStrs.append(gram)
            index +=1

        return  subStrs


    # build index from given list of entities (one per entity ,
    # column are : entity name , score , .... )
    def buildIndex(self , invIxObj ):
        word_id = 0
        for word in invIxObj.inverted_lists.keys():
            NgramPerms = self.Ngrams(word)
            word_id+=1
            self.word_ids[word_id] = word
            for gram in NgramPerms :
                if not gram in self.inverted_lists :
                    self.inverted_lists[gram] = set()

                self.inverted_lists[gram].add(word_id)


    def presentIndex(self):
        for subWord , words in self.inverted_lists.items() :
            print('{} => {}'.format(subWord, words))


    def presentWords(self):
        for subWord , word_ids in self.inverted_lists.items() :
            print('{} => '.format(subWord) , end="[ ")
            for id in word_ids :
                print(self.word_ids[id] , end=" ,")

            print(" ]")


    def QgramFrequence(self):
        self.gram_frequences = {}
        for gram , ids in self.grams_matche.items() :
            for id in ids :
                if not id in self.gram_frequences :
                    self.gram_frequences[id] = 0
                self.gram_frequences[id] += 1

        self.gram_frequences = sorted(self.gram_frequences.items(), key=lambda x: x[1], reverse=True)



    def Top_k_words(self , invIxObj , limit ):

        topWords = {}
        if limit < 0 :
            return  {}
        for word_id, freq in self.gram_frequences:
            word = self.word_ids[word_id]
            topWords[word] = invIxObj.inverted_lists[word]
            limit -=1
            if not limit:
                break;

        return  topWords


    def QgramMatches(self , Qry_Ngrmas):
        self.grams_matche = {}
        for Qry_gram in Qry_Ngrmas:
            if Qry_gram in self.inverted_lists :
                self.grams_matche[Qry_gram] = self.inverted_lists[Qry_gram]
                #print(subWord)


    def editDistance(self , s1, s2):
        m=len(s1)+1
        n=len(s2)+1

        tbl = {}
        for i in range(m): tbl[i,0]=i
        for j in range(n): tbl[0,j]=j
        for i in range(1, m):
            for j in range(1, n):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

        return tbl[i,j]

    def matchTermCadediates(self, candediates , term ):
        result = []
        term_ed = []
        term_length = len(term)
        taken_w = []

        for candediate, ids in candediates.items():
            ED = self.editDistance(candediate, term)
            # full matched --> no need for correct spelling ....
            if ( ED == 0 ):
                self.taken_term.append([candediate])
                return  [set(candediates[candediate])]

            # full non-matched ---> change all letter to match term
            if ( term_length != ED ):
                term_ed.append( (ED , candediate) )

            print(f"ED : {ED} between ({term},{candediate})")

        term_ed.sort()
        print("After Sort " , term_ed)

        for  ED , candediate in  term_ed :
            result.append(set(candediates[candediate]))
            taken_w.append(candediate)

        self.taken_term.append(taken_w)

        return  result


    def permutation(self, arr , terms , row , matcher  ):

        if (row == self.max_propTermArr):
            matcher.intersectionHandler.inrSecLists = arr
            Result = matcher.intersectionHandler.intersectMatchedDocs()

            if (Result != -1):
                # ranking ....
                matcher.ranker.ranking(Result , terms , self.combinedPropDocs)
            return

        index = 0
        while index < len(self.proposalTermsArr[row]):
            arr.append(self.proposalTermsArr[row][index])
            terms.append( self.taken_term[row][index] )
            self.permutation(arr,terms, row + 1 , matcher)
            terms.pop()
            arr.pop()
            index += 1




