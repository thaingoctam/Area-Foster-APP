import numpy as np
import cv2
import imutils
import math
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist
mang_x=[]
height_x = []
height_xm=[]
height_xh=[]

mang_y=[]
height_y = []
height_ym=[]
height_yh=[]
def nothing(x):
  pass
cv2.namedWindow('Colorbars')
hh='Max'
hl='Min'
wnd = 'Colorbars'
cv2.createTrackbar("Max", "Colorbars",0,255,nothing)
cv2.createTrackbar("Min", "Colorbars",0,255,nothing)
img = cv2.imread('ROI1.png',0)
img = cv2.resize(img, (0,0), fx=1.5, fy=1.5)
while(1):
   hul=cv2.getTrackbarPos("Max", "Colorbars")
   huh=cv2.getTrackbarPos("Min", "Colorbars")
   ret,thresh1 = cv2.threshold(img,hul,huh,cv2.THRESH_BINARY)
   ret,thresh2 = cv2.threshold(img,hul,huh,cv2.THRESH_BINARY_INV)
   ret,thresh3 = cv2.threshold(img,hul,huh,cv2.THRESH_TRUNC)
   ret,thresh4 = cv2.threshold(img,hul,huh,cv2.THRESH_TOZERO)
   ret,thresh5 = cv2.threshold(img,hul,huh,cv2.THRESH_TOZERO_INV)
   cv2.imshow("thresh1",thresh1)
   k = cv2.waitKey(1) & 0xFF
   if k == ord('m'):
     cv2.imwrite('thresh1.png',thresh1)
   elif k == 27:
    anh = cv2.imread('thresh1.png')
    thresh = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cnt = np.array(contours)
    c = max(cnt, key=cv2.contourArea)
    #result = np.where(c==np.amin(cnt))
    x,y,w,h = cv2.boundingRect(c)
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(anh, (cx,cy), 2, (255,255,0), -1)
    cv2.drawContours(anh, [c], -1, (0,0, 255), 1)
    min_ar = (np.amin(c, axis=0))
    min_x = min_ar[0][0]
    min_y = min_ar[0][1]
    max_ar = (np.amax(c, axis=0))
    max_x = max_ar[0][0]
    max_y = max_ar[0][1]
    kc_x = min_x

####################################################################################
    number = 10
    if 0<number<max_x:
     for i in range (1,len(c)):
       kc_x = kc_x+int(max_x/(number+1))
       if 0<=len(mang_x)<number:
          mang_x.append(kc_x)    
    else:
      pass
    for i in range (len(c)):
      for j in range (len(mang_x)):
        if c[i][0][0] == mang_x[j]:
           height_x.append(c[i])
           
    div_mangx = int(len(height_x)/2)      
    for i in range (div_mangx):
      for j in range (1,len(height_x)):
        if height_x[i][0][0] == height_x[j][0][0] and height_x[i][0][1]!=height_x[j][0][1]:
           height_xm.append((height_x[i],height_x[j]))
    #print(d)
    for i7 in range (len(height_xm)):
     cv2.arrowedLine(anh, (height_xm[i7][0][0][0],height_xm[i7][0][0][1]),(height_xm[i7][1][0][0],height_xm[i7][1][0][1]),(150,100,255),1, 1,0, 0.05)
     cv2.arrowedLine(anh, (height_xm[i7][1][0][0],height_xm[i7][1][0][1]),(height_xm[i7][0][0][0],height_xm[i7][0][0][1]),(1500,100,255),1, 1,0, 0.05)
     dA = dist.euclidean((height_xm[i7][0][0][0],height_xm[i7][0][0][1]),(height_xm[i7][1][0][0],height_xm[i7][1][0][1]))
     print(dA)
    cv2.imshow("anh",anh) 
         

##################################################################################################
    number2 = 1
    kc_y = min_y
    if 0<number2<max_y:
     for i in range (1,len(c)):
       kc_y = kc_y+int(max_y/(number2+1))
       if 0<=len(mang_y)<number2:
          mang_y.append(kc_y)
    else:
      pass      
    for i in range (len(c)):
      for j in range (0,len(mang_y)):
        if c[i][0][1] == mang_y[j]:
           height_y.append(c[i])       
    div_mangy = int(len(height_y)/2)      
    for i in range (div_mangy):
      for j in range (1,len(height_y)):
        if height_y[i][0][1] == height_y[j][0][1] and height_y[i][0][0]!=height_y[j][0][0]:
           height_ym.append((height_y[i],height_y[j]))
    print((height_ym))       
    for i7 in range (len(height_ym)):
     cv2.arrowedLine(anh, (height_ym[i7][0][0][0],height_ym[i7][0][0][1]),(height_ym[i7][1][0][0],height_ym[i7][1][0][1]),(150,100,255),1, 1,0, 0.01)
     cv2.arrowedLine(anh, (height_ym[i7][1][0][0],height_ym[i7][1][0][1]),(height_ym[i7][0][0][0],height_ym[i7][0][0][1]),(1500,100,255),1, 1,0, 0.01)
     dB = dist.euclidean((height_ym[i7][0][0][0],height_ym[i7][0][0][1]),(height_ym[i7][1][0][0],height_ym[i7][1][0][1]))
     print(dB)
    cv2.imshow("anh",anh) 
