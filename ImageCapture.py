# import OpenCV
import cv2
# import time lib for countdown
import time
#import os for file saving
import os
# for getting screen size
from win32api import GetSystemMetrics
import TesseractTesting as tt

# class for accessing the camera, taking an image,
# and manipulating the data to be un-mirrored and cropped properly
class ImageCapture:
    # class attributes
    countdownTime = 2
    filepath = ""
    filename = ""
    frame = None
    # constructor
    def __init__(self, countdownTime, filepathFolder, filename):
        # Check OpenCV version
        print("OpenCV version: ", cv2.__version__)
        # initialize class variable
        self.countdownTime = countdownTime
        self.filepathFolder = filepathFolder
        self.filename = filename

    def TakePhoto(self):
        # create video capture object; arg1: device index or name of video file
        print("Accessing camera...")
        camera = cv2.VideoCapture(0)
        # if could not get input device or video file, end program
        if not camera.isOpened():
            print("Cannot open camera.")
            exit()
        self.Countdown(camera)
        #userOption = self.DisplayFrame()
        self.SaveFrame()
        newFrame = tt.output_final(os.getcwd() + os.sep + self.filepathFolder + os.sep + self.filename)
        self.SaveNewFrame(newFrame)

        # release camera and end
        camera.release()

    def Countdown(self, camera):
        # function for taking a picture, returns an image
        # the countdown
        countdownNum = self.countdownTime
        totalTime = 0.0
        print("Get ready to take the picture!")
        print("Countdown start: ")
        print(f"...{countdownNum}...")
        countdownNum -= 1
        while True:
            startTime = time.time()
            success, videoFrame = camera.read()
            # if frame is not read correctly
            if not success:
                print("ERROR: Could not receive frame.")
                return
            # display the number on the video frame
            cv2.putText(
                videoFrame,
                str(countdownNum),  # text
                (20,120),  # position of bottom left corner
                cv2.FONT_HERSHEY_PLAIN, # font
                10,  # font scale
                (17,32,43),    # color: transparent white
                5,  # line thickness
                cv2.LINE_AA # line type
            )
            cv2.namedWindow("VideoFeed", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("VideoFeed", (int)(GetSystemMetrics(0)*0.7), (int)(GetSystemMetrics(1)*0.8))
            cv2.imshow('VideoFeed', videoFrame)
            cv2.waitKey(1)
            # decrement countdown
            if totalTime >= 1.0 and countdownNum > 0:
                print(f"...{countdownNum}...")
                countdownNum -= 1   # decrement
                totalTime = 0.0     # reset
            # end video loop
            elif countdownNum <= 0:
                # read a final frame to save
                success, self.frame = camera.read()
                # if frame is not read correctly
                if not success:
                    print("ERROR: Could not receive frame.")
                    return
                print("...CAPTURED")
                # break loop
                break
            else:
                totalTime += time.time() - startTime
        # close the video window
        cv2.destroyAllWindows()
    
    def DisplayFrame(self):
        print("Displaying image")
        print("Press 'y' to confirm, 'r' to retake, 'n' to exit")
        cv2.imshow('frame', self.frame)
        # wait for enter key to be pressed
        while True:
            keyPressed = cv2.waitKey(0)
            if keyPressed == ord('y'):
                return 1
            elif keyPressed == ord('r'):
                return 2
            elif keyPressed == ord('n'):
                return 3
            
    def SaveFrame(self):
        #change directories to where to save the file
        os.chdir(os.getcwd() + os.sep + self.filepathFolder)
        # write the frame there
        cv2.imwrite(self.filename, self.frame)
        # change back the directory
        os.chdir('..')

    def SaveNewFrame(self, frame):
        #change directories to where to save the file
        os.chdir(os.getcwd() + os.sep + self.filepathFolder)
        # write the frame there
        cv2.imwrite("new_"+self.filename, frame)
        # change back the directory
        os.chdir('..')

    
