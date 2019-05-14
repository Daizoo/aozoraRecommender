'''
推薦部分本体
'''

import numpy as np
import pickle
from collections import Counter


def recomender(bookDB, bookIndexPath, matDataPath, fbDistMatPath, fbTempoPath,
               recordPath, tempo, bookRange, count,
               prevBook=None, genre=None, genreDB=None):
    recBooks = []  # 推薦書籍リスト
    with open(bookIndexPath, mode='rb') as f:
        bookIndex = pickle.load(f)
    if prevBook is not None:  # 2回目以降, ジャンル同基準
        bookName = prevBook

    else:  # 初回推薦
        baseList = []
        for gName in genre:
            baseList.extend(genreDB[gName])

        recBaseList = Counter(baseList)

        bias = 3
        while bias > 0:
            recBookList = []
            print('Book Bias:', bias)
            for i in recBaseList.items():
                if i[1] >= bias:
                    recBookList.append(i[0])

            if len(recBookList) > 0:
                bookName = np.random.choice(recBookList, 1, replace=False)[0]
                print(bookName)
                break
            else:
                bias -= 1

    bookDist = np.load(matDataPath)  # 距離行列
    fbTempoMat = np.load(fbTempoPath)
    fbDistMat = np.load(fbDistMatPath)
    record = np.load(recordPath)

    i = bookIndex[bookName]
    recBookDist = bookDist[i] * (fbDistMat[i] / (record[i] + 1))

    recIndex = np.argsort(recBookDist)[1:18]
    recBooksbase = [b for b, num in bookIndex.items() if num in recIndex]
    recTempo = []
    recCount = []
    recRange = []

    for tname in recBooksbase:
        j = bookIndex[tname]
        bname = tname[:-4]
        bookDataPath = bookDB[bname]['binData']
        with open(bookDataPath, mode='rb') as f:
            bookInfo = pickle.load(f)

        recTempo.append(bookInfo.tempo * (fbTempoMat[j] / (record[j] + 1)))
        recCount.append(bookInfo.rentCount)
        recRange.append(bookInfo.length)

    sortedTempo = np.argsort(np.array(recTempo))[
        3 * (tempo - 1):tempo * 3 + 2]
    print(sortedTempo)
    sortedCount = np.argsort(np.array(recCount))[
        3 * (count - 1):count * 3 + 2]
    print(sortedCount)
    sortedRange = np.argsort(np.array(recRange))[
        3 * (bookRange - 1):bookRange * 3 + 2]
    print(sortedRange)

    baseRecommend = np.vstack((sortedTempo, sortedCount, sortedRange))

    # 3項目共通
    for i in range(5):
        print('------First Check-------')
        k = baseRecommend[0][i]
        if k in baseRecommend[1, :] and k in baseRecommend[2, :]:
            recBooks.append(recBooksbase[k])
            print(recBooksbase[k])

    if len(recBooks) >= 3:
        return recBooks, bookName

    # 2項目共通
    for i in range(5):
        print('------Second Check------')
        k = baseRecommend[0][i]
        if (k in baseRecommend[1, :] or k in baseRecommend[2, :])\
                and recBooksbase[k] not in recBooks:
            recBooks.append(recBooksbase[k])
            print(recBooksbase[k])

    if len(recBooks) >= 3:
        return recBooks, bookName

    # ランダム抽出
    while len(recBooks) < 3:
        print('-----Final Check--------')
        i = np.random.randint(0, 2)
        j = np.random.randint(0, 4)

        k = baseRecommend[i][j]
        if recBooksbase[k] not in recBooks:
            recBooks.append(recBooksbase[k])
            print(recBooksbase[k])
    return recBooks, bookName
