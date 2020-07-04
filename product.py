
"""Class to model a food product you buy at the store.
Contains information like name, amount per product, 
unit of measurement for the amount, and cost per product.
"""

class Product:
	def __init__(self, info_dict=None):
		self.info = {'foodname': None, 'amount': None, 'unit': None,
				'cost': None}
		if info_dict:
			for key in self.info.keys():
				self.info[key] = info_dict[key]
			self.numberize_info()


	def __str__(self):
		rtrn = "\n"
		for key in self.info.keys():
			rtrn += f"{key}: {self.info[key]}   "
		return rtrn

	def set_info_from_tuple(self, info_tup):		
		i = 0
		for key in self.info.keys():
			self.info[key] = info_tup[i]
			i += 1
		self.numberize_info()

	def numberize_info(self):
		
		try:
			int(self.amount)
		except ValueError:
			raise ValueError("Amount must be number.")
		if self.amount != int(self.amount):
			raise ValueError("Amount must be integer.")

		try:
			float(self.cost)
		except ValueError:
			raise ValueError("Cost must be number.")

		self.info['amount'] = int(self.amount)
		self.info['cost'] = "{:.2f}".format(float(self.cost))
	
	def is_info_same(self, product):
		"""Returns True if param product has the same
		values for class attributes as self.
		Else returns False."""
		for key in self.info.keys():
			if product[key] != self.info[key]:
				return False
		else:
			return True







	@property
	def foodname(self):
		return self.info['foodname']

	@property
	def amount(self):
		return self.info['amount']

	@property
	def unit(self):
		return self.info['unit']

	@property
	def cost(self):
		return self.info['cost']

