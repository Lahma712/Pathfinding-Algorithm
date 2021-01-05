import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time
from Grid import Grid
from Algorithm import Cells, drawCell, drawFrame, drawPath
import os
import PIL
import getpass
import math
import random
host = getpass.getuser()
kivy.require("2.0.0")



class Drw(Widget):
	Width = int(input("\n\nWindow width (in pixels): "))
	Height = int(input("\nWindow height (in pixels): "))
	GCostMult = int(input("\nG Cost Multiplier; "))
	HCostMult = int(input("\nH Cost Multiplier: "))
	time.sleep(1)
	Window.size = (Width, Height)
	GWidth = int(Width) 
	GHeight = int(Height * 0.9) #grid height is a little bit shorter than the full window size because of the buttons 
	Obstacle = [] #holds current live cells of the frame in form of columns/rows. 2D list e.g [[0,0], [4,5], .... , [column, row]]
	Start = [5,5]
	End = [10,10]
	Parent = Start
	StartCheck = True
	source = r"C:\Users\{}\Desktop\Grid.png".format(host)
	EndCheck = True
	def __init__(self,**kwargs):
		super(Drw, self).__init__(**kwargs)
		self.CellCount = 50
		with self.canvas:
			self.check = False
			self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
			self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
			drawCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], (255,0,0), r"C:\Users\{}\Desktop\Grid.png".format(host))
			drawCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], (0,255,0) , r"C:\Users\{}\Desktop\Grid.png".format(host))


			self.bg = Image(source= r"C:\Users\{}\Desktop\Grid.png".format(host), pos=(0, self.Height * 0.1), size = (self.GWidth, self.GHeight))
            
			self.add = Button(text = "zoom out", font_size =self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos = (0, 0))
			self.sub = Button(text="zoom in", font_size=self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 0.75*self.Width, 0))
            
			self.add.bind(on_press= self.AddClock)
			self.add.bind(on_release = self.AddClockCancel)
			self.sub.bind(on_press = self.SubClock)
			self.sub.bind(on_release = self.SubClockCancel)
			self.add_widget(self.sub)
			self.add_widget(self.add)

			self.start = Button(text="start", font_size=self.Height*0.05, size = (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 0.50*self.Width, 0))
			self.start.bind(on_press = self.StartClock)
			self.add_widget(self.start)

			self.clear = Button(text="clear", font_size=self.Height*0.05, size = (self.Width *0.25, self.Height*0.10), pos =(self.Width - 0.25*self.Width, 0))
			self.clear.bind(on_press = self.Clear)
			self.add_widget(self.clear)





	def Add(self, instance):

		self.CellCount += 1
		self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight) #new grid dataset is made when zoomed out
		self.Cells = Cells(self.Grids[0], self.Grids[1]) #new cell dataset is made when zoomed out 
		drawCell(self.Cells[0][self.Start[0]],self.Cells[1][self.Start[1]], (255,0,0), r"C:\Users\{}\Desktop\Grid.png".format(host))
		drawCell(self.Cells[0][self.End[0]],self.Cells[1][self.End[1]], (0,255,0) , r"C:\Users\{}\Desktop\Grid.png".format(host))
		with self.canvas:
			self.bg.reload()

	def Sub(self, instance):
		self.CellCount -= 1
		self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight)#new grid dataset is made when zoomed in
		self.Cells = Cells(self.Grids[0], self.Grids[1])#new cell dataset is made when zoomed in
		drawCell(self.Cells[0][self.Start[0]],self.Cells[1][self.Start[1]], (255,0,0), r"C:\Users\{}\Desktop\Grid.png".format(host))
		drawCell(self.Cells[0][self.End[0]],self.Cells[1][self.End[1]], (0,255,0) , r"C:\Users\{}\Desktop\Grid.png".format(host))
		with self.canvas:
			self.bg.reload()

	def AddClock(self, instance):
		self.event = Clock.schedule_interval(self.Add, 0.01) #starts clock to continually zoom out
		self.event()

	def AddClockCancel(self, instance):
		self.event.cancel() #cancels clock when you release the button
    
	def SubClock(self, instance):
		self.event = Clock.schedule_interval(self.Sub, 0.01)#starts clock to continually zoom in
		self.event()

	
	def SubClockCancel(self, instance):
		self.event.cancel()#cancels clock when you release the button


	def StartClock(self, instance):

		if self.check == True:
			self.Startevent.cancel()
			self.check = False
			return
        
		else:
			
			self.Open = {}
			self.Explored = {}
			self.Startevent = Clock.schedule_interval(self.StartFrame, 0.01)
			self.check = True
			self.Startevent()

	def StartFrame(self, instance): 

		self.Frame = drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.Cells, self.Obstacle, self.Start, self.End, self.Parent, self.Open, self.Explored, self.GCostMult, self.HCostMult) #creates cells
		self.Parent = list(self.Frame[0])
		
		with self.canvas:
			self.bg.reload()

		if self.Parent == self.End:
			drawCell(self.Cells[0][self.End[0]],self.Cells[1][self.End[1]], (0,255,0), r"C:\Users\{}\Desktop\Grid.png".format(host))
			
			while self.Parent != self.Start:
				self.Parent = drawPath(r"C:\Users\{}\Desktop\Grid.png".format(host), self.Cells, self.Explored, self.Parent)
				self.check = False
			with self.canvas:
				self.bg.reload()
			
			self.Startevent.cancel()
		return

	def Clear(self, instance):
		self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
		self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
		drawCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], (255,0,0), r"C:\Users\{}\Desktop\Grid.png".format(host))
		drawCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], (0,255,0) , r"C:\Users\{}\Desktop\Grid.png".format(host))
		self.Obstacle = []
		self.Open = {}
		self.Explored = {}
		self.Parent = self.Start

		with self.canvas:
			self.bg.reload()
		return


	def Draw(self, instance, X):
		self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
		self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0] #finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
		self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse

		
		if self.Start == [] or self.End == []:
			if self.Start == []:
				self.Start = self.cellIndexList
				self.color = (255,0,0)
				self.StartCheck = True
				self.Parent = self.cellIndexList

			if self.End == []:
				self.End = self.cellIndexList
				self.color = (0,255,0)
				self.EndCheck = True



		elif self.checkSingleClick == True and (self.cellIndexList == self.Start or self.cellIndexList == self.End):
			if self.cellIndexList == self.Start:
				self.color = (200, 200,200)
				self.Start = []
				
				self.StartCheck = False

			if self.cellIndexList == self.End:
				
				self.color = (200, 200 ,200)
				self.End = []
				self.EndCheck = False


		elif self.cellIndexList not in self.Obstacle: #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to CurrentCells and the cell gets colored
			self.Obstacle.append(self.cellIndexList)
			
			self.color = (0,0,0)
		elif self.checkSingleClick == True and self.cellIndexList in self.Obstacle: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
			self.Obstacle.remove(self.cellIndexList)
			self.color = (200, 200, 200)

		drawCell(self.XcellList,self.YcellList, self.color, r"C:\Users\{}\Desktop\Grid.png".format(host)) #function that draws (or erases, based on the previous conditions) the cell you clicked
		with self.canvas:
			self.bg.reload()
		
        

	def onTouchFunctions(self, touch):
		self.touchpos = touch.pos #tuple that contains the X/Y coords of your mouse click
		self.Xtouch = math.floor(self.touchpos[0]) #rounds the coords down
		self.Ytouch = math.floor(abs(self.touchpos[1]-self.Height)) #inverts the Y coord. In kivy the origin (0,0) is bottom left, in PIL it is top left
		try: 
			self.Draw(self, 0) 
			super(Drw, self).on_touch_down(touch) 

		except(IndexError): #if you press exactly on a grid pixel (in between 2 cells), you would get an Index error. In that case, just move your mouseclick 1 pixel up and left
			try:
				self.Draw(self, -1)
				super(Drw, self).on_touch_down(touch) 
			except(IndexError): #if you press on a grid pixel at the border of the window, just do nothing
				super(Drw, self).on_touch_down(touch)

	def on_touch_down(self, touch): #function if you only click once
		self.checkSingleClick = True
		self.onTouchFunctions(touch)

	def on_touch_move(self, touch): #function if you click once and then start moving (with button still pressed). Is used for drawing lines
		if (self.StartCheck and self.EndCheck) == True:
			self.checkSingleClick = False
			self.onTouchFunctions(touch)


class AStar(App):
	def build(self):
		return Drw()

if __name__ == "__main__":
	AStar().run()
	os.remove(r"C:\Users\{}\Desktop\Grid.png".format(host)) 