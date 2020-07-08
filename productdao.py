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
			foodname text, amount integer, unit text, cost real, key text
			)""")
		self.conn.commit()



	def insert_product(self, product):
		"""Inserts param Product into the db."""
		key = self.generate_unique_key()
		new_dict = {'foodname': product.foodname, 'amount': product.amount,
			 'unit': product.unit, 'cost': product.cost, 'key': key}
		with self.conn:
			self.c.execute("""INSERT INTO products VALUES(
				:foodname, :amount, :unit, :cost, :key
				)""", new_dict)

	def update_product(self, product):
		"""
		foodname -> str
		product -> Product object
		"""
		key = self._get_product_keys_with_name(product.foodname)[0]
		new_dict = {'foodname': product.foodname, 'amount': product.amount,
			'unit': product.unit, 'cost': product.cost, 'key':key}
		with self.conn:
			self.c.execute("""UPDATE products SET foodname=:foodname, amount=:amount, 
				unit=:unit, cost=:cost, key=:key WHERE foodname=:foodname""", new_dict)
		return self.c.rowcount



	def delete_product_by_foodname(self, foodname):
		with self.conn:
			self.c.execute("DELETE FROM products WHERE foodname = ?", (foodname,))
		return self.c.rowcount



	def delete_product_by_key(self, key):
		"""Tries to delete the product that has the param key."""
		with self.conn:
			self.c.execute("DELETE FROM products WHERE key = ?", (key,))
		return self.c.rowcount

	def generate_unique_key(self):
		k = []
		while len(k) < 10:
			l_u = random.randint(0, 1)
			c = chr(random.randint(65, 90))
			if l_u == 0:
				c = c.lower()
			k.append(c)
		key = "".join(k)
		if key in self.get_all_keys():
			key = self.generate_unique_key()
		return key

	def get_all_keys(self):
		with self.conn:
			self.c.execute("""SELECT key FROM products""")
			keys_tup_list = self.c.fetchall()
		# return a list of keys instead of a list of tuples
		keys = [item[0] for item in keys_tup_list]
		return keys

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

	def _get_product_keys_with_name(self, name):
		"""Takes str name as arg. Returns a list of keys for all
		rows in the DB where foodname matches arg name."""
		with self.conn:
			self.c.execute("SELECT key FROM products WHERE foodname=?", (name,))
			tup_list = self.c.fetchall()
		key_list = [tup[0] for tup in tup_list]
		return key_list



	def _retrieve_product_by_key(self, key):
		"""Takes arg key. Searches DB for the row where the key column matches
		the arg key. If the key is not in the DB, returns None.
		Else returns a Product object."""
		all_keys = self.get_all_keys()
		if key not in all_keys:
			return None
		with self.conn:
			self.c.execute("SELECT * FROM products WHERE key=?", (key,))
			tup_list = self.c.fetchall()
		product = self._convert_to_products_list(tup_list)
		return product[0]


	def retrieve_products_by_name(self, name):
		"""Takes arg name and returns a list of Product objects 
		whose name column matches arg name"""
		keys = self._get_product_keys_with_name(name)
		products_list = []
		for key in keys:
			products_list.append(self._retrieve_product_by_key(key))
		return products_list


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


	def _is_product_unique(self, product):
		"""Checks if param product is unique in the DB.
		i.e. if another product exists with same name, 
		amount, unit, and cost, returns False.
		Otherwise returns True.
		This is to deal with hard duplicates, but still
		allow soft duplicates (same name, same unit, different
		cost and amount)"""

		# for p in self.
		pass



