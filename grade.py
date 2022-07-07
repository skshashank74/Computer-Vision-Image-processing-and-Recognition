import PIL
from PIL import Image
from PIL import Image, ImageFilter
# import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter
from PIL import Image, ImageDraw
import PIL.ImageOps 
import sys
import random
import numpy as np
# import cv2
import pandas as pd
def horz(arr,x1,x2,y1,y2,q):
  marked=""
  for i in range(5):
    # y1=i*60
    # print(y1)
    # print(np.sum(arr[x1:x2,y1+i*60:y2+i*60]))
    if np.sum(arr[x1:x2,y1+i*60:y2+i*60])>550:
      # print(np.sum(arr[x1:x2,y1+i*60:y2+i*60]))
      marked+=str(chr(65+i))
  if q<=9:
    if np.sum(arr[x1:x2,0:y2-80])>100:
      marked+=' x'
  else:
    # print(np.sum(arr[x1:x2,0:y2-100]))
    if np.sum(arr[x1:x2,0:y2-100])>100:
      marked+=' x'
  
  return marked
def vert(arr,x1,y1,itr):
  ans=[]
  for i in range(29):
    ans.append(horz(arr,x1+i*47,x1+45+i*47,y1,y1+45,itr*10+i))
  return ans
def retrive_ans(img,left,right,itr):
  top = 0.3 * height
  bottom = height
  
  # Cropped image of above dimension
  # (It will not change original image)
  imc=img.copy()
  im1 = img.crop((left, top, right, bottom))
  gray = im1.convert("L")
  im2=gray.copy()
  gray_edge = gray.filter(ImageFilter.FIND_EDGES)
  gray_edge_np = np.array(gray_edge)
  gray_edge_np=gray_edge_np
  ## columns 
  sum_mat_col = np.sum(gray_edge_np, axis=0)
  n = 50
  max_intensity_col = (-sum_mat_col).argsort()[:n]


  ## rows
  sum_mat_row = np.sum(gray_edge_np, axis=1)
  m = 80
  max_intensity_row = (-sum_mat_row).argsort()[:m]

  # sorting row and column
  max_intensity_col_st = np.sort(max_intensity_col) 
  max_intensity_row_st = np.sort(max_intensity_row) 
  # checking the distance in column
  i,j = 0,1
  col = []
  while j < len(max_intensity_col_st):
    if abs(max_intensity_col_st[i] - max_intensity_col_st[j])> 25:
      col.append(max_intensity_col_st[j])
      j+= 1
      i =j-1
    else:
      j+= 1 
  # checking the distance in row

  i,j = 0,1
  row = []
  while j < len(max_intensity_row_st):
    if j== 1:
      row.append(max_intensity_row_st[i])
    if abs(max_intensity_row_st[i] - max_intensity_row_st[j])> 12:
      row.append(max_intensity_row_st[j])
      j+= 1
      i =j-1
    else:
      j+= 1 
  
  uj_gray = np.array(im1)
  uj_gray2= np.array(im1)
  for i in range(len(col)):
    x1 = col[i]
    y1 = 0

    x2 = col[i]
    y2 = 2200

    # genp8 = cv2.line(uj_gray,(x1,y1),(x2,y2),(0,0,0),2)
    img12 = ImageDraw.Draw(im1)  
    img12.line([(x1,y1),(x2,y2)], fill ="black", width = 2)
  # plt.imshow(genp9)
  im1.save("genp8.png")
  temph=np.array(im1).copy()
  temph=temph/255
  xcord=[]
  for y in range(10,len(temph)):
    for x in range(90,len(temph[0])):
      if temph[y][x]==0:
        xcord.append(x)
        # print(xcord)
        break
  for i in range(len(row)):
    x1 = 0
    y1 = row[i]

    x2 = 1600
    y2 = row[i]

    # genp9 = cv2.line(uj_gray2,(x1,y1),(x2,y2),(0,0,0),2)
    img1 = ImageDraw.Draw(im2)  
    img1.line([(x1,y1),(x2,y2)], fill ="black", width = 2)
  # plt.imshow(genp9)
  im2.save("genp9.png")
  temph=np.array(im2)
  ycord=[]
  for y in range(10,len(temph)):
    for x in range(len(temph[0])):
      if temph[y][x]==0:
        ycord.append(y)
        # print(ycord)
        break
  # plt.imshow(genp8)
  # cv2.imwrite("genp8.png",genp8)



  im1l = imc.crop((left, top, right, bottom))
  gray2 = PIL.ImageOps.invert(im1l.convert("L"))
  gray2=np.array(gray2)/255
  results=vert(gray2,ycord[0],xcord[0],itr)
  return results
if __name__ == '__main__':
  # Load an image 
  im = Image.open(sys.argv[1])
  width, height = im.size
  left = 0
  right = width/3
  r1= retrive_ans(im,left,right,0)
  left = width/3
  right = 1.8 * width/3
  r2= retrive_ans(im,left,right,1)
  left = 1.8*width/3
  right = width
  r3= retrive_ans(im,left,right,2)
  r3.pop()
  r3.pop()
  results=r1+r2+r3
  qn=[]
  for i in range(85):
    qn.append(i+1)
  fr=pd.DataFrame(qn)
  # fr.insert(results)
  fr[1]=results
  fr.to_csv(sys.argv[2], header=None, index=None, sep='\t', mode='a')
    
