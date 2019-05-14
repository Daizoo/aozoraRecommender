'''
ユーザーの記録やアンケートの結果、選択した内容などを保存
及び呼び出しを担当する
'''

import json
import os


def userSave(datapath, userID: str, answerSet, recBook, baseBook):
    if os.path.exists(datapath + "/" + userID + '.json'):
        with open(datapath + "/" + userID + '.json', mode='r')\
                as data:
            userData = json.load(data)
            userData['ansHist'].append(answerSet)
            userData['bookHist'].append(recBook)
            userData['baseBook'].append(baseBook)

            with open(datapath + "/" + userID + '.json', mode='w')\
                    as data:
                json.dump(userData, data, indent=4)

    else:
        with open(datapath + "/" + userID + '.json', mode='a+', encoding='utf-8')\
                as data:
            userData = {}
            userData['ID'] = userID
            userData['ansHist'] = []
            userData['ansHist'].append(answerSet)
            userData['bookHist'] = []
            userData['bookHist'].append(recBook)
            userData['rentaBook'] = []
            userData['baseBook'] = []
            userData['baseBook'].append(baseBook)
            json.dump(userData, data, indent=4)


def userSaveRentBook(dataPath, userId, rentaBooks: list):
    with open(dataPath + "/" + userId + '.json', mode='r') as data:
        userData = json.load(data)

    userData['rentaBook'].append(rentaBooks)

    with open(dataPath + "/" + userId + '.json', mode='w') as data:
        json.dump(userData, data, indent=4)


def userLoad(datapath, userId: str):
    if os.path.exists(datapath + "/" + userId + '.json'):
        with open(datapath + '/' + userId + '.json', mode='r', encoding='utf-8')\
                as data:
            userData = json.load(data)

        return userData

    else:
        return False
