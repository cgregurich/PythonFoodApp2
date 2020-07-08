
import math
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
		ttk.Button(self.frame_controls, text="Go", command=self.redraw_orders_and_cost).grid(row=0, column=2)

		self.rb_var = IntVar()
		self.rb_var.set(14)
		rb1 = ttk.Radiobutton(self.frame_controls, text="1 day", var=self.rb_var, value=1, command=self.rb_clicked)
		rb1.grid(row=0, column=3)
		
		rb2 = ttk.Radiobutton(self.frame_controls, text="2 weeks", var=self.rb_var, value=14, command=self.rb_clicked)
		rb2.grid(row=0, column=4)

		lbl_total = Label(self.frame_controls, text="Total:")
		lbl_total.grid(row=0, column=5, padx=(10,0))

		self.entry_total = ttk.Entry(self.frame_controls, foreground="black")
		self.entry_total.grid(row=0, column=6)

		
		self.last_control_col = 3
		

		self.col_widths = []
		self.header_entries = []
		self.headers = ('food name', 'amt/unit', 'cost/unit', 'units needed', 'inventory', 'order', 'actual cost')
		

		self.cells = {} # dictionary of row entry objects

		self.rows = {} # dictionary of row data

		self.draw_page()


	def _draw_headers(self):
		self.header_entries = []
		for i in range(len(self.headers)):
			e = ttk.Entry(self.frame_cells, font=BOLD_MONOSPACED, foreground="black", background="blue", width=self.col_widths[i])
			e.insert(0, self.headers[i].upper())
			e.config(state=DISABLED)
			e.grid(row=0, column=i)
			self.header_entries.append(e)


	def _calc_col_widths(self):
		self.col_widths = []
		for i in range(len(self.headers)):
			self.col_widths.append(len(self.headers[i]))

		
		COL_PAD = 3
		
		if not self.rows: # DB is empty
			return

		row_names = ['foodname', 'amtunit', 'cost', 'need', 'have', 'order', 'actual_cost']

		for i in range(len(self.headers)):
			max_width = self.col_widths[i]
			for r in self.rows.values():
				max_width = max(max_width, len(str(r[row_names[i]])))

			self.col_widths[i] = max_width + COL_PAD

	def _create_food_dict(self):
		"""Returns a dictionary of format:
		key=foodname, value=amount of food needed per day * number of days selected"""
		days = self.rb_var.get()
		food_dict = self._calc_daily_amounts()
		for name in food_dict.keys():
			food_dict[name] *= days
		return food_dict


	def _init_rows(self):
		"""Returns a dictionary representing the rows to be
		drawn to the page."""
		self.rows = {}
		all_products = productdao.retrieve_all_products()
		foodnames = mealdao.retrieve_all_food_names_set()
		name_amt_dict = self._create_food_dict()
		for name in foodnames:
			row = {}
			product = productdao.retrieve_products_by_name(name)[0]
			row['foodname'] = product.foodname
			row['amtunit'] = f"{name_amt_dict[product.foodname]} {product.unit}"
			row['cost'] = "${:.2f}".format(product.cost)
			row['need'] = self._calc_need(name_amt_dict[product.foodname], product.foodname)
			row['have'] = 0
			row['order'] = 0
			row['actual_cost'] = "${:.2f}".format(0.00)
			self.rows[product.foodname] = row



	def _calc_need(self, amt, foodname):
		product = productdao.retrieve_products_by_name(foodname)[0]
		try:
			need = amt / product.amount
		except ZeroDivisionError:
			need = 0
		return "{:.2f}".format(need)



	def draw_total_cost(self):
		total_cost = self._calc_total_cost()
		self.entry_total.config(state=NORMAL)
		self.entry_total.delete(0, END)
		self.entry_total.insert(0, total_cost)
		self.entry_total.config(state=DISABLED)
		


	def _calc_total_cost(self):
		total = 0
		


		for row in self.cells.values():
			total += self._calc_cost(row)
		return "${:.2f}".format(total)




	def test_func(self):
		print("\n")
		print(self.col_widths)
		print(f"len(self.header_entries): {len(self.header_entries)}")
		print(f"len(self.rows): {len(self.rows)}")
		print(f"len(self.cells): {len(self.cells)}")





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
		self._calc_col_widths()
		self._draw_headers()
		self._init_rows()
		if not self.rows: # DB is empty
			return
		self._draw_rows()
		self.draw_orders()
		self.draw_costs()
		self.draw_total_cost()
		self._disable_cells()

	def _draw_rows(self):
		grid_row = 1

		for row in self.rows.values():
			col_i = 0
			foodname = row['foodname']
			cells_dict = {}
			for key, cell in row.items():
				e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, foreground="black", background="white", width=self.col_widths[col_i])
				e.insert(0, cell)
				e.grid(row=grid_row, column=col_i, sticky=NE)
				cells_dict[key] = e
				col_i += 1
			self.cells[foodname] = cells_dict
			grid_row += 1

	def redraw_orders_and_cost(self):
		self.draw_orders()
		self.draw_costs()
		self.draw_total_cost()

	def draw_orders(self):
		for row in self.cells.values():
			row['order'].config(state=NORMAL)
			order = self._calc_order_count(row)
			row['order'].delete(0, END)
			row['order'].insert(0, order)
			row['order'].config(state=DISABLED)



	def _calc_cost(self, row):
		# 2 weeks selected.
		# if 2 weeks selected, then display realistic
		# cost of groceries i.e. if I need 3.4 containers of
		# oats for 2 weeks, and I have 1, then I need to buy 3 to
		# have enough, even though I truly only need 2.4
		if self.rb_var.get() == 14: # 2 weeks selected
			ceil_order = math.ceil(float(row['order'].get()))
			cost_per_unit = float(row['cost'].get()[1:])
			cost = ceil_order * cost_per_unit
		# 1 day selected. 
		# if 1 day selected, then display cost of one day
		# of eating; unrealistic number because of limiting
		# factor i.e. I may consume 1/10th of a product, but I would
		# still have to buy the entire product when the time comes.
		else: # 1 day selected
			cost_per_unit = float(row['cost'].get()[1:])
			units_needed = float(row['need'].get())
			cost = cost_per_unit * units_needed
		return cost


	def draw_costs(self):
		for row in self.cells.values():
			cost = self._calc_cost(row)
			cost = "${:.2f}".format(cost)
			row['actual_cost'].config(state=NORMAL)
			row['actual_cost'].delete(0, END)
			row['actual_cost'].insert(0, cost)
			row['actual_cost'].config(state=DISABLED)
			


	def _calc_order_count(self, row):
		# order is need - have
		need = float(row['need'].get())

		# validate have cell
		# set to 0 if empty or invalid
		# otherwise take data from cell
		if not self._is_have_valid(row):
			have = 0
			row['have'].delete(0, END)
			row['have'].insert(0, 0)
		else:
			have = float(row['have'].get())	

		order = need - have
		if need - have < 0:
			order = 0
		return "{:.2f}".format(order)

	def _is_have_valid(self, row):
		have = row['have'].get()
		try:
			float(have)
		except ValueError:
			return False
		return True



	def _disable_cells(self):
		"""Sets all cells in self.cells to disabled so the info
		can't be edited. The cells don't appear disabled because the colors
		have been modified."""
		for row in self.cells.values():
			for key in row.keys():
				if key == 'have':
					continue
				else:
					row[key].config(state=DISABLED)


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
		for row in self.cells.values():
			for entry in row.values():
				entry.destroy()
		for entry in self.header_entries:
			entry.destroy()
		self.header_entries = []

		self.entry_total.config(state=NORMAL)
		self.entry_total.delete(0, END)
		self.entry_total.config(state=DISABLED)

		self.cells = {}
		




	def reset(self):
		self._clear_page()
		self.draw_page()
