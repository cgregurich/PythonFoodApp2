from product import Product
from productdao import ProductDAO
from fooditemdao import FoodItemDAO

def user_input_product():
	foodname = input("Foodname: ")
	amount = int(input("Amount per unit: "))
	unit = input("Unit of measurement: ")
	cost = float(input("Cost of 1 unit: $"))

	tup = (foodname, amount, unit, cost)
	p = Product()
	p.set_info_from_tuple(tup)


	return p

def ask_for_prices_of_foods_in_db():
	for food in fooditemdao.retrieve_all_foods():
		info = {'foodname': food.name, 'amount': None, 'unit': food.unit, 'cost': None}
		info['amount'] = int(input(f"Enter amount of {food.unit} in 1 unit of {food.name}: "))
		info['cost'] = float(input(f"Enter cost of 1 unit of {food.name}: $"))

		product = Product(info)
		productdao.insert_product(product)




info_dict = {'foodname': 'oats', 'amount': 1176, 'unit': 'g', 'cost': '2.67'}

p = Product(info_dict)

fooditemdao = FoodItemDAO()
productdao = ProductDAO()

# productdao.insert_product(p)

# all_products = productdao.retrieve_all_products()
# for p in all_products:
# 	print(p)

# p1 = user_input_product()
# print(p1)

ask_for_prices_of_foods_in_db()

