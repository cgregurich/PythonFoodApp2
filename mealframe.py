from tkinter import *
from tkinter import ttk

from fooditemdao import FoodItemDAO
from mealdao import MealDAO

import startpage

from utilities import *


class MealFrame(Frame):
class MealFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)


		self.frame_controls = Frame(self)
		self.frame_rows = Frame(self)

		self.frame_controls.grid(row=0, column=0);
		self.frame_rows.grid(row=0, column=1)

		# Create controls
		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame(startpage.StartPage))

		btn_back.grid(row=0, column=0)



		self.entry_meal_name = ttk.Entry(self.frame_rows, font=MONOSPACED_FONT)
		self.entry_meal_name.grid(row=0, column=0)
		self.rows = {}
		self.create_headers()
		self.create_row()



	def create_headers(self):
		headers = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		for i in range(len(headers)):
			Label(self.frame_rows, text=headers[i].upper(), font=MONOSPACED_FONT).grid(row=0, column=i+3, sticky=W)



	def create_row(self, food=None):
		var = StringVar()
		optionmenu = ttk.OptionMenu(self.frame_rows, var, "Select Food", command=self.food_selected, *fooditemdao.retrieve_all_food_names())
		entry_amount = ttk.Entry(self.frame_rows, font=MONOSPACED_FONT)
		lbl_unit = Label(self.frame_rows, text="unit")
		lbl_cal = Label(self.frame_rows)
		lbl_carb = Label(self.frame_rows)
		lbl_fat = Label(self.frame_rows)
		lbl_protein = Label(self.frame_rows)
		lbl_fiber = Label(self.frame_rows)
		lbl_sugar = Label(self.frame_rows)

		new_dict = {}
		new_dict['optionmenu'] = optionmenu
		new_dict['var'] = var
		new_dict['entry_amount'] = entry_amount
		new_dict['unit'] = lbl_unit
		new_dict['cal'] = lbl_cal
		new_dict['carb'] = lbl_carb
		new_dict['fat'] = lbl_fat
		new_dict['protein'] = lbl_protein
		new_dict['fiber'] = lbl_fiber
		new_dict['sugar'] = lbl_sugar

		self.rows[len(self.rows)] = new_dict

	
		self.draw_row(self.rows[len(self.rows)-1], food)



		


	def draw_row(self, row, food=None):

		# tags = {'unit':'ss', 'cal':'cal', 'carb':'carb', 'fat':'fat', 'protein':'protein',
		# 		'fiber':'fiber', 'sugar':'sugar'}
		macro_tags = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		if not food:
			c = 0
			for key in row.keys():
				if key == 'var':
					continue
				else:
					row[key].grid(row=len(self.rows), column=c)
					c += 1
				if key in macro_tags:
					row[key].config(text="--")






	def food_selected(self):
		pass



	def reset(self):
		pass

