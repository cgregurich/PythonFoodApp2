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




info_dict = {'foodname': 'kale', 'amount': 400, 'unit': 'g', 'cost': '2.98'}

p = Product(info_dict)

fooditemdao = FoodItemDAO()
productdao = ProductDAO()

print(type(p.foodname))
print(type(p.amount))
print(type(p.unit))
print(type(p.cost))

# productdao.insert_product(p)

# all_products = productdao.retrieve_all_products()
# for p in all_products:
# 	print(p)

# p1 = user_input_product()
# print(p1)

# keys = productdao._get_product_keys_with_name('kale')
# print(f"kale keys: {keys}")
# # product = productdao._retrieve_product_by_key(keys[0])
# product = productdao._retrieve_product_by_key('notakey')
# print(product)
# products_list = productdao.retrieve_products_by_name('kale')
# for p in products_list:
# 	print(p)


