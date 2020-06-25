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
		self.calc_col_widths()

		

		# Create frames (controls frame and cells frame)
		self.frame_controls = Frame(self)
		self.frame_cells = Frame(self)

		# Put the frames on the window
		self.frame_controls.grid(row=0, column=0, sticky=N, padx=(10, 0), pady=(10, 0))
		self.frame_cells.grid(row=0, column=1, sticky=N, padx=10)


		# Vars for the option menus
		self.sort_mode = StringVar()
		self.sort_order = StringVar()

		# Tuple of options for what order to sort the foods in
		self.SORT_ORDERS = ("Ascending", "Descending")

		# Boolean flag to know if we need to resort the sheet when changes are made
		self.sorted = False

		# Create controls
		btn_back = ttk.Button(self.frame_controls, text="Back", command=lambda: controller.show_frame(startpage.StartPage))
		btn_add_row = ttk.Button(self.frame_controls, text="Add row", command=self.create_empty_row)
		optionmenu_sort_mode = ttk.OptionMenu(self.frame_controls, self.sort_mode,"Unsorted", command=self.sort_mode_selected,  *self.HEADERS)
		optionmenu_sort_order = ttk.OptionMenu(self.frame_controls, self.sort_order, "Order", command=self.sort_order_selected, *self.SORT_ORDERS)

		# Label for displaying that changes were saved
		self.lbl_status = Label(self.frame_controls, text="", fg="green")		
		btn_save_changes = ttk.Button(self.frame_controls, text="Save changes", command=self.save_clicked)

		

		# Put the controls on the grid
		btn_back.grid(row=0, column=0, pady=self.PADY_CONTROLS)
		btn_add_row.grid(row=1, column=0, pady=self.PADY_CONTROLS)
		optionmenu_sort_mode.grid(row=2, column=0, sticky=EW, pady=self.PADY_CONTROLS)
		optionmenu_sort_order.grid(row=3, column=0, sticky=EW, pady=self.PADY_CONTROLS)
		self.lbl_status.grid(row=4, column=0, pady=self.PADY_CONTROLS, padx=10)
		btn_save_changes.grid(row=5, column=0, pady=self.PADY_CONTROLS, padx=12) # padx of 10 to make optionmenus' size static




		# List of lists for the rows of cells in the sheet
		# each element in this list is a list of Entry widgets; each is a row. Each Entry in a row is a cell.
		self.rows = []


		# Create the sheet
		self.draw_sheet()


	def draw_sheet(self, all_foods=None):
		"""Draws the sheet; used for initializing the sheet."""
		self.create_col_headers()

		# if no arg was passed for all_foods, retrieve all the foods from db
		if not all_foods:
			all_foods = fooditemdao.retrieve_all_foods()

		# If no foods in db, create a single empty row
		if not all_foods:
			self.create_row()
		# If there are foods in the db, then display each on a separate row
		else:
			for food in all_foods:
				row = self.create_row(food)


	def create_col_headers(self):
		"""Creates and places Labels with the column headers in row 0 of frame_cells"""
		for i in range(self.width):
			l = Label(self.frame_cells, text=self.HEADERS[i].upper(), font=MONOSPACED_FONT)
			l.grid(row=0, column=i)

	def create_row(self, food=None):
		"""Creates a row in the sheet.
		If arg food is None, each cell will be empty.
		If there is arg food, each cell will be filled with the appropriate data"""

		row = []


		for i in range(self.width):
			e = Entry(self.frame_cells, width=self.col_widths[i], font=MONOSPACED_FONT)
			if food:
				e.insert(0, food.info[self.HEADERS[i]])
			e.grid(row=len(self.rows)+1, column=i)
			row.append(e)

		self.rows.append(row)


	def calc_col_widths(self):
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


	def create_empty_row(self):
		"""Creates an empty row on the sheet"""
		self.create_row(None)

	def _is_sheet_filled_out(self):
		"""Checks if each row is either all filled out, or all empty.
		If either of these, True is returned. 
		But if a row has some info and some blanks, error is shown and False is returned"""

		for row in self.rows:
			if self._is_row_empty(row) == -1:
				messagebox.showerror(f"Can't add food" , f"row {self.rows.index(row)+1} is missing info")
				return False
		return True




	def _is_row_empty(self, row):
		"""Checks if the arg row's entries are all empty, all full, or a mix
		Returns 0 if all empty
		Returns 1 if all filled
		Returns -1 if some filled, some empty"""

		counter = []
		for i in range(self.width):
			counter.append(-1)

		for e in row:
			if e.get() == "":
				counter[row.index(e)] = 0
			else:
				counter[row.index(e)] = 1

		if 0 in counter and 1 in counter: # has empty and filled entries -> row has some filled cells
			return -1

		elif 0 in counter: # all entries empty -> row is entirely empty
			return 0

		else: # all entries full -> row is entirely full
			return 1


	def refresh_db_from_sheet(self):
		"""Clears the database and rewrites all foods from the sheet to the database"""
		
		sheet_foods = self.get_all_foods_from_sheet()

		fooditemdao.clear_database()

		for food in sheet_foods:
			fooditemdao.insert_food(food)


	def get_all_foods_from_sheet(self):
		"""Returns a list of FoodItems based off what's in the sheet"""

		foods = []

		if self._is_sheet_filled_out():
			for row in self.rows:
				# create FoodItem for the current row if the row is filled and add it to list foods
				if self._is_row_empty(row) == 1:
					foods.append(self._get_food_from_current_row(row))
		return foods


	def _get_food_from_current_row(self, row):
		"""Returns a FoodItem from info in arg row.
		Checking for validity of row should be done before calling this func."""
		info = []
		food = FoodItem()
		for e in row:
			info.append(e.get())
		food.set_info_from_string_list(info)
		return food


	def save_clicked(self):
		"""Func bound to Save Changes button
		When clicked, func save_changes is called
		If save_changes returns True, label displays
		that changes were successfully saved"""
		if self.save_changes():
			self.lbl_status.config(text="Changes saved")
			self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))


		
	def save_changes(self):
		# Validate all data in the sheet
		# Returns False early if any validation failss

		# Checks if every row is either totally full or totally empty
		if not self._is_sheet_filled_out():
			return False

		# Checks if any cells in the name column have the same text
		if self._has_duplicate_names():
			return False

		# Checks that all number columns have valid data (no chars, no negatives)
		if not self.validate_number_columns():
			return False

		
		# Overwrite DB with the data in the sheet
		self.refresh_db_from_sheet()

		# Recalculate column widths in case of name changes
		self.calc_col_widths()

		# clear rows and redraw sheet
		self.reset()

		# if the sheet has no rows, add an empty row
		if self._is_sheet_empty():
			self.create_empty_row()

		# if the sheet was sorted prior to changes, sort again so 
		# any changes don't mess up the sort
		if self.sorted:
			self.sort_sheet()
		return True


	def _is_sheet_empty(self):
		"""Returns True if the sheet contains zero rows
		Returns False otherwise"""
		return len(self.rows) == 0

	def validate_number_columns(self):
		"""Validates the cells of a row in a number column.
		A number column is a column where the data should only be a number
		(and a positive one)"""
		for row in self.rows:

			# if row is totally empty, the number cols don't need to be validated
			if self._is_row_empty(row) == 0:
				continue

			for i in range(self.width):
				if i != 0 and i != 2: # is a number column
					try:
						float(row[i].get())
					except ValueError:
						messagebox.showerror(f"Error: (Row {self.rows.index(row)+1}, Column {i})", 
											 f"Info in column {self.HEADERS[i].upper()} must be a valid number.")
						return False
					if float(row[i].get()) < 0:
						messagebox.showerror(f"Error: (Row {self.rows.index(row)+1}, Column {i})",
											f"Info in column {self.HEADERS[i].upper()} must be positive.")
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




	def sort_mode_selected(self, arg):
		"""If both sort_mode and sort_order have been selected,
		the sheet is sorted"""

		# Checks the other sort OM
		# If other is non-default value, then sort happens
		if self.sort_order.get() != "Order": # order has been selected
			self.sort_sheet()


	def sort_order_selected(self, arg):
		"""If both sort_order and sort_mode have been selected,
		the sheet is sorted"""

		# Checks the other sort OM
		# If other is non-default value, then sort happens
		if self.sort_mode.get() != "Unsorted": # mode has been selected
			self.sort_sheet()

	def sort_sheet(self):
		"""Sorts the entire database according to selected mode and order.
		Then clears sheet and redraws the foods in the sheet.
		Sets class var sorted to True, so when changes are made, the sheet remains
		sorted."""
		self.sorted = True
		order = "ASC" if self.sort_order.get() == "Ascending" else "DESC"
		all_foods = fooditemdao.sort_foods(self.sort_mode.get(), order)

		self.clear_sheet()
		self.draw_sheet(all_foods)

	def clear_sheet(self):
		"""Removes all cells/entries from the sheet and empties self.rows"""
		for row in self.rows:
			for e in row:
				e.destroy()
		self.rows = []
		

	def reset(self):
		"""Removes all rows from the sheet, empties self.rows, and creates the sheet from scratch"""
		self.clear_sheet()
		self.draw_sheet()