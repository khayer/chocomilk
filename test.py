import numpy as np
import cv2

CV_CAP_PROP_POS_MSEC = 0
CV_CAP_PROP_POS_FRAMES = 1
CV_CAP_PROP_POS_AVI_RATIO = 2
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_FOURCC = 6
CV_CAP_PROP_FRAME_COUNT = 7
CV_CAP_PROP_FORMAT = 8
CV_CAP_PROP_MODE = 9

cap = cv2.VideoCapture('../dunkin1.4.15.14.mov')


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.BackgroundSubtractorMOG2()
cap.set(CV_CAP_PROP_POS_FRAMES,3000)


def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

while(1):
    ret, frame = cap.read()
    cv2.imshow('frame2',frame)

    #fgmask = fgbg.apply(frame)
    fgmask = cv2.imread("background.png")
    cv2.imshow('fmask',cv2.absdiff(frame, fgmask))
    fmask = cv2.absdiff(frame, fgmask)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()