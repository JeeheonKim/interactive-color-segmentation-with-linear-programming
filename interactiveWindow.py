from tkinter import *
import linearAlgorithm

class InteractiveWindow:
	COLORS = [(255,0,0), (0,255,0)]

	def __init__(self, master):
		self.master = master
		master.title("Interactive Demo")
		propogate_components()
		place_components()
		self.rawimg2array("nemo01.jpg")
 		self.user_input = np.zeros([height,width,3],dtype=np.uint8)
        self.set=set()


	def rawimg2array(self, img):
		input_img = cv2.imread(img)
        self.img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

	def propogate_components(self):
		self.label = Label(master, text = "(Instruction) left/right click and drag")

		self.classify_button = Button(master, text = "Process!", command = self.process_time)
        self.close_button = Button(master, text="Close", command=master.quit)
        self.reset_button = Button(master, text="Reset", command=self.reset)

        propogate_canvas()

        self.canvas.bind("<Button-1>", self.canvas_onclick_fg)
        self.canvas.bind("<B1-Motion>", self.canvas_onclick_fg)
        self.canvas.bind("<Button-3>", self.canvas_onclick_bg)
        self.canvas.bind("<B3-Motion>", self.canvas_onclick_bg)

    def propogate_canvas(self):
    	height, width, _ = self.img.shape
        self.canvas = Canvas(master, width = width, height = height )

    def place_components(self):
    	self.label.grid(row=1,columnspan=3)

        self.classify_button.grid(row=0, column=0, sticky=E+W)
        self.reset_button.grid(row=0, column=1, sticky=E+W)
        self.close_button.grid(row=0, column=2, sticky=E+W)

        place_canvas()

    def place_canvas(self):
        self.canvas.grid(row=2,columnspan=3)

    def mask(self, color_number):
    	#mask the result image

        print("Done!")

    def reset_scribble(self):
        self.cv_img = self.cv_img_copy.copy()
        self.user_input.fill(0) #reset user_input

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)
        

    def process_time(self):
        """
        Calculate the time passed to test the efficiency of the algorithm
        """
        start = time.time()
        processed = LinearAlgorithm.process(self) #supply information for info
        end = time.time()
        print("Elapsed time", end-start)
        display_result(self, processed)

    # REMOVING FLAGS ARE BETTER BUT STILL
    def canvas_onclick(self, event, color_number):
        self.label.config(text= "Color {} selection at ({},{})".format(color_number, event.x, event.y) )
        record_scribble(event, color_number)

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def record_scribble(self, event, color_number):
    	#only tags are different
        cv2.circle(self.user_input, (event.x, event.y), 2, COLORS[color_number],2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLORS[color_number],2)
        #self.set.add((event.x, event.y,1)) -- better to put this after done
