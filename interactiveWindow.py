from tkinter import *
import linearAlgorithm

class InteractiveWindow:
	def __init__(self, master):
		self.master = master
		master.title("Interactive Demo")
		propogate_components()
		place_components()
		self.img =[]
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

    def place_components(self):
    	self.label.grid(row=1,columnspan=3)

        self.classify_button.grid(row=0, column=0, sticky=E+W)
        self.reset_button.grid(row=0, column=1, sticky=E+W)
        self.close_button.grid(row=0, column=2, sticky=E+W)

        place_canvas()

    def propogate_canvas(self):
    	height, width, _ = self.img.shape
        self.canvas = Canvas(master, width = width, height = height )

    def place_canvas(self):
        self.canvas.grid(row=2,columnspan=3)

    def mask(self, color):
    	#mask the result image

        print("Done!")

    def reset_scribble(self):


    def process_time(self):
        """
        Calculate the time passed to test the efficiency of the algorithm
        """
        start = time.time()
        processed = linearAlgorithm.process(self) #supply information for info
        end = time.time()
        print("Elapsed time", end-start)
        display_result(self, processed)

    def canvas_onclick_fg(self, event):
        self.label.config(text= "Foreground selection at ({},{})".format(event.x, event.y) )
        record_user_input_foreground(event)

        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def record_user_input_foreground(self, event):
        cv2.circle(self.user_input, (event.x, event.y), 2, COLOR_FG,2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLOR_FG,2)
        self.set.add((event.x, event.y,1))

    def canvas_onclick_bg(self, event):
        self.label.config(text= "Background selection at ({},{})".format(event.x, event.y) )
        # just overwrite pixels
        record_user_input_background()
        # Display on Window
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0, image=self.photo, anchor=NW)

    def record_user_input_background(self, event):
        cv2.circle(self.user_input, (event.x, event.y), 2, COLOR_BG,2)
        cv2.circle(self.cv_img, (event.x, event.y), 2, COLOR_BG,2)
        self.set.add((event.x, event.y, 0))