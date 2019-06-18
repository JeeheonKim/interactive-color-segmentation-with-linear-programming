from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np
import time
from skimage import color
from sklearn import mixture 
from scipy.spatial.distance import mahalanobis as mahal

COLOR_FG = [255, 0, 0]
COLOR_BG = [0, 255, 0]
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]
GAUSS_MODE = 5

class InteractiveWindow:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Demo")

        self.label = Label(master, text = "(Instruction) left/right click and drag")
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
        self.cv_img_copy = self.cv_img.copy()

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
        cv2.circle(self.user_input, (event.x, event.y), 2, COLOR_FG,2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLOR_FG,2)
        
        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def canvas_onclick_bg(self, event):
        self.label.config(text= "Background selection at ({},{})".format(event.x, event.y) )
        
        # just overwrite pixels
        cv2.circle(self.user_input, (event.x, event.y), 2, COLOR_BG,2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLOR_BG,2)

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)


    def reset(self):
        self.cv_img = self.cv_img_copy.copy() #reset display
        self.user_input.fill(0) #reset user_input

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)
        
    def display_result(self, processed):
        # Output the label as the result
        photo = ImageTk.PhotoImage(image = Image.fromarray(processed))
        self.canvas.create_image(0,0, image=photo, anchor=NW)


#### ALGORITHM
    def process_time(self):
        start = time.time()
        processed = self.process()
        end = time.time()
        print("Elapsed time", end-start)
        display_result(self, processed)

    def process(self):

        # Algorithm described in the paper
        print("process needs to be implemented")
        height, width, no_channels = self.cv_img.shape 
        label = np.zeros([height,width,3],dtype=np.uint8)
        f_vec = np.zeros([height,width,15])
        f_vec.fill(np.NaN)

        # Convert img to CIE-Lab space
        lab = color.rgb2lab(self.cv_img)

        # Construct feature vector I at each pixel
        right = np.roll(lab, 1, axis=1) #right shift
        right[:,0] = lab[:,0] #instead of irrelevant vector, add itself
        left = np.roll(lab, -1, axis=1) 
        left[:,width-1] = lab[:,width-1]
        down = np.roll(lab, 1, axis=0) 
        down[0,:] = lab[0,:]
        up = np.roll(lab, -1, axis=0) 
        up[height-1,:] = lab[height-1,:]

        for i in range(height):
            for j in range(width):
                # Not sure if this is correct
                tmp = np.concatenate((lab[i,j], right[i,j], left[i,j]))
                tmp = np.concatenate((tmp, up[i,j], down[i,j]))
                f_vec[i,j] = tmp
                
        # Compute the delta-distance 
        dist = self.compute_delta_distance(f_vec) 
        print("Look at this to see if the calculation is reasonable")
        print(dist.shape)
        # Establish the LP formulation based on Eq.14

        # Solve the LP problem
        processed = self.lp_formulation(0.2, f_vec)

        return processed

    def lp_formulation(self, reg_param, f_vec):
        print("to be implemented")
        delta_mtx = self.compute_delta_distance(f_vec)
        #user input - vectors





    def weight_calculation(self, f1, f2):
        a = (np.linalg.norm(f1-f2))**2
        a = -a/(2*(sigma_calculation(f1,f2)**2))
        a = np.exp(a)
        return a

    def sigma_calculation(self, f1, f2):
        2* np.mean(np.power(np.absolute(f1-f2), 2)) 


    def idx2xy(self, idx):
        h, w, _ = self.cv_img.shape
        y = idx%w
        x = idx//w

    def compute_delta_distance(self,x):
        gmm = mixture.GaussianMixture(n_components=GAUSS_MODE, covariance_type = 'full')
        bg_x = self.compute_vec(x, COLOR_BG)
        fg_x = self.compute_vec(x, COLOR_FG)
        gmm = gmm.fit(bg_x)
        bg_means = gmm.means_
        bg_cov = gmm.covariances_
        
        gmm = mixture.GaussianMixture(n_components=GAUSS_MODE, covariance_type = 'full')
        gmm = gmm.fit(fg_x)
        fg_means = gmm.means_
        fg_cov = gmm.covariances_
        
        fg_dist = 0
        bg_dist = 0
        h, w, _ = self.cv_img.shape
        dist = np.zeros([h, w])
        for i in range(h):
            for j in range(w):
                b = np.min([mahal(x[i,j], bg_means[p], bg_cov[p]) for p in range(5)])
                f = np.min([mahal(x[i,j], fg_means[p], fg_cov[p]) for p in range(5)])
                dist[i,j] = b-f 
        return dist

    def compute_vec(self, x, color):
        height, width, no_channels = self.cv_img.shape 
        result = np.NaN
        for i in range(height):
            for j in range(width):
                if (self.user_input[i,j][0] ==  color[0] and self.user_input[i,j][1] == color[1] and self.user_input[i,j][2] == color[2]):
                    if np.isnan(result).all():
                        #print("currently result is  NaN------")
                        #print(i,j)
                        #print("printing x[i,j]...")
                        #print(x[i,j])
                        result = np.array([x[i,j]])
                    else:
                        #print("----------------")
                        #print(result)
                        #print("printing x[i,j]...")
                        #print(x[i,j])
                        result = np.append(np.array(result), np.array([x[i,j]]), axis=0)
        print("result is--- this should contains arrays that have user interacted arraays")
        print(result)
        return result

# Execution
root = Tk()
my_gui = InteractiveWindow(root)
root.mainloop()
