from tkinter import *


from tkinter import ttk

from viewfoodspage import ViewFoodsPage
from viewmealspage import ViewMealsPage
from addmealpage import AddMealPage
from addfoodspage import AddFoodsPage
from foodspricepage import FoodsPricePage
from calcdailyamounts import CalcDailyAmounts
from viewproductspage import ViewProductsPage




class StartPage(Frame):
	"""Displays main menu with options for what functionality to do."""

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		btn_add_food = ttk.Button(self, text="Add Food", command=lambda: controller.show_frame(AddFoodsPage))
		
		btn_view_foods = ttk.Button(self, text="View Foods", command=lambda: controller.show_frame(ViewFoodsPage))

		btn_add_meals = ttk.Button(self, text="Add Meal", command=lambda: controller.show_frame(AddMealPage))

		btn_view_meals = ttk.Button(self, text="View Meals", comman=lambda: controller.show_frame(ViewMealsPage))

		btn_foods_price = ttk.Button(self, text="Foods Price (beta)", command=lambda: controller.show_frame(FoodsPricePage))

		btn_calc_daily_amounts = ttk.Button(self, text="Calc Daily Amts (beta)", command=lambda: controller.show_frame(CalcDailyAmounts))

		btn_view_products = ttk.Button(self, text="View Products", command=lambda: controller.show_frame(ViewProductsPage))
		

		PADY = 5
		self.grid_columnconfigure(0, weight=1) # put buttons in center of screen
		btn_add_food.grid(row=0, column=0, pady=PADY)
		btn_view_foods.grid(row=1, column=0, pady=PADY)
		btn_add_meals.grid(row=2, column=0, pady=PADY)
		btn_view_meals.grid(row=3, column=0, pady=PADY)
		btn_foods_price.grid(row=4, column=0, pady=PADY)
		btn_calc_daily_amounts.grid(row=5, column=0, pady=PADY)
		btn_view_products.grid(row=6, column=0, pady=PADY)
		


	def reset(self):
		pass
