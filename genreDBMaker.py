import os
import re
import json

bookTxtList1 = os.listdir('./data/book_orig')
bookTxtList2 = os.listdir('./data/book_trimed')
bookTxtList1.extend(bookTxtList2)

genreDB = {}

for tname in bookTxtList1:
    trimData = re.match(r".*@", tname)
    if trimData is not None:
        end = trimData.end()
        genres = trimData.group()[:-1]
        genreList = genres.split(',')
        bname = tname[end:]

    for genre in genreList:
        if genre not in genreDB:
            genreDB[genre] = []

        genreDB[genre].append(bname)
with open('./data/genreDB.json', mode='wt', encoding='utf-8') as f:
    json.dump(genreDB, f, indent=4)
