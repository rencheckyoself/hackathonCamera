import numpy as np
import time
import argparse
import cv2
import serial
import servoLibrary
import os

ser = serial.Serial('/dev/ttyACM0',9600)

screenX = 640
screenY = 480

base = servoLibrary.Servo(0)
head = servoLibrary.Servo(1)

sys = time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screenX)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screenY)

os.system("v4l2-ctl -d /dev/video0 -c exposure_auto=1")
os.system("v4l2-ctl -d /dev/video0 -c exposure_absolute=100")
os.system("v4l2-ctl -d /dev/video0 -c white_balance_temperature_auto=0")
os.system("v4l2-ctl -d /dev/video0 -c white_balance_temperature=2800")
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (screenX,screenY))

os.system("")


def main():
        maxCnt = None
        defaultX = int(screenX/2)
        defaultY = int(screenY/2)

        stepSize = 25

        prevArea = 0

        blurVal = 25

        while (True):
                tic = sys.time()
                ret, frame = cap.read()

                blur = cv2.blur(frame,(blurVal,blurVal))

                hsvFlip = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

                #ping pong ball - 15,100,100 30,255,255
                lowerColor = np.array([6,20,20])
                upperColor = np.array([25,255,255])

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


                if maxCnt is None:
                        setX = defaultX
                        setY = defaultY
                else:
                        x,y,w,h = cv2.boundingRect(maxCnt)
                        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        setX = int(.5*w+x)
                        setY = int(.5*h+y)
                        cv2.line(frame, (setX,y), (setX, y+h), (0,255,0), 2)
                        cv2.line(frame, (x,setY), (x+w,setY), (0,255,0), 2)
                        #print(setX,setY)

                cv2.drawContours(frame, [maxCnt], -1, (0,125,0), 2)

                cv2.imshow('Original',frame)
                #cv2.imshow('mask',maskColor)

                toc = sys.time()
                loopTime = toc - tic
                fpsCamera = cap.get(cv2.CAP_PROP_FPS)
                #print("System Loop Time: " + str(loopTime) + " Camera FPS: " + str(fpsCamera))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                moveBase = int(((-defaultX + setX)/(.5*screenX))**3 * stepSize)
                moveHead = int(((-defaultY + setY)/(.5*screenY)) * stepSize)

                ser.write(base.Move(moveBase))
                ser.write(head.Move(moveHead))

ser.write(base.Move(0))
ser.write(head.Move(0))
main()
cap.release()
cv2.destroyAllWindows()
