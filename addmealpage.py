from tkinter import *
from tkinter import ttk

from fooditemdao import FoodItemDAO
from mealdao import MealDAO

import startpage

from utilities import *

class AddMealPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		
		# Create frames

		# Frame for grouping
		self.frame_upper = Frame(self)

		# Frames
		self.frame_controls = Frame(self)
		self.frame_meal_name = Frame(self.frame_upper)
		self.frame_macros = Frame(self.frame_upper)
		self.frame_adders = Frame(self)
		self.frame_show = Frame(self.frame_upper)
		

		
		# Vars for keeping track of dynamic widgets
		self.macro_labels = []
		self.adders = {} 



		# Put frames in window
		self.frame_upper.grid(row=0, column=1, sticky=NW)

		self.frame_controls.grid(row=0, column=0, sticky=NW, padx=15)

		# Widgets in upper frame
		self.frame_meal_name.grid(row=0, column=0, sticky=NW, pady=10)
		self.frame_macros.grid(row=1, column=0, sticky=NE, pady=10)
		self.frame_show.grid(row=0, column=1)

		# Widgets for foods
		self.frame_adders.grid(row=2, column=1, sticky=NW)
		


		# Initialize window with widgets

		# frame show 
		self.selected_meal = StringVar()
		self.optionmenu_select_meal = ttk.OptionMenu(self.frame_show, self.selected_meal, "Select Meal", *mealdao.retrieve_all_meal_names())
		self.optionmenu_select_meal.grid(row=0, column=1)
		ttk.Button(self.frame_show, text="Show Meal", command=self.show_clicked).grid(row=0, column=2, sticky=N)

		# flag to keep track of if we're viewing a meal or creating a meal
		self.is_show = False


		# frame_controls -> create controls
		self.lbl_status = Label(self.frame_controls, text="", fg="green")

		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame("StartPage"))
		btn_new_adder = ttk.Button(self.frame_controls, text="Add Food", command=self.create_adder)
		btn_clear_page = ttk.Button(self.frame_controls, text="Clear Page", command=self.reset)
		btn_calc = ttk.Button(self.frame_controls, text="Calculate", command=self.display_food_nutrition)
		btn_clear_checked = ttk.Button(self.frame_controls, text="Clear Checked", command=self.clear_checked)
		btn_save_meal = ttk.Button(self.frame_controls, text="Save Meal", command=self.save_meal_clicked)
		

		# frame_controls grid controls
		PADY = 7

		btn_back.grid(row=0, column=0, sticky=N, pady=PADY)
		btn_new_adder.grid(row=1, column=0, sticky=N, pady=PADY)
		btn_clear_page.grid(row=2, column=0, pady=PADY)
		
		btn_calc.grid(row=3, column=0, pady=PADY)
		btn_clear_checked.grid(row=4, column=0, pady=PADY)
		self.lbl_status.grid(row=5, column=0, sticky=N)
		btn_save_meal.grid(row=6, column=0, sticky=N, pady=PADY)


		# frame_meal_name setup 
		self.lbl_meal_name = Label(self.frame_meal_name, text="Meal name:")
		self.entry_meal_name = ttk.Entry(self.frame_meal_name)
		self.lbl_meal_name.grid(row=0, column=0, sticky=S)
		self.entry_meal_name.grid(row=0, column=1, sticky=S)
		self._init_frame_macros()


	def _init_frame_macros(self):
		"""Sets up the frame for displaying the meal's nutrition"""
		headers = ("Calories", "Carbs", "Fat", "Protein", "Fiber", "Sugar")
		for i in range(len(headers)):
			lbl = Label(self.frame_macros, text=f"{headers[i]}:", font=HEADER_FONT)
			lbl.grid(row=i+1, column=0, sticky=E, padx=10, pady=0)
		
		for i in range(len(headers)):
			lbl = Label(self.frame_macros)
			lbl.grid(row=i+1, column=1)
			self.macro_labels.append(lbl)


	def show_clicked(self):
		meal_name = self.selected_meal.get()
		if meal_name == "Select Meal":
			return False
		self.is_show = True
		self._clear_page()
		self.draw_filled_form(meal_name)


	def draw_filled_form(self, meal_name):
		"""This func is called when user has selected a meal to show
		and has clicked Show Meal button.
		This displays the existing meal in the window."""

		meal = mealdao.retrieve_meal(meal_name)

		# Create an adder for each food in meal
		for food in meal.foods:
			self.create_adder()

		self.entry_meal_name.insert(0, meal_name)

		# Fill each adder
		for i in range(len(self.adders)):
			adder = self.adders[i]
			food = meal.foods[i]
			adder['food_var'].set(food.name)
			adder['entry_amount'].insert(0, food.ss)
			adder['lbl_unit'].config(text=food.unit)
			adder['lbl_cal'].config(text=food.cal)
			adder['lbl_carb'].config(text=food.carb)
			adder['lbl_fat'].config(text=food.fat)
			adder['lbl_protein'].config(text=food.protein)
			adder['lbl_fiber'].config(text=food.fiber)
			adder['lbl_sugar'].config(text=food.sugar)

		# Display the meal's nutrition
		self.display_meal_macros()
		


	def create_adder(self):
		"""Creates an adder:
		An adder is the frame that allows user to select a food,
		enter an amount, and then displays that specific food's nutrition.
		self.adders is a dict with format key=adder row, value=adder dict
		eg. first adder's key is 0. """
		new_frame = Frame(self.frame_adders)
		food_var = StringVar()
		check_var = IntVar()

		food_options = fooditemdao.retrieve_all_food_names()

		# Create adder widgets
		check_del = ttk.Checkbutton(new_frame, var=check_var)
		optionmenu = ttk.OptionMenu(new_frame, food_var, "Select Food", command=self.food_selected, *food_options)
		lbl_amount = Label(new_frame, text="Amount:")
		entry_amount = ttk.Entry(new_frame)
		lbl_unit = Label(new_frame, text="unit")


		# Create nutrition info headers
		headers = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		for i in range(len(headers)):
			Label(new_frame, text=headers[i].upper()).grid(row=0, column=i+3, padx=2)


		# Create dynamic adder widgets for nutrition info
		info_font = MONOSPACED_FONT
		lbl_cal = Label(new_frame, text="-", font=info_font)
		lbl_carb = Label(new_frame, text="-", font=info_font)
		lbl_fat = Label(new_frame, text="-", font=info_font)
		lbl_protein = Label(new_frame, text="-", font=info_font)
		lbl_fiber = Label(new_frame, text="-", font=info_font)
		lbl_sugar = Label(new_frame, text="-", font=info_font)

		# Put widgets in adder frame
		check_del.grid(row=0, column=0, sticky=NE)
		optionmenu.grid(row=0, column=1, sticky=NE)
		lbl_amount.grid(row=1, column=0, sticky=NE)
		entry_amount.grid(row=1, column=1, sticky=NW)
		lbl_unit.grid(row=1, column=2, sticky=NW, padx=(0, 10))

		# Put nutrition info widgets in adder frame
		lbl_cal.grid(row=1, column=3)
		lbl_carb.grid(row=1, column=4)
		lbl_fat.grid(row=1, column=5)
		lbl_protein.grid(row=1, column=6)
		lbl_fiber.grid(row=1, column=7)
		lbl_sugar.grid(row=1, column=8)
		

		# Put the new adder frame on the window
		new_frame.grid(row=len(self.adders), column=0, pady=10)
		
		# create a dict to add to self.adders
		adder_dict = {}
		adder_dict['frame'] = new_frame
		adder_dict['food_var'] = food_var
		adder_dict['check_var'] = check_var
		adder_dict['optionmenu'] = optionmenu
		adder_dict['lbl_amount'] = lbl_amount
		adder_dict['entry_amount'] = entry_amount
		adder_dict['lbl_unit'] = lbl_unit
		adder_dict['lbl_cal'] = lbl_cal
		adder_dict['lbl_carb'] = lbl_carb
		adder_dict['lbl_fat'] = lbl_fat
		adder_dict['lbl_protein'] = lbl_protein
		adder_dict['lbl_fiber'] = lbl_fiber
		adder_dict['lbl_sugar'] = lbl_sugar
		self.adders[len(self.adders)] = adder_dict


	def clear_checked(self):
		"""Clears all adders where the checkbutton is checked.
		Also recalculates daily nutrition."""
		for adder in self.adders.values():
			if adder['check_var'].get() == 1:
				self._clear_adder(adder)

		self.display_meal_macros()



	def _clear_adder(self, adder):
		adder['food_var'].set("Select Food")
		adder['entry_amount'].delete(0, END)
		adder['lbl_unit'].config(text="unit")
		adder['lbl_unit'].config(text="unit")
		adder['lbl_cal'].config(text="-") 
		adder['lbl_carb'].config(text="-") 
		adder['lbl_fat'].config(text="-") 
		adder['lbl_protein'].config(text="-")
		adder['lbl_fiber'].config(text="-")
		adder['lbl_sugar'].config(text="-")
		adder['check_var'].set(0)

	

	def food_selected(self, selected):
		"""When a food is selected in any of the optionmenus,
		each adder's unit label is then set to the appropriate label.
		Not sure how to check which adder was interacted with, so it checks
		all adders."""
		for adder in self.adders.values():
			if adder['food_var'].get() != "Select Food": # a food has been selected
				food = fooditemdao.retrieve_food(adder['food_var'].get())
				adder['lbl_unit'].config(text=food.info['unit'])
		



	def save_meal_clicked(self):
		"""Func bound to Save Meal button."""

		# Validate meal name i.e. unique name.
		if not self._is_meal_name_valid():
			return False

		# Checks if showing an existing meal or creating a new meal.
		# If showing an existing meal, delegates to a different func.
		if self.is_show:
			self._save_meal_show()
			return True



		# Validate adders
		for adder in self.adders.values():
			if not self._is_adder_valid(adder):
				return False # stop the process if there is invalid data

		# Get meal name from form
		meal_name = self.entry_meal_name.get()

		# Check for duplicate foods
		if self._is_duplicate_foods():
			return False

		foods = self.get_foods_from_adders()
		meal = Meal(meal_name, *foods)
		mealdao.insert_meal(meal)


		self.display_food_nutrition()

		# Display message to user that disappears after time
		self.lbl_status.config(text="Changes saved")
		self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))

		self._refresh_meal_option_menu()


	def _is_duplicate_foods(self):
		"""Displays error message and returns True if there is a duplicate food in the adders.
		Else returns False"""

		foods = self.get_foods_from_adders()
		if not foods:
			return True

		food_names = []

		for food in foods:
			food_names.append(food.name)

		foods_set = set(food_names)
		if len(foods_set) != len(food_names):
			messagebox.showerror("Duplicate Food", "Only one of each food is allowed")
			return True
		else:
			return False


	def _save_meal_show(self):
		"""Function for when user clicks save, but the page is showing an existing food"""
		if self._is_duplicate_foods():
			return False

		old_meal_name =self.selected_meal.get()
		meal_name = self.entry_meal_name.get()

		ans = messagebox.askyesno("Update Food", f"Would you like to overwrite '{old_meal_name}' with this data?")
		if ans == False:
			return False

		# Check if user changed meal's name
		old_name = self.selected_meal.get()
		
		# Check that new meal_name is unique and that meal_name actually changed
		if meal_name in mealdao.retrieve_all_meal_names() and meal_name != old_name:
			messagebox.showerror("Duplicate Meal Name", f"Meal with name '{meal_name}' already exists")
			return False
		# If new meal name is different and valid, update that meal in the database
		if meal_name != old_name:
			mealdao.update_meal_names_of_foods((meal_name, old_name))
		self._overwrite_meal(meal_name)
		self.display_food_nutrition()
		self._refresh_meal_option_menu()
		self.selected_meal.set(meal_name)
			

		
	def _overwrite_meal(self, meal_name):
		"""Deletes the meal from the DB by name.
		Then creates a new Meal object from the window
		and adds that Meal to the DB."""
		mealdao.delete_meal(meal_name)
		foods = self.get_foods_from_adders()
		meal = Meal(meal_name)
		meal.set_foods_from_list(foods)
		mealdao.insert_meal(meal)



	def _is_meal_name_valid(self):
		"""Checks for uniqueness of meal name against mealnames in DB
		Displays an error and returns False if name is duplicate or empty"""
		meal_name = self.entry_meal_name.get()

		if meal_name == "":
			messagebox.showerror("Invalid Meal Name", f"Please enter a name for the meal")
			return False

		# Check for duplicate name
		all_names = mealdao.retrieve_all_meal_names()
		if meal_name in all_names:
			if self.is_show: 
				return True
			else:
				messagebox.showerror("Duplicate Meal Name", f"Meal with name '{meal_name}' already exists")
			return False
		return True


	def _get_index_of_adder(self, adder):
		"""Returns index of adder in self.adders."""
		for key, value in self.adders.items():
			if adder == value:
				return key


	def _is_adder_valid(self, adder):
		"""Checks if the arg adder has a food selected and a valid amount entered.
		Returns True if yes to both.
		Displays an error message and returns False if no to either."""
		if self._is_adder_unused(adder):
			return True

		if adder['food_var'].get() == "Select Food":
			messagebox.showerror("No Food Selected", "Please select a food")
			return False
		
		adder_index = self._get_index_of_adder(adder)

		amount = adder['entry_amount'].get()

		# Check if an amount was entered
		if amount == "":
			return False

		# Check if amount is a valid number
		try: 
			float(amount)
		except ValueError:
			messagebox.showerror(f"Error for Food {adder_index+1}", "Amount must be a valid number")
			return False

		# Check if amount entered is positive
		if float(amount) < 0:
			messagebox.showerror(f"Error for Food {adder_index+1}", "Amount must be positive")
			return False

		return True


	def _is_adder_unused(self, adder):
		"""Checks if arg adder is completely empty.
		i.e. no food selected and no amount entered, returns True.
		Else returns False"""

		if adder['food_var'].get() == "Select Food" and adder['entry_amount'].get() == "":
			return True
		return False


	def _calc_meal_macros(self):
		"""Calculates the meal's nutrition based on the foods in the adders.
		Returns the meal macros as a list (??)"""

		# Make sure each adder is valid
		for adder in self.adders.values():
			if not self._is_adder_valid(adder):
				return False

		all_foods = self.get_foods_from_adders()

		tags = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		meal_macros = []
		for i in range(len(tags)):
			meal_macros.append(0)

		for i in range(len(tags)):
			for food in all_foods:
				meal_macros[i] += food.info[tags[i]]

		meal_macros = self._format_macros(meal_macros)
		return meal_macros
		


	def _format_macros(self, meal_macros):
		"""Formats arg meal_macros.
		If a whole number, displays as such eg. 4
		If not a whole number, displays to one decimal place eg. 4.2"""
		dec = 0
		for i in range(len(meal_macros)):
			if i > 3: # fiber or sugar
				dec = 2
			meal_macros[i] = round(meal_macros[i], dec)
			if i <= 3: # not fiber or sugar
				meal_macros[i] = int(meal_macros[i])
		return meal_macros


	def display_meal_macros(self):
		"""Puts arg meal_macros on page"""
		meal_macros = self._calc_meal_macros()
		if meal_macros == False:
			return False

		for i in range(len(self.macro_labels)):
			macro = meal_macros[i]
			self.macro_labels[i].config(text=meal_macros[i])
		return True



	def get_foods_from_adders(self):
		"""Returns a list of FoodItems based on what is in the adders.
		If an adder is unused, it's ignored.
		If an adder is partially filled (only food selected or only amount entered)
		then it will also be ignored."""
		foods = []
		for adder in self.adders.values():
			if not self._is_adder_unused(adder):
				food = fooditemdao.retrieve_food(adder['food_var'].get())
				try:
					food.proportionalize(float(adder['entry_amount'].get()))
				except ValueError:
					messagebox.showerror("", f"Enter amount for {food.name}")
					return []
				foods.append(food)
		return foods


	def display_food_nutrition(self):
		if not self.display_meal_macros():
			return False

		for adder in self.adders.values():
			if not self._is_adder_unused(adder) and self._is_adder_valid(adder):
				self._display_food_macros(adder)


	def _display_food_macros(self, adder):
		"""Displays each filled-out adder's nutrition section with 
		the food's nutrition"""
		tags = ('cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		food = fooditemdao.retrieve_food(adder['food_var'].get())
		food.proportionalize(float(adder['entry_amount'].get()))

		info = food.info

		# Formats cal to be a whole number
		info['cal'] = round(info['cal'])

		for i in range(len(tags)):
			adder[f"lbl_{tags[i]}"].config(text=f"{info[tags[i]]}")
			

	def _clear_page(self):
		for adder in self.adders.values():
			adder['frame'].destroy()
		for lbl in self.macro_labels:
			lbl.config(text="")
		self.entry_meal_name.delete(0, END)
		self.adders = {}



	def _refresh_meal_option_menu(self):
		# Refresh meal option menu
		meal_options = mealdao.retrieve_all_meal_names()
		self.optionmenu_select_meal.destroy()
		self.optionmenu_select_meal = ttk.OptionMenu(self.frame_show, self.selected_meal, "Select Meal", *meal_options)
		self.optionmenu_select_meal.grid(row=0, column=1)


	def _reset_meal_name_entry(self):
		self.entry_meal_name.config(state=NORMAL)
		self.entry_meal_name.delete(0, END)
		



	def reset(self):
		self._clear_page()
		self._reset_meal_name_entry()
		self.is_show = False
		self.create_adder()
		self.food_options = fooditemdao.retrieve_all_food_names()
		self._refresh_meal_option_menu()