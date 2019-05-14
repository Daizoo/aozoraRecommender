from flask import Flask, render_template, request, redirect, url_for
from recmb.manage.userDataManage import userLoad, userSave, userSaveRentBook
from recmb.recomender import recomender
from recmb.fb.feedback import feedBacker
import os
import json
import chardet

dPath = './data'
app = Flask(__name__)
id = ""
with open('./data/bookTitle.json', mode='r') as j:
    bookDB = json.load(j)


@app.route('/')
# トップ画面
def top():
    return render_template('top.html')


@app.route('/anq', methods=['POST'])
# アンケートシート
def anqSheet():
    global id
    id = request.form['id']
    print('{} is Accessed!'.format(id))
    if os.path.exists(dPath + '/user_data' + '/' + id + '.json'):
        userData = userLoad(dPath + '/user_data', id)
        prevAns = userData['ansHist'][-1]
        print(prevAns)
        prevBook = userData['bookHist'][-1]
        print(prevBook)
        # つい最近のデータをロード
        return render_template('sheet.html', prevAns=prevAns,
                               prevBook=prevBook, firstFlag=0)

    else:
        print('{} does not have cash And Not found UserData.'.format(id))
        return render_template('sheet.html', prevAns={},
                               prevBook=[], firstFlag=1)


@app.route('/return', methods=['POST', 'GET'])
# 返却書籍選択画面
def retBook():
    if 'id' not in list(request.form.keys()):
        return render_template('inputID.html')
    else:
        global id
        id = request.form['id']
        userData = userLoad('./data/user_data', userId=id)
        if userData is False:
            return render_template('returnBookNothing.html')

        bookList = userData['rentaBook'][-1]
        return render_template('selectReturnBook.html',
                               bookList=bookList, ID=id)


@app.route('/fbAnq', methods=['POST'])
# フィードバックアンケート部分
def feedbackAnq():
    global id
    id = request.form['id']
    userData = userLoad('./data/user_data', id)
    prevAns = userData['ansHist'][-1]
    print(prevAns)
    bookList = request.form.getlist("selectReturnBook")
    count = len(bookList)
    tempo = prevAns['tempo']
    if 'prevBook' in list(prevAns.keys()):
        # 推薦本ベースの場合
        prevBook = userData['baseBook'][-1]
        return render_template('feedback_bookBase.html',
                               bookList=bookList, prevBook=prevBook,
                               tempo=tempo, count=count)
    else:
        # ジャンル選択の場合
        chooseGenre = prevAns['genreSelect']
        baseBook = userData['baseBook'][-1]
        return render_template('feedback_genreBase.html',
                               bookList=bookList, chooseGenre=chooseGenre,
                               tempo=tempo, baseBook=baseBook,
                               count=count)


@app.route('/rec', methods=['POST'])
# 推薦画面
def recommendBook():
    btype = request.form['btype']
    answerSet = {}

    if (btype is 'n'):
        brange = int(request.form['storyLen'])
        print('User wants range of book:', brange)
        answerSet['storyLen'] = brange
        tempo = int(request.form['tempo'])
        print('User wants tempo of book:', tempo)
        answerSet['tempo'] = tempo
        count = int(request.form['rentaCount'])
        print('Count:', count)
        answerSet['rentaCount'] = count

        if 'prevBook' in list(request.form.keys()):
            prevBook = request.form['prevRecView']
            print("User choose Pre Reccomend Book.")
            answerSet['prevBook'] = "1"
            answerSet['prevRecView'] = prevBook
            genre = None
            answerSet['genreSelect'] = ''
            genreDB = None
        else:
            prevBook = None
            answerSet['prevRecView'] = ''
            genre = request.form.getlist('genreSelect')
            answerSet['genreSelect'] = genre
            print('User choose genre:', genre)
            with open('./data/genreDB.json', mode='r', encoding='utf-8') as f:
                genreDB = json.load(f)

        recBooks, baseBook = recomender(bookDB=bookDB, tempo=tempo,
                                        matDataPath='./data/bookDist.npy',
                                        bookIndexPath='./data/bookIndex.pickle',
                                        fbTempoPath='./data/fbTempo.npy',
                                        fbDistMatPath='./data/fbDist.npy',
                                        recordPath='./data/record.npy',
                                        bookRange=brange, count=count,
                                        prevBook=prevBook, genre=genre,
                                        genreDB=genreDB)
        print(recBooks)
        userID = str(id)
        print(userID)
        userSave('./data/user_data', userID,
                 answerSet, recBooks, baseBook)
    else:
        print('No Available')

    recBooklink = []
    recBookContent = []

    for tname in recBooks:
        bname = tname[:-4]
        link = bookDB[bname]['WebLink'][-1]
        txtPath = bookDB[bname]['Full']
        with open(txtPath, mode='rb') as f:
            encCheck = chardet.detect(f.read())

        with open(txtPath, mode='r', encoding=encCheck['encoding']) as f:
            txt = f.readline()
            content = txt[:100] + '・・・'

        recBooklink.append(link)
        recBookContent.append(content)
    return render_template('result.html', recBooks=recBooks,
                           recBookContent=recBookContent,
                           recBookLink=recBooklink, ID=id)


@app.route('/renta', methods=['POST'])
# 貸し出し画面
def rentaBookManage():
    id = request.form['id']
    rentaBooks = request.form.getlist('rentaBook')

    userSaveRentBook('./data/user_data', userId=id, rentaBooks=rentaBooks)
    return render_template('finish_renta.html')


@app.route('/fb', methods=['POST'])
# フィードバックアンケート結果処理
def fbDataManage():
    i = 0
    prevBook = request.form['baseBook']
    count = int(request.form['returnBookNum'])
    for i in range(0, count):
        targetBook = request.form['bName_' + str(i)]
        fbGenre = int(request.form['genreSame_' + str(i)])
        fbTempo = int(request.form['tempoCompare_' + str(i)])

        feedBacker(tempoMatPath='./data/fbTempo.npy',
                   distMatPath='./data/fbDist.npy',
                   recordPath='./data/record.npy',
                   bookIndexPath='./data/bookIndex.pickle',
                   baseBook=prevBook, targetBook=targetBook,
                   fbDist=fbGenre, fbTempo=fbTempo)
    return (render_template('finish.html'))


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
