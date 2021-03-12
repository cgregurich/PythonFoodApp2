import math

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from fooditemdao import FoodItemDAO
from mealdao import MealDAO
from productdao import ProductDAO
from grocerydao import GroceryDAO
from utilities import *


class GroceryForm(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.controller = controller

		self.headers = ('Food', 'Amount', 'Amt / Product', 'Cost / Product', '# Products Needed', 'Amt In Inventory',
					 'Inventory Type', 'How Many To Order', 'Cost of Order')

		self.column_headers = []
		self.row_data = {}
		self.row_widgets = {}
		

		self.create_frames()
		self.draw_controls()
		self.draw_sheet()


	def create_frames(self):
		self.frame_controls = Frame(self)
		self.frame_sheet = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_sheet.grid(row=1, column=0)


	def draw_controls(self):
		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: self.controller.show_frame("StartPage"))
		btn_go = ttk.Button(self.frame_controls, text="Go", command=self.go_clicked)
		self.rb_var = StringVar()
		self.rb_var.set("14")
		self.rb1 = ttk.Radiobutton(self.frame_controls, text="1 day", variable=self.rb_var, value="1", command=self.rb_clicked)
		self.rb2 = ttk.Radiobutton(self.frame_controls, text="2 weeks", variable=self.rb_var, value="14", command=self.rb_clicked)

		self.lbl_total = Label(self.frame_controls, text="Daily Total (exact): $0.00", font=BOLD_MONOSPACED)


		btn_back.grid(row=0, column=0)
		self.rb1.grid(row=0, column=1)
		self.rb2.grid(row=0, column=2)
		btn_go.grid(row=0, column=3)
		self.lbl_total.grid(row=0, column=4)


	def go_clicked(self):
		"""Validates each row, calculates and draws the order_count and cost, 
		and calculates and draws the total cost"""
		for row in self.row_widgets.values():
			if not self.is_row_valid(row):
				return False
			order_count, cost = self.calc_order_count_and_cost(row)
			self.draw_order_count_and_cost(row, order_count, cost)

		self.change_total_label()

		self.overwrite_db()

	def overwrite_db(self):
		"""Each time go is clicked, the grocery db is cleared, and all the data
		the user has entered in the grocery form is saved to the database.
		Only if grocery form is set to two weeks"""
		if self.rb_var.get() != "14":
			return
		grocerydao.clear_db()
		food_names = mealdao.retrieve_all_food_names_set()
		for row in self.row_widgets.values():
			info = {"name": row["foodname"].get(), "amount": row["amtininventory"].get(), 
					  "type": row["om_var"].get()}
			grocerydao.insert_food(info)

		

	def is_row_valid(self, row):
		"""Validates that input is a valid number and non-negative"""
		amt = row['amtininventory'].get()

		# Treat empty input as a zero, change it to a zero
		if amt == '':
			row['amtininventory'].delete(0, END)
			row['amtininventory'].insert(0, 0)
			return True
		try:
			float(amt)
		except ValueError:
			messagebox.showerror("Invalid Input", "Values must be valid numbers")
			return False

		if float(amt) < 0:
			messagebox.showerror("Invalid Input", "Values must be positive")
			return False

		return True


	def calc_order_count_and_cost(self, row):
		"""Calculates the number of product to order given 
		a dictionary representing the row's widgets
		Returns tuple of order_count and cost"""


		# Which mode is it in? product vs unit 
		mode = row['om_var'].get()
		
		cost_per_product = float(row['costperproduct'].get()[1:])

		if mode == 'product':
			# If input is nothing, treat it as a zero
			order_count = float(row['numproductsneeded'].get()) - float(row['amtininventory'].get() or 0)
			cost = order_count * cost_per_product

		else: # mode is the food's unit of measure
			# Use of split()[0] is because the data used is of format "number unit"
			# eg. "448 g", so we use split()[0] to grab the number value from that string

			amt_needed = float(row['amtneeded'].get().split()[0])
			amt_have = float(row['amtininventory'].get())
			amt_per_product = float(row['amtperproduct'].get().split()[0])
			order_count = math.ceil((amt_needed - amt_have) / amt_per_product)
			cost = order_count * cost_per_product

		
		# If set to 2 weeks, do round up count
		# If set to 1 day, don't round up count
		if self.rb_var.get() == '14':
			order_count = math.ceil(order_count)



		# Calculate cost now that order_count is correct
		cost = order_count * cost_per_product

		# Check for negative values, convert to 0 if negative
		if order_count < 0:
			order_count = 0
			cost = 0

		# Format cost
		cost = "${:0.2f}".format(cost)

		return (order_count, cost)


	def draw_order_count_and_cost(self, row, order_count, cost):
		"""Draws the order_count and cost data to the screen"""

		row['howmanytoorder'].config(state=NORMAL)
		row['howmanytoorder'].delete(0, END)
		row['howmanytoorder'].insert(0, order_count)


		row['costoforder'].config(state=NORMAL)
		row['costoforder'].delete(0, END)
		row['costoforder'].insert(0, cost)

		row['howmanytoorder'].config(state=DISABLED)
		row['costoforder'].config(state=DISABLED)


	def rb_clicked(self):
		self.clear_sheet()
		self.draw_sheet()
		self.change_total_label()


	def calc_total(self):
		"""Calculate the total cost of the order and returns it"""
		total = 0
		for row in self.row_widgets.values():
			order_cost = float(row['costoforder'].get()[1:])
			total += order_cost

		# Format it as currency
		total = "${:0.2f}".format(total)
		return total


	def change_total_label(self):
		if self.rb_var.get() == '1':
			self.lbl_total.config(text=f"Daily Total (exact): {self.calc_total()}")
		elif self.rb_var.get() == '14':
			self.lbl_total.config(text=f"2 Week Total: {self.calc_total()}")


	def draw_sheet(self):
		self.init_row_data()
		self.calculate_col_widths()
		self.draw_column_headers()

		# Draw each food (i.e. each row)
		self.draw_data()

		# This runs the logic to calculate the cost of each row and the total cost
		self.go_clicked()


	def init_row_data(self):
		"""Creates and stores all data that will be displayed on the page"""
		all_food_names = mealdao.retrieve_all_food_names_set()

		# Number of days to do calculations for; either 1 or 14
		days = int(self.rb_var.get())

		grocery_data = grocerydao.retrieve_data()
		grocery_data = self.fix_grocery_data(grocery_data, all_food_names)
		for name in all_food_names:
			product = productdao.retrieve_product_by_name(name)
			row_dict = {
				'foodname': name,
				'amtneeded': f"{self.calc_daily_amount_needed(name, days)} {product.unit}",
				'amtperproduct': f"{round(product.amount, 2)} {product.unit}",
				'costperproduct': "${:.2f}".format(product.cost),
				'numproductsneeded': self.calc_num_products_needed(name, days),
				# Grabs the saved data from previous runs of the program
				# and fills the row's data with it
				'amtininventory': grocery_data[name]["amount"], 
				'inventorytype': grocery_data[name]["type"],
				'howmanytoorder': 0,
				'costoforder': "${:.2f}".format(0),
			}
			self.row_data[name] = row_dict

	def fix_grocery_data(self, grocery_data, food_names=None):
		"""Should ideally go through the grocery_data dict, and for
		each name in food_names, if the name doesn't exist, will put
		starting values in the dict to avoid KeyErrors later"""
		if not food_names:
			food_names = mealdao.retrieve_all_food_names_set()
		days = int(self.rb_var.get())
		for name in food_names:
			product = productdao.retrieve_product_by_name(name)
			if name not in grocery_data:
				inner_dict = {"amount": 0, "type": "product"}
				grocery_data[name] = inner_dict
		return grocery_data


	def calc_daily_amount_needed(self, food_name, days):
		"""Receives a str food_name and searches meal db and 
		sums all the ss attribute of each food object in the db.
		 i.e. returns the total amount needed daily for given food"""
		all_foods = mealdao.retrieve_all_food_objects()
		amount = 0
		for food in all_foods:
			if food.name == food_name:
				amount += food.ss
		return round(amount * days, 2)


	def calc_num_products_needed(self, food_name, days):
		"""Returns the number of products needed in the specified day for the specified food"""
		product = productdao.retrieve_product_by_name(food_name)
		product_cost = product.cost
		if product_cost == 0: 
			# to avoid ZeroDivisionError
			return 0
		else:
			return round(self.calc_daily_amount_needed(food_name, days) / product.amount, 2)


	def calculate_col_widths(self):
		"""Finds the correct column widths for each column based
		on the data that will be displayed. Saves it in class variable"""
		
		self.col_widths = [0 for i in range(len(self.headers))]
		for i, header in enumerate(self.headers):
			self.col_widths[i] = len(header)

		
		for row_dict in self.row_data.values():
			col_i = 0
			for value in row_dict.values():
				self.col_widths[col_i] = max(self.col_widths[col_i], len(str(value))) # prob returns error for when value isn't a string
				col_i += 1

		# Add some padding to each column
		for i in range(len(self.col_widths)):
			self.col_widths[i] += 2


	def get_all_foods_to_be_drawn(self):
		all_foods = mealdao.retrieve_all_food_objects()


	def draw_column_headers(self):
		# Draws column headers as disabled entries
		for i, header in enumerate(self.headers):
			entry = ttk.Entry(self.frame_sheet, width=self.col_widths[i], font=BOLD_MONOSPACED, foreground="black")
			entry.insert(0, header)
			entry.config(state=DISABLED)
			entry.grid(row=0, column=i)
			self.column_headers.append(entry)


	def draw_data(self):
		# Gets data for each food to be drawn
		# Draws that data to the screen
		# Saves widgets in class variable self.row_dicts
		for row in self.row_data.values():
			self.draw_row(row)


	def draw_row(self, row_dict):
		"""row_dict is a dictionary representing the data of a row"""
		grocery_data = grocerydao.retrieve_data()
		grocery_data = self.fix_grocery_data(grocery_data)
		row_widgets = {}
		col = 0
		for key, value in row_dict.items():
			# Only one that isn't an entry
			if key == 'inventorytype':
				om_var = StringVar()
				unit = fooditemdao.retrieve_food(row_dict['foodname']).unit
				widget = ttk.OptionMenu(self.frame_sheet, om_var, 'product', *('product', unit))
				row_widgets['om_var'] = om_var
				om_var.set(grocery_data[row_dict["foodname"]]["type"])
			else:
				widget = ttk.Entry(self.frame_sheet, font=MONOSPACED_FONT, foreground="black", width=self.col_widths[col])
				widget.insert(0, value)
				if key != 'amtininventory':
					widget.config(state=DISABLED)
				
			widget.grid(row=len(self.row_widgets)+1, column=col)
			row_widgets[key] = widget
			col += 1
		self.row_widgets[len(self.row_widgets)] = row_widgets

	
	def clear_sheet(self):
		"""Destroys all widgets in frame_sheet and resets the
		class vars for keeping track of the widgets and their data"""
		for row in self.row_widgets.values():
			for widget in row.values():
				if type(widget) != StringVar:
					widget.destroy()
		for entry in self.column_headers:
			entry.destroy()

		self.row_widgets = {}
		self.row_data = {}
		self.column_headers = []


	def reset(self):
		self.clear_sheet()
		self.draw_sheet()


def main():
	root = Tk()
	gf = GroceryForm(root)
	gf.pack()
	root.mainloop()


if __name__ == '__main__':
	main()