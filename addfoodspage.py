from tkinter import *
from tkinter import ttk

from fooditemdao import FoodItemDAO

import startpage

from utilities import *


class AddFoodsPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(startpage.StartPage))
		btn_back.grid(row=0, column=0)

		self.entries = self._create_form()
		self.error_labels = []

	def _create_form(self):
		prompts = ["Name", "Serving Size", "Unit", "Calories", "Carbs", "Fat", "Protein", "Fiber", "Sugar"]
		prompt_row = 1
		entry_dict = {}
		for p in prompts:
			Label(self, text=p, font=ADD_FONT, anchor="e").grid(row=prompt_row, column=0, sticky=E)
			entry = ttk.Entry(self)
			entry_dict[p] = entry
			entry.grid(row=prompt_row, column=1)
			prompt_row += 1

		btn_clear = ttk.Button(self, text="Clear", command=self.clear_form)
		btn_clear.grid(row=0, column=2)

		btn_add = ttk.Button(self, text="Add", command=self.add_food)
		btn_add.grid(row=prompt_row, column=2)
		return entry_dict


	def clear_form(self):
		"""Deletes info from each entry on the page
		and clears all error labels"""
		for entry in self.entries.values():
			entry.delete(0,END)
		self._clear_error_labels()

	def _clear_error_labels(self):
		"""Sets all error labels to empty.
		Empties self.error_labels"""
		for label in self.error_labels:
			label.config(text="")
		self.error_labels = []


	def add_food(self):
		self._clear_error_labels()

		food = FoodItem()
		self.create_info_tuple()
		if self.validate_form():
			food_info_list = []
			for e in self.entries.values():
				food_info_list.append(e.get())
			food.set_info_from_string_list(food_info_list)
			fooditemdao.insert_food(food)
			status_lbl = Label(self, text="Food added")
			status_lbl.grid(row=0, column=1)
			self.error_labels.append(status_lbl)

	def validate_form(self):
		"""
		Checks if the name already exists in the database and
		if all number entries are valid numbers
		Returns True if unique name and valid info for number entries.
		Returns False if info is invalid.
		"""
		
		if not self._is_form_complete():
			return False

		is_valid = True
		is_valids = []

		for prompt, entry in self.entries.items():
			if prompt != "Name" and prompt != "Unit": # i.e should be a number
				is_valid = self._is_valid_number_label(entry.get(), prompt)
			is_valids.append(is_valid)
		
					
		return not False in is_valids

	def _is_form_complete(self):
		"""Checks that each entry has information in it.
		If any are empty, error message is displayed and False is returned.
		Otherwise returns True."""
		lbl = Label(self, text="", font=ERROR_FONT, fg="red")
		for entry in self.entries.values():
			info = entry.get()
			if info == "":
				lbl.config(text="Fill out all lines")
				lbl.grid(row=0, column=1)
				self.error_labels.append(lbl)
				return False
		return True


	

	def _is_valid_number_label(self, info, prompt):
		"""Checks arg info for validity as a number.
		Displays error label next to invalid lines.
		Checks for invalid numbers (eg. 38g).
		and Checks for negative numbers (eg -9).
		Returns True if valid.
		This func checks only one line, passed as arg. 
		Lines are looped through in parent function."""
		lbl = Label(self, text="", font=ERROR_FONT, fg="red")
		self.error_labels.append(lbl)

		try:
			info = float(info)
		except:
			lbl.config(text="Invalid number format")
			w_row = self.entries[prompt].grid_info()['row']
			w_col = self.entries[prompt].grid_info()['column']
			lbl.grid(row=w_row, column=w_col+1)
			return False

		if info < 0:
			lbl.config(text="Number can't be negative")
			w_row = self.entries[prompt].grid_info()['row']
			w_col = self.entries[prompt].grid_info()['column']
			lbl.grid(row=w_row, column=w_col+1)
			return False
		return True

	def create_info_tuple(self):
		"""Takes the information in all the entries
		and returns it as a tuple."""
		info_list = []
		for entry in self.entries.values():
			info_list.append(entry.get())

	def reset(self):
		self.clear_form()