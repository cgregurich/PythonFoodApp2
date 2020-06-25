from tkinter import *
from tkinter import ttk

from fooditemdao import FoodItemDAO
from mealdao import MealDAO

import startpage

from utilities import *


# THIS CLASS WILL PROBABLY BE USED TO HELP WITH MEAL FUNCTIONALITY
# IT PROBABLY DOESN'T NEED TO BE A STANDALONE FEATURE OF THE APPLICATION
class CalculateMacros(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		# Padding settings
		PADY = 3

		# Create frames
		
		# frame_calc holds two other frames
		self.frame_calc = Frame(self)
		self.frame_controls = Frame(self.frame_calc)
		self.frame_info = Frame(self.frame_calc)

		# frame that holds the DisplayAllFoods frame
		self.frame_display_foods = Frame(self)

		# Put frames in window
		self.frame_controls.grid(row=0, column=0, sticky=N)
		self.frame_info.grid(row=1, column=0, sticky=NW)


		self.frame_calc.grid(row=0, column=1, sticky=N, padx=(0, 10))

		# Var for which food is selected for calculating
		self.selected_food = StringVar()

		# Create controls
		self.optionmenu_foods = ttk.OptionMenu(self.frame_controls, self.selected_food, "Select food", command=self.food_selected,
												 *fooditemdao.retrieve_all_food_names())
		self.entry_amount = ttk.Entry(self.frame_controls, justify="right")
		self.lbl_unit = Label(self.frame_controls, text="unit")

		self.btn_calc = ttk.Button(self.frame_controls, text="Calculate", command=self.calculate_clicked)


		# Tuples for labels and keys
		self.headers =  ("Name", "Serving Size", "Unit", "Calories", "Carbs", "Fat", "Protein", "Fiber", "Sugar")
		self.info_tags = ("name", "ss", "unit", "cal", "carb", "fat", "protein", "fiber", "sugar")
		
		# Create info labels
		self.header_labels = []
		self.info_labels = []
		for i in range(len(self.headers)):
			lbl = Label(self.frame_info, text=f"{self.headers[i]}:", font=ADD_FONT, anchor=W)
			lbl.grid(row=i, column=0, sticky=E, pady=PADY)
			self.header_labels.append(lbl)
			lbl2 = Label(self.frame_info, font=MONOSPACED_FONT)
			lbl2.grid(row=i, column=1, pady=PADY)
			self.info_labels.append(lbl2)



		# Put controls on the screen
		self.optionmenu_foods.grid(column=0, row=1)
		self.entry_amount.grid(column=0, row=2)
		self.lbl_unit.grid(column=1, row=2, padx=3)
		self.btn_calc.grid(column=0, row=3)


	def food_selected(self, arg):
		"""Command for when a food is selected.
		This sets the unit label to the selected food's unit"""
		food = fooditemdao.retrieve_food(self.selected_food.get())
		self.lbl_unit.config(text=food.info['unit'])

	def calculate_clicked(self):
		"""Retrieves the appropriate food from the DB
		Validates form and info
		Fills the info labels with the proportionalized info"""
		food = fooditemdao.retrieve_food(self.selected_food.get())

		if not self._is_form_filled_out():
			return False


		if not self._is_amount_valid():
			return False

		for i in range(len(self.headers)):
			food.proportionalize(float(self.entry_amount.get()))
			self.info_labels[i].config(text=food.info[self.info_tags[i]])


	def _is_form_filled_out(self):
		"""Returns False if amount entry is blank and a food has not been selected
		Otherwise returns True"""
		if self.entry_amount.get() == "":
			return False

		if self.selected_food.get() == "Select food":
			return False

		return True

	def _is_amount_valid(self):
		"""Checks if the info in the amount entry is a valid, positive number
		Displays an error and returns False if not
		Otherwise returns True"""
		amount = self.entry_amount.get()

		try:
			float(amount)
		except ValueError:
			messagebox.showerror("Invalid Amount", "Amount must be a positive number")
			return False

		if float(amount) < 0:
			messagebox.showerror("Invalid Amount", "Amount must be a positive number")
			return False
		else:
			return True



	def reset(self):
		pass