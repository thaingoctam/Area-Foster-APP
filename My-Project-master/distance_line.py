import numpy as np
import cv2
import imutils
import math
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist
a =[]
b = []
d = []
e = []
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
n = 10
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
    result = np.where(c==np.amin(cnt))
    x,y,w,h = cv2.boundingRect(c)
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(anh, (cx,cy), 2, (255,255,0), -1)
    cv2.drawContours(anh, [c], -1, (0,0, 255), 1)

    #tim gia tri nho nhat trong mang [c] va chen cac mang co phan tu nho nhat vao mang [a]
    for i1 in range (len(c)):
          if np.min(c) == c[i1][0][0]:
            a.append(c[i1])

    # chia mang [a] thanh number phan tu va bo vao  mang [b]      
    m = 0
    number = 1
    for i2 in range (len(a)): 
     if m< len(a): 
      b.append(a[m])
      m = m+int(len(a)/(number))
      print(m)
     else:
        break
      
    for i3 in range (len(c)):
      for i4 in range (1,len(b)):
        if b[i4][0][1] == c[i3][0][1]and b[i4][0][0]!=c[i3][0][0]: 
           d.append((b[i4],c[i3]))
           
    m1 = 0
    while(1):
      if m1<len(d)-1:
              for i5 in range (len(d)-1):
                if d[m1][0][0][0]==d[i5][0][0][0] and d[m1][0][0][1]==d[i5][0][0][1] :
                  e.append(d[i5])
                else:
                 if m1<len(d)-1: 
                   m1 = m1+1        
      else:
        break
    i10 = 0
    for i9 in range (len(d)):
        if i10<len(e):
          if e[i10][0][0][0] == d[0][0][0][0]:
              del(d[0])
              i10 = i10+1
        else:
          break
    for i7 in range (len(d)):       
       cv2.arrowedLine(anh, (d[i7][0][0][0],d[i7][0][0][1]),(d[i7][1][0][0],d[i7][1][0][1]),(150,100,255),1, 1,0, 0.01)
       cv2.arrowedLine(anh, (d[i7][1][0][0],d[i7][1][0][1]),(d[i7][0][0][0],d[i7][0][0][1]),(1500,100,255),1, 1,0, 0.01)
       dA = dist.euclidean((d[i7][0][0][0],d[i7][0][0][1]), (d[i7][1][0][0],d[i7][1][0][1]))
       print(dA)
       cv2.imshow("anh",anh)        
          
        
    

