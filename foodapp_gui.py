from tkinter import *
from tkinter import messagebox

from tkinter.font import Font
from tkinter import ttk

from fooditemdao import FoodItemDAO
from fooditem import FoodItem
from mealdao import MealDAO
from meal import Meal


# Testing splitting up classes into different files

from startpage import StartPage
from viewmealspage import ViewMealsPage
from addfoodspage import AddFoodsPage
from viewfoodspage import ViewFoodsPage
from addmealpage import AddMealPage
from displaydaily import DisplayDaily
from foodspricepage import FoodsPricePage
from calcdailyamounts import CalcDailyAmounts









class FoodApp(Tk):

	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)


		self.title("Booter Food")

		self.iconbitmap("bootericon.ico")

		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}


		# MEAL FRAME IS FOR TESTING
		for F in (StartPage, ViewMealsPage, AddFoodsPage, ViewFoodsPage, AddMealPage,
					DisplayDaily, FoodsPricePage, CalcDailyAmounts):
			
			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)


	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.reset()
		frame.tkraise()


app = FoodApp()
app.mainloop()