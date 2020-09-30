from tkinter import *
from tkinter import ttk
from fooditem import FoodItem
from fooditemdao import FoodItemDAO
from mealdao import MealDAO
from productdao import ProductDAO
import math





# how to calculate how many to order:
# if product:
# 	howmanytoorder = roundup(#productsneeded - amtininventory) | (validate for negative -> 0)
# 	costoforder = howmanytoorder * costperproduct
# elif unit:
# 	howmanytoorder: roundup((amtneeded - amtininventory) / amtperproduct)
# 	costoforder = howmanytoorder * costperproduct











MONOSPACED = ("Consolas", 10)
BOLD = ("Consolas", 10, "bold")

fooditemdao = FoodItemDAO()
mealdao = MealDAO()
productdao = ProductDAO()



# DISPLAY RICE AND ALMOND MILK
foodnames = "rice", "almond milk"
row_dicts = []



def draw_headers():
	headers = ('foodname', 'amtneeded', 'amtperproduct', 'costperproduct', '#productsneeded', 'amtininventory', 
		'inventorytype', 'howmanytoorder', 'costoforder')
	col = 0
	for h in headers:
		Label(root, text=h, font=BOLD, borderwidth=2, relief="groove").grid(row=0, column=col)
		col += 1


def _calc_daily_amount(foodname):
	all_foods = mealdao.retrieve_all_food_objects()
	total_amount = 0
	for food in all_foods:
		if food.name == foodname:
			total_amount += food.ss
	return total_amount


def draw_foods(days):
	for foodname in foodnames:
		row_info = generate_row_info(foodname, days)
		col = 0
		widgets_dict = {}

		for key, value in row_info.items():
			if key == 'inventorytype':
				om_var = StringVar()
				unit = fooditemdao.retrieve_food(foodname).unit
				optionmenu = ttk.OptionMenu(root, om_var, 'product', *('product', unit))
				optionmenu.grid(row=master_row.get(), column=col)
				widgets_dict[key] = optionmenu
				widgets_dict['om_var'] = om_var
			else: # create a widget
				entry = ttk.Entry(root, font=MONOSPACED, foreground="black")
				# print(f"\n\nvalue: {value}")
				entry.insert(0, value)
				if key != 'amtininventory':
					entry.config(state=DISABLED)
				entry.grid(row=master_row.get(), column=col)
				widgets_dict[key] = entry
			col += 1
		row_dicts.append(widgets_dict)
		master_row.set(master_row.get() + 1)



def generate_row_info(foodname, days):
	row_info = {
		'foodname': foodname,
		'amtneeded': _calc_daily_amount(foodname) * days,
		'amtperproduct': productdao.retrieve_product_by_name(foodname).amount,
		'costperproduct': productdao.retrieve_product_by_name(foodname).cost,
		'#productsneeded': round((_calc_daily_amount(foodname) * days) / productdao.retrieve_product_by_name(foodname).amount, 2), 
		'amtininventory': 0,
		'inventorytype': "none selected",
		'howmanytoorder': 0,
		'costoforder': 0.00,
	}
	# print(row_info)
	# print("\n\n")
	return row_info

def go_clicked():
	for d in row_dicts: # d for dictionary
		if d['om_var'].get() == 'product':
			order_count = math.ceil(float(d['#productsneeded'].get()) - float(d['amtininventory'].get())) # TODO: Input validation
			cost_of_order = order_count * float(d['costperproduct'].get())
		else:
			order_count = math.ceil((float(d['amtneeded'].get()) - float(d['amtininventory'].get())) / float(d['amtperproduct'].get()))
			cost_of_order = order_count * float(d['costperproduct'].get())

		d['howmanytoorder'].config(state=NORMAL)
		d['howmanytoorder'].delete(0, END)
		d['howmanytoorder'].insert(0, order_count)
		d['howmanytoorder'].config(state=DISABLED)

		d['costoforder'].config(state=NORMAL)
		d['costoforder'].delete(0, END)
		d['costoforder'].insert(0, cost_of_order)
		d['costoforder'].config(state=DISABLED)




root = Tk()

draw_headers()
master_row = IntVar()
master_row.set(4)


btn1 = ttk.Button(root, text="1 day", command=lambda: draw_foods(1))
btn2 = ttk.Button(root, text="2 weeks", command=lambda: draw_foods(14))
btn3 = ttk.Button(root, text="Go", command=go_clicked)

btn1.grid(row=1, column=0)
btn2.grid(row=2, column=0)
btn3.grid(row=3, column=0)







root.mainloop()
