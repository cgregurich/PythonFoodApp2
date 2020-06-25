import unittest
from fooditem import FoodItem
from fooditemdao import FoodItemDAO

class TestFoodItemDAO(unittest.TestCase):
    def setUp(self):
        self.fooditem_dao = FoodItemDAO(':memory:')
        info_1 = {'name': 'oats2', 'ss': 40, 'unit': 'g', 'cal': 120, 'carb': 30,
                  'fat': 5, 'protein': 6, 'fiber': 4, 'sugar': 2}

        info_2 = {'name': 'apple', 'ss': 30, 'unit': 'g', 'cal': 75, 'carb': 30,
                  'fat': 1, 'protein': 3, 'fiber': 5, 'sugar': 26}
        self.food_1 = FoodItem(info_1)
        self.food_2 = FoodItem(info_2)

    def test_insert_food(self):
        fooditem_dao = FoodItemDAO(':memory:')
        fooditem_dao.insert_food(self.food_1)
        fooditem_dao.insert_food(self.food_2)
        fooditem_dao.insert_food(self.food_2)
        fooditem_dao.insert_food(self.food_2)
        self.assertEqual(fooditem_dao.c.lastrowid, 4)

    def test_delete_food(self):
        fooditem_dao = FoodItemDAO(':memory:')
        # delete a food that doesn't exist
        self.assertEqual(fooditem_dao.delete_food('oats2'), 0)

        # delete a food that exists once
        fooditem_dao.insert_food(self.food_1)
        self.assertEqual(fooditem_dao.delete_food('oats2'), 1)

        # delete a food that exists multiple times
        fooditem_dao.insert_food(self.food_2)
        fooditem_dao.insert_food(self.food_2)
        fooditem_dao.insert_food(self.food_2)
        self.assertEqual(fooditem_dao.delete_food('apple'), 3)

    def test_update_food(self):
        fooditem_dao = FoodItemDAO(':memory:')

        # update a food that doesn't exist
        updated_info = {'name': 'nonexistent', 'ss': 40, 'unit': 'g', 'cal': 100,
                        'carb': 3, 'fat': 5, 'protein': 6, 'fiber': 4, 'sugar': 2}
        updated_food = FoodItem(updated_info)
        self.assertEqual(fooditem_dao.update_food(updated_food, 'fakename'), 0)

        # update a food that exists once
        fooditem_dao.insert_food(self.food_1)
        updated_info = {'name': 'newoats', 'ss': 20, 'unit': 'grams', 'cal': 100,
                        'carb': 20, 'fat': 4, 'protein': 3, 'fiber': 1, 'sugar': 3}
        updated_food = FoodItem(updated_info)
        old_name = self.food_1.name
        self.assertEqual(fooditem_dao.update_food(updated_food, old_name), 1)

    def test_retrieve_food(self):
        fooditem_dao = FoodItemDAO(':memory:')

        # retrieve food that doesn't exist
        name = 'oats'
        self.assertEqual(fooditem_dao.retrieve_food(name), None)

        # retrieve food that does exist
        fooditem_dao.insert_food(self.food_2)
        name = 'apple'
        food = fooditem_dao.retrieve_food(name)
        self.assertEqual(food.name, 'apple')
        self.assertEqual(food.ss, 30)
        self.assertEqual(food.unit, 'g')
        self.assertEqual(food.cal, 75)
        self.assertEqual(food.carb, 30)
        self.assertEqual(food.fat, 1)
        self.assertEqual(food.protein, 3)
        self.assertEqual(food.fiber, 5)
        self.assertEqual(food.sugar, 26)


    def test_convert_to_food_items_list(self):
        fooditem_dao = FoodItemDAO()

        # empty list as arg
        self.assertIsNone(fooditem_dao._convert_to_food_items_list([]))

        # tuple within list is wrong length i.e. not 9
        wrong_list = [('name', 2, 'unit', 100, 20, 4, 7, 4)] # 8 elements instead of 9
        self.assertRaises(ValueError, fooditem_dao._convert_to_food_items_list, wrong_list )

        info_tup_1 = ('oats', 28, 'g', 100, 30, 5, 6, 4, 3)
        info_tup_2 = ('apple', 1, 'apple', 75, 20, 0, 1, 3, 15)
        info_tup_3 = ('potato', 25, 'g', 90, 25, 1, 3, 3, 0)
        info_tup_list = [info_tup_1, info_tup_2, info_tup_3]
        foods_list = fooditem_dao._convert_to_food_items_list(info_tup_list)

        food_1 = foods_list[0]
        food_2 = foods_list[1]
        food_3 = foods_list[2]

        self.assertEqual(food_1.name, 'oats')
        self.assertEqual(food_1.ss, 28)
        self.assertEqual(food_1.unit, 'g')
        self.assertEqual(food_1.cal, 100)
        self.assertEqual(food_1.carb, 30)
        self.assertEqual(food_1.fat, 5)
        self.assertEqual(food_1.protein, 6)
        self.assertEqual(food_1.fiber, 4)
        self.assertEqual(food_1.sugar, 3)

        self.assertEqual(food_2.name, 'apple')
        self.assertEqual(food_2.ss, 1)
        self.assertEqual(food_2.unit, 'apple')
        self.assertEqual(food_2.cal, 75)
        self.assertEqual(food_2.carb, 20)
        self.assertEqual(food_2.fat, 0)
        self.assertEqual(food_2.protein, 1)
        self.assertEqual(food_2.fiber, 3)
        self.assertEqual(food_2.sugar, 15)

        self.assertEqual(food_3.name, 'potato')
        self.assertEqual(food_3.ss, 25)
        self.assertEqual(food_3.unit, 'g')
        self.assertEqual(food_3.cal, 90)
        self.assertEqual(food_3.carb, 25)
        self.assertEqual(food_3.fat, 1)
        self.assertEqual(food_3.protein, 3)
        self.assertEqual(food_3.fiber, 3)
        self.assertEqual(food_3.sugar, 0)


    def test_retrieve_all_foods(self):
        fooditem_dao = FoodItemDAO(':memory:')

        # retrieve all when table is empty
        self.assertIsNone(fooditem_dao.retrieve_all_foods())

        fooditem_dao.insert_food(self.food_1)
        fooditem_dao.insert_food(self.food_2)
        info_3 = {'name': 'potato', 'ss': 25, 'unit': 'g', 'cal': 90,
                        'carb': 25, 'fat': 0, 'protein': 2, 'fiber': 2, 'sugar': 4}
        food_3 = FoodItem(info_3)
        fooditem_dao.insert_food(food_3)
        retrieved_foods = fooditem_dao.retrieve_all_foods() # a FoodItem list
        food_1 = retrieved_foods[0]
        food_2 = retrieved_foods[1]
        food_3 = retrieved_foods[2]

        self.assertEqual(food_1.name, 'oats2')
        self.assertEqual(food_1.ss, 40)
        self.assertEqual(food_1.unit, 'g')
        self.assertEqual(food_1.cal, 120)
        self.assertEqual(food_1.carb, 30)
        self.assertEqual(food_1.fat, 5)
        self.assertEqual(food_1.protein, 6)
        self.assertEqual(food_1.fiber, 4)
        self.assertEqual(food_1.sugar, 2)

        self.assertEqual(food_2.name, 'apple')
        self.assertEqual(food_2.ss, 30)
        self.assertEqual(food_2.unit, 'g')
        self.assertEqual(food_2.cal, 75)
        self.assertEqual(food_2.carb, 30)
        self.assertEqual(food_2.fat, 1)
        self.assertEqual(food_2.protein, 3)
        self.assertEqual(food_2.fiber, 5)
        self.assertEqual(food_2.sugar, 26)

        self.assertEqual(food_3.name, 'potato')
        self.assertEqual(food_3.ss, 25)
        self.assertEqual(food_3.unit, 'g')
        self.assertEqual(food_3.cal, 90)
        self.assertEqual(food_3.carb, 25)
        self.assertEqual(food_3.fat, 0)
        self.assertEqual(food_3.protein, 2)
        self.assertEqual(food_3.fiber, 2)
        self.assertEqual(food_3.sugar, 4)

    def test_sort_foods(self):
        info_3 = {'name': 'potato', 'ss': 25, 'unit': 'grams', 'cal': 90,
                  'carb': 25, 'fat': 0, 'protein': 2, 'fiber': 2, 'sugar': 4}
        food_3 = FoodItem(info_3)
        fooditem_dao = FoodItemDAO(':memory:')
        fooditem_dao.insert_food(self.food_1)
        fooditem_dao.insert_food(self.food_2)
        fooditem_dao.insert_food(food_3)

        # test valid criteria and valid order
        sorted = fooditem_dao.sort_foods('name', 'ASC')
        self.assertEqual(sorted[0].name, 'apple')
        self.assertEqual(sorted[1].name, 'oats2')
        self.assertEqual(sorted[2].name, 'potato')

        # test valid criteria and invalid order
        self.assertRaises(ValueError, fooditem_dao.sort_foods, 'name', 'ASCENDING')

        # test invalid criteria and valid order
        self.assertRaises(ValueError, fooditem_dao.sort_foods, 'namee', 'ASC')


        # test invalid criteria and invalid order
        self.assertRaises(ValueError, fooditem_dao.sort_foods, 'namee', 'ASCENDING')

        # test all 9 criteria and 2 order types
        sorted = fooditem_dao.sort_foods('name', 'ASC')
        self.assertEqual(sorted[0].name, 'apple')
        self.assertEqual(sorted[1].name, 'oats2')
        self.assertEqual(sorted[2].name, 'potato')

        sorted = fooditem_dao.sort_foods('name', 'DESC')
        self.assertEqual(sorted[0].name, 'potato')
        self.assertEqual(sorted[1].name, 'oats2')
        self.assertEqual(sorted[2].name, 'apple')

        sorted = fooditem_dao.sort_foods('ss', 'ASC')
        self.assertEqual(sorted[0].ss, 25)
        self.assertEqual(sorted[1].ss, 30)
        self.assertEqual(sorted[2].ss, 40)

        sorted = fooditem_dao.sort_foods('ss', 'DESC')
        self.assertEqual(sorted[0].ss, 40)
        self.assertEqual(sorted[1].ss, 30)
        self.assertEqual(sorted[2].ss, 25)

        sorted = fooditem_dao.sort_foods('unit', 'ASC')
        self.assertEqual(sorted[0].unit, 'g')
        self.assertEqual(sorted[1].unit, 'g')
        self.assertEqual(sorted[2].unit, 'grams')

        sorted = fooditem_dao.sort_foods('unit', 'DESC')
        self.assertEqual(sorted[0].unit, 'grams')
        self.assertEqual(sorted[1].unit, 'g')
        self.assertEqual(sorted[2].unit, 'g')

        sorted = fooditem_dao.sort_foods('cal', 'ASC')
        self.assertEqual(sorted[0].cal, 75)
        self.assertEqual(sorted[1].cal, 90)
        self.assertEqual(sorted[2].cal, 120)

        sorted = fooditem_dao.sort_foods('cal', 'DESC')
        self.assertEqual(sorted[0].cal, 120)
        self.assertEqual(sorted[1].cal, 90)
        self.assertEqual(sorted[2].cal, 75)

        sorted = fooditem_dao.sort_foods('carb', 'ASC')
        self.assertEqual(sorted[0].carb, 25)
        self.assertEqual(sorted[1].carb, 30)
        self.assertEqual(sorted[2].carb, 30)

        sorted = fooditem_dao.sort_foods('carb', 'DESC')
        self.assertEqual(sorted[0].carb, 30)
        self.assertEqual(sorted[1].carb, 30)
        self.assertEqual(sorted[2].carb, 25)

        sorted = fooditem_dao.sort_foods('fat', 'ASC')
        self.assertEqual(sorted[0].fat, 0)
        self.assertEqual(sorted[1].fat, 1)
        self.assertEqual(sorted[2].fat, 5)

        sorted = fooditem_dao.sort_foods('fat', 'DESC')
        self.assertEqual(sorted[0].fat, 5)
        self.assertEqual(sorted[1].fat, 1)
        self.assertEqual(sorted[2].fat, 0)

        sorted = fooditem_dao.sort_foods('protein', 'ASC')
        self.assertEqual(sorted[0].protein, 2)
        self.assertEqual(sorted[1].protein, 3)
        self.assertEqual(sorted[2].protein, 6)

        sorted = fooditem_dao.sort_foods('protein', 'DESC')
        self.assertEqual(sorted[0].protein, 6)
        self.assertEqual(sorted[1].protein, 3)
        self.assertEqual(sorted[2].protein, 2)

        sorted = fooditem_dao.sort_foods('fiber', 'ASC')
        self.assertEqual(sorted[0].fiber, 2)
        self.assertEqual(sorted[1].fiber, 4)
        self.assertEqual(sorted[2].fiber, 5)

        sorted = fooditem_dao.sort_foods('fiber', 'DESC')
        self.assertEqual(sorted[0].fiber, 5)
        self.assertEqual(sorted[1].fiber, 4)
        self.assertEqual(sorted[2].fiber, 2)

        sorted = fooditem_dao.sort_foods('sugar', 'ASC')
        self.assertEqual(sorted[0].sugar, 2)
        self.assertEqual(sorted[1].sugar, 4)
        self.assertEqual(sorted[2].sugar, 26)

        sorted = fooditem_dao.sort_foods('sugar', 'DESC')
        self.assertEqual(sorted[0].sugar, 26)
        self.assertEqual(sorted[1].sugar, 4)
        self.assertEqual(sorted[2].sugar, 2)

    def test_retrieve_all_food_names(self):
        self.assertEqual(self.fooditem_dao.retrieve_all_food_names(), []) # empty list? Tuple? None? idk
        self.fooditem_dao.insert_food(self.food_1)
        self.fooditem_dao.insert_food(self.food_2)
        self.assertEqual(self.fooditem_dao.retrieve_all_food_names(), ['oats2', 'apple'])


if __name__ == '__main__':
    unittest.main()



