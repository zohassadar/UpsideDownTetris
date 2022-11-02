from itertools import cycle

import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

nametable = "nametables/title_screen_nametable.bak.bin"
nametable2 = "nametables/title_screen_nametable.bin"
title_chr = "title_menu_tileset.png"

import re

OLD_TITLE = '/home/rwd/TetrisNESDisasm/gfx/title_menu_tileset.bak.png'
NEW_TITLE = "/home/rwd/TetrisNESDisasm/gfx/title_menu_tileset.png"





attr_table = """
2222222222222222
2222222222222222
3233333333333323
2222222222222222
2222222222222222
2111111111111122
0200000000000022
2200000000000022
2200000000333322
2000000000333322
2200000000333322
2200000000333322
2222222222222222
2220311100000022
0000000000000000
2222222222222222
"""


attr_values = re.findall('[0123]', attr_table)

attrs = []
for row in range(0, len(attr_values), 32):
    data = attr_values[row:row+32]
    line1 = data[:16]
    line2 = data[16:]
    for i in range(0,16,2):
        tl = int(line1[i]) << 6
        tr = int(line1[i+1]) << 4
        br = int(line2[i+1]) << 2
        bl = int(line2[i])
        byte = tl | tr | br | bl
        attrs.append(byte)



def nt_to_raw(nametable):
    results = []
    with open(nametable, "rb") as file:
        while True:
            chunk = file.read(3)
            if not chunk or chunk == 0xFF:
                break
            results.extend(list(file.read(32)))
    return results


ntbytes = nt_to_raw(nametable)

def raw_to_nt(ntbytes):
    start_byte = 0x2000
    suffix = 0x20
    finale = 0xFF
    results = []
    ntbytes_len = len(ntbytes)
    print(f'{ntbytes_len}')
    for i in range(0, ntbytes_len, 32):
        results_len = len(results)
        chunk = ntbytes[i: i + 32]
        print (f'{i=} {chunk=} {results_len=}')
        results.extend(list((start_byte + i).to_bytes(2, byteorder="big")))
        results.append(suffix)
        results.extend(chunk)
    results.append(finale)
    with open(nametable2, 'wb') as file:
        file.write(bytes(results) )
    return results



raw_to_nt(ntbytes)

def raw_print(ntbytes):
    ntbytes_len = len(ntbytes)
    print(f'{ntbytes_len}')
    for i in range(0, ntbytes_len, 32):
        print(' '.join([f'{b:02x}' for b in ntbytes[i: i+32]]))



array = np.array(ntbytes)
array.shape = (32,32)
subset = array[6:14,3:29]
array[6:14,3:29] = np.flip(subset)

subset = array[6:14,3:29]
new_subset = subset.copy()

# new_subset[0:8, 24:28] = np.flip(subset[0:8, 0:2])
# new_subset[0:8,0:24] = subset[0:8, 2:26]

array[6:14,3:29] = new_subset

uniques = set(subset.reshape(208,).tolist())
print(uniques)



tail =array[30:32, 0:32]
tail.shape = 8,8

# tail[1:3,0:8] =  tail[2:0:-1, 0:8]
tail.shape= 2,32

array[30:32, 0:32] = tail


array.shape = (1024,)
array[-64:] = np.array(attrs)
raw_to_nt(array.tolist())




title = Image.open(OLD_TITLE)
title

array = np.asarray(title, dtype=np.uint8)
array


new_array = array.copy()
for i in range(16):
    for j in range(16):
        idx = j | (i << 4)
        print(idx)
        if idx not in uniques:
            continue
        print('flippin')
        x = i * 8
        y = j * 8
        new_array[x:x+8, y: y+8] = np.flip(array[x:x+8, y: y+8])

title = Image.fromarray(new_array)
title.save(NEW_TITLE)


