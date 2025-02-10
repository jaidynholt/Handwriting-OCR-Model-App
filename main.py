from ImageCapture import ImageCapture
import customtkinter as ctk
from PIL import Image
import cv2
#import os for file saving
import os
import ImageProcessing as ip
import TesseractTesting as tt

LARGEFONT =("Verdana", 35)
SMALLFONT =("Verdana", 28)
BUTTONFONT =("Verdana", 18)
RELATIVEFILEPATH = "photos"
FILENAME = "imagecapture"

class App(ctk.CTk):
    pages = {}
    filecount = 0
    dictionaryDefs = {}
    dictionary = {}
    dictionaryWordCount = 0
     
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
        for PageClass in (Page0, Page1, Page2, Page3, Page4):
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
            self.filecount += 1
            self.TakePhoto(RELATIVEFILEPATH, FILENAME + str(self.filecount) + ".jpg")
            self.pages[Page2].DisplayPicture(RELATIVEFILEPATH, FILENAME+str(self.filecount)+".jpg")
            self.switchFrame(Page2)
        # if photo confirmed, run the OCR
        if (pageClass == Page3):
            text = self.RunOCR(RELATIVEFILEPATH, FILENAME+str(self.filecount)+".jpg")
            dictionaries = self.RunPartsSpeech(text)
            # if not initialized, initialize
            if len(self.dictionaryDefs) == 0:
                self.dictionaryDefs = dictionaries[1]
            #add to the class dict and make a string
            outputString = ""
            for pos in dictionaries[0]:
                if pos not in self.dictionary:
                    self.dictionary[pos] = []
                for word in dictionaries[0].get(pos):
                    self.dictionary[pos].append(word)
                    self.dictionaryWordCount += 1
                outputString += str(pos) + " (" + dictionaries[1][pos] + "):\n\t" + (", ".join(dictionaries[0][pos])) + "\n"
            #update the page3 text
            self.pages[Page3].SetText(text, outputString)
        if (pageClass == Page4):
            if self.dictionaryWordCount == 0:
                self.pages[Page4].SetText("No words so far. Please take a photo.")
            else:
                self.pages[Page4].SetText(self.CreateOutputStringFull())

    def TakePhoto(self, relativefilepath, filename):
        # the arg is the countdown time
        imageCapture = ImageCapture(11, relativefilepath, filename)
        # take the photo, returns the photo, or if the user exited, returns -1
        imageCapture.TakePhoto()

    def ExtraCrop(self, relativefilepath, filename):
        #crop extra
        tt.lil_extra_crop(os.getcwd() + os.sep + relativefilepath + os.sep + "new_"+filename)
        self.pages[Page2].DisplayPicture(RELATIVEFILEPATH, FILENAME+str(self.filecount)+".jpg")    #reload picture

    def RunOCR(self, relativefilepath, filename):
        return ip.filter_text(os.getcwd() + os.sep + relativefilepath + os.sep + "new_"+filename)
    
    def RunPartsSpeech(self, string):
        return ip.sort_by_pos(string)

    def CreateOutputStringFull(self):
        text = ""
        for pos in self.dictionary:
            text += str(pos) + " (" + self.dictionaryDefs[pos] + "): " + str(round(len(self.dictionary.get(pos)) / self.dictionaryWordCount * 100)) + "%\n\t"
            print(self.dictionary[pos])
            text += (", ".join(self.dictionary.get(pos))) + "\n"
        return text


