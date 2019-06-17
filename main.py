from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np
import time
from skimage import color

COLOR_FG = [300, 0, 0]
COLOR_BG = [0, 300, 0]
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]

class InteractiveWindow:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Demo")

        self.label = Label(master, text = "foreground: left/right click and drag")
        self.label.grid(row=1,columnspan=3)

        self.classify_button = Button(master, text = "Process!", command = self.process_time)
        self.close_button = Button(master, text="Close", command=master.quit)
        self.reset_button = Button(master, text="Reset", command=self.reset)
        self.classify_button.grid(row=0, column=0, sticky=E+W)
        self.reset_button.grid(row=0, column=1, sticky=E+W)
        self.close_button.grid(row=0, column=2, sticky=E+W)
        
        #specify image
        self.cv_img = cv2.imread("nemo1.jpg")
        self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2RGB)
        height, width, no_channels = self.cv_img.shape 
        
        # Store user input
        self.user_input = np.zeros([height,width,3],dtype=np.uint8)
        self.user_input.fill(0)

        # Create a canvas that can fit the above image
        self.canvas = Canvas(master, width = width, height = height )
        self.canvas.grid(row=2,columnspan=3)
        print(width, height) 
        # Bind user interaction

        self.canvas.bind("<Button-1>", self.canvas_onclick_fg)
        self.canvas.bind("<B1-Motion>", self.canvas_onclick_fg)
        
        self.canvas.bind("<Button-3>", self.canvas_onclick_bg)
        self.canvas.bind("<B3-Motion>", self.canvas_onclick_bg)

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

#### USER INTERACTION
    def canvas_onclick_fg(self, event):
        self.label.config(text= "Foreground selection at ({},{})".format(event.x, event.y) )
        
        # just overwrite pixels
        cv2.circle(self.user_input, (event.x, event.y), 3, COLOR_FG,3)
        cv2.circle(self.cv_img, (event.x, event.y), 3, COLOR_FG,3)
        
        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def canvas_onclick_bg(self, event):
        self.label.config(text= "Background selection at ({},{})".format(event.x, event.y) )
        
        # just overwrite pixels
        cv2.circle(self.user_input, (event.x, event.y), 3, COLOR_BG,3)
        cv2.circle(self.cv_img, (event.x, event.y), 3, COLOR_BG,3)

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)


    def reset(self):
        self.cv_img = self.cv_img_copy.copy() #reset display
        self.user_input.fill(0) #reset user_input

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

#### ALGORITHM
    def process_time(self):
        start = time.time()
        self.process()
        end = time.time()
        print("Elapsed time", end-start)
        
    def process(self):
        # Algorithm described in the paper
        print("process needs to be implemented")
        height, width, no_channels = self.cv_img.shape 
        label = np.zeros([height,width,3],dtype=np.uint8)
        f_vec = np.zeros([height*width,5,3])
        f_vec.fill(np.NaN)

        # Convert img to CIE-Lab space
        lab = color.rgb2lab(self.cv_img)
        # Construct feature vector I at each pixel
        right = np.roll(lab, 1, axis=1) #right
        right[:,0] = lab[:,0] #instead of irrelevant vector, add itself
        left = np.roll(lab, -1, axis=1) #left
        left[:,width-1] = lab[:,width-1]
        down = np.roll(lab, 1, axis=0) #down
        down[0,:] = lab[0,:]
        up = np.roll(lab, 1, axis=0) #up
        up[height-1,:] = lab[height-1,:]

        for i in range(height):
            for j in range(width):
                # Not sure if this is correct
                f_vec[i*width+j] = np.array([np.array(lab[i,j]), np.array(right[i,j]), np.array(left[i,j]), np.array(up[i,j]), np.array(down[i,j])])

        # Compute the delta-distance at every pixel and the weights for each of its 4-neighbor
        

        # Establish the LP formulation based on Eq.14

        # Solve the LP problem

        # Output the label as the result
        photo = ImageTk.PhotoImage(image = Image.fromarray(label))
        self.canvas.create_image(0,0, image=photo, anchor=NW)


    def lp_formulation(self):
        print("to be implemented")        

    def weight_calculation(self, f1, f2):
        a = (np.linalg.norm(f1-f2))**2
        sigma = 2.
        np.exp(np.mul)

    def idx2xy(self, idx):
        h, w, _ = self.cv_img.shape
        y = idx%w
        x = idx//w

# Execution
root = Tk()
my_gui = InteractiveWindow(root)
root.mainloop()
