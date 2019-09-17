# Using a web cam to track balls of different colors.

import numpy as np
import time
import argparse
import cv2

sys = time

cap = cv2.VideoCapture(2)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

blurVal = 25

while (True):
        tic = sys.time()
        ret, frame = cap.read()
        if ret == True:

                blur = cv2.blur(frame,(blurVal,blurVal))

                hsvFlip = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
                gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
                                                    #ping pong ball - 15,100,100 30,255,255
                lowerColor = np.array([15,100,100])
                upperColor = np.array([30,255,255])

                maskColor = cv2.inRange(hsvFlip, lowerColor, upperColor)
                curveIm = cv2.inRange(hsvFlip, lowerColor, upperColor)

                im2, contours, hierarchy = cv2.findContours(curveIm,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                i = 0
                maxArea = 0

                for i in range(len(contours)):
                        cnt = contours[i]
                        checkArea = cv2.contourArea(cnt)

                        if maxArea < checkArea:
                                maxCnt = contours[i]
                                maxArea = checkArea


                x,y,w,h = cv2.boundingRect(maxCnt)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                midX = int(.5*w+x)
                midY = int(.5*h+y)

                cv2.line(frame, (midX,y), (midX, y+h), (0,255,0), 2)
                cv2.line(frame, (x,midY), (x+w,midY), (0,255,0), 2)

                cv2.drawContours(frame, [maxCnt], -1, (0,125,0), 2)

                cv2.imshow('Original',frame)
                cv2.imshow('mask',maskColor)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                toc = sys.time()
                loopTime = toc - tic
                fpsCamera = cap.get(cv2.CAP_PROP_FPS)

                #print("System Loop Time: " + str(loopTime) + " Camera FPS: " + str(fpsCamera))
        else:
                break

cap.release()
out.release()
cv2.destroyAllWindows()
