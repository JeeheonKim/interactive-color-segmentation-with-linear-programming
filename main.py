from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np
import time
from skimage import color
from sklearn import mixture 
from scipy.spatial.distance import mahalanobis as mahal
import gurobipy as grb

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
        self.set=set()
        
        # Create a canvas that can fit the above image
        self.canvas = Canvas(master, width = width, height = height )
        self.canvas.grid(row=2,columnspan=3)
        
        # Bind user interaction with GUI component
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
        self.set.add((event.x, event.y,1))
        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def canvas_onclick_bg(self, event):
        self.label.config(text= "Background selection at ({},{})".format(event.x, event.y) )
        
        # just overwrite pixels
        cv2.circle(self.user_input, (event.x, event.y), 2, COLOR_BG,2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLOR_BG,2)
        self.set.add((event.x, event.y, 0))
        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def reset(self):
        """ Resets scribbles of the user
        
        """
        self.cv_img = self.cv_img_copy.copy() #reset display
        self.user_input.fill(0) #reset user_input

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)
        
    def display_result(self, processed):
        # Output the label as the result
        #photo = ImageTk.PhotoImage(image = Image.fromarray(processed))
        #self.canvas.create_image(0,0, image=photo, anchor=NW)
        print("Done!")

#### ALGORITHM
    def process_time(self):
        """
        Calculate the time passed to test the efficiency of the algorithm
        """
        start = time.time()
        processed = self.process()
        end = time.time()
        print("Elapsed time", end-start)
        display_result(self, processed)

    def process(self):
        """
        process the image
        """
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

        # Solve the LP problem
        processed = self.lp_formulation(0.2, f_vec)

        return processed
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def lp_formulation(self, reg_param, f_vec):
        """
        formulates a linear programming problem mentioned in the paper
        """
        print("to be implemented")
        delta_mtx = self.compute_delta_distance(f_vec)
        #user input - vectors
        opt_model = grb.Model(name="EnergyFunction")
        # set variables for relaxed binary problem
        x_vars = {(i,j): opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
            lb = 0,
            ub = 1,
            name="x_{0}_{1}".format(i,j)) for i in range(self.cv_img.shape[0]) for j in range(self.cv_img.shape[1])}
        ## we need pixels that are colored by user input

        for a in self.set:
            # a has to be set to real numbers
            objective = grb.quicksum(x_vars[i,j]*delta_mtx[i,j] for i in range(self.cv_img.shape[0]) for j in range(self.cv_img.shape[1]))
            # NOT YET COMPLETE
            objective+= reg_param*grb.quicksum( compute_vars[i,j]*delta_mtx[i,j] for i in range(self.cv_img.shape[0]) for j in range(self.cv_img.shape[1])) 
        
        opt_model.setObjectiveN(objective)
        

        # for minimization
        opt.model.ModelSense = grb.GRB.MINIMIZE
        opt_model.optimize()

        opt_df = pd.DataFrame.from_dict(x_vars, orient="index",
                columns=["variable_object"])
        opt_df.index = pd.MultiIndex.from_tuples(opt_df.index, names=["column_i","column_j"])
        opt_df.reset_index(inplace=True)

        opt_df["solution_value"]= opt_df["variable_object"].apply(lambda item: item.x)


    def neighbour_pixels_weight_for_feature(self, f1):
        """Compute weights of a feature with four neighbouring pixel
        Receives a set of features and output weights for a set
        """

    # Weight defined in paper -- can customize the function to change weight
    def _weight_calculation(self, f1, f2):
        """
        weight of two feature vectors
        """
        a = (np.linalg.norm(f1-f2))**2
        a = -a/(2*(_sigma_calculation(f1,f2)**2))
        a = np.exp(a)
        return a

    
    def _sigma_calculation(self, f1, f2):
        2* np.mean(np.power(np.absolute(f1-f2), 2)) 
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Delta distance in paper
    def compute_delta_distance(self,x):
        gmm = mixture.GaussianMixture(n_components=GAUSS_MODE, covariance_type = 'full')
        bg_x = self.compute_usr_input(x, COLOR_BG)
        fg_x = self.compute_usr_input(x, COLOR_FG)
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
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Execution
root = Tk()
my_gui = InteractiveWindow(root)
root.mainloop()
