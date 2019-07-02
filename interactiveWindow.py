from tkinter import *

class InteractiveWindow:
	def __init__(self, master):
		self.master = master
		master.title("Interactive Demo")
		propogate_components()
		place_components()
		self.img =[]
		self.img2array("nemo.jpg")
 		self.user_input = np.zeros([height,width,3],dtype=np.uint8)
        self.set=set()

	def img2array(self, img):
		input_img = cv2.imread(img)
        self.img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

	def propogate_components(self):
		self.label = Label(master, text = "(Instruction) left/right click and drag")

		self.classify_button = Button(master, text = "Process!", command = self.process_time)
        self.close_button = Button(master, text="Close", command=master.quit)
        self.reset_button = Button(master, text="Reset", command=self.reset)

        propogate_canvas()


    def place_components(self):
    	self.label.grid(row=1,columnspan=3)

        self.classify_button.grid(row=0, column=0, sticky=E+W)
        self.reset_button.grid(row=0, column=1, sticky=E+W)
        self.close_button.grid(row=0, column=2, sticky=E+W)

        place_canvas()

    def mask(self):
        # Output the label as the result
        #photo = ImageTk.PhotoImage(image = Image.fromarray(processed))
        #self.canvas.create_image(0,0, image=photo, anchor=NW)
        print("Done!")

    def propogate_canvas(self):
    	height, width, _ = self.img.shape
        self.canvas = Canvas(master, width = width, height = height )

    def place_canvas(self):
        self.canvas.grid(row=2,columnspan=3)

    def initialize_user_variables(self):
