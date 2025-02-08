from ImageCapture import ImageCapture
import customtkinter as ctk
from PIL import Image
import cv2
#import os for file saving
import os
import ImageProcessing as ip

LARGEFONT =("Verdana", 35)
RELATIVEFILEPATH = "photos"
FILENAME = "imagecapture.jpg"

class App(ctk.CTk):
    pages = {}
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        # __init__ function for class CTk
        ctk.CTk.__init__(self, *args, **kwargs)
        
        # selt window
        self._state_before_windows_set_titlebar_color = 'zoomed' # fullscreen
        self.title("TrOCR Handwriting App - WiNGHacks 2025")  # set window title
        # set window mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("colorTheme.json")
         
        # draw the frame for the entire app
        appFrame = ctk.CTkFrame(self)
        appFrame.grid_rowconfigure(0, weight=1)
        appFrame.grid_columnconfigure(0, weight=1)
        appFrame.pack(padx=100, pady=100, side="top", fill="both", expand=True)
  
        # iterating through a tuple consisting
        # of the different page layouts
        for PageClass in (Page0, Page1, Page2, Page3):
            frame = PageClass(appFrame, self)  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.pages[PageClass] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.switchFrame(Page0)

    # method to switch between frames and show them
    def switchFrame(self, pageClass):
        frame = self.pages[pageClass]
        frame.tkraise()
        # if taking the photo, call the photo functions
        if (pageClass == Page1):
            self.TakePhoto(RELATIVEFILEPATH, FILENAME)
            self.pages[Page2].DisplayPicture(RELATIVEFILEPATH, FILENAME)
            self.switchFrame(Page2)
        # if photo confirmed, run the OCR
        if (pageClass == Page3):
            text = self.runOCR()
            self.pages[Page3].SetText(text)

    def TakePhoto(self, relativefilepath, filename):
        # the arg is the countdown time
        imageCapture = ImageCapture(5, relativefilepath, filename)
        # take the photo, returns the photo, or if the user exited, returns -1
        imageCapture.TakePhoto()

    def RunOCR(self, relativefilepath, filename):
        return ip.filter_text(os.getcwd() + os.sep + relativefilepath + os.sep + "new_"+filename)
    
    def RunPartsSpeech(self, string):
        ip.sort_by_pos(string)



class Page0(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        
        # draw frame1: main screen
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side="top", fill="both", expand=True)
        # the divisions of the full frame
        frameInnerTop = ctk.CTkFrame(frame, width=200, height=200)
        frameInnerLeft = ctk.CTkFrame(frame, width=200, height=200)
        frameInnerRight = ctk.CTkFrame(frame, width=200, height=200)
        frameInnerTop.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        frameInnerLeft.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frameInnerRight.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        # title
        titleText = HeaderText(frameInnerTop, "Machine Learning Handwriting App")
        titleText.pack()
        # instructions text
        instructions = ("Welcome! This app takes a picture of handwritten text "
                        "and uses optical character recognition to recognize it. "
                        "Please begin by taking a photo, "
                        "or you can view the results of previous uses.")
        instructionsText = SubheaderTextBox(frameInnerTop, instructions)
        instructionsText.pack()
        # take photo button
        button_takePhoto = SmallButton(frameInnerLeft, "Take Photo", lambda : controller.switchFrame(Page1))
        button_takePhoto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button_takePhoto.pack()
        # see stats button
        button_stats = SmallButton(frameInnerRight, "Stats", lambda : controller.switchFrame(Page2))
        button_stats.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        button_stats.pack()

# page for loading camera
class Page1(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        # draw frame1: main screen
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.pack(side="top", fill="both", expand=True)
        # text
        text = HeaderText(frame, "Connecting to camera...\nOne moment...")
        text.pack()

# second window frame page1 
class Page2(ctk.CTkFrame):     
    def __init__(self, parent, controller):
         
        ctk.CTkFrame.__init__(self, parent)

        # draw frame2: photo screen
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.pack(side="top", fill="both", expand=True)

        # the divisions of the full frame
        frameInnerTop = ctk.CTkFrame(frame, width=200, height=200)
        frameInnerBottom = ctk.CTkFrame(frame, width=200, height=200)
        frameInnerBottom.grid_columnconfigure(0, weight=1)
        frameInnerBottom.grid_columnconfigure(1, weight=1)    
        frameInnerBottom.grid_columnconfigure(2, weight=1)
        frameInnerTop.grid(row=0, column=0, sticky="nsew", columnspan=3)
        frameInnerBottom.grid(row=1, column=0,sticky="nsew")

        # display the new image
        self.imageLabel = ctk.CTkLabel(frameInnerTop, text="")
        self.imageLabel.pack()

        # buttons for image
        retakeButton = ctk.CTkButton(frameInnerBottom, text="Retake", command=lambda : controller.switchFrame(Page1))
        confirmButton = ctk.CTkButton(frameInnerBottom, text="Confirm", command=lambda : controller.switchFrame(Page3))
        cancelButton = ctk.CTkButton(frameInnerBottom, text="Cancel", command=lambda : controller.switchFrame(Page0))
        retakeButton.grid(row=0, column=0)
        confirmButton.grid(row=0, column=1, padx=10)
        cancelButton.grid(row=0, column=2) 
    
    def DisplayPicture(self, relativeFilepath, filename):
        # load image
        os.getcwd()
        photo = ctk.CTkImage(light_image=Image.open(os.getcwd() + os.sep + relativeFilepath + os.sep + "new_"+filename),
                             dark_image=Image.open(os.getcwd() + os.sep + relativeFilepath + os.sep + "new_"+filename),
                             size=(800, 600))
        self.imageLabel.configure(image=photo)


# third window frame page2
class Page3(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

    def SetText(self, newText):
        self.label.configure(text=newText)

# standard styles for widgets
def HeaderText(app, text):
    return ctk.CTkLabel(
        app,
        text=text,
        width=600,
        height=100,
        fg_color="transparent",
        font=("Helvetica", 36),
	)
def SubheaderTextBox(app, text):
    textbox =  ctk.CTkTextbox(
        app,
        width=600,
        height=120,
        fg_color="transparent",
        font=("Helvetica", 24),
        activate_scrollbars = False,
        wrap="word"
	)
    textbox.insert("0.0", text)  # insert at line 0 character 0
    return textbox
def SmallButton(app, text, func):
    return ctk.CTkButton(
        app,
        width=120,
        height=40,
        font=("Helvetica", 18),
        text=text,
        command=func
    )
    

if __name__ == '__main__':
    app = App()
    app.mainloop()