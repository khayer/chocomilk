"""Script to evaluate mice experiments."""
import sys
import cv2
import cv2.cv as cv
import numpy as np
import report

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

def light_on(k):
    original = k
    original = cv2.cvtColor(k,cv2.COLOR_BGR2GRAY)
    retval, image = cv2.threshold(original, 110, 180, cv2.cv.CV_THRESH_BINARY)

    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    image = cv2.dilate(image, el, iterations=6)

    cv2.imshow("dilated.png", image)

    contours, hierarchy = cv2.findContours(
        image,
        cv2.cv.CV_RETR_LIST,
        cv2.cv.CV_CHAIN_APPROX_SIMPLE
    )

    drawing = k

    centers = []
    radii = []
    if contours is not None:
        for contour in contours:
            area = cv2.contourArea(contour)

            # there is one contour that contains all others, filter it out
            if area < 2900 or area > 4500:
                continue

            br = cv2.boundingRect(contour)
            radii.append(br[2])

            m = cv2.moments(contour)
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            centers.append(center)

        print("There are {} circles".format(len(centers)))

        if not len(centers) == 0 :
            radius = int(np.average(radii)) + 5

            for center in centers:

                if center[0] > 540 and center[0] < 620 and center[1] > 120 and center[1] < 150:
                    print center

                    cv2.circle(drawing, center, 3, (255, 0, 0), -1)
                    cv2.circle(drawing, center, radius, (0, 255, 0), 1)
                    cv2.imshow("drawing.png", drawing)
                    cv2.waitKey(50)
                    #return True


    return False

    im = k
    height, width, depth = im.shape
    #print height, width, depth
    thresh = 170
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(5,5),0)
    edges = cv2.Canny(blur,thresh,thresh+50)
    #thresh2 = cv2.inRange(blur, (100,100), (180,180))
    #edges = thresh2
    cv2.imshow('edges',edges)
    circles = cv2.HoughCircles(edges, cv.CV_HOUGH_GRADIENT, 1, 10, thresh+50,300)

    if circles is not None:
        for c in circles[0]:
            cv2.circle(im,(c[0],c[1]),c[2],(255,0,0),2)
            cv2.imshow('circles',im)
            cv2.waitKey(10000)
            print c
            if c[2] < 30 and c[2] > 10:
                return True
    else:
        return False
    return False
    #contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cnt = contours[0]
    #cv2.drawContours(im,contours,-1,(0,255,0),-1)
#
    ##centroid_x = M10/M00 and centroid_y = M01/M00
    #M = cv2.moments(cnt)
    #x = int(M['m10']/M['m00'])
    #y = int(M['m01']/M['m00'])
    #print x,y
    #print width/2.0,height/2.0
    #print width/2-x,height/2-y
#
#
    #cv2.circle(im,(x,y),1,(0,0,255),2)
    #cv2.putText(im,"center of Sun contour", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
    #cv2.circle(im,(width/2,height/2),1,(255,0,0),2)
    #cv2.putText(im,"center of image", (width/2,height/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
        #cv2.waitKey(1000)
    #return True

class Target:

    def __init__(self,video,csv_file,background=None,xls_sheet=None):
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
        self.report = report.Report(csv_file).read_csv
        self.offset = self.get_offset()


    def get_background(self):
        self.capture.set(CV_CAP_PROP_POS_FRAMES,int(self.fps*10))
        _,background = self.capture.read()

        return background

    def get_offset(self):
        # Find the first house light on event
        print >> sys.stderr, "Offset ..."
        self.capture.set(CV_CAP_PROP_POS_FRAMES,0)
        self.offset = 0
        while self.offset == 0:
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            k,frame = self.capture.read()
            difference  = cv2.absdiff(frame, self.background)
            cv2.imshow(self.sample_name,difference)
            if light_on(difference):
                self.offset = self.capture.get(CV_CAP_PROP_POS_MSEC)
                print >> sys.stderr, ("Offset is %s" % self.offset)
            k = cv2.waitKey(1)
            pass
        exit()


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
    t = Target(sys.argv[1],sys.argv[2])
    t.run()
    pass

if __name__ == '__main__':
    sys.exit(main())