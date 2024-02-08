import sys
import WOSRaw as wos
import WOS
import glob
import dbgz
import json
from pathlib import Path
from tqdm.auto import tqdm
from nltk import ngrams

# install with pip install git+https://github.com/filipinascimento/WOS.git -U
# install with pip install dbgz -U

from collections import Counter
from itertools import combinations

# %% paths and setup

DirPath = Path("../../WoS/")
WoSPapers = DirPath/"WoS_2022_DBGZ/WoS_2022_All.dbgz"

valid_papers = []
to_save_size = 100000



first_term = [('langmuir',)]

second_term_startwith = ['monolayer', 'film',]

third_term = [('blodgett',), ('langmuir-blodgett',)]

def is_valid_start_or(terms, title):
    words = title.split()
    for word in words:
        for term in terms:
            if word.startswith(term):
                return True
    return False

def is_valid_n_gram(terms, title):
    terms1 = set(terms)
    title_ngrams = list(ngrams(title, 1)) + list(ngrams(title, 2)) + list(ngrams(title, 3))    
    title_ngrams = set(title_ngrams)
    return len(title_ngrams & terms1) > 0

def valid_complete(title):
    title1 = title.lower()
    valid_first = is_valid_n_gram(first_term, title1.split())
    # print(valid_first, 'first')
    valid_second = is_valid_start_or(second_term_startwith, title1)
    valid_third = is_valid_n_gram(third_term, title1.split())
    return (valid_first and valid_second) or valid_third


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
            #print(title)
            #print(abst)
            is_valid1 = valid_complete(title)
            is_valid2 = False
        
            if abst != '':
                is_valid2 = valid_complete(abst)
    
            if is_valid1 or is_valid2:
                valid_papers.append(entry)

        pbar.update(len(entries))
        
pbar.refresh()
pbar.close()

output = open('lang_mono_film_last.json', 'w')
output.write(json.dumps(valid_papers))
output.close()
