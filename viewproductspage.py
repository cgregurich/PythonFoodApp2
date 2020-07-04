from tkinter import *
from tkinter import ttk
import startpage
from utilities import *
from fooditemdao import FoodItemDAO
from product import Product
from productdao import ProductDAO



class ViewProductsPage(Frame):
	"""Pseudo spreadsheet for adding, deleting, and viewing all foods."""
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_cells.grid(row=1, column=1)

		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame(startpage.StartPage))
		btn_save = ttk.Button(self.frame_controls, text="Save", command=self.save_clicked)

		btn_back.grid(row=0, column=0)
		btn_save.grid(row=1, column=0)

		self.draw_page()


	def draw_page(self):
		all_foods = fooditemdao.retrieve_all_foods()
		row = 1
		for food in all_foods:
			self._draw_row(food, row)
			row += 1

	#STILL NEED TO CALCULATE COLUMN WIDTHS

	def _draw_row(self, food, row):
		e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, foreground="black", background="white")
		e.insert(0, food.name)
		e.config(state=DISABLED)
		e.grid(row=row, column=0)

		e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT)
		e.grid(row=row, column=1)

		Label(self.frame_cells, text=f"{food.unit}", font=MONOSPACED_FONT).grid(row=row, column=2)

		e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT)
		e.grid(row=row, column=3)






	def save_clicked(self):
		pass



	def reset(self):
		#self.draw_page()
		pass

		