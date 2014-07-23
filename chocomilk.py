"""Script to evaluate mice experiments."""
import sys
import cv2
import numpy as np

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

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def is_within(p1,p2,dis=50):
    return abs(p1-p2) <= dis

class Target:

    def __init__(self,video,background=None,xls_sheet=None):
        self.sample_name = video.split("/")[-1]
        self.capture = cv2.VideoCapture(video)
        self.numframes = self.capture.get(CV_CAP_PROP_FRAME_COUNT)
        print >> sys.stderr, self.numframes
        self.fps = self.capture.get(CV_CAP_PROP_FPS)
        print >> sys.stderr, self.fps
        self.increaser = int(self.fps/5)
        if self.increaser == 0:
            self.increaser = 1
        self.length_cali = 250
        self.width = self.capture.get(CV_CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(CV_CAP_PROP_FRAME_HEIGHT)
        if xls_sheet:
            self.xls_sheet = xls_sheet
        if background:
            self.background = cv2.LoadImageM(background)
        else:
            self.background = self.get_background()

    def get_background(self):
        self.capture.set(CV_CAP_PROP_POS_FRAMES,int(self.fps*10))
        _,background = self.capture.read()

        return background

    def run(self):
        print >> sys.stderr, "Calibration ..."
        #frame_size = cv.GetSize(cv.fromarray(self.capture))
        #grey_image2 = cv2.createimage(frame_size, cv.IPL_DEPTH_8U, 1)
        self.capture.set(CV_CAP_PROP_POS_FRAMES,int(self.fps*500))
        k,frame = self.capture.read()

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        fgbg = cv2.BackgroundSubtractorMOG2()

        mask = np.zeros(frame.shape[:2],np.uint8)

        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        last_x = int(self.width/2)
        last_y = int(self.height/2)


        for i in range(1,self.length_cali):
            #print >> sys.stderr, int(self.fps*100+i*self.increaser)
            self.capture.set(CV_CAP_PROP_POS_FRAMES,int(self.fps*500+i*self.increaser))
            #print >> sys.stderr, self.capture.get(CV_CAP_PROP_POS_FRAMES)
            k = self.capture.read(frame)
            cv2.imwrite("test.png",frame)
            #print >> sys.stderr, k
            difference  = cv2.absdiff(frame, self.background)
            cv2.imshow(self.sample_name,difference)
            thresh = cv2.inRange(frame, (30,30,30), (65,65,65))
            thresh2 = cv2.inRange(difference, (200,200,200), (255,255,255))
            cv2.imshow("THRESH",thresh)
            test = cv2.convertScaleAbs(thresh)
            test2 = cv2.convertScaleAbs(thresh2)
            #difference = cv2.convertScaleAbs(difference)
            test = cv2.bitwise_and(test,test2)
            cv2.imshow("test",test)
            fgmask = fgbg.apply(frame)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            #ret,thresh = cv2.threshold(test, 200, 255,0)
            #cv2.imshow("THRESH",thresh)
            new_test = cv2.bitwise_and(fgmask, test)
            ret,new_test = cv2.threshold(new_test, 100, 255,0)
            #cv2.imshow("THRESH",thresh)
            element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(10,10))
            #new_test = cv2.dilate(new_test, element, 10)
            #new_test = cv2.erode(new_test,element, 1)
            #new_test = cv2.dilate(new_test,element, 1)
            countours,hierarchy = cv2.findContours(test,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            cv2.imshow("test2",new_test)

            #gray = cv2.cvtColor(test,cv2.COLOR_BGR2GRAY)

            #gray = cv2.cvtColor(test,cv2.COLOR_BGR2GRAY)

            corners = cv2.goodFeaturesToTrack(new_test,100,0.05,5)
            corners = np.int0(corners)

            mask = np.zeros(frame.shape[:2],np.uint8)

            bgdModel = np.zeros((1,65),np.float64)
            fgdModel = np.zeros((1,65),np.float64)

            rect = (last_x-125,last_y-125,last_x+125,last_y+125)
            #rect = (100,100,200,200)
            #cv2.grabCut(frame ,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

            #mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
            #k = frame*mask2[:,:,np.newaxis]
            mask = np.zeros(frame.shape,np.uint8)
            mask[rect[1]:rect[3],rect[0]:rect[2]] = frame[rect[1]:rect[3],rect[0]:rect[2]]
            cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),240)
            background2 = np.zeros(frame.shape,np.uint8)
            background2[rect[1]:rect[3],rect[0]:rect[2]] = self.background[rect[1]:rect[3],rect[0]:rect[2]]
            mask = cv2.absdiff(mask, background2)
            difference  = cv2.absdiff(mask, background2)
            thresh = cv2.inRange(mask, (40,40,40), (65,65,65))
            thresh2 = cv2.inRange(difference, (10,10,10), (25,25,25))
            cv2.imshow("THRESH2",difference)
            test = cv2.convertScaleAbs(thresh)
            cv2.imshow('mask1',test)
            test2 = cv2.convertScaleAbs(thresh2)
            cv2.imshow('mask2',test2)
            #difference = cv2.convertScaleAbs(difference)
            mask = cv2.bitwise_and(test,test2)
            #mask = test2
            #mask = cv2.dilate(test2,element, 3)

            cv2.imshow('mask',mask)
            #cv2.imshow('b',frame)
            all_x = []
            all_y = []

            for i in corners:

                x,y = i.ravel()
                if not is_within(x,last_x,100) or not is_within(y,last_y,100) :
                    continue
                if not (x > rect[0] and x<rect[2]) or not (y > rect[1] and y<rect[3]) :
                    print >> sys.stderr, x
                    print >> sys.stderr, y
                    continue
                cv2.circle(frame,(x,y),3,(200,200),-1)
                all_x.append(x)
                all_y.append(y)

            if all_x:
                x_med = int(np.median(all_x))
                y_med = int(np.median(all_y))
            else:
                x_med = last_x
                y_med = last_y

            corners = cv2.goodFeaturesToTrack(mask,100,0.05,5)
            corners = np.int0(corners)

            all_x = []
            all_y = []


            for i in corners:

                x,y = i.ravel()
                if not is_within(x,x_med,100) or not is_within(y,y_med,100) :
                    continue
                #if not (x > rect[0] and x<rect[2]) or not (y > rect[1] and y<rect[3]) :
                #    print >> sys.stderr, x
                #    print >> sys.stderr, y
                #    continue
                cv2.circle(frame,(x,y),3,(200,100),-1)
                all_x.append(x)
                all_y.append(y)

            x = int(np.median(all_x))
            y = int(np.median(all_y))

            if (x > rect[0] and x<rect[2]) and (y > rect[1] and y<rect[3]):
                last_x = x
                last_y = y

            #plt.imshow(frame),plt.colorbar(),plt.show()
            cv2.circle(frame,(last_x,last_y),6,255,5)
            cv2.imshow('dst',frame)

            #print >> sys.stderr, countours[0]
            #print >> sys.stderr, hierarchy[0]
            k = cv2.waitKey(1)
        return

def main():
    """Main entry point for the script."""
    t = Target(sys.argv[1])
    t.run()
    pass

if __name__ == '__main__':
    sys.exit(main())