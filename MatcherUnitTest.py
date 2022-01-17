
from invertedIndexProcess import invertedIndex
from QgramIndexProcess import QgramIndex
from MatcherProcess import Matcher
invertedIX = invertedIndex()
Q_gramIX = QgramIndex(3)

invertedIX.readFromFile('dataset/andQueryMatch.txt')
invertedIX.presentIndexOrderByOccur()
Q_gramIX.buildIndex(invertedIX)


matcher = Matcher(invertedIX , Q_gramIX)
print('----------------------------------')
invertedIX.presentInvertedIndex()
print('----------------------------------')

query = "how to get loca chin"
print('----------------------------------')
matcher.queryBuildIX(False,query)
print(
matcher.QUR_IX.inverted_lists.keys()
)
print('----------------------------------')

matcher.parse(False , query)