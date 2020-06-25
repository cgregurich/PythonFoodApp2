from tkinter import *
from tkinter import ttk

from utilities import *

import startpage




class FoodsPricePage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		ttk.Button(self, text="Back", command=lambda: controller.show_frame(startpage.StartPage)).grid(row=0, column=0)

		ttk.Button(self, text="Run it", command=self.run_it_clicked).grid(row=0, column=1)

		Label(self, text="$/Unit").grid(row=1, column=1)
		Label(self, text="Amt/Unit").grid(row=1, column=2)

		self.food_options = fooditemdao.retrieve_all_food_names()
		self.selected_food = StringVar()
		self.optionmenu_foodnames = ttk.OptionMenu(self, self.selected_food, "Select Food", command=self.food_selected, *self.food_options)
		self.entry_price = ttk.Entry(self)
		self.entry_amount = ttk.Entry(self)
		self.lbl_unit = Label(self, text="unit")
		self.lbl_cals_per_dol = Label(self, text="----")



		self.optionmenu_foodnames.grid(row=2, column=0)
		self.entry_price.grid(row=2, column=1)
		self.entry_amount.grid(row=2, column=2)
		self.lbl_unit.grid(row=2, column=3)
		self.lbl_cals_per_dol.grid(row=2, column=4)

	def food_selected(self, arg):
		food = fooditemdao.retrieve_food(self.selected_food.get())
		self.lbl_unit.config(text=food.unit)

	def run_it_clicked(self):
		
		self._calc_cals_per_dol()
		# Obv assuming input is valid; need to validate
		

	def _calc_cals_per_dol(self):
		foodname = self.selected_food.get()
		food = fooditemdao.retrieve_food(foodname)
		price = float(self.entry_price.get())
		amount = int(self.entry_amount.get())

		num = ((amount / food.ss) * food.cal) / price
		self.lbl_cals_per_dol.config(text=num)


	def _refresh_food_options(self):
		self.food_options = fooditemdao.retrieve_all_food_names()
		self.optionmenu_foodnames.destroy()
		self.optionmenu_foodnames = ttk.OptionMenu(self, self.selected_food, "Select Food", *self.food_options)
		self.optionmenu_foodnames.grid(row=2, column=0)

	def _clear_form(self):
		self.entry_price.delete(0, END)
		self.entry_amount.delete(0, END)
		self.lbl_unit.config(text="unit")
		self.lbl_cals_per_dol.config(text="----")


	def reset(self):
		self._refresh_food_options()
		self._clear_form()