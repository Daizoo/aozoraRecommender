import pandas as pd
import json
import re
import os
import pickle
import chardet
from recmb.trim.trimAozoraFrame import trimAuthor
from recmb.trim.constract import bookData

# 各種変数設定
linkIndex = "XHTML/HTMLファイルURL"
fullData = './data/book_data/full/'
halfData = './data/book_data/half/'
binData = './data/book_data/binary/'

# データの読み込み
bookList = pd.read_csv('./data/bookList.csv', encoding='utf-8',
                       names=('title', 'file'))
aozoraDB = pd.read_csv('./data/aozora_DB.csv',
                       encoding='utf-8', na_filter=False)
bookFileListBase = os.listdir('./data/book_orig')
bookFileListBaseTrimed = os.listdir('./data/book_trimed')
bookFileList = []
bookFileListTrimed = []
# タイトルトリミング
for bname in bookFileListBase:
    trimData = re.match(r".*@", bname)
    if trimData is not None:
        end = trimData.end()
        fileName = bname[end:]
    else:
        fileName = bname

    bookFileList.append(fileName)

for bname in bookFileListBaseTrimed:
    trimData = re.match(r".*@", bname)
    if trimData is not None:
        end = trimData.end()
        fileName = bname[end:]
    else:
        fileName = bname

    bookFileListTrimed.append(fileName)


# データベース作成
bookDB = {}
print("Start Not Trimed Data")
for i in range(0, len(bookFileList)):
    bookInfo = {}
    bname = bookFileListBase[i]  # ファイル名取得
    fname = bookFileList[i]

    title = bookList[bookList['file'] == fname]['title'].tolist()[0]  # タイトル取得
    bookInfo['Title'] = title
    link = aozoraDB[aozoraDB['作品名'] == title][linkIndex].tolist()  # webリンク取得
    bookInfo['WebLink'] = link

    # 読み込み
    with open('./data/book_orig/' + bname, mode='r', encoding='shift_jis')\
            as f:
        content = trimAuthor(f.read())  # 青空文庫の内部データ

    content_half = content[round(len(content) / 2):]

    # 書き込み
    with open(fullData + fname, mode='wt', encoding='utf-8') as w:
        w.write(content)
        print('{} is Full written.'.format(fname))

    with open(halfData + fname, mode='wt', encoding='utf-8') as w:
        w.write(content_half)
        print('{} is Half written'.format(fname))

    bookInfo['Full'] = fullData + fname
    bookInfo['Half'] = halfData + fname

    # 計算用バイナリデータ
    dataForCalc = bookData('./data/book_data', fname, 1.0)
    txtName = fname[:-4]
    with open(binData + txtName + '.pickle', mode='wb') as p:
        pickle.dump(dataForCalc, p)
        print('{} is binary Saved.'.format(fname))

    bookInfo['binData'] = binData + txtName + '.pickle'
    bookDB[txtName] = bookInfo

for i in range(0, len(bookFileListTrimed)):
    bookInfo = {}
    bname = bookFileListBaseTrimed[i]  # ファイル名取得
    fname = bookFileListTrimed[i]

    title = bookList[bookList['file'] == fname]['title'].tolist()[
        0]  # タイトル取得
    if len(title) <= 0:
        print("Book Not Found:", fname)
        continue
    bookInfo['Title'] = title
    link = aozoraDB[aozoraDB['作品名'] == title][linkIndex].tolist()
    # webリンク取得
    bookInfo['WebLink'] = link

    # 読み込み
    with open('./data/book_trimed/' + bname, mode='rb') as f:
        encChecker = chardet.detect(f.read())  # エンコード確認

    with open('./data/book_trimed/' + bname, mode='r', encoding=encChecker['encoding'])\
            as f:
        content = f.read()  # 青空文庫の内部データ

    content_half = content[round(len(content) / 2):]

    # 書き込み
    with open(fullData + fname, mode='wt', encoding='utf-8') as w:
        w.write(content)
        print('{} is Full written.'.format(fname))

    with open(halfData + fname, mode='wt', encoding='utf-8') as w:
        w.write(content_half)
        print('{} is Half written'.format(fname))

    bookInfo['Full'] = fullData + fname
    bookInfo['Half'] = halfData + fname

    # 計算用バイナリデータ
    dataForCalc = bookData('./data/book_data', fname, 1.0)
    txtName = fname[: -4]
    with open(binData + txtName + '.pickle', mode='wb') as p:
        pickle.dump(dataForCalc, p)
        print('{} is binary Saved.'.format(fname))

    bookInfo['binData'] = binData + txtName + '.pickle'
    bookDB[txtName] = bookInfo

with open('./data/bookTitle.json', mode='w', encoding='utf-8') as j:
    json.dump(bookDB, j, indent=4)

print('DB is made.')
