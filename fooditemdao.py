from fooditem import FoodItem

import sqlite3


class FoodItemDAO:
    def __init__(self, db_name='fooditem.db'):
        """Creates the database of param db_name (if no name is supplied, defaults to
        fooditem.db). Creates table fooditems if it doesn't yet exist"""
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS fooditems (
                name text, ss integer, unit text, cal integer, carb integer, 
                fat integer, protein integer, fiber integer, sugar integer        
                )""")
        self.conn.commit()


    def clear_database(self):
        with self.conn:
            self.c.execute("""DELETE FROM fooditems""")

    def insert_food(self, food):
        """Inserts the FoodItem param food into the db"""
        with self.conn:
            self.c.execute("""INSERT INTO fooditems VALUES(
            :name, :ss, :unit, :cal, :carb, :fat, :protein, :fiber, :sugar
            )""", food.info)

    def delete_food(self, name):
        """Deletes the food(s) that matches the param name from the db"""
        with self.conn:
            self.c.execute("""DELETE FROM fooditems WHERE name=?""", (name,))
        return self.c.rowcount

    def update_food(self, updated_food, old_name):
        """Updates the food in the db that has param old_name with all of the info
        from param FoodItem updated_food. Name can be updated"""
        with self.conn:
            if old_name != updated_food.name:
                self.c.execute("""UPDATE fooditems SET name=? WHERE name=?""", (updated_food.name, old_name))
            self.c.execute("""UPDATE fooditems SET name=:name, ss=:ss, unit=:unit, cal=:cal,
                            carb=:carb, fat=:fat, protein=:protein, fiber=:fiber, 
                            sugar=:sugar WHERE name=:name""", updated_food.info)
        return self.c.rowcount

    def retrieve_food(self, name):
        """Returns a FoodItem from the db that has the param name
        (names should be unique, and this func assumes such)"""
        with self.conn:
            self.c.execute("""SELECT * FROM fooditems WHERE name=?""", (name,))
            fetched_info = self.c.fetchone()
            if fetched_info is None:
                return None
            food = FoodItem()
            food.set_info_from_tuple(fetched_info)
        return food

    def retrieve_all_foods(self):
        """Return all FoodItems from the db as a list of FoodItems"""
        with self.conn:
            self.c.execute("""SELECT * FROM fooditems""")
            info_tup_list = self.c.fetchall()
            if not info_tup_list:
                return None
        foods_list = self._convert_to_food_items_list(info_tup_list)
        return foods_list

    def _convert_to_food_items_list(self, info_tup_list):
        """Receives param of a list of tuples which are info for a FoodItem.
        Returns a list of FoodItems with the info supplised by the param"""
        if not info_tup_list:
            return None


        foods_list = []
        for info_tup in info_tup_list:
            if len(info_tup) != 9:
                raise ValueError("Element of list is not tuple of 9 elements.")
            food = FoodItem()
            food.set_info_from_tuple(info_tup)
            foods_list.append(food)
        return foods_list

    def sort_foods(self, sort_type, order):
        """Sorts the FoodItems in the db and returns a FoodItems list of those sorted items
        Param sort_type is a string of the column name
        Param order is either 'ASC' or 'DESC'"""
        crits = ('name', 'ss', 'unit', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
        if sort_type not in crits:
            raise ValueError('Invalid arg for criteria')

        if order != 'ASC' and order != 'DESC':
            raise ValueError('Invalid arg for order')

        with self.conn:
            self.c.execute(f"SELECT * FROM fooditems ORDER BY {sort_type} {order}")
            sorted_list = self.c.fetchall()
        sorted_list = self._convert_to_food_items_list(sorted_list)
        return sorted_list

    def retrieve_all_food_names(self):
        """Returns a list of all FoodItems' names from fooditems table in DB"""
        with self.conn:
            self.c.execute("SELECT name FROM fooditems")
            names = self.c.fetchall()
        # return list of str instead of list of tuples
        names_list = [name[0] for name in names]
        return names_list