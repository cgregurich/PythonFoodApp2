from fooditem import FoodItem
import random
from product import Product

import sqlite3

class ProductDAO:
	def __init__(self, db_name='products.db'):
		"""Creates the database of param db_name (if no name is supplied, defaults to
		products.db). Creates table prices if it doesn't yet exist."""
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS products (
			foodname text, amount integer, unit text, cost real, calpercost integer)""")
		self.conn.commit()



	def insert_product(self, product):
		"""Inserts param Product into the db."""
		new_dict = {'foodname': product.foodname, 'amount': product.amount,
			 'unit': product.unit, 'cost': product.cost, 'calpercost': product.calpercost}
		with self.conn:
			self.c.execute("""INSERT INTO products VALUES(
				:foodname, :amount, :unit, :cost, :calpercost
				)""", new_dict)

	def update_product(self, product):
		"""
		foodname -> str
		product -> Product object
		"""
		new_dict = {'foodname': product.foodname, 'amount': product.amount,
			'unit': product.unit, 'cost': product.cost, 'calpercost': product.calpercost}
		with self.conn:
			self.c.execute("""UPDATE products SET foodname=:foodname, amount=:amount, 
				unit=:unit, cost=:cost, calpercost=:calpercost WHERE foodname=:foodname""", new_dict)
		return self.c.rowcount



	def delete_product_by_foodname(self, foodname):
		with self.conn:
			self.c.execute("DELETE FROM products WHERE foodname = ?", (foodname,))
		return self.c.rowcount





	# def generate_unique_key(self):
	# 	k = []
	# 	while len(k) < 10:
	# 		l_u = random.randint(0, 1)
	# 		c = chr(random.randint(65, 90))
	# 		if l_u == 0:
	# 			c = c.lower()
	# 		k.append(c)
	# 	key = "".join(k)
	# 	if key in self.get_all_keys():
	# 		key = self.generate_unique_key()
	# 	return key


	def retrieve_all_foodnames(self):
		"""Returns a list of all Product's foodnames from products table in DB."""
		with self.conn:
			self.c.execute("SELECT foodname FROM products")
			foodnames = self.c.fetchall()
		# return list of str instead of list of tuples
		names_list = [item[0] for item in foodnames]
		return names_list

	def retrieve_all_products(self):
		"""Returns list of Product objects from the db."""
		with self.conn:
			self.c.execute("SELECT * FROM products")
			tup_list = self.c.fetchall()
		products = self._convert_to_products_list(tup_list)
		return products

	def retrieve_all_products_as_dict(self):
		"""Returns dictionary of format: {product1name: <product object>, product2name: <product object>}"""
		products = self.retrieve_all_products()
		p_dict = {}
		for p in products:
			p_dict[p.foodname] = p
		return p_dict

	def _convert_to_products_list(self, tup_list):
		"""Helper method for retrieve_all_products()
		Takes a list of tuples as arg.
		Each tuple in the list is the information for
		a Product object. Turn each tuple into a Product object
		and return a list of all the Products."""
		products = []
		for tup in tup_list:
			new_product = Product()
			new_product.set_info_from_tuple(tup)
			products.append(new_product)
		return products






	def retrieve_product_by_name(self, name):
		"""Takes arg name and returns a list of Product objects 
		whose name column matches arg name"""
		with self.conn:
			self.c.execute("""SELECT * FROM products WHERE foodname=?""", (name, ))
			fetched_info = self.c.fetchone()
			if fetched_info is None:
				return None
			product = Product()
			product.set_info_from_tuple(fetched_info)
		return product


	# for testing, prob not a useful func
	def print_all_products(self):
		with self.conn:
			self.c.execute("""SELECT * FROM products""")
			info_tup_list = self.c.fetchall()
			if not info_tup_list: # if DB is empty
				return None
		for tup in info_tup_list:
			print("\n")
			for t in tup:
				print(t)






