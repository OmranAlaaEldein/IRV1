from QgramIndexProcess import QgramIndex
from  invertedIndexProcess import invertedIndex
from IntersectionProcess import Intersection
from RankerProcess import Ranker

# basic index
BSC_IX = invertedIndex()
# query index
QUR_IX = invertedIndex()

# basic Q-gram index
BSC_QG_IX = QgramIndex(3)
# query Q-gram index
QUR_QG_IX = QgramIndex(3)

BSC_IX.readFromFile("dataset/andQueryMatch.txt")
QUR_IX.readFromFile("dataset/query.txt")


BSC_IX.presentKeywordsIndex()
print("----------------------------------")

QUR_IX.presentKeywordsIndex()
print("----------------------------------")


BSC_QG_IX.buildIndex(BSC_IX)

# foreach term in Query create n-grams

for term in QUR_IX.inverted_lists.keys():
    print("==> ( ", term, " ) " )
    ngrams = BSC_QG_IX.Ngrams(term)

    print('--------- Matches ---------')
    BSC_QG_IX.QgramMatches(ngrams)

    if (not len(BSC_QG_IX.grams_matche.items())):
        continue;


    BSC_QG_IX.QgramFrequence()

    for word_id, freq in BSC_QG_IX.gram_frequences:
        print(f"{BSC_QG_IX.word_ids[word_id]} => {freq}")

    print("----------------TOP K------------------")

    result = BSC_QG_IX.Top_k_words(BSC_IX, 3)

    for word, ids in result.items():
        print(f"{word}=>{ids}")

    print("----------------After Edit Distance------------------")
    result = BSC_QG_IX.matchTermCadediates(result,term)
    print(result)
    BSC_QG_IX.proposalTermsArr.append(result)

    print("----------------- End -----------------")
    print("---------------------------------------")

#BSC_QG_IX.presentIndex()
#print("----------------------------------")
#BSC_QG_IX.presentWords()

max_row = len(BSC_QG_IX.proposalTermsArr)

print("-------Prposal Array --------- ")
print( BSC_QG_IX.proposalTermsArr )


intersecProc = Intersection()
queryResult = set()
BSC_QG_IX.max_propTermArr = len(BSC_QG_IX.proposalTermsArr)
ranker = Ranker(BSC_IX)
BSC_QG_IX.permutation([] , [], 0 ,  intersecProc , ranker )

print('Proposal Docs for Query ')
print(BSC_QG_IX.combinedPropDocs)
