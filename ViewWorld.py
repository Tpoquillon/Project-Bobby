import tkinter as tk
import time
class CreateWorld(tk.Canvas):
	def __init__(self):
		self.window = tk.Tk() #Creating a window
		self.window.title("Fantastic Bobby")
		self.frame = tk.Frame(master=self.window, width=1000, height=800, bg='blue')
		self.frame.pack(expand=tk.YES)
		self.mycanvas = tk.Canvas.__init__(self, width = 1915, height = 1000, highlightthickness=0 ,bg="green")
		self.bind("<Configure>", self.on_resize)
		self.height = self.winfo_reqheight()
		self.width = self.winfo_reqwidth()
				
	def on_resize(self,event):
		# determine the ratio of old width/height to new width/height
		wscale = float(event.width)/self.width
		hscale = float(event.height)/self.height
		self.width = event.width
		self.height = event.height
		# resize the canvas 
		self.config(width=self.width, height=self.height)
		# rescale all the objects tagged with the "all" tag
		self.scale("all",0,0,wscale,hscale)
	
	def draw_grid(self, Grid):
		self.w = len(Grid[0])
		self.h = len(Grid)
		self.pixels_height = int(self.height)/self.h
		self.pixels_width = int(self.width)/self.w
		for i in range(self.h):
		    for j in range(self.w):
		        if (Grid[i][j]==0):
		            self.create_rectangle(j*self.pixels_width,i*self.pixels_height, (j+1)*self.pixels_width,(i+1)*self.pixels_height,fill="blue", width=0)
		        elif (Grid[i][j]==2):
		            #imglabel = tk.Label(image=self.img)
		            self.create_rectangle(j*self.pixels_width,i*self.pixels_height, (j+1)*self.pixels_width,(i+1)*self.pixels_height,fill="blue", width=0)
		            self.create_oval(j*self.pixels_width,i*self.pixels_height, (j+1)*self.pixels_width,(i+1)*self.pixels_height,fill="cyan")
		            self.create_oval((0.5+j)*self.pixels_width,(i+0.2)*self.pixels_height, (j+1-0.2)*self.pixels_width,(i+1-0.4)*self.pixels_height,fill="white")
		            self.create_oval((0.65+j)*self.pixels_width,(i+0.3)*self.pixels_height, (j+1-0.25)*self.pixels_width,(i+1-0.6)*self.pixels_height,fill="black")