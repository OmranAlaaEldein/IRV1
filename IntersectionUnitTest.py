import invertedIndexProcess
import IntersectionProcess

invertedIndex = invertedIndexProcess.invertedIndex
Intersection = IntersectionProcess.Intersection

index = invertedIndex()
query = invertedIndex()
#query.inverted_lists

index.readFromFile('dataset/andQueryMatch.txt')
index.presentIndexOrderByOccur()
print('-------------------------------------------')

# query : how to get my own localhost machine
query.readFromFile('dataset/query.txt')
query.presentIndexOrderByOccur()
# 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9   (a)
# 1 , 5 , 8 , 12 , 80                 (b)

# a and b ==> intersection ==> a & b = 1 , 5 , 8
# a or b ==>     union     ==> a | b = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 12 , 80
# a not b ==>  difference  ==> a - b = 2 , 3 , 4 , 6 , 7 , 9
intersection = Intersection()

# check for words exist in index
temp = intersection.matchWords(index , query)
taked_terms= intersection.taked_terms
print( taked_terms )
print( "Existing Words ..." )
print(temp )

# ckeck the operators (and , or , not )
queryResult = intersection.intersectMatchedDocs()
if( queryResult == -1 ):
    print("Unfortunately! no selected document(s) ...")
else :
    print("Docs Result :")
    print(queryResult)


a = set([1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9])
b = set([1 , 5 , 8 , 12 , 80 ])
c = set([1 , 5 , 7 , 9])
