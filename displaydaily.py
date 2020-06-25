from tkinter import *
from tkinter import ttk

from fooditemdao import FoodItemDAO
from mealdao import MealDAO

import startpage
import viewmealspage

from utilities import *


class DisplayDaily(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)



		self.headers = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')

		self.frame_title = ttk.Frame(self)
		self.frame_info = Frame(self)

		self.frame_title.grid(row=0, column=1)
		self.frame_info.grid(row=1, column=1, padx=15)

		self.frame_title.grid_columnconfigure(0, weight=1)
		self.frame_title.grid_columnconfigure(1, weight=1)

		self.frame_info.grid_columnconfigure(0, weight=1)




		btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(viewmealspage.ViewMealsPage))


		self.lbl_title = Label(self.frame_title, text="Daily Nutrition", font=LARGE_FONT)


		btn_back.grid(row=0, column=0, padx=5, pady=20)
		self.lbl_title.grid(row=0, column=1, sticky="")


	def draw(self):
		self._draw_headers()
		self._draw_info()

	def _draw_headers(self):
		

		
		for i in range(len(self.headers)):
			Label(self.frame_info, text=self.headers[i].upper(), font=BOLD_MONOSPACED_BIG).grid(row=0, column=i+1)
		

	def _draw_info(self):
		info_dict = self._calc_daily_nutrition()
		col_width = 7

		for i in range(len(self.headers)):
			pad = len(self.headers[i]) - col_width
			Label(self.frame_info, text=info_dict[self.headers[i]], width=col_width, font=MONOSPACED_BIG).grid(row=1, column=i+1)
			



	def _calc_daily_nutrition(self):
		all_meals = mealdao.retrieve_all_meals()

		info_dict = {'cal': 0, 'carb': 0, 'fat': 0, 'protein': 0, 'fiber': 0, 'sugar': 0}
		for key in info_dict.keys():
			for meal in all_meals:
				info_dict[key] += meal.formatted_meal_info[key]

		info_dict = self._format_daily_nutrition(info_dict)

		return info_dict

	def _format_daily_nutrition(self, info_dict):

		for key in info_dict.keys():
			info = info_dict[key]
			if info == int(info):
				info = int(info)
			else:
				info = round(info, 1)
			info_dict[key] = info

		return info_dict



	def reset(self):
		self.draw()