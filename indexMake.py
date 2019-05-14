import pickle
from recmb.trim.constract import bookIndexMake, wordIndexMake

bookPath = './data/book_data/half'

bookIndex = bookIndexMake(bookPath)
with open('./data/bookIndex.pickle', mode='wb') as f:
    pickle.dump(bookIndex, f)

print('BookIndex has been made.')

wordIndex = wordIndexMake(bookPath)
with open('./data/wordIndex.pickle', mode='wb') as f:
    pickle.dump(wordIndex, f)

print('WordIndex has been made.')
