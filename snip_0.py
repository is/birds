import csv
import time

from typing import List, Dict, Tuple, TypeAlias


INDEX_FN = 'dongniao-DIB-10K-index'

def read_index(fn:str) -> List[str]:
    with open(fn) as fin:
        return fin.readlines()


def stat_category(fns:List[str]) -> Tuple[Dict[int, str], Dict[int, int]]:
    label_map = {}
    number_map = {}
    for fn in fns:
        tokens = fn.strip().split('/')
        tokens = tokens[-2:]
        dirname = tokens[0]
        id, _, name = dirname.partition('.')
        id = int(id)
        if id in label_map:
            number_map[id] += 1
        else:
            number_map[id] = 1
            label_map[id] = name
    return (label_map, number_map)


def main__0():
    ts = time.time()
    i = read_index(INDEX_FN)
    labels, numbers = stat_category(i)
    ids = sorted(labels.keys())
    with open('label_map.csv', 'w') as fout:
        for id in ids:
            fout.write(f"{id},{labels[id]},{numbers[id]}\n")
    te = time.time()
    print(f'read {len(i):,} lines, use {te - ts:,.2f}s')

    

if __name__ == '__main__':
    main__0()