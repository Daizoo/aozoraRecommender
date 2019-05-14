from recmb.fb.fbCalc import initialize
import numpy as np

fbDistMat, fbTempo, record = initialize('./data/book_data/full')

np.save('./data/fbDist.npy', fbDistMat)
np.save('./data/fbTempo.npy', fbTempo)
np.save('./data/record.npy', record)
