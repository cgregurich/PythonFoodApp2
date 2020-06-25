from meal import Meal
import sqlite3
from fooditem import FoodItem

class MealDAO:
    def __init__(self, db_name='meal.db'):
        """Creates the database of param db_name (if no name is supplied, defaults to
        meal.db). Creates table meals if it doesn't yet exist"""
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS meals (
                mealname text, foodname text, ss integer, unit text, cal integer, carb integer, 
                fat integer, protein integer, fiber integer, sugar integer        
                )""")
        self.conn.commit()

    # test
    def insert_meal(self, meal):
        """Iterates through param meal's list of FoodItems
        For each FoodItem, a dict is populated with the food's info
        This dict is used as the insertion value for the db query"""
        dict = {'mealname': meal.meal_name, 'foodname': '', 'ss': 0, 'unit': '', 'cal': 0, 'carb': 0,
                'fat': 0, 'protein': 0, 'fiber': 0, 'sugar': 0}
        with self.conn:
            for food in meal.foods:
                for key, value in food.info.items():
                    if key == 'name':
                        dict['foodname'] = value
                    else:
                        dict[key] = food.info[key]
                self.c.execute("""INSERT INTO meals VALUES(
                :mealname, :foodname, :ss, :unit, :cal, :carb, :fat, :protein, :fiber, :sugar
                )""", dict)

    # test
    def delete_meal(self, meal_name):
        """Deletes all fields whose col mealname equals the param meal_name"""
        with self.conn:
            self.c.execute("""DELETE FROM meals WHERE mealname=?""", (meal_name,))
        return self.c.rowcount

    # test
    def update_meal(self, meal_name, updated_food):
        dict = {'mealname': meal_name, 'foodname': '', 'ss': 0, 'unit': '', 'cal': 0, 'carb': 0,
                'fat': 0, 'protein': 0, 'fiber': 0, 'sugar': 0}

        for key, value in updated_food.info.items():
            if key == 'mealname':
                continue
            if key == 'name':
                dict['foodname'] = updated_food.name
            else:
                dict[key] = value
        with self.conn:
            self.c.execute("""UPDATE meals SET ss=:ss, unit=:unit, cal=:cal,
                            carb=:carb, fat=:fat, protein=:protein, fiber=:fiber, sugar=:sugar
                             WHERE mealname=:mealname AND foodname=:foodname""", dict)
        return self.c.rowcount

    # test
    def update_meal_names_of_foods(self, new_old_tup):
        """Changes all mealnames of foods with the meal name of arg[1] to arg[0]
        Receives a two element tuple of format (new_name, old_name)"""
        with self.conn:
            self.c.execute("UPDATE meals SET mealname=:new_name WHERE mealname=:old_name", new_old_tup)
        return self.c.rowcount



    # test
    def retrieve_meal(self, meal_name):
        with self.conn:
            self.c.execute("SELECT * FROM meals WHERE mealname=?", (meal_name,))
            fetched_info = self.c.fetchall()
        return self.parse_fetched_meal(fetched_info)

    # test
    def parse_fetched_meal(self, tup_list):
        """Func for parsing a single meal i.e. mealname is the same in all tups.
        Returns a Meal object
        Param should be a list of tuples of format:
        (mealname, foodname, ss, unit, cal, carb, fat, protein, fiber, sugar)
        Returns a Meal object"""
        info_dict = {'name': None, 'ss': 0, 'unit': None, 'cal': 0, 'carb': 0, 'fat': 0,
                'protein': 0, 'fiber': 0, 'sugar':0 }
        foods_list = []
        if not tup_list:
            return None
        for tup in tup_list:
            i = 1
            for key in info_dict.keys():
                info_dict[key] = tup[i]
                i += 1
            foods_list.append(FoodItem(info_dict))
        meal = Meal(tup_list[0][0])
        meal.set_foods_from_list(foods_list)
        return meal

    # test
    def retrieve_all_meals(self):
        """Should return a list of all Meals in db"""
        return self.parse_fetched_meals(self.retrieve_all_foods())

    # test
    def retrieve_all_foods(self):
        """Returns list of tups of all fields in DB
               Format is: (mealname, foodname, ss, unit, cal, carb, fat, protein, fiber, sugar)"""
        with self.conn:
            self.c.execute("""SELECT * FROM meals""")
            all_foods_tups = self.c.fetchall()
        return all_foods_tups

    # NO TESTS WRITTEN
    def retrieve_all_food_objects(self):
        """Returns a list of FoodItem objects from foods in DB"""
        with self.conn:
            self.c.execute("""SELECT * FROM meals""")
            all_foods_tups = self.c.fetchall()
        foods = []
        for food_tup in all_foods_tups:
            new_food = FoodItem()
            new_food.set_info_from_tuple(food_tup[1:])
            foods.append(new_food)
        return foods


    # NO TESTS WRITTEN
    def retrieve_all_food_names_set(self):
        """Returns a "set" of all foods' names in the DB.
        Because it's a set, it's cast as a list then returned
        to keep some sort of consistency with order."""
        with self.conn:
            self.c.execute("""SELECT foodname FROM meals""")
            all_food_names = self.c.fetchall()
        all_food_names = [food[0] for food in all_food_names]

        names = list(set(all_food_names))
        names.sort()
        return names



    # test
    def parse_fetched_meals(self, tup_list):
        """Takes fooditem info from meals db and turns it all into a list of Meals
        Receives a list of tuples of format:
         (mealname, foodname, ss, unit, cal, carb, fat, protein, fiber, sugar)
         Mealname will not be the same in all. Each matching mealname must be put into
         the same list."""
        meal_names = self.retrieve_all_meal_names()
        meals_list = []

        all_foods = self.retrieve_all_foods()
        for meal_name in meal_names:
            cur_foods_list = []
            for tup in all_foods:
                if tup[0] == meal_name:
                    food = FoodItem()
                    food.set_info_from_tuple(tup[1:])
                    cur_foods_list.append(food)
            meal = Meal(meal_name)
            meal.set_foods_from_list(cur_foods_list)
            meals_list.append(meal)
        return meals_list

    # test
    def retrieve_all_meal_names(self):
        """Returns list of unique mealnames"""
        with self.conn:
            self.c.execute("""SELECT DISTINCT mealname FROM meals""")
            meal_names = self.c.fetchall() # returns a list of tups
        # convert list of tups to list of strings
        meal_names_list = []
        for tup in meal_names:
            meal_names_list.append(tup[0])
        return meal_names_list

    # test
    def delete_food_with_name(self, food_name):
        with self.conn:
            self.c.execute("""DELETE FROM meals WHERE foodname = ?""", (food_name,))
        return self.c.rowcount








