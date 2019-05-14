'''
得られたデータよりジャンル推定のための距離行列を計算する関数
これを実行する前には必ず書籍リストの更新と語彙リストの更新を行い,
更新書籍の語彙データをdataConstractで生成しておくこと
'''

import numpy as np
from numpy.linalg import norm


class matrixCalc:

    def __init__(self, bookIndex: dict, wordIndex: dict):
        self.__bookIndex = bookIndex
        self.__wordIndex = wordIndex
        self.__bookList = list(bookIndex.keys())
        self.__wordList = list(wordIndex.keys())

        self.__N = len(self.__bookList)
        self.__M = len(self.__wordList)

        self.__binMat = np.zeros((self.__N, self.__M))
        self.__binDistMat = np.zeros((self.__N, self.__N))
        self.__tfMat = np.zeros((self.__N, self.__M))
        self.__idfMat = np.zeros(self.__M)
        self.__weightMat = np.zeros((self.__N, self.__N))

    def calcFromMorphData(self, morphData):
        bname = morphData.bookName
        i = self.__bookIndex[bname]

        morphsCount = morphData.wordSet

        for word, count in morphsCount.items():
            if word in self.__wordList:
                j = self.__wordIndex[word]
                self.__tfMat[i][j] = np.log10(count)
                self.__binMat[i][j] = 1
                self.__idfMat[j] += 1
            else:
                print('{} is not found'.format(word))

    def calcBookDist(self):
        # バイナリ距離の計算
        for bname1 in self.__bookList:
            i = self.__bookIndex[bname1]
            x = np.uint64(self.__binMat[i])

            for bname2 in self.__bookList:
                j = self.__bookIndex[bname2]
                y = np.uint64(self.__binMat[j])

                a = x ^ y
                b = x | y
                self.__binDistMat[i][j] = np.sum(a) / np.sum(b)

        # idf計算
        realIdfMat = np.log10(self.__N / self.__idfMat)

        # tf-idf計算
        tfidfMat = self.__tfMat * realIdfMat

        # tf-idf行列正規化
        tfidfMat = tfidfMat / norm(tfidfMat)

        # 重み行列の計算
        for bname1 in self.__bookList:
            i = self.__bookIndex[bname1]
            x = tfidfMat[i]

            for bname2 in self.__bookList:
                j = self.__bookIndex[bname2]
                y = tfidfMat[j]

                self.__weightMat[i][j] = np.sqrt(np.sum(np.power((x - y), 2)))

        return self.__binDistMat * self.__weightMat

    def reInitialize(self):
        '''
        再初期化関数
        '''
        self.__binMat = np.zeros((self.__N, self.__M))
        self.__binDistMat = np.zeros((self.__N, self.__N))
        self.__tfMat = np.zeros((self.__N, self.__M))
        self.__idfMat = np.zeros((1, self.__M))
        self.__weightMat = np.zeros((self.__N, self.__N))
