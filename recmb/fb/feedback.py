import numpy as np
from .fbCalc import ansCalcFb
import pickle


def feedBacker(tempoMatPath, distMatPath, recordPath,
               bookIndexPath, baseBook: str, targetBook: str, fbTempo, fbDist):

    with open(bookIndexPath, mode='rb') as f:
        bookIndex = pickle.load(f)

    tempoMat = np.load(tempoMatPath)
    distMat = np.load(distMatPath)
    record = np.load(recordPath)

    i = bookIndex[targetBook]
    j = bookIndex[baseBook]

    tempo = ansCalcFb(fbTempo)
    dist = ansCalcFb(fbDist)

    tempoMat[i] += tempo
    distMat[i][j] += dist
    distMat[j][i] += dist
    record[i] += 1

    np.save(tempoMatPath, tempoMat)
    np.save(distMatPath, distMat)
    np.save(recordPath, record)
