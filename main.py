from ImageCapture import ImageCapture
import tkinter as tk
import cv2

def main():
    # Create the main window
    # window = tk.Tk()
    # window.title("My Window")

    # # Add a label
    # label = tk.Label(window, text="Hello, World!")
    # label.pack()

    # # Start the main event loop
    # window.mainloop()
    # the image capture class instance instantiation
    # the arg is the countdown time
    imageCapture = ImageCapture(1, "./photos", "photo1.jpg")
    # take the photo, returns the photo, or if the user exited, returns -1
    imageCapture.TakePhoto()

    # save image
    

if __name__ == '__main__':
    main()