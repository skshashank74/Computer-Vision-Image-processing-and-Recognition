# Approach discused with Ujwala Musku

from PIL import Image
import sys
import pandas as pd
import numpy as np

with open(sys.argv[2], 'r') as f:
    data = f.readlines()

for itr in range(len(data)):
    data[itr] = data[itr].split(' \n')[0]
    data[itr] = data[itr].split('\n')[0]

df = pd.DataFrame([itr.split(" ") for itr in data])
df.columns = ['questions', 'answers']

im = Image.open(sys.argv[1])
# Injecting
def color_pixel(im, col_move, row_move):
    for pix_row in range(10):
        for pix_col in range(10):
            im.putpixel((col_move + pix_col, row_move + pix_row), (0))

col_move = 5
column_spacing = 20
row_spacing = 20

for i in range(df.shape[0]):
    row_move = 350
    if 'A' in df['answers'][i]:
        color_pixel(im, col_move, row_move)
    row_move = row_move + row_spacing
    if 'B' in df['answers'][i]:
        color_pixel(im, col_move, row_move)
    row_move = row_move + row_spacing
    if 'C' in df['answers'][i]:
        color_pixel(im, col_move, row_move)
    row_move = row_move + row_spacing
    if 'D' in df['answers'][i]:
        color_pixel(im, col_move, row_move)
    row_move = row_move + row_spacing
    if 'E' in df['answers'][i]:
        color_pixel(im, col_move, row_move)
    col_move = col_move + column_spacing

im.save(sys.argv[3])



