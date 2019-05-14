'''
話のテンポを計測する.
句点の個数と, 一文の長さと文章全体の長さを元に計算する.
最終的には平均テンポを返す.
'''
import numpy as np


def calcBookTempo(target, encode='utf-8'):
    aveTempo = 0
    with open(target, mode='rt', encoding='utf-8') as story:
        content = story.readline()
        storyLength = len(content)

    sentences = content.split('。')
    tempo = []

    for sentence in sentences:
        kuten = sentence.count('、')
        tempo.append(len(sentence) * kuten / np.sqrt(storyLength))

    aveTempo = np.average(tempo)

    return aveTempo


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    result = calcBookTempo(path)
    print('結果:', result)
