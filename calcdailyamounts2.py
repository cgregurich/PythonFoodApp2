from tkinter import *
from tkinter import ttk

class CalcDailyAmounts(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.controller = controller

		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_cells.grid(row=1, column=0)

		self.draw_controls()
		self.draw_cells()

	def draw_controls(self):
		btn_back = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame(startpage.StartPage))
		btn_go = ttk.Button(self, text="Go", command=self.go_clicked)
		btn_back.grid(row=0, column=0)
		btn_go.grid(row=0, column=1)

		self.rb_var = StringVar()
		rb_day = ttk.Radiobutton(self, text="1 day", variable=self.rb_var, value="1day")
		rb_twoweeks = ttk.Radiobutton(self, text="2 weeks", variable=self.rb_var, value="2weeks")

		rb_day.grid(row=0, column=2)
		rb_twoweeks.grid(row=0, column=3)

		lbl_total = Label(self, text="Total:")
		entry_total = ttk.Entry(self)

		lbl_total.grid(row=0, column=4)
		entry_total.grid(row=0, column=5)

	def draw_cells(self):
		# Draw headers
		self.draw_headers()
		self.init_rows_data()


	def draw_headers(self):
		self._calc_col_widths()


	def _calc_daily_amount(self, food_name):
		"""
		food_name -> str
		return    -> integer
		Returns the total amount of a food used in a day based on 
		all the meals in the meal database.
		"""
		all_foods_in_meals = mealdao.retrieve_all_food_objects()
		total_amount = 0
		for food in all_foods_in_meals:
			if food.name == food_name:
				total_amount += food.amount

		return total_amount


	



	def init_rows_data(self):
		"""Initializes all rows' data in a class var"""
		self.rows = {}
		all_foodnames = mealdao.retrieve_all_food_names_set()

		# Create a row for each food to be displayed
		if self.rb_var.get() == "1day":
			fooditem = fooditemdao.retrieve_food()
			product = productdao.retrieve_product_by_name

			row[0] = fooditem.name
			row[1] = self._calc_daily_amount(fooditem.name)
			row[2] = product.amount
			row[3] = product.cost
			row[4] = self._calc_daily_amount(fooditem.name) / product.amount
			row[5] = ""
			row[6] = 

		else: # self.rb_var.get() == "2weeks"
			pass





		#########
		self.rows = {}
		all_foodnames = mealdao.retrieve_all_food_names_set()

		if self.rb_var.get() == "1day":
			for name in all_foodnames:
				fooditem = 
				product = productdao.retrieve_product_by_name(name)
				row = {} 
				row['foodname'] = name
				row['amtneeded'] =  # amount needed daily
				row['amtperitem'] = product.amount # amount in each product
				row['costperitem'] = product.cost # cost of product
				row['itemsneeded'] = # number of products needed daily
				row['inventory'] = 
				row['invtype'] = 
				row['actualcost'] =  

		else: # self.rb_var.get() == "2weeks"
			pass


	def _calc_col_widths(self):
		headers = ('food name', 'amt needed', 'amt per item', 'cost per item', 'items needed', 'inventory', 'inv type', 'actual cost')
		all_foods = mealdao.retrieve_all_food_names_set()







