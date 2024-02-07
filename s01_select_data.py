import sys
import WOSRaw as wos
import WOS
import glob
import dbgz
import json
from pathlib import Path
from tqdm.auto import tqdm

# install with pip install git+https://github.com/filipinascimento/WOS.git -U
# install with pip install dbgz -U

from collections import Counter
from itertools import combinations

# %% paths and setup

DirPath = Path("../../WoS/")
WoSPapers = DirPath/"WoS_2022_DBGZ/WoS_2022_All.dbgz"

keyterms1 = ['machine learning', 'artificial intelligence']
keyterms2 = 'sens'

valid_papers = []
to_save_size = 100000

# Example of reading the data and printing Categories up to 1000 entries
entryIndex = 0
with dbgz.DBGZReader(WoSPapers) as paperDB:
    print("Scheme: ", paperDB.scheme)
    print("Number of Entries:", paperDB.entriesCount)
    pbar = tqdm(total=paperDB.entriesCount)
    while True:
        entries = paperDB.read(100)
        if(not entries): 
            break
        for entry in entries:
            title = wos.utilities.getTitle(entry).lower()
            abst = ' '.join(wos.utilities.getAbstract(entry)).lower()
            
            if keyterms2 in title:
                valid_papers.append(entry)
            elif keyterms2 in abst:
                valid_papers.append(entry)
            entryIndex+=1
            # if len(valid_papers) > 2:
            #     break
            # if entryIndex > 100:
            #     break
        if len(valid_papers) > to_save_size:
            output = open('data/sens_papers_{}.json'.format(entryIndex), 'w')
            output.write(json.dumps(valid_papers))
            output.close()
            valid_papers = []

        pbar.update(len(entries))
        
pbar.refresh()
pbar.close()

output = open('data/sens_papers.json', 'w')
output.write(json.dumps(valid_papers))
output.close()