class Page0(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        
        # draw frame1: main screen
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side="top", fill="both", expand=True)
        # title
        titleText = HeaderText(frame, "Machine Learning Handwriting App")
        titleText.grid(row=0, column=0, padx=40, pady=40, sticky="ew", columnspan=2)
        # instructions text
        instructions = ("Welcome! This app takes a picture of handwritten text "
                        "and uses optical character recognition to recognize it. "
                        "Please begin by taking a photo, "
                        "or you can view the results of previous uses.")
        instructionsText = SubheaderText(frame, instructions)
        instructionsText.grid(row=1, column=0, padx=40, pady=40, sticky="ew", columnspan=2)
        # take photo button
        button_takePhoto = SmallButton(frame, "Take Photo", lambda : controller.switchFrame(Page1))
        button_takePhoto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        # see stats button
        button_stats = SmallButton(frame, "Stats", lambda : controller.switchFrame(Page4))
        button_stats.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

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
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.pack(side="top", fill="both", expand=True)

        # display the new image
        imageFrame = ctk.CTkFrame(frame)
        imageFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        self.imageLabel = ctk.CTkLabel(imageFrame, text="")
        self.imageLabel.pack()
        cropButton = SmallButton(imageFrame, "Extra Crop", lambda : controller.ExtraCrop(RELATIVEFILEPATH, FILENAME+str(controller.filecount)+".jpg"))
        cropButton.pack()

        # buttons for image
        retakeButton = SmallButton(frame, "Retake", lambda : controller.switchFrame(Page1))
        confirmButton = SmallButton(frame, "Confirm", lambda : controller.switchFrame(Page3))
        cancelButton = SmallButton(frame, "Cancel", lambda : controller.switchFrame(Page0))
        retakeButton.grid(row=2, column=0)
        confirmButton.grid(row=2, column=1, padx=10)
        cancelButton.grid(row=2, column=2) 
    
    def DisplayPicture(self, relativeFilepath, filename):
        # load image
        photo = ctk.CTkImage(light_image=Image.open(os.getcwd() + os.sep + relativeFilepath + os.sep + "new_"+filename),
                             dark_image=Image.open(os.getcwd() + os.sep + relativeFilepath + os.sep + "new_"+filename),
                             size=(800, 600))
        self.imageLabel.configure(image=photo)


# third window frame page2
class Page3(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.pack(side="top", fill="both", expand=True)

        self.label = HeaderText(frame, "")
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky="ew", columnspan=3)
        self.partsOfSpeech = SubheaderTextBox(frame, "")
        # scrollbar = ctk.CTkScrollbar(frame, command=self.partsOfSpeech.yview)
        # scrollbar.grid(row=1, column=1)
        # self.partsOfSpeech.configure(yscrollcommand=scrollbar.set)
        self.partsOfSpeech.grid(row = 1, column = 0, padx = 40, sticky="nsew", columnspan=3)

        # take photo button
        button_takePhoto = SmallButton(frame, "Take Another Photo", lambda : controller.switchFrame(Page1))
        button_takePhoto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button_stats = SmallButton(frame, "View Stats", lambda : controller.switchFrame(Page4))
        button_stats.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        button_return = SmallButton(frame, "Return", lambda : controller.switchFrame(Page0))
        button_return.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    def SetText(self, newText, POStext):
        self.label.configure(text=newText)
        self.partsOfSpeech.configure(state="normal")
        self.partsOfSpeech.delete("0.0", "end")
        self.partsOfSpeech.insert("0.0", POStext)
        self.partsOfSpeech.configure(state="disabled")

# fourth window: stats
class Page4(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.pack(side="top", fill="both", expand=True)

        header = HeaderText(frame, "App Statistics:")
        header.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan=2)
        self.dataText = SubheaderTextBox(frame, "No stats yet! Take a photo first.")
        self.dataText.grid(row = 1, column = 0, padx = 40, sticky="nsew", columnspan=2)

        # buttons
        button_takePhoto = SmallButton(frame, "Take Another Photo", lambda : controller.switchFrame(Page1))
        button_takePhoto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button_return = SmallButton(frame, "Return", lambda : controller.switchFrame(Page0))
        button_return.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def SetText(self, fullString):
        self.dataText.configure(state="normal")
        self.dataText.delete("0.0", "end")
        self.dataText.insert("0.0", fullString)
        self.dataText.configure(state="disabled")

# standard styles for widgets
def HeaderText(app, text):
    return ctk.CTkLabel(
        app,
        text=text,
        width=600,
        height=100,
        fg_color="transparent",
        font=LARGEFONT,
	)
def SubheaderText(app, text):
    textbox =  ctk.CTkLabel(
        app,
        text=text,
        width=600,
        height=120,
        fg_color="transparent",
        text_color="#e4ebf4",
        wraplength=1000,
        font=SMALLFONT,
	)
    return textbox
def SubheaderTextBox(app, text):
    textbox =  ctk.CTkTextbox(
        app,
        activate_scrollbars=True,
        width=600,
        height=120,
        fg_color="transparent",
        text_color="#e4ebf4",
        wrap="word",
        font=SMALLFONT,
        state="disabled"
	)
    textbox.insert("0.0", text)
    return textbox
def SmallButton(app, text, func):
    return ctk.CTkButton(
        app,
        width=120,
        height=40,
        font=BUTTONFONT,
        text=text,
        command=func
    )
    

if __name__ == '__main__':
    app = App()
    app.mainloop()