import invertedIndexProcess


module = invertedIndexProcess

li = module.invertedIndex()
li.readFromFile('dataset/andQueryMatch.txt')
#li.readFromFile('dataset/testDS_num1.txt')
#li.readFromFile('dataset/testDS_num2.txt')
#li.readFromFile('dataset/Million Query Track.txt')

#li.readFromFile("dataset/ds_num_1.txt")


# query's vector
#print("------- Score -------")

# matching (using frequency in doc) ==> scores



print("\nIndex... \n")
li.presentInvertedIndex()

print("\nKeywords... \n")
li.presentKeywordsIndex()

print("\nindex by (keyword , occurrence)... \n")
li.presentKeywordsOccur()

print("\nindex by (keyword , Total occurrence) ordered by occurrence ... \n")
li.presentIndexOrderByOccur()

print("\n doc_occur \n")

for word , doc in li.doc_occur.items() :
    print( word , " --- " , doc )
    for doc_id in doc.keys() :
        print(li.word_occur[doc_id])





