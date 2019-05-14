import codecs
import re
import os


def trimAuthor(s):
    s = s.replace("\n", "")
    s = s.replace("\r", "")
    reg = re.compile(r'''.*\-\-\-\-\-\-\-\-''')
    match = reg.match(s)
    s = s[match.end():]  # 最後のハイフン連打から前を取る

    reg = re.compile(".*底本：")
    match = reg.match(s)
    s = s[:match.end() - 3]  # 底本：　から先をとる

    while True:
        # ルビの削除
        atamare = re.compile(r".*《")
        atamamatch = atamare.match(s)

        if atamamatch is None:
            break

        atamapos = atamamatch.end() - 1

        sippore = re.compile(r".*》")
        sippomatch = sippore.match(s)
        sippopos = sippomatch.end()

        s = s[:atamapos] + s[sippopos:]

    while True:
        # 注意部分の削除
        start = re.compile(r'''.*［''')
        startm = start.match(s)

        if startm is None:
            break

        stratp = startm.end() - 1

        end = re.compile(r".*］")
        endm = end.match(s)
        endp = endm.end()

        s = s[:stratp] + s[endp:]

    s = s.replace("｜", "")

    return s


if __name__ == "__main__":
    origPath = './orig_txt'
    savePath = './books_full/'
    txtList = os.listdir('./orig_txt')

    for txtname in txtList:
        with codecs.open(origPath + '/' + txtname, encoding='shift_jis', mode='r') as txt:
            data = txt.read()
            data = trimAuthor(data)

        with codecs.open(savePath + txtname, encoding='utf-8', mode='w') as writer:
            writer.write(data)
