import sqlite3

class GroceryDAO:
	def __init__(self, db_name="grocery.db"):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS grocery (
			name text, amount integer, type text)""")
		self.conn.commit()

	def insert_food(self, food_info):
		"""Takes arg of food_info -> dict of format
		{name: "foodname", amount: 4, type: "product"}"""
		with self.conn:
			self.c.execute("""INSERT INTO grocery VALUES(
				:name, :amount, :type)""", food_info)

	def clear_db(self):
		with self.conn:
			self.c.execute("""DELETE FROM grocery""")

	def retrieve_data(self):
		with self.conn:
			self.c.execute("""SELECT * FROM grocery""")
			tup_list = self.c.fetchall()

		data = {}
		for tup in tup_list:
			data[tup[0]] = {"amount": tup[1], "type": tup[2]}
		return data
