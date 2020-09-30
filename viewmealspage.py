from tkinter import *
from tkinter import ttk


from utilities import *
from fooditemdao import FoodItemDAO
from mealdao import MealDAO

import displaydaily

import startpage

from utilities import *


class ViewMealsPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.frame_controls = Frame(self)
		self.frame_mealname = Frame(self)
		self.frame_info = Frame(self)


		self.frame_controls.grid(row=0, column=0, pady=15)
		self.frame_mealname.grid(row=1, column=0)
		self.frame_info.grid(row=2, column=0, pady=10, padx=20)

		self.frame_controls.grid_columnconfigure(0, weight=0)
		self.frame_controls.grid_columnconfigure(1, weight=1)
		self.frame_controls.grid_columnconfigure(2, weight=1)
		self.frame_controls.grid_columnconfigure(3, weight=1)


		self.labels = []

		self.meal_index = 0

		self.headers = ('ss', 'unit', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame("StartPage"))
		self.btn_prev = ttk.Button(self.frame_controls, text="Previous", command=lambda: self.change_meal("prev"))
		self.btn_next = ttk.Button(self.frame_controls, text="Next", command=lambda: self.change_meal("next"))
		self.btn_del = ttk.Button(self.frame_controls, text="Delete Meal", command=self.delete_clicked)
		self.btn_view_nutrition = ttk.Button(self.frame_controls, text="View Day Total", 
										command=lambda: controller.show_frame("DisplayDaily"))

		self.viewing_meals = True


		btn_back.grid(row=0, column=0, padx=20, sticky=W)
		self.btn_view_nutrition.grid(row=0, column=1, padx=20)
		self.btn_prev.grid(row=0, column=2, padx=20, sticky=W)
		self.btn_next.grid(row=0, column=3, sticky=E)
		self.btn_del.grid(row=0, column=4, padx=40)



		self.all_meals = mealdao.retrieve_all_meals()
		self.check_buttons()

		self.col_widths = self._calc_max_col_widths()
		


	def _calc_max_col_widths(self):
		widths = [0, 0, 0, 0, 0, 0, 0, 0, 0]
		for meal in self.all_meals:
			meal_widths = meal.get_widths_of_info()
			for i in range(len(widths)):
				widths[i] = max(widths[i], meal_widths[i])
		return widths


		


	def check_buttons(self):
		if self.meal_index == 0:
			self.btn_prev.config(state=DISABLED)
		else:
			self.btn_prev.config(state=NORMAL)
		if self.meal_index == len(self.all_meals) - 1:
			self.btn_next.config(state=DISABLED)
		else:
			self.btn_next.config(state=NORMAL)


	def draw_form(self):
		if len(self.all_meals) == 0: # no meals found
			self._display_no_meals()
			return False

		self.btn_del.config(state=NORMAL)

		self.draw_meal_name()
		

		self.draw_headers()
		
		self.draw_meal_info()
		self.draw_foods()

	def _display_no_meals(self):
		lbl = Label(self.frame_mealname, text="NO MEALS FOUND", font=LARGE_FONT)
		lbl.grid(row=0, column=0)
		self.labels.append(lbl)

		self.btn_prev.config(state=DISABLED)
		self.btn_next.config(state=DISABLED)
		self.btn_del.config(state=DISABLED)

	def draw_meal_name(self):
		meal_name = self.all_meals[self.meal_index].meal_name
		lbl = Label(self.frame_mealname, text=meal_name, font=LARGE_FONT)
		lbl.grid(row=1, column=1)
		self.labels.append(lbl)


	def draw_meal_info(self):
		lbl = Label(self.frame_info, text="TOTAL", font=BOLD_MONOSPACED_BIG)
		lbl.grid(row=1, column=0)
		self.labels.append(lbl)


		info = self.all_meals[self.meal_index].formatted_meal_info
		for i in range(len(self.headers)):

			if i <= 1: # 0 and 1 are un-needed headers; dispay a dash in the cell
				lbl = Label(self.frame_info, text="--", font=BOLD_MONOSPACED_BIG)
				lbl.grid(row=1, column=i+1)

			else: 
				if i == 2: # cal should be whole number
					lbl = Label(self.frame_info, text=round(info[self.headers[i]]), font=BOLD_MONOSPACED_BIG)
				else:
					lbl = Label(self.frame_info, text=info[self.headers[i]], font=BOLD_MONOSPACED_BIG)
				lbl.grid(row=1, column=i+1)
			self.labels.append(lbl)
				


	def draw_headers(self):
		for i in range(len(self.headers)):
			Label(self.frame_info, text=self.headers[i], font=BOLD_MONOSPACED).grid(row=0, column=i+1, padx=15)

	def draw_foods(self):
		foods = self.all_meals[self.meal_index].get_foods()
		for i in range(len(foods)):
			self._draw_food(foods[i], row=i+2)

	def _draw_food(self, food, row):
		lbl = Label(self.frame_info, text=food.name, font=MONOSPACED_FONT, width=self.col_widths[0])
		lbl.grid(row=row, column=0, pady=3)
		self.labels.append(lbl)
		for i in range(len(self.headers)):
			if i == 2: # cal; should be whole number
				lbl = Label(self.frame_info, text=round(food.info[self.headers[i]]), font=MONOSPACED_FONT, width=self.col_widths[i+1])
			else:
				lbl = Label(self.frame_info, text=food.info[self.headers[i]], font=MONOSPACED_FONT, width=self.col_widths[i+1])
			lbl.grid(row=row, column=i+1, pady=3) 
			self.labels.append(lbl)


	def change_meal(self, dir):
		if dir == "next":
			self.next_meal()

		elif dir == "prev":
			self.prev_meal()
		self.check_buttons()

	def next_meal(self):
		self.meal_index += 1
		self.clear_form()
		self.draw_form()

	def prev_meal(self):
		self.meal_index -= 1
		self.clear_form()
		self.draw_form()

	def clear_form(self):
		for lbl in self.labels:
			lbl.destroy()
		self.labels = []

	def delete_clicked(self):
		name = self.all_meals[self.meal_index].meal_name

		ans = messagebox.askyesno("Delete Meal", f"Are you sure you want to delete '{name}'?")
		if not ans:
			return False
		else:
			self._delete_current_meal()
		self.reset()

	def _delete_current_meal(self):
		name = self.all_meals[self.meal_index].meal_name
		mealdao.delete_meal(name)




	def reset(self):
		self.meal_index = 0
		self.all_meals = mealdao.retrieve_all_meals()
		self.col_widths = self._calc_max_col_widths()
		self.check_buttons()
		self.clear_form()
		self.draw_form()