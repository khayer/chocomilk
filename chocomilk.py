"""Script to evaluate mice experiments."""
import sys
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

    def run():
        self.capture.set(CV_CAP_PROP_POS_FRAMES,int(self.fps*100))
        for i in range(1,self.length_cali)
            _.frame = self.capture.read()
            cv2.imshow('background',frame)

def main():
    """Main entry point for the script."""
    t = Target(sys.argv[1])
    t.run
    pass

if __name__ == '__main__':
    sys.exit(main())