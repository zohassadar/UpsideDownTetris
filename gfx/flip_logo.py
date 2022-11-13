
import numpy as np
from PIL import Image
import re

np.set_printoptions(formatter={'int': hex})

OLD_NAMETABLE = "nametables/title_screen_nametable.bak.bin"
NEW_NAMETABLE = "nametables/title_screen_nametable.bin"

OLD_TITLE = '/home/rwd/UpsideDownTetris/gfx/title_menu_tileset.bak.png'
NEW_TITLE = "/home/rwd/UpsideDownTetris/gfx/title_menu_tileset.png"





attr_table = """
2222222222222222
2222222222222222
2222222222222222
2333333333333332
2111111111111122
2222222222222222
2200000000000022
2000000000000022
2000000000333322
2200000000333322
2200000000333322
2200000000333322
2220311100000022
2222222222222222
2222222222222222
0000000000000000
"""


attr_values = re.findall('[0123]', attr_table)

attrs = []
for row in range(0, len(attr_values), 32):
    data = attr_values[row:row+32]
    line1 = data[:16]
    line2 = data[16:]
    for i in range(0,16,2):
        tl = int(line1[i])
        tr = int(line1[i+1]) << 2
        bl = int(line2[i]) << 4
        br = int(line2[i+1]) << 6
        byte = br | bl | tr | tl
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


ntbytes = nt_to_raw(OLD_NAMETABLE)



attr_array = np.array(ntbytes, dtype=np.uint8)
footer = attr_array[-64:]
footer.shape = 8,8
print("Original Attr Table:")
for row in footer:
    line1 = ""
    line2 = ""
    for byte in row:
        #0xNN......
        br = (byte & 0b11_00_00_00) >> 6
        #0x..NN....
        bl = (byte & 0b00_11_00_00) >> 4
        #0x....NN..
        tr = (byte & 0b00_00_11_00) >> 2
        #0x......NN
        tl = byte & 0b00_00_00_11
        line1 += f'{tl}{tr}'
        line2 += f'{bl}{br}'
    print(line1)
    print(line2)


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
    with open(NEW_NAMETABLE, 'wb') as file:
        file.write(bytes(results) )
    return results



def raw_print(ntbytes):
    ntbytes_len = len(ntbytes)
    print(f'{ntbytes_len}')
    for i in range(0, ntbytes_len, 32):
        print(' '.join([f'{b:02x}' for b in ntbytes[i: i+32]]))



array = np.array(ntbytes)
array.shape = (32,32)
subset = array[6:14,3:27]

#Flip Logo portion
array[6:14,4:28] = np.flip(subset)


#Blank out overlap on left
array[6:14,3] = 0xFF


#Determine tile indexes to flip
uniques = set(array[6:14,4:28].reshape(192,).tolist())

#Replace the blanked out "T" for the "TM"
array[6,27] = 0xB0



array.shape = (1024,)

#Replace with attrs from table above
array[-64:] = np.array(attrs)
#Write to file
raw_to_nt(array.tolist())


#Flip relevant tiles

title = Image.open(OLD_TITLE)


array = np.asarray(title, dtype=np.uint8)


new_array = array.copy()
for i in range(16):
    for j in range(16):
        idx = j | (i << 4)
        if idx not in uniques:
            continue
        x = i * 8
        y = j * 8
        new_array[x:x+8, y: y+8] = np.flip(array[x:x+8, y: y+8])

title = Image.fromarray(new_array)
title.save(NEW_TITLE)


