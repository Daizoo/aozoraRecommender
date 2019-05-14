'''
書籍データから形態素を抽出し, その一覧とジャンルデータと更新日時を記録する
'''

import MeCab
import os
from numpy.random import randint
from collections import Counter
from ..calc.storyLengthCheck import storyLenCheck
from ..calc.tempoCounter import calcBookTempo


class bookData:

    def __init__(self, baseFolder, target, ver, encode='utf-8'):
        # 変数設定
        wordList = []
        self.version = ver

        self.bookName = target
        self.fbTempo = []
        self.rentCount = randint(0, 100)  # 本来は0に初期化するが、今回は何回か貸し出しを受けているという体で

        # 形態素抽出
        m = MeCab.Tagger("-x 未知語")
        with open(baseFolder + '/half/' + target, encoding=encode, mode='rt') as txt:
            parseResult = m.parse(txt.readline())
            parseList = parseResult.split('\n')

            for parseData in parseList:
                morphData = parseData.split('\t')
                if len(morphData) < 2:
                    break

                pos = morphData[1].split(',')[0]
                if morphData[0] is '見よ':
                    print('checked')
                if pos in ['名詞', '形容詞']:
                    wordList.append(morphData[0])

        print('{} morph count : {}'.format(target, len(wordList)))
        self.wordSet = dict(Counter(wordList))
        self.length = storyLenCheck(baseFolder + '/full/' + target)
        self.tempo = calcBookTempo(baseFolder + '/full/' + target)


def bookIndexMake(bookPath):

    bookList = os.listdir(bookPath)
    bookIndex = {}
    for i, bname in enumerate(bookList):
        bookIndex[bname] = i

    return bookIndex


def wordIndexMake(bookPath, encode='utf-8'):
    '''
    半分に削除した書籍データを渡す
    '''

    wordList = []
    wordIndex = {}
    m = MeCab.Tagger("-x 未知語")

    bookList = os.listdir(bookPath)

    for bname in bookList:
        with open(bookPath + '/' + bname, mode='rt', encoding=encode) as book:
            parseResult = m.parse(book.readline())
            parseList = parseResult.split('\n')

            for parseData in parseList:
                morphData = parseData.split('\t')
                if len(morphData) < 2:
                    break

                pos = morphData[1].split(',')[0]
                if morphData[0] is '見よ':
                    print('checked')
                if pos in ['名詞', '形容詞']:
                    wordList.append(morphData[0])

    wordList = set(wordList)

    for i, word in enumerate(wordList):
        wordIndex[word] = i

    return wordIndex
