# import OpenCV
import cv2
# import time lib for countdown
import time

# class for accessing the camera, taking an image,
# and manipulating the data to be un-mirrored and cropped properly
class ImageCapture:
    # class attributes
    countdownTime = 2
    # constructor
    def __init__(self, countdownTime):
        # Check OpenCV version
        print("OpenCV version: ", cv2.__version__)
        # initialize class variable
        self.countdownTime = countdownTime

    def TakePhoto(self):
        # create video capture object; arg1: device index or name of video file
        print("Accessing camera...")
        camera = cv2.VideoCapture(0)
        # if could not get input device or video file, end program
        if not camera.isOpened():
            print("Cannot open camera.")
            exit()
        
        userOption = -1
        while True:
            # take the frame
            frame = self.GetFrame(camera)
            # display the frame
            userOption = self.DisplayFrame(frame)
            if (userOption == 1):
                return frame
            elif userOption == 3:
                print("Bye!")
                exit()

    def GetFrame(self, camera):
        # function for taking a picture, returns an image
        # the countdown
        countdownNum = self.countdownTime
        print("Get ready to take the picture!")
        print("Countdown start: ")
        print(f"...{countdownNum}...")
        countdownNum -= 1
        startTime = time.time()
        totalTime = 0.0
        while countdownNum > 0:
            startTime = time.time()
            if totalTime >= 1.0 and countdownNum > 0:
                print(f"...{countdownNum}...")
                countdownNum -= 1   # decrement
                totalTime = 0.0     # reset
            totalTime += time.time() - startTime
        # access camera
        success, frame = camera.read()
        # if frame is not read correctly
        if not success:
            print("ERROR: Could not receive frame.")
            return
        print("...CAPTURED")
        return frame
    
    def DisplayFrame(self, frame):
        print("Displaying image")
        print("Press 'y' to confirm, 'r' to retake, 'n' to exit")
        cv2.imshow('frame', frame)
        # wait for enter key to be pressed
        while True:
            keyPressed = cv2.waitKey(0)
            if keyPressed == ord('y'):
                return 1
            elif keyPressed == ord('r'):
                return 2
            elif keyPressed == ord('n'):
                return 3

    
