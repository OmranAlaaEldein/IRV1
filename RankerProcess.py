from numpy import log2 , array , dot , linalg ,around

class Ranker :

    def __init__(self , basicIX):
        self.BSC_IX = basicIX


    def TF_IDF(self , word , doc_id):
        TF  = self.BSC_IX.doc_occur[word][doc_id] / self.BSC_IX.word_occur[doc_id]
        IDF = self.BSC_IX.totalDcos / len(self.BSC_IX.inverted_lists[word])
        return around(TF * log2(IDF) , decimals=8)

                        # query index       docs result     , taken words
    def sum_TF_IDF_Score(self , taken_docs , taken_words):

        print("------------- inside sum_TF_IDF_Score -------------- ")
        ranked_docs = []
        for doc in taken_docs :
            sum = 0
            for term in taken_words :
                sum += self.TF_IDF(term ,doc)
            ranked_docs.append( (sum , doc) )

        ranked_docs.sort(reverse=True)
        doc_vector = []
        for sum , doc in ranked_docs :
            print("( " , sum , " , " , doc ," )" )
            doc_vector.append(doc)
        return  doc_vector


    def cosine(self , vec1 , vec2):

        dot_product = dot(vec1, vec2)
        norm_a = linalg.norm(vec1)
        norm_b = linalg.norm(vec2)
        return around(dot_product / (norm_a * norm_b) , decimals=8)


    def vectorSpace(self, taken_docs , taken_words , tf_idf = False):

        print('------- inside vectorSpace ---------')
        ranked_docs = []
        query_vec = []

        for i in range(len(taken_words)):
            query_vec.append(1)

        query_vec = array(query_vec)
        print("Query vector : " , query_vec )

        for doc in taken_docs :
            doc_vec = []
            for word in taken_words :
                if tf_idf:
                    doc_vec.append(self.TF_IDF(word, doc))
                else:
                    doc_vec.append(self.BSC_IX.doc_occur[word][doc])

            doc_vec = array(doc_vec)
            print("Doc Vector : " , doc_vec)
            cos_teta = self.cosine(doc_vec , query_vec)
            ranked_docs.append( (cos_teta , doc) )
        ranked_docs.sort(reverse=True)

        sortedArr = []
        for cos_teta, doc in ranked_docs:
            print("( ", cos_teta, " , ", doc, " )")
            sortedArr.append(doc)
        return sortedArr


    def Union(self , arr1 , arr2 ):

        result = []
        for item1 in arr1:
            if item1 not in arr2:
                result.append(item1)

        for item2 in arr2:
            result.append(item2)

        return result


    def rankingBySumOfTF_IDF(self, docs , terms , sortedRank):

        sortedRes = self.sum_TF_IDF_Score(docs, terms)
        if (len(sortedRank)):
            sortedRank = self.Union(sortedRank ,sortedRes)
        else:
            sortedRank = sortedRes

        return  sortedRank



    def rankingByVS(self, docs , terms , sortedRank , tf_idf = False):

        sortedRes = self.vectorSpace(docs, terms , tf_idf)
        if (len(sortedRank)):
            sortedRank = self.Union(sortedRank, sortedRes)
        else:
            sortedRank = sortedRes
        return sortedRank



    def ranking(self , docs , terms ,  combinedPropDocs):
        print("------------- Start Ranking ----------------")
        print('taken Docs : ' , docs)
        print("Words : " , terms)
        # sorting by ( sum TF-IDF )
        combinedPropDocs['sum_tf_idf'] = self.rankingBySumOfTF_IDF( docs , terms ,  combinedPropDocs['sum_tf_idf'])
        # sorting by ( vector space according to frequency of terms in doc )
        combinedPropDocs['vs_freq'] = self.rankingByVS( docs , terms ,  combinedPropDocs['vs_freq'])
        # sorting by ( vector space according to if-idf of terms in doc )
        combinedPropDocs['vs_tf_idf'] = self.rankingByVS(docs, terms, combinedPropDocs['vs_tf_idf'] ,True)




