'''
小説作品の話の長さを取得する
といってもただ単に長さをそのまま返すだけの関数にしてある.
モジュール化のために分割
'''


def storyLenCheck(story):
    '''
    ストーリーのデータ(一行にまとめたもの)の長さをそのまま返す関数
    Return:
    長さ(int)
    '''
    length = len(story)

    return length
