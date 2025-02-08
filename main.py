from ImageCapture import ImageCapture
import cv2

# the image capture class instance instantiation
# the arg is the countdown time
imageCapture = ImageCapture(3)
# take the photo, returns the photo, or if the user exited, returns -1
photo = imageCapture.TakePhoto()

