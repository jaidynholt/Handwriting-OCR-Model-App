from ImageCapture import ImageCapture
import customtkinter as ctk
from PIL import Image
import cv2
#import os for file saving
import os

def main():
    # Create the main window
    app = ctk.CTk()
    app._state_before_windows_set_titlebar_color = 'zoomed' # fullscreen
    app.title("TrOCR Handwriting App - WiNGHacks 2025")  # set window title

    # set window mode
    ctk.set_appearance_mode("dark")

    # get window size

    # button callback func
    def delete():
        my_text.delete(0.0, 'end')

    def copy():
        global thing
        thing = my_text.get(0.0, 'end')

    def paste():
        if thing:
            my_text.insert('end', thing)
        else:
            my_text.insert('end', "There is nothing to paste!!")
    def button1_callback():
        # the image capture class instance instantiation
        # the arg is the countdown time
        imageCapture = ImageCapture(1, "photos", "photo1.jpg")
        # take the photo, saves it
        imageCapture.TakePhoto()

        # load image
        os.getcwd()
        photo = ctk.CTkImage(light_image=Image.open(os.getcwd() + os.sep + 'photos/photo1.jpg'),
                             dark_image=Image.open(os.getcwd() + os.sep + 'photos/photo1.jpg'),
                             size=(600, 600))
        imageLabel.configure(image=photo)
        imageLabel.pack(pady=10)

    titleText = HeaderText(app, "Machine Learning Handwriting App")
    titleText.pack(pady=20)

    instructions = ("Welcome! This app takes a picture of handwritten text "
        "and uses optical character recognition to recognize it. "
        "Please begin by taking a photo, "
        "or you can view the results of previous uses.")
    instructionsText = SubheaderTextBox(app, instructions)
    instructionsText.pack(pady=10)

    button = SmallButton(app, "Take Photo", button1_callback)
    button.pack(pady=10) 

    # image
    imageLabel = ctk.CTkLabel(app, text="")
    imageLabel.pack(pady=10) 

    # frame for buttons
    frame = ctk.CTkFrame(app)
    frame.pack(pady=10)

    retakeButton = ctk.CTkButton(frame, text="Delete", command=delete)
    confirmButton = ctk.CTkButton(frame, text="Copy", command=copy)
    cancelButton = ctk.CTkButton(frame, text="Paste", command=paste)

    retakeButton.grid(row=0, column=0)
    confirmButton.grid(row=0, column=1, padx=10)
    cancelButton.grid(row=0, column=2) 

    # # Start the main event loop
    app.mainloop()

def HeaderText(app, text):
    return ctk.CTkLabel(
        app,
        text=text,
        width=600,
        height=100,
        text_color="#ffffff",
        fg_color="transparent",
        font=("Helvetica", 36),
	)
def SubheaderTextBox(app, text):
    textbox =  ctk.CTkTextbox(
        app,
        width=600,
        height=120,
        text_color="#ffffff",
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
        corner_radius=20,
        hover_color="#29d3db",
        font=("Helvetica", 18),
        text=text,
        command=func
    )
    

if __name__ == '__main__':
    main()