import csv
from typing import Dict

def read_label_map(fn:str) -> Dict[int, str]:
    label_map = {}
    with open(fn) as fin:
        cr = csv.reader(fin)
        for r in cr:
            id = int(r[0])
            name = r[1]
            label_map[int(id)] = name.partition(",")[0]
    return label_map

def label_map_reverse(map:Dict[int,str]) -> Dict[str, int]:
    name_map = { v: k for (k, v) in map.items() }
    return name_map

    

# vim: ts=4 sts=4 sw=4 expandtab ai

