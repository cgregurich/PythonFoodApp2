from tkinter import *
from tkinter import ttk
import startpage
from utilities import *
from fooditemdao import FoodItemDAO
from product import Product
from productdao import ProductDAO
import math



class ViewProductsPage(Frame):
	"""Pseudo spreadsheet for adding, deleting, and viewing all foods."""
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_cells.grid(row=1, column=1, pady=(0, 20))

		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame("StartPage"))
		self.lbl_save = Label(self.frame_controls, text="", fg="green")
		btn_save = ttk.Button(self.frame_controls, text="Save", command=self.save_clicked)

		btn_back.grid(row=0, column=0)
		self.lbl_save.grid(row=1, column=0)
		btn_save.grid(row=2, column=0)


		self.rows = {}

		self.headers = ['food', 'amt', 'unit', 'cost', 'cal/$']
		self.col_widths = []
		self.draw_headers()
		self.draw_page()


	def draw_headers(self):
		for i, h in enumerate(self.headers):
			Label(self.frame_cells, text=h.upper(), font=MONOSPACED_FONT).grid(row=0, column=i)

	def _calc_col_widths(self):

		self.col_widths = [len(h) for h in self.headers]

		all_products = productdao.retrieve_all_products()
		if not all_products:
			return
		for i in range(len(all_products)):
			p = all_products[i] # current product
			self.col_widths[0] = max(len(p.foodname), self.col_widths[0])
			self.col_widths[1] = max(len(str(p.amount)), self.col_widths[1])
			self.col_widths[2] = max(len(p.unit), self.col_widths[2])
			self.col_widths[3] = max(len(str(p.cost)), self.col_widths[3])
			self.col_widths[4] = max(len(str(p.calpercost)), self.col_widths[4])
		for i in range(len(self.col_widths)):
			self.col_widths[i] += 3



	def draw_page(self):
		self._calc_col_widths()
		products = productdao.retrieve_all_products()
		row = 1
		for p in products:
			self._draw_product(p, row)
			row += 1

	def _draw_product(self, product, row):
		"""
		product -> Product object
		row -> integer
		Creates a row based on arg product. Puts this row on the screen and
		adds the row to dict self.rows (as a dictionary)."""
		name_entry = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, foreground="black", background="white", width=self.col_widths[0])
		name_entry.insert(0, product.foodname)
		name_entry.config(state=DISABLED)
		name_entry.grid(row=row, column=0)

		amt_entry = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, width=self.col_widths[1])
		amt_entry.insert(0, product.amount)
		amt_entry.grid(row=row, column=1)

		lbl_unit = Label(self.frame_cells, text=product.unit, font=MONOSPACED_FONT, width=self.col_widths[2], anchor=W)
		lbl_unit.grid(row=row, column=2)

		cost_entry = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, width=self.col_widths[3])
		cost_entry.insert(0, "{:.2f}".format(product.cost))
		cost_entry.grid(row=row, column=3)

		cals_per_dollar = product.calpercost
		calpercost_entry = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, width=self.col_widths[4], foreground="black", background="white")
		calpercost_entry.insert(0, cals_per_dollar)
		calpercost_entry.config(state=DISABLED)
		calpercost_entry.grid(row=row, column=4)

		# save all widgets
		row = {}
		row['name_entry'] = name_entry
		row['amt_entry'] = amt_entry
		row['lbl_unit'] = lbl_unit	
		row['cost_entry'] = cost_entry
		row['calpercost_entry'] = calpercost_entry
		self.rows[product.foodname] = row


	def _calc_cals_per_dollar(self, row):
		"""Pulls numbers from amount and cost entries and calculates based on the food's ss 
		and calories how many calories you get per dollar for each product"""
		foodname = row['name_entry'].get()
		f = fooditemdao.retrieve_food(foodname)
		p = productdao.retrieve_product_by_name(foodname)

		# these cur vars are because if we pulled these figures from the DB
		# at this stage, with a newly added food/product, the values would be 0,
		# so instead we have to pull them from the entry
		cur_amount = int(row['amt_entry'].get())
		cur_cost = float(row['cost_entry'].get())
		
		

		try:
			ans = math.ceil(((cur_amount / f.ss) * f.cal) / cur_cost)
		except ZeroDivisionError:
			ans = 0
		
		return ans


	def _is_form_valid(self):
		for row in self.rows.values():
			amount = row['amt_entry'].get()
			cost = row['cost_entry'].get()
			
			# Validate amount
			try:
				int(amount)
			except ValueError:
				messagebox.showerror("Invalid Amount", "Amount must be a number.")
				return False

			if int(amount) != float(amount):
				messagebox.showerror("Invalid Amount", "Amount must be a whole number.")
				return False

			if int(amount) < 0:
				messagebox.showerror("Invalid Amount", "Amount must be positive.")
				return False

			# Validate cost
			try:
				float(cost)
			except ValueError:
				messagebox.showerror("Invalid Cost", "Cost must be a valid price.")
				return False

			if float(cost) < 0:
				messagebox.showerror("Invalid Cost", "Cost must be positive.")
				return False
		return True



	def save_clicked(self):
		# Validate form
		if not self._is_form_valid():
			return False


		for row in self.rows.values():
			foodname = row['name_entry'].get() # needed for updating DB
			amount = int(row['amt_entry'].get())
			unit = row['lbl_unit'].cget('text')
			cost = "{:.2f}".format(float(row['cost_entry'].get()))
			cal_per_cost = self._calc_cals_per_dollar(row)

			row['cost_entry'].delete(0, END)
			row['cost_entry'].insert(0, cost)

			

			row['calpercost_entry'].config(state=NORMAL)
			row['calpercost_entry'].delete(0, END)
			row['calpercost_entry'].insert(0, cal_per_cost)
			row['calpercost_entry'].config(state=DISABLED)

			info_tup = (foodname, amount, unit, cost, cal_per_cost)


			product = Product()
			product.set_info_from_tuple(info_tup)
			productdao.update_product(product)
			

		self.lbl_save.config(text="Saved")
		self.lbl_save.after(2000, lambda: self.lbl_save.config(text=""))

		return True
				


	def clear_page(self):
		"""Removes all on-screen widgets from the screen.
		Resets the dict of all rows to be empty."""
		for row in self.rows.values():
			for key in row.keys():
				row[key].destroy()
		self.rows = {}



	def reset(self):
		self.clear_page()
		self.draw_page()

		

