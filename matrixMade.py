import numpy as np
import pickle
import json
from recmb.calc.matrixCalc import matrixCalc

with open('./data/bookIndex.pickle', mode='rb') as f:
    bookIndex = pickle.load(f)

print('BookIndex was loaded')

with open('./data/wordIndex.pickle', mode='rb') as f:
    wordIndex = pickle.load(f)

print('WordIndex was loaded')

with open('./data/bookTitle.json', mode='r') as f:
    bookDB = json.load(f)

bookList = bookDB.keys()

matData = matrixCalc(bookIndex, wordIndex)
print("Calculation Rady.")
for bname in bookList:
    print(bname)
    bookDataPath = bookDB[bname]['binData']
    with open(bookDataPath, mode='rb') as b:
        bookData = pickle.load(b)

    matData.calcFromMorphData(bookData)

bookDist = matData.calcBookDist()
np.save('./data/bookDist.npy', bookDist)
print('BookDist has been Saved.')
with open('./data/matData.pickle', mode='wb') as f:
    pickle.dump(matData, f)
print('MatrixData has been Saved')
