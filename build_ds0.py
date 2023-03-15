import os
import sys
import json
import csv
import common
import glob

LABEL_FN = 'label_map.csv'

def build_ds(src_dir:str, dest_dir:str, cfile:str, samples:int) -> None:
    if not os.path.exists(src_dir):
        print(f"source {src_dir} is not existed!")
        return

    if os.path.exists(dest_dir):
        print(f"target {dest_dir} is existed!")
        return

    with open(cfile) as fi:
        classes = [ l.strip() for l in fi.readlines()]

    label_map = common.read_label_map(LABEL_FN)
    name_map = common.label_map_reverse(label_map)
 
    for c in classes:
        id = name_map[c]
        src_sub_dir = f'{src_dir}/{id}.{c}'
        fns = glob.glob(f'{src_sub_dir}/*.jpg')
        fn0 = len(fns)
        if fn0 > samples:
            fns = fns[:samples]

        os.makedirs(f'{dest_dir}/{id}')
        for i in range(len(fns)):
            sfn = fns[i]
            dfn = f'{dest_dir}/{id}/{i}.jpg'
            with open(sfn, 'rb') as fi:
                with open(dfn, 'wb') as fo:
                    fo.write(fi.read())
            print(f'{sfn} -> {dfn}')
        print(f'{c} - {id} - {len(fns)}')


    

def main__0():
    build_ds('ds0', 'ds-tiny-20-450', 'species-tiny-20', 450)

if __name__ == '__main__':
    main__0()

# vim: ts=4 sts=4 sw=4 expandtab ai
