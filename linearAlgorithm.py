class LinearAlgorithm:
	def __init__(self):
		#do nothing
		
	@staticmethod
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
        a = (np.linalg.norm(f1-f2))**2
        a = -a/(2*(_sigma_calculation(f1,f2)**2))
        a = np.exp(a)
        return a

    
    def _sigma_calculation(self, f1, f2):
        2* np.mean(np.power(np.absolute(f1-f2), 2)) 


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