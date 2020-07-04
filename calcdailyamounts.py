from tkinter import *

from tkinter.font import Font
from tkinter import ttk

from fooditemdao import FoodItemDAO
from fooditem import FoodItem
from mealdao import MealDAO
from meal import Meal

import startpage

from utilities import *



class CalcDailyAmounts(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_cells.grid(row=1, column=0)

		ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame(startpage.StartPage)).grid(row=0, column=0)
		ttk.Button(self.frame_controls, text="Test", command=self.test_func).grid(row=0, column=1)

		self.rb_var = IntVar()
		self.rb_var.set(14)
		rb1 = ttk.Radiobutton(self.frame_controls, text="1 day", var=self.rb_var, value=1, command=self.rb_clicked)
		rb1.grid(row=0, column=2)
		
		rb2 = ttk.Radiobutton(self.frame_controls, text="2 weeks", var=self.rb_var, value=14, command=self.rb_clicked)
		rb2.grid(row=0, column=3)
		
		self.last_control_col = 3
		
		self.col_widths = []
		self.headers = ('food name', 'amount')
		self.cells = []

		self._calc_col_widths()
		self._draw_headers()
		self.draw_page()


	def _draw_headers(self):
		for i in range(len(self.headers)):
			print(f"\ncol_width[i]: {self.col_widths[i]}")
			print(f"current header: {self.headers[i]}")

			e = ttk.Entry(self.frame_cells, font=BOLD_MONOSPACED, foreground="black", background="white", width=self.col_widths[i])
			e.insert(0, self.headers[i].upper())
			e.config(state=DISABLED)
			if i == 1:
				print(f"current header: {self.headers[i]}")
				print(f"e.cget('width'): {e.cget('width')}")
			e.grid(row=0, column=i)




	def _calc_col_widths(self):
		for i in range(len(self.headers)):
			self.col_widths.append(len(self.headers[i]))

		
		COL_PAD = 3
		rows = self._init_rows()
		for i in range (len(self.headers)):
			max_width = self.col_widths[i]
			for r in range(len(rows)):
				if len(rows[r][i]) > max_width:
					max_width = len(rows[r][i])

			self.col_widths[i] = max_width
		
		self.col_widths = [self.col_widths[i] + COL_PAD for i in range(0, len(self.col_widths))]
		

	def test_func(self):
		pass

	
	def _create_food_dict(self):
		"""Returns a dictionary of format:
		key=foodname, value=amount of food needed per day * number of days selected"""
		days = self.rb_var.get()
		food_dict = self._calc_daily_amounts()
		for name in food_dict.keys():
			food_dict[name] *= days
		return food_dict


	def _init_rows(self):
		"""Returns list of tuples. Each tuple in the list is 
		a row on the page.
		Row format: ["foodname", "foodamount foodunit"]
		eg. ["oats", "140 g"]. """
		rows = []


		food_dict = self._create_food_dict()

		units = [fooditemdao.retrieve_food(name).unit for name in food_dict.keys()]
		
		i = 0
		for name in food_dict.keys():
			new_row = (name, f"{food_dict[name]} {units[i]}")
			i += 1
			rows.append(new_row)
		return rows




	def _calc_daily_amounts(self):
		"""Returns a dictionary of format:
		key=foodname, value=amount of food in all meals
		i.e. amount of each food needed daily."""
		food_names = mealdao.retrieve_all_food_names_set()

		food_dict = {}

		for name in food_names:
			food_dict[name] = 0

		all_foods = mealdao.retrieve_all_food_objects()
		for food in all_foods:
			food_dict[food.name] += food.ss

		return food_dict

	def draw_page(self):
		rows = self._init_rows()

		grid_row = 1

		# row -> list of format ["foodname", "foodamount foodunit"]
		# eg. ["oats", "140 g"]
		for row in rows:
			for i in range(0, len(self.headers)):
				e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, foreground="black", background="white", width=self.col_widths[i])
				e.insert(0, row[i])
				e.grid(row=grid_row, column=i, sticky=NE)
				self.cells.append(e)
			grid_row += 1

		self._disable_cells()


	def _disable_cells(self):
		"""Sets all cells in self.cells to disabled so the info
		can't be edited. The cells don't appear disabled because the colors
		have been modified."""
		for cell in self.cells:
			cell.configure(state=DISABLED)
		
	def redraw_page(self):
		self._clear_page()
		self.draw_page()




	def rb_clicked(self):
		"""Func bound to Radiobuttons.
		When either RB is clicked, the page is cleared and redrawn
		in order to show the information for 1 day vs 14 days depending on RB."""
		self._clear_page()
		self.draw_page()


	def _clear_page(self):
		for lbl in self.cells:
			lbl.destroy()

		self.cells = []




	def reset(self):
		self._clear_page()
		self.draw_page()
