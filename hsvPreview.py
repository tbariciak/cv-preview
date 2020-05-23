import cv2
import tkinter as tk
import numpy as np
import PIL.Image
import PIL.ImageTk
import imutils
import argparse
import subprocess

class HSVPreview():
    def __init__(self, window, inputImage):
        """
        Configures the Tkinter GUI layout and saves optional preprocessors

        Parameters:
            master: Tkinter main window
            inputImage: Image to be displayed
        """
        self.image = inputImage

        # Define UI colours
        self.white = "#ffffff"
        self.gray = "#282c34"

        # Configure main window
        self.root = window
        self.root.configure(background=self.gray)
        self.root.title("HSV Calibration Util")

        # The left frame is used for the HSV sliders while the right frame
        # displays the original image along with a live preview of the
        # thresholding operation
        self.leftFrame = tk.Frame(self.root, bg=self.gray)
        self.rightFrame = tk.Frame(self.root, bg=self.gray)
        self.rightUpperFrame = tk.Frame(self.rightFrame, bg=self.gray)
        self.rightLowerFrame = tk.Frame(self.rightFrame, bg=self.gray)

        # Each HSV slider and corresponding label is contained within its own
        # frame for simplified packing
        self.sliderFrame1 = tk.Frame(self.leftFrame, bg=self.gray)
        self.sliderFrame2 = tk.Frame(self.leftFrame, bg=self.gray)
        self.sliderFrame3 = tk.Frame(self.leftFrame, bg=self.gray)
        self.sliderFrame4 = tk.Frame(self.leftFrame, bg=self.gray)
        self.sliderFrame5 = tk.Frame(self.leftFrame, bg=self.gray)
        self.sliderFrame6 = tk.Frame(self.leftFrame, bg=self.gray)

        # Window labels
        self.hsvTitleLabel = tk.Label(self.leftFrame, text="HSV Ranges",
            bg=self.gray, fg=self.white, font=("Calibri Bold", 25))
        self.hsvLowerLabel = tk.Label(self.leftFrame, text="Lower",
            bg=self.gray, fg=self.white, font=("Calibri Light", 22))
        self.hsvUpperLabel = tk.Label(self.leftFrame, text="Upper",
            bg=self.gray, fg=self.white, font=("Calibri Light", 22))

        # Slider labels
        self.sliderLabel1 = tk.Label(self.sliderFrame1, text="H", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))
        self.sliderLabel2 = tk.Label(self.sliderFrame2, text="S", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))
        self.sliderLabel3 = tk.Label(self.sliderFrame3, text="V", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))
        self.sliderLabel4 = tk.Label(self.sliderFrame4, text="H", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))
        self.sliderLabel5 = tk.Label(self.sliderFrame5, text="S", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))
        self.sliderLabel6 = tk.Label(self.sliderFrame6, text="V", bg=self.gray,
            fg=self.white, font=("Calibri Light", 18))

        # HSV Sliders
        self.slider1 = tk.Scale(self.sliderFrame1, from_=0, to=180,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)
        self.slider2 = tk.Scale(self.sliderFrame2, from_=0, to=255,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)
        self.slider3 = tk.Scale(self.sliderFrame3, from_=0, to=255,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)
        self.slider4 = tk.Scale(self.sliderFrame4, from_=0, to=180,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)
        self.slider5 = tk.Scale(self.sliderFrame5, from_=0, to=255,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)
        self.slider6 = tk.Scale(self.sliderFrame6, from_=0, to=255,
            orient='horizontal', bg=self.gray, activebackground=self.gray,
            fg=self.white, highlightbackground=self.gray,
            highlightcolor=self.white, length=350, font=("Calibri Light", 14),
            command=self.updateValues)

        # Button to generate Python code
        self.generateButton = tk.Button(self.leftFrame, text="Generate Code",
            command=self.generateCode, bg=self.gray, fg=self.white,
            activebackground=self.gray, activeforeground=self.gray,
            highlightbackground=self.gray, highlightcolor=self.white,
            font=("Calibri Light", 16))

        # Canvas elements are used to display preview images
        h, w = self.image.shape[:2]
        rH = 400 / h
        canvasWidth = w * rH
        self.upperImageCanvas = tk.Canvas(self.rightUpperFrame,
            width=canvasWidth, height=400, bg=self.gray)
        self.lowerImageCanvas = tk.Canvas(self.rightLowerFrame,
            width=canvasWidth, height=400, bg=self.gray)

        # All Frames
        self.leftFrame.pack(side=tk.LEFT)
        self.rightFrame.pack(side=tk.RIGHT)
        self.rightUpperFrame.pack(side=tk.TOP)
        self.rightLowerFrame.pack(side=tk.BOTTOM)

        # Left Frame
        self.hsvTitleLabel.pack(pady=10)
        self.hsvUpperLabel.pack(pady=(10, 0))

        # Upper Hue Frame
        self.sliderFrame1.pack(padx=10)
        self.sliderLabel1.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider1.pack(side=tk.LEFT)

        # Upper Saturation Frame
        self.sliderFrame2.pack(padx=10)
        self.sliderLabel2.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider2.pack(side=tk.LEFT)

        # Upper Value Frame
        self.sliderFrame3.pack(padx=10)
        self.sliderLabel3.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider3.pack(side=tk.LEFT)
        self.hsvLowerLabel.pack(pady=(10, 0))

        # Lower Hue Frame
        self.sliderFrame4.pack(padx=10)
        self.sliderLabel4.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider4.pack(side=tk.LEFT)

        # Lower Saturation Frame
        self.sliderFrame5.pack(padx=10)
        self.sliderLabel5.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider5.pack(side=tk.LEFT)

        # Lower Value Frame
        self.sliderFrame6.pack(padx=10)
        self.sliderLabel6.pack(side=tk.LEFT, pady=(20, 0), padx=5)
        self.slider6.pack(side=tk.LEFT)
        self.generateButton.pack()

        # Right Upper Frame
        self.upperImageCanvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.lowerImageCanvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Initialize list for slider positions
        self.sliderPos = [0, 0, 0, 0, 0, 0]

        # Specify closing protocol?

        # Push original image to canvas
        inputImage = imutils.resize(inputImage, height=400)
        inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
        self.root.image = image = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(inputImage))
        self.lowerImageCanvas.create_image(0, 0, image=image, anchor=tk.NW)
        self.updateImages()

    def updateValues(self, event):
        """
        Updates the slider positions (triggered by change in slider value)

        Parameters:
            event: Triggering event (unused)
        """
        self.sliderPos = [
            self.slider1.get(),
            self.slider2.get(),
            self.slider3.get(),
            self.slider4.get(),
            self.slider5.get(),
            self.slider6.get()
        ]
        self.updateImages()

    def updateImages(self):
        """
        Applies the thresholding operation and updates the image preview
        """
        # Convert image to HSV colour space and apply mask
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        hsvMask = cv2.inRange(hsv, np.array(self.sliderPos[3:]),
            np.array(self.sliderPos[:3]))

        # Push image to canvas
        hsvMask = imutils.resize(hsvMask, height=400)
        self.root.hsvImage = image = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(hsvMask))
        self.upperImageCanvas.create_image(0, 0, image=image, anchor=tk.NW)

    def generateCode(self):
        """
        Generates OpenCV Python code and copies it to the active clipboard
        """
        code = "\n".join((
            "__VAR__ = cv2.cvtColor(__IMAGE__, cv2.COLOR_BGR2HSV)",
            "__VAR__ = cv2.inRange(__VAR__, {0}, {1})"
            .format(tuple(self.sliderPos[3:]), tuple(self.sliderPos[:3]))
        ))

        # copy the code to the clipboard
        subprocess.check_call("echo '{}' | pbcopy".format(code), shell=True)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="Path to input image")
args = vars(parser.parse_args())

# Create main window and start preview
root = tk.Tk()
image = cv2.imread(args["image"], cv2.COLOR_BGR2RGB)
HSVPreview(root, image)
root.mainloop()
