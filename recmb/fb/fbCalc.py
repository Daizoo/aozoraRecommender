'''
フィードバックに必要なデータの計算や, フィードバックの記録を行ったりする(予定)
'''

import os
import numpy as np


def initialize(bookpath):
    '''
    フィードバックデータの初期化を担当する.
    データのリセットや, 修復にも使えるかもしれない.
    '''
    size = len(os.listdir(bookpath))

    fbDistMat = np.ones((size, size))
    fbtempoMat = np.ones(size)
    fbRecord = np.zeros(size)

    return fbDistMat, fbtempoMat, fbRecord


def ansCalcFb(ansNum: int):
    result = 0.25 * (ansNum + 1)
    return result
