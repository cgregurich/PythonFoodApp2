from tkinter import *


from tkinter import ttk

import startpage

from utilities import *

class ViewFoodsPage(Frame):
	"""Pseudo spreadsheet for adding, deleting, and viewing all foods."""
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		# The column headers
		self.HEADERS = ('name', 'ss', 'unit', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')

		# The number of columns in the sheet; equal to the number of headers
		self.width = len(self.HEADERS)

		# The padding to add at the end of each column width
		self.COL_PADDING = 3

		# The padding between controls
		self.PADY_CONTROLS = 5

		# The width that each column should be
		self.col_widths = []

		#Init each col width to 0
		for w in range(self.width):
			self.col_widths.append(0)
		self._calc_col_widths()

		

		# Create frames (controls frame and cells frame)
		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		# Put the frames on the window
		self.frame_controls.grid(row=0, column=0, sticky=N, padx=(10, 0), pady=(10, 0))
		self.frame_cells.grid(row=0, column=1, sticky=N, padx=10)


		# Create controls
		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame("StartPage")) 
		
		# Label for displaying that changes were saved
		self.lbl_status = Label(self.frame_controls, text="", fg="green")		
		btn_delete_checked = ttk.Button(self.frame_controls, text="Delete", command=self.delete_checked)
		btn_save_changes = ttk.Button(self.frame_controls, text="Save changes", command=self.save_changes)


		
		# Put the controls on the grid
		btn_back.grid(row=0, column=0, pady=self.PADY_CONTROLS)
		self.lbl_status.grid(row=4, column=0, pady=self.PADY_CONTROLS, padx=10)
		btn_delete_checked.grid(row=5, column=0, pady=self.PADY_CONTROLS)
		btn_save_changes.grid(row=6, column=0, pady=self.PADY_CONTROLS, padx=12) # padx of 10 to make optionmenus' size static

		# List of lists for the rows of cells in the sheet
		# each element in this list is a list of Entry widgets; each is a row. Each Entry in a row is a cell.
		self.rows = {}

		# List of lists. Rows (inner lists) are: [<checkbutton object>, <intvar object>]
		self.checkbuttons = []


		# Create the sheet
		self.draw_sheet()


	def draw_sheet(self):
		"""Draws the sheet; used for initializing the sheet.
		If there are no foods to display, then a message is displayed to the user."""

		all_foods = fooditemdao.retrieve_all_foods()

		if not all_foods:
			return False

		self.create_col_headers()

		for food in all_foods:
			row = self._draw_row(food)


	def create_col_headers(self):
		"""Creates and places Labels with the column headers in row 0 of frame_cells"""
		for i in range(self.width):
			l = Label(self.frame_cells, text=self.HEADERS[i].upper(), font=MONOSPACED_FONT)
			l.grid(row=0, column=i+1)


	def _draw_row(self, food):
		"""Creates and draws a row in the sheet.
		Each cell will be filled with the appropriate data based on arg food."""

		row = {}
		cb_var = IntVar()
		cb = ttk.Checkbutton(self.frame_cells, var=cb_var)
		cb.grid(row=len(self.rows)+1, column=0)
		row['cb'] = cb
		row['cb_var'] = cb_var
		for i, h in enumerate(self.HEADERS):
			e = ttk.Entry(self.frame_cells, font=MONOSPACED_FONT, width=self.col_widths[i])
			e.insert(0, food.info[h])
			if i == 0:

				e.config(foreground="black", state=DISABLED)
			row[f"{h}_entry"] = e
			e.grid(row=len(self.rows)+1, column=i+1)
		self.rows[food.name] = row

		

	def _calc_col_widths(self):
		"""Calculates how wide columns need to be based on headers and avail data (if any)"""

		# Set the widths based on the headers
		for i in range(self.width):
			self.col_widths[i] = len(self.HEADERS[i])

		# Set the widths based on the headers or the longest piece of data; whichever is longer
		all_foods = fooditemdao.retrieve_all_foods()
		if all_foods:
			for i in range(self.width):
				for food in all_foods:
					self.col_widths[i] = max(self.col_widths[i], len(str(food.info[self.HEADERS[i]])))

		# Add padding to the widths
		for i in range(self.width):
			self.col_widths[i] += self.COL_PADDING


	def _is_sheet_filled_out(self):
		"""Returns False if there are no rows/foods or if there are 
		cells that are empty.
		Else returns True.
		"""
		if not self.rows:
			return False
		for row in self.rows.values():
			for key in row.keys():
				if key == 'cb' or key == 'cb_var':
					continue
				text = row[key].get()
				if text == '':
					messagebox.showerror("Empty Cells Found", "Please fill out every cell")
					return False
		else:
			return True



	def delete_checked(self):
		"""Goes through the rows and finds all rows where the CB is selected.
		Adds the names of these rows to a list, then goes through the list and deletes
		(destroys) each row and removes the row dict from self.rows and deletes
		the row's food from the DB."""

		# list of names of foods to delete
		to_delete = []

		# finds which rows to mark for deletion
		for key in self.rows.keys():
			if self.rows[key]['cb_var'].get() == 1:
				to_delete.append(self.rows[key]['name_entry'].get())

		# destroys and removes the rows marked for deletion
		for key in to_delete:
			self._delete_row(self.rows[key], True)

			# deletes the food from fooditem DB
			fooditemdao.delete_food(key)
			productdao.delete_product_by_foodname(key)
			mealdao.delete_food_with_name(key)



	def _get_all_foods_from_sheet(self):
		"""Returns a list of FoodItems based off what's in the sheet"""
		foods = []

		if not self._is_sheet_filled_out():
			return False

		for row in self.rows.values():
			food = self._create_fooditem_from_row_dict(row)
			foods.append(food)

		return foods

	def _create_fooditem_from_row_dict(self, row_dict):
		"""Returns a FoodItem representing the arg row_dict."""
		food = FoodItem()
		infos = ('name_entry', 'ss_entry', 'unit_entry', 'cal_entry', 'carb_entry', 
				'fat_entry', 'protein_entry', 'fiber_entry', 'sugar_entry')
		food_info = []
		for key in row_dict.keys():
			if key in infos:
				food_info.append(row_dict[key].get())
		food.set_info_from_string_list(food_info)
		return food

	def _get_food_from_current_row(self, row):
		"""Returns a FoodItem from info in arg row.
		Checking for validity of row should be done before calling this func."""
		info = []
		food = FoodItem()
		for e in row:
			info.append(e.get())
		food.set_info_from_string_list(info)
		return food




		
	def save_changes(self):
		# Validate all data in the sheet
		# Returns False early if any validation failss

		# Checks if every row is either totally full or totally empty
		if not self._is_sheet_filled_out():
			return False

		# Checks that all number columns have valid data (no chars, no negatives)
		if not self.validate_number_columns():
			return False

		# Update the fooditem and product DB.
		self.update_databases()

		# Recalculate column widths in case of name changes
		self._calc_col_widths()

		# clear rows and redraw sheet
		self.reset()

		return True



	def update_databases(self):
		"""Checks which foods have been modified (all but name can be changed).
		If none were changed, 'No changes' is displayed.
		Else, changes are saved to the db and 'Changes saved' is displayed."""	
		sheet_foods = self._get_all_foods_from_sheet()

		db_foods = fooditemdao.retrieve_all_foods()
		changes_made = False
		for i in range(len(db_foods)):

			if not sheet_foods[i].is_info_same(db_foods[i]):
				food = sheet_foods[i]
				fooditemdao.update_food(sheet_foods[i], sheet_foods[i].name)
				changed_product = Product()
				self.update_product_db(food)
				changes_made = True
		if changes_made:
			self.lbl_status.config(text="Changes saved")

		else:
			self.lbl_status.config(text="No changes")
		self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))


	def update_product_db(self, food):
		if self._is_unit_different(food):
			old_product = productdao.retrieve_products_by_name(food.name)[0]

			tup = (old_product.foodname, old_product.amount, food.unit, old_product.cost)
			new_product = Product()
			new_product.set_info_from_tuple(tup)
			productdao.update_product(new_product)



	def _is_unit_different(self, food):
		"""Checks if the arg food has a different unit than
		the same row in the products DB's unit."""
		product = productdao.retrieve_products_by_name(food.name)[0]
		if product.unit == food.unit:
			return False
		else:
			return True


	def validate_number_columns(self):
		"""Validates the cells of a row in a number column.
		A number column is a column where the data should only be a number
		(and a positive one)"""

		# First check if any cells are empty
		if not self._is_sheet_filled_out():
			return False

		num_cols = ('ss', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
		for row in self.rows.values():
			for key in row.keys():
				if key in num_cols:
					try:
						float(row[key].get())
					except ValueError:
						messagebox.showerror(f"Error", f"Values in '{key}' column must be a valid number.")
						return False
					if float(row[key].get()) < 0:
						messagebox.showerror(f"Error", f"Values in column '{key}' must be positive.")
						return False
		return True

	def _has_duplicate_names(self):
		"""Returns False if all names in the sheet are unique
		Displays an error and returns True otherwise.
		It is case sensitive (names can be the same if different capitalization)
		Doesn't validate is rows are empty or not because this should be done before
		calling this function."""
		name_set = set()
		for row in self.rows:
			name = row[0].get()
			if name in name_set:
				messagebox.showerror("Duplicate names not allowed", f"Food named '{name}' exists more than once")
				return True
			if name != "":
				name_set.add(name)
		return False

	def _delete_row(self, row_dict, pop):
		"""
		row_dict -> dictionary
		pop -> boolean
		Destroys row based on arg row_dict. If pop is True, pops the row from self.rows"""
		# saves name for later reference
		name = row_dict['name_entry'].get()

		# destroys all widgets in row
		for key in row_dict.keys():
			if key == 'cb_var':
				continue
			row_dict[key].destroy()

		# removes row from self.rows if pop
		if pop:
			self.rows.pop(name)
		


	def clear_sheet(self):
		"""Removes all cells/entries from the sheet and empties self.rows"""
		for row_dict in self.rows.values():
			self._delete_row(row_dict, False)

		self.rows = {}
		

	def reset(self):
		"""Removes all rows from the sheet, empties self.rows, and creates the sheet from scratch"""
		self.clear_sheet()
		self.draw_sheet()