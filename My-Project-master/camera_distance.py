from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
cen = []
def midpoint(ptA, ptB, ptC, ptD):
	return ((ptA + ptC * 0.5), ptB, (ptA + ptC * 0.5), ptB + ptD)
cap=cv2.VideoCapture(0)

while(1):
    d=0.1
    centers=[]
    _,img = cap.read()

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    blue_lower=np.array([80,100,100],np.uint8)
    blue_upper=np.array([130,255,255],np.uint8)

    blue=cv2.inRange(hsv, blue_lower, blue_upper)

    kernal = np.ones((5,5), "uint8")

    blue=cv2.erode(blue,kernal,iterations=1)
    resl=cv2.bitwise_and(img,img,mask = blue)
    
    (contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate (contours):
            area = cv2.contourArea(contour)
            if(area>300):
                    x,y,w,h = cv2.boundingRect(contour)
                    (a,b,c,d) = midpoint(x,y,w,h)
                    dA = dist.euclidean((a,b), (c,d))
                    W = 0.264
                    dimA = dA*W
                    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.putText(img, "Marcador", (x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))
                    cv2.putText(img, "{:.1f}mm".format(dimA),
                                (int(a-15), int(b-10)), cv2.FONT_HERSHEY_SIMPLEX,
                                 0.65,(255,255,255),1)
                    cv2.line(img, (int(a), int(b)), (int(c), int(d)),
                        (250,0,255), 2)
                    M = cv2.moments(contour)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    centers = (cx,cy)
                    cen.append(centers)
                    #centers.append(centers)
                    
                    cv2.circle(img, (cx,cy), 7, (255,255,255), -1)

                    if len(centers)==2:
                            print(abs(cen[0][1]-cen[0][0]))
                            print(cen[0][0],cen[0][1])
                            D=np.linalg.norm(cx-cy)
                            #print(D)
    cv2.imshow("Color Tracking",img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
              cap.release()
              cv2.destroyAllWindows()
              break
