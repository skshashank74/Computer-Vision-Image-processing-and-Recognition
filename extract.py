# Approach discused with Ujwala Musku

from PIL import Image
import sys
import numpy as np

im1 = Image.open(sys.argv[1])
gray = im1.convert("L")
gray_np = np.array(gray)

# Decrpytion
col_move = 5
col = 20
row = 20
col_pixel = 10
row_pixel = 10

insert = [[]]
for i in range(85):
    row_move = 350
    a = np.sum(gray_np[row_move:row_move + row_pixel, col_move:col_move + col_pixel])
    row_move = row_move + row
    if a < 3000:
        insert[i].append('A')
    b = np.sum(gray_np[row_move:row_move + row_pixel, col_move:col_move + col_pixel])
    row_move = row_move + row
    if b < 3000:
        insert[i].append('B')
    c = np.sum(gray_np[row_move:row_move + row_pixel, col_move:col_move + col_pixel])
    row_move = row_move + row
    if c < 3000:
        insert[i].append('C')
    d = np.sum(gray_np[row_move:row_move + row_pixel, col_move:col_move + col_pixel])
    row_move = row_move + row
    if d < 3000:
        insert[i].append('D')
    e = np.sum(gray_np[row_move:row_move + row_pixel, col_move:col_move + col_pixel])
    if e < 3000:
        insert[i].append('E')
    col_move = col_move + col
    if i != 84:
        insert.append([])

answer = [''.join(sub_list) for sub_list in insert]
print(answer)

textfile = open(sys.argv[2], "w")
[textfile.write("{} {}\n".format(idx,val)) for idx,val in enumerate(answer,1)]
textfile.close()