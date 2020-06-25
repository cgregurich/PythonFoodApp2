import unittest
from fooditem import FoodItem
from meal import Meal
from mealdao import MealDAO

class TestMealDAO(unittest.TestCase):
    def setUp(self):
        self.meal_dao = MealDAO(':memory:')
        info_1 = {'name': 'apple', 'ss': 30, 'unit': 'g', 'cal': 75, 'carb': 30,
                  'fat': 1, 'protein': 3, 'fiber': 5, 'sugar': 26}
        info_2 = {'name': 'banana', 'ss': 1, 'unit': 'banana', 'cal': 90, 'carb': 25,
                  'fat': 0, 'protein': 1, 'fiber': 2, 'sugar': 16}
        info_3 = {'name': 'potato', 'ss': 50, 'unit': 'g', 'cal': 120, 'carb': 20,
                  'fat': 0, 'protein': 2, 'fiber': 4, 'sugar': 3}
        info_4 = {'name': 'oats', 'ss': 40, 'unit': 'g', 'cal': 150, 'carb': 35,
                  'fat': 5, 'protein': 4, 'fiber': 6, 'sugar': 2}
        self.food_1 = FoodItem(info_1)
        self.food_2 = FoodItem(info_2)
        self.food_3 = FoodItem(info_3)
        self.food_4 = FoodItem(info_4)

        self.meal_1 = Meal('Meal1', self.food_1, self.food_2)
        self.meal_2 = Meal('Meal2', self.food_3, self.food_4)
        self.meal_3 = Meal('Meal3', self.food_1, self.food_2, self.food_3, self.food_4)

    def test_insert_meal(self):
        self.meal_dao.insert_meal(self.meal_1)
        expected_rows = self.meal_1.food_count()
        self.assertEqual(self.meal_dao.c.lastrowid, expected_rows)

        self.meal_dao.insert_meal(self.meal_2)
        expected_rows += self.meal_2.food_count()
        self.assertEqual(self.meal_dao.c.lastrowid, expected_rows)

        self.meal_dao.insert_meal(self.meal_3)
        expected_rows += self.meal_3.food_count()
        self.assertEqual(self.meal_dao.c.lastrowid, expected_rows)


    def test_delete_meal(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)

        # delete a meal that doesn't exist
        self.assertEqual(self.meal_dao.delete_meal('nonexistent'), 0)

        # delete meal_1
        self.assertEqual(self.meal_dao.delete_meal(self.meal_1.meal_name), self.meal_1.food_count())

        # delete meal 2
        self.assertEqual(self.meal_dao.delete_meal(self.meal_2.meal_name), self.meal_2.food_count())

        # try to delete meal 1 after it's been deleted
        self.assertEqual(self.meal_dao.delete_meal(self.meal_1.meal_name), 0)

    def test_update_meal(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        apple_info = {'name': 'apple', 'ss': 60, 'unit': 'g', 'cal': 150, 'carb': 60,
                  'fat': 2, 'protein': 6, 'fiber': 10, 'sugar': 52}
        new_apple = FoodItem(apple_info)
        self.assertEqual(self.meal_dao.update_meal(self.meal_1.meal_name, new_apple), 1)

        # test new info but same name for a food in all three meals
        oats_info = {'name': 'oats', 'ss': 80, 'unit': 'g', 'cal': 300, 'carb': 70,
                  'fat': 10, 'protein': 8, 'fiber': 12, 'sugar': 4}
        new_oats = FoodItem(oats_info)
        self.assertEqual(self.meal_dao.update_meal(self.meal_2.meal_name, new_oats), 1)

        banana_info = info_2 = {'name': 'banana', 'ss': 2, 'unit': 'banana', 'cal': 180,
                                'carb': 30, 'fat': 0, 'protein': 2, 'fiber': 4, 'sugar': 32}
        new_banana = FoodItem(banana_info)
        self.assertEqual(self.meal_dao.update_meal(self.meal_3.meal_name, new_banana), 1)

    def test_retrieve_meal(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        retrieved_meal_1 = self.meal_dao.retrieve_meal('Meal1')
        self.assertEqual(retrieved_meal_1.meal_name, 'Meal1')
        self.assertEqual(retrieved_meal_1.foods[0].name, 'apple')
        self.assertEqual(retrieved_meal_1.foods[1].name, 'banana')
        self.assertEqual(retrieved_meal_1.foods[0].ss, 30)
        self.assertEqual(retrieved_meal_1.foods[1].ss, 1)
        self.assertEqual(retrieved_meal_1.foods[0].unit, 'g')
        self.assertEqual(retrieved_meal_1.foods[1].unit, 'banana')
        self.assertEqual(retrieved_meal_1.foods[0].cal, 75)
        self.assertEqual(retrieved_meal_1.foods[1].cal, 90)
        self.assertEqual(retrieved_meal_1.foods[0].carb, 30)
        self.assertEqual(retrieved_meal_1.foods[1].carb, 25)
        self.assertEqual(retrieved_meal_1.foods[0].fat, 1)
        self.assertEqual(retrieved_meal_1.foods[1].fat, 0)
        self.assertEqual(retrieved_meal_1.foods[0].protein, 3)
        self.assertEqual(retrieved_meal_1.foods[1].protein, 1)
        self.assertEqual(retrieved_meal_1.foods[0].fiber, 5)
        self.assertEqual(retrieved_meal_1.foods[1].fiber, 2)
        self.assertEqual(retrieved_meal_1.foods[0].sugar, 26)
        self.assertEqual(retrieved_meal_1.foods[1].sugar, 16)

        retrieved_meal_2 = self.meal_dao.retrieve_meal('Meal2')
        self.assertEqual(retrieved_meal_2.meal_name, 'Meal2')
        self.assertEqual(retrieved_meal_2.foods[0].name, 'potato')
        self.assertEqual(retrieved_meal_2.foods[1].name, 'oats')
        self.assertEqual(retrieved_meal_2.foods[0].ss, 50)
        self.assertEqual(retrieved_meal_2.foods[1].ss, 40)
        self.assertEqual(retrieved_meal_2.foods[0].unit, 'g')
        self.assertEqual(retrieved_meal_2.foods[1].unit, 'g')
        self.assertEqual(retrieved_meal_2.foods[0].cal, 120)
        self.assertEqual(retrieved_meal_2.foods[1].cal, 150)
        self.assertEqual(retrieved_meal_2.foods[0].carb, 20)
        self.assertEqual(retrieved_meal_2.foods[1].carb, 35)
        self.assertEqual(retrieved_meal_2.foods[0].fat, 0)
        self.assertEqual(retrieved_meal_2.foods[1].fat, 5)
        self.assertEqual(retrieved_meal_2.foods[0].protein, 2)
        self.assertEqual(retrieved_meal_2.foods[1].protein, 4)
        self.assertEqual(retrieved_meal_2.foods[0].fiber, 4)
        self.assertEqual(retrieved_meal_2.foods[1].fiber, 6)
        self.assertEqual(retrieved_meal_2.foods[0].sugar, 3)
        self.assertEqual(retrieved_meal_2.foods[1].sugar, 2)

        retrieved_meal_3 = self.meal_dao.retrieve_meal('Meal3')
        self.assertEqual(retrieved_meal_3.meal_name, 'Meal3')
        self.assertEqual(retrieved_meal_3.foods[0].name, 'apple')
        self.assertEqual(retrieved_meal_3.foods[1].name, 'banana')
        self.assertEqual(retrieved_meal_3.foods[2].name, 'potato')
        self.assertEqual(retrieved_meal_3.foods[3].name, 'oats')
        self.assertEqual(retrieved_meal_3.foods[0].ss, 30)
        self.assertEqual(retrieved_meal_3.foods[1].ss, 1)
        self.assertEqual(retrieved_meal_3.foods[2].ss, 50)
        self.assertEqual(retrieved_meal_3.foods[3].ss, 40)
        self.assertEqual(retrieved_meal_3.foods[0].unit, 'g')
        self.assertEqual(retrieved_meal_3.foods[1].unit, 'banana')
        self.assertEqual(retrieved_meal_3.foods[2].unit, 'g')
        self.assertEqual(retrieved_meal_3.foods[3].unit, 'g')
        self.assertEqual(retrieved_meal_3.foods[0].cal, 75)
        self.assertEqual(retrieved_meal_3.foods[1].cal, 90)
        self.assertEqual(retrieved_meal_3.foods[2].cal, 120)
        self.assertEqual(retrieved_meal_3.foods[3].cal, 150)
        self.assertEqual(retrieved_meal_3.foods[0].carb, 30)
        self.assertEqual(retrieved_meal_3.foods[1].carb, 25)
        self.assertEqual(retrieved_meal_3.foods[2].carb, 20)
        self.assertEqual(retrieved_meal_3.foods[3].carb, 35)
        self.assertEqual(retrieved_meal_3.foods[0].fat, 1)
        self.assertEqual(retrieved_meal_3.foods[1].fat, 0)
        self.assertEqual(retrieved_meal_3.foods[2].fat, 0)
        self.assertEqual(retrieved_meal_3.foods[3].fat, 5)
        self.assertEqual(retrieved_meal_3.foods[0].protein, 3)
        self.assertEqual(retrieved_meal_3.foods[1].protein, 1)
        self.assertEqual(retrieved_meal_3.foods[2].protein, 2)
        self.assertEqual(retrieved_meal_3.foods[3].protein, 4)
        self.assertEqual(retrieved_meal_3.foods[0].fiber, 5)
        self.assertEqual(retrieved_meal_3.foods[1].fiber, 2)
        self.assertEqual(retrieved_meal_3.foods[2].fiber, 4)
        self.assertEqual(retrieved_meal_3.foods[3].fiber, 6)
        self.assertEqual(retrieved_meal_3.foods[0].sugar, 26)
        self.assertEqual(retrieved_meal_3.foods[1].sugar, 16)
        self.assertEqual(retrieved_meal_3.foods[2].sugar, 3)
        self.assertEqual(retrieved_meal_3.foods[3].sugar, 2)

    def test_parse_fetched_meal(self):
        tup_1 = ('meal1', 'foodname', 28, 'unit', 120, 20, 5, 12, 5, 4)
        tup_2 = ('meal1', 'oats', 40, 'g', 150, 25, 1, 5, 2, 3)
        tup_3 = ('meal1', 'apple', 50, 'grams', 90, 20, 0, 2, 4, 12)
        list_1 = [tup_1, tup_2, tup_3]

        meal = self.meal_dao.parse_fetched_meal(list_1)


        self.assertEqual(meal.foods[0].name, 'foodname')
        self.assertEqual(meal.foods[1].name, 'oats')
        self.assertEqual(meal.foods[2].name, 'apple')
        self.assertEqual(meal.foods[0].ss, 28)
        self.assertEqual(meal.foods[1].ss, 40)
        self.assertEqual(meal.foods[2].ss, 50)
        self.assertEqual(meal.foods[0].unit, 'unit')
        self.assertEqual(meal.foods[1].unit, 'g')
        self.assertEqual(meal.foods[2].unit, 'grams')
        self.assertEqual(meal.foods[0].cal, 120)
        self.assertEqual(meal.foods[1].cal, 150)
        self.assertEqual(meal.foods[2].cal, 90)
        self.assertEqual(meal.foods[0].carb, 20)
        self.assertEqual(meal.foods[1].carb, 25)
        self.assertEqual(meal.foods[2].carb, 20)
        self.assertEqual(meal.foods[0].fat, 5)
        self.assertEqual(meal.foods[1].fat, 1)
        self.assertEqual(meal.foods[2].fat, 0)
        self.assertEqual(meal.foods[0].protein, 12)
        self.assertEqual(meal.foods[1].protein, 5)
        self.assertEqual(meal.foods[2].protein, 2)
        self.assertEqual(meal.foods[0].fiber, 5)
        self.assertEqual(meal.foods[1].fiber, 2)
        self.assertEqual(meal.foods[2].fiber, 4)
        self.assertEqual(meal.foods[0].sugar, 4)
        self.assertEqual(meal.foods[1].sugar, 3)
        self.assertEqual(meal.foods[2].sugar, 12)

    def test_retrieve_all_meals(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        all_meals = self.meal_dao.retrieve_all_meals() # list of all meals


        self.assertEqual(all_meals[0].meal_name, 'Meal1')
        self.assertEqual(all_meals[1].meal_name, 'Meal2')
        self.assertEqual(all_meals[2].meal_name, 'Meal3')

        self.assertEqual(all_meals[0].foods[0].name, 'apple')
        self.assertEqual(all_meals[0].foods[1].name, 'banana')
        self.assertEqual(all_meals[0].foods[0].ss, 30)
        self.assertEqual(all_meals[0].foods[1].ss, 1)
        self.assertEqual(all_meals[0].foods[0].unit, 'g')
        self.assertEqual(all_meals[0].foods[1].unit, 'banana')
        self.assertEqual(all_meals[0].foods[0].cal, 75)
        self.assertEqual(all_meals[0].foods[1].cal, 90)
        self.assertEqual(all_meals[0].foods[0].carb, 30)
        self.assertEqual(all_meals[0].foods[1].carb, 25)
        self.assertEqual(all_meals[0].foods[0].fat, 1)
        self.assertEqual(all_meals[0].foods[1].fat, 0)
        self.assertEqual(all_meals[0].foods[0].protein, 3)
        self.assertEqual(all_meals[0].foods[1].protein, 1)
        self.assertEqual(all_meals[0].foods[0].fiber, 5)
        self.assertEqual(all_meals[0].foods[1].fiber, 2)
        self.assertEqual(all_meals[0].foods[0].sugar, 26)
        self.assertEqual(all_meals[0].foods[1].sugar, 16)

        self.assertEqual(all_meals[1].foods[0].name, 'potato')
        self.assertEqual(all_meals[1].foods[1].name, 'oats')
        self.assertEqual(all_meals[1].foods[0].ss, 50)
        self.assertEqual(all_meals[1].foods[1].ss, 40)
        self.assertEqual(all_meals[1].foods[0].unit, 'g')
        self.assertEqual(all_meals[1].foods[1].unit, 'g')
        self.assertEqual(all_meals[1].foods[0].cal, 120)
        self.assertEqual(all_meals[1].foods[1].cal, 150)
        self.assertEqual(all_meals[1].foods[0].carb, 20)
        self.assertEqual(all_meals[1].foods[1].carb, 35)
        self.assertEqual(all_meals[1].foods[0].fat, 0)
        self.assertEqual(all_meals[1].foods[1].fat, 5)
        self.assertEqual(all_meals[1].foods[0].protein, 2)
        self.assertEqual(all_meals[1].foods[1].protein, 4)
        self.assertEqual(all_meals[1].foods[0].fiber, 4)
        self.assertEqual(all_meals[1].foods[1].fiber, 6)
        self.assertEqual(all_meals[1].foods[0].sugar, 3)
        self.assertEqual(all_meals[1].foods[1].sugar, 2)

        self.assertEqual(all_meals[2].foods[0].name, 'apple')
        self.assertEqual(all_meals[2].foods[1].name, 'banana')
        self.assertEqual(all_meals[2].foods[0].ss, 30)
        self.assertEqual(all_meals[2].foods[1].ss, 1)
        self.assertEqual(all_meals[2].foods[0].unit, 'g')
        self.assertEqual(all_meals[2].foods[1].unit, 'banana')
        self.assertEqual(all_meals[2].foods[0].cal, 75)
        self.assertEqual(all_meals[2].foods[1].cal, 90)
        self.assertEqual(all_meals[2].foods[0].carb, 30)
        self.assertEqual(all_meals[2].foods[1].carb, 25)
        self.assertEqual(all_meals[2].foods[0].fat, 1)
        self.assertEqual(all_meals[2].foods[1].fat, 0)
        self.assertEqual(all_meals[2].foods[0].protein, 3)
        self.assertEqual(all_meals[2].foods[1].protein, 1)
        self.assertEqual(all_meals[2].foods[0].fiber, 5)
        self.assertEqual(all_meals[2].foods[1].fiber, 2)
        self.assertEqual(all_meals[2].foods[0].sugar, 26)
        self.assertEqual(all_meals[2].foods[1].sugar, 16)

        self.assertEqual(all_meals[2].foods[2].name, 'potato')
        self.assertEqual(all_meals[2].foods[3].name, 'oats')
        self.assertEqual(all_meals[2].foods[2].ss, 50)
        self.assertEqual(all_meals[2].foods[3].ss, 40)
        self.assertEqual(all_meals[2].foods[2].unit, 'g')
        self.assertEqual(all_meals[2].foods[3].unit, 'g')
        self.assertEqual(all_meals[2].foods[2].cal, 120)
        self.assertEqual(all_meals[2].foods[3].cal, 150)
        self.assertEqual(all_meals[2].foods[2].carb, 20)
        self.assertEqual(all_meals[2].foods[3].carb, 35)
        self.assertEqual(all_meals[2].foods[2].fat, 0)
        self.assertEqual(all_meals[2].foods[3].fat, 5)
        self.assertEqual(all_meals[2].foods[2].protein, 2)
        self.assertEqual(all_meals[2].foods[3].protein, 4)
        self.assertEqual(all_meals[2].foods[2].fiber, 4)
        self.assertEqual(all_meals[2].foods[3].fiber, 6)
        self.assertEqual(all_meals[2].foods[2].sugar, 3)
        self.assertEqual(all_meals[2].foods[3].sugar, 2)




    def test_retrieve_all_foods(self):
        self.meal_dao.insert_meal(self.meal_1)
        all_foods = self.meal_dao.retrieve_all_foods()
        self.assertEqual(all_foods[0][0], 'Meal1')
        self.assertEqual(all_foods[0][1], 'apple')
        self.assertEqual(all_foods[0][2], 30)
        self.assertEqual(all_foods[0][3], 'g')
        self.assertEqual(all_foods[0][4], 75)
        self.assertEqual(all_foods[0][5], 30)
        self.assertEqual(all_foods[0][6], 1)
        self.assertEqual(all_foods[0][7], 3)
        self.assertEqual(all_foods[0][8], 5)
        self.assertEqual(all_foods[0][9], 26)

        self.assertEqual(all_foods[1][0], 'Meal1')
        self.assertEqual(all_foods[1][1], 'banana')
        self.assertEqual(all_foods[1][2], 1)
        self.assertEqual(all_foods[1][3], 'banana')
        self.assertEqual(all_foods[1][4], 90)
        self.assertEqual(all_foods[1][5], 25)
        self.assertEqual(all_foods[1][6], 0)
        self.assertEqual(all_foods[1][7], 1)
        self.assertEqual(all_foods[1][8], 2)
        self.assertEqual(all_foods[1][9], 16)

    def test_parse_fetched_meals(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)
        tup_list = self.meal_dao.retrieve_all_foods()
        meals_list = self.meal_dao.parse_fetched_meals(tup_list)
        meal1 = meals_list[0]
        meal2 = meals_list[1]
        meal3 = meals_list[2]

        with self.assertRaises(IndexError):
            meal1.foods[2]
        with self.assertRaises(IndexError):
            meal2.foods[2]
        with self.assertRaises(IndexError):
            meal3.foods[4]

        self.assertEqual(meal1.foods[0].name, 'apple')
        self.assertEqual(meal1.foods[0].ss, 30)
        self.assertEqual(meal1.foods[0].unit, 'g')
        self.assertEqual(meal1.foods[0].cal, 75)
        self.assertEqual(meal1.foods[0].carb, 30)
        self.assertEqual(meal1.foods[0].fat, 1)
        self.assertEqual(meal1.foods[0].protein, 3)
        self.assertEqual(meal1.foods[0].fiber, 5)
        self.assertEqual(meal1.foods[0].sugar, 26)
        self.assertEqual(meal1.foods[1].name, 'banana')
        self.assertEqual(meal1.foods[1].ss, 1)
        self.assertEqual(meal1.foods[1].unit, 'banana')
        self.assertEqual(meal1.foods[1].cal, 90)
        self.assertEqual(meal1.foods[1].carb, 25)
        self.assertEqual(meal1.foods[1].fat, 0)
        self.assertEqual(meal1.foods[1].protein, 1)
        self.assertEqual(meal1.foods[1].fiber, 2)
        self.assertEqual(meal1.foods[1].sugar, 16)

        self.assertEqual(meal2.foods[0].name, 'potato')
        self.assertEqual(meal2.foods[0].ss, 50)
        self.assertEqual(meal2.foods[0].unit, 'g')
        self.assertEqual(meal2.foods[0].cal, 120)
        self.assertEqual(meal2.foods[0].carb, 20)
        self.assertEqual(meal2.foods[0].fat, 0)
        self.assertEqual(meal2.foods[0].protein, 2)
        self.assertEqual(meal2.foods[0].fiber, 4)
        self.assertEqual(meal2.foods[0].sugar, 3)
        self.assertEqual(meal2.foods[1].name, 'oats')
        self.assertEqual(meal2.foods[1].ss, 40)
        self.assertEqual(meal2.foods[1].unit, 'g')
        self.assertEqual(meal2.foods[1].cal, 150)
        self.assertEqual(meal2.foods[1].carb, 35)
        self.assertEqual(meal2.foods[1].fat, 5)
        self.assertEqual(meal2.foods[1].protein, 4)
        self.assertEqual(meal2.foods[1].fiber, 6)
        self.assertEqual(meal2.foods[1].sugar, 2)

        self.assertEqual(meal3.foods[0].name, 'apple')
        self.assertEqual(meal3.foods[0].ss, 30)
        self.assertEqual(meal3.foods[0].unit, 'g')
        self.assertEqual(meal3.foods[0].cal, 75)
        self.assertEqual(meal3.foods[0].carb, 30)
        self.assertEqual(meal3.foods[0].fat, 1)
        self.assertEqual(meal3.foods[0].protein, 3)
        self.assertEqual(meal3.foods[0].fiber, 5)
        self.assertEqual(meal3.foods[0].sugar, 26)
        self.assertEqual(meal3.foods[1].name, 'banana')
        self.assertEqual(meal3.foods[1].ss, 1)
        self.assertEqual(meal3.foods[1].unit, 'banana')
        self.assertEqual(meal3.foods[1].cal, 90)
        self.assertEqual(meal3.foods[1].carb, 25)
        self.assertEqual(meal3.foods[1].fat, 0)
        self.assertEqual(meal3.foods[1].protein, 1)
        self.assertEqual(meal3.foods[1].fiber, 2)
        self.assertEqual(meal3.foods[1].sugar, 16)
        self.assertEqual(meal3.foods[2].name, 'potato')
        self.assertEqual(meal3.foods[2].ss, 50)
        self.assertEqual(meal3.foods[2].unit, 'g')
        self.assertEqual(meal3.foods[2].cal, 120)
        self.assertEqual(meal3.foods[2].carb, 20)
        self.assertEqual(meal3.foods[2].fat, 0)
        self.assertEqual(meal3.foods[2].protein, 2)
        self.assertEqual(meal3.foods[2].fiber, 4)
        self.assertEqual(meal3.foods[2].sugar, 3)
        self.assertEqual(meal3.foods[3].name, 'oats')
        self.assertEqual(meal3.foods[3].ss, 40)
        self.assertEqual(meal3.foods[3].unit, 'g')
        self.assertEqual(meal3.foods[3].cal, 150)
        self.assertEqual(meal3.foods[3].carb, 35)
        self.assertEqual(meal3.foods[3].fat, 5)
        self.assertEqual(meal3.foods[3].protein, 4)
        self.assertEqual(meal3.foods[3].fiber, 6)
        self.assertEqual(meal3.foods[3].sugar, 2)


    def test_retrieve_all_meal_names(self):
        self.assertEqual(self.meal_dao.retrieve_all_meal_names(), [])

        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        self.assertEqual(self.meal_dao.retrieve_all_meal_names(), ['Meal1', 'Meal2', 'Meal3'])
        self.assertEqual(len(self.meal_dao.retrieve_all_meal_names()), 3)

    def test_delete_food_with_name(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        # to test delete with arg 'potato' and check that no field has foodname 'potato'
        self.assertEqual(self.meal_dao.delete_food_with_name('potato'), 2)

        all_foods = self.meal_dao.retrieve_all_foods()
        for tup in all_foods:
            self.assertNotEqual(tup[1], 'potato')

    def test_update_meal_names_of_foods(self):
        self.meal_dao.insert_meal(self.meal_1)
        self.meal_dao.insert_meal(self.meal_2)
        self.meal_dao.insert_meal(self.meal_3)

        names = ('new meal1', 'Meal1')
        self.assertEqual(self.meal_dao.update_meal_names_of_foods(names), 2)

        names = ('new meal3', 'Meal3')
        self.assertEqual(self.meal_dao.update_meal_names_of_foods(names), 4)

        names = ('not real', 'no such meal')
        self.assertEqual(self.meal_dao.update_meal_names_of_foods(names), 0)





if __name__ == '__main__':
    unittest.main()