import unittest
from fooditem import FoodItem
from meal import Meal


class TestMeal(unittest.TestCase):
    def setUp(self):
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


    def test_init(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2, self.food_3, self.food_4)

        self.assertEqual(meal_1.meal_name, 'Meal1')

        self.assertEqual(meal_1.foods[0].name, 'apple')
        self.assertEqual(meal_1.foods[1].name, 'banana')
        self.assertEqual(meal_1.foods[2].name, 'potato')
        self.assertEqual(meal_1.foods[3].name, 'oats')
        self.assertEqual(meal_1.foods[0].cal, 75)
        self.assertEqual(meal_1.foods[1].cal, 90)
        self.assertEqual(meal_1.foods[2].cal, 120)
        self.assertEqual(meal_1.foods[3].cal, 150)


        meal_2 = Meal('SingleFood', self.food_1)
        self.assertEqual(meal_2.meal_name, 'SingleFood')
        self.assertEqual(meal_2.foods[0].name, 'apple')
        self.assertEqual(meal_2.foods[0].ss, 30)
        self.assertEqual(meal_2.foods[0].unit, 'g')
        self.assertEqual(meal_2.foods[0].cal, 75)
        self.assertEqual(meal_2.foods[0].carb, 30)
        self.assertEqual(meal_2.foods[0].fat, 1)
        self.assertEqual(meal_2.foods[0].protein, 3)
        self.assertEqual(meal_2.foods[0].fiber, 5)
        self.assertEqual(meal_2.foods[0].sugar, 26)

        # exclude initial arg of meal_name
        self.assertRaises(TypeError, Meal, self.food_2, self.food_3)

    def test_get_foods(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2, self.food_3, self.food_4)
        meal_1_foods = meal_1.get_foods()

        self.assertEqual(meal_1_foods[0].name, 'apple')
        self.assertEqual(meal_1_foods[1].name, 'banana')
        self.assertEqual(meal_1_foods[2].name, 'potato')
        self.assertEqual(meal_1_foods[3].name, 'oats')
        self.assertEqual(meal_1_foods[0].ss, 30)
        self.assertEqual(meal_1_foods[1].ss, 1)
        self.assertEqual(meal_1_foods[2].ss, 50)
        self.assertEqual(meal_1_foods[3].ss, 40)
        self.assertEqual(meal_1_foods[0].unit, 'g')
        self.assertEqual(meal_1_foods[1].unit, 'banana')
        self.assertEqual(meal_1_foods[2].unit, 'g')
        self.assertEqual(meal_1_foods[3].unit, 'g')
        self.assertEqual(meal_1_foods[0].cal, 75)
        self.assertEqual(meal_1_foods[1].cal, 90)
        self.assertEqual(meal_1_foods[2].cal, 120)
        self.assertEqual(meal_1_foods[3].cal, 150)
        self.assertEqual(meal_1_foods[0].carb, 30)
        self.assertEqual(meal_1_foods[1].carb, 25)
        self.assertEqual(meal_1_foods[2].carb, 20)
        self.assertEqual(meal_1_foods[3].carb, 35)
        self.assertEqual(meal_1_foods[0].fat, 1)
        self.assertEqual(meal_1_foods[1].fat, 0)
        self.assertEqual(meal_1_foods[2].fat, 0)
        self.assertEqual(meal_1_foods[3].fat, 5)
        self.assertEqual(meal_1_foods[0].protein, 3)
        self.assertEqual(meal_1_foods[1].protein, 1)
        self.assertEqual(meal_1_foods[2].protein, 2)
        self.assertEqual(meal_1_foods[3].protein, 4)
        self.assertEqual(meal_1_foods[0].fiber, 5)
        self.assertEqual(meal_1_foods[1].fiber, 2)
        self.assertEqual(meal_1_foods[2].fiber, 4)
        self.assertEqual(meal_1_foods[3].fiber, 6)
        self.assertEqual(meal_1_foods[0].sugar, 26)
        self.assertEqual(meal_1_foods[1].sugar, 16)
        self.assertEqual(meal_1_foods[2].sugar, 3)
        self.assertEqual(meal_1_foods[3].sugar, 2)

    def test_del_food(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2, self.food_3, self.food_4)

        self.assertEqual(meal_1.foods[0].name, 'apple')

        self.assertTrue(meal_1.del_food('apple'))
        self.assertFalse(meal_1.del_food('apple'))
        self.assertFalse(meal_1.del_food('fake food'))
        self.assertTrue(meal_1.del_food('oats'))

        self.assertEqual(meal_1.foods[0].name, 'banana')
        self.assertEqual(meal_1.foods[1].name, 'potato')
        self.assertEqual(meal_1.foods[0].ss, 1)
        self.assertEqual(meal_1.foods[1].ss, 50)
        self.assertEqual(meal_1.foods[0].unit, 'banana')
        self.assertEqual(meal_1.foods[1].unit, 'g')
        self.assertEqual(meal_1.foods[0].cal, 90)
        self.assertEqual(meal_1.foods[1].cal, 120)
        self.assertEqual(meal_1.foods[0].carb, 25)
        self.assertEqual(meal_1.foods[1].carb, 20)
        self.assertEqual(meal_1.foods[0].fat, 0)
        self.assertEqual(meal_1.foods[1].fat, 0)
        self.assertEqual(meal_1.foods[0].protein, 1)
        self.assertEqual(meal_1.foods[1].protein, 2)
        self.assertEqual(meal_1.foods[0].fiber, 2)
        self.assertEqual(meal_1.foods[1].fiber, 4)
        self.assertEqual(meal_1.foods[0].sugar, 16)
        self.assertEqual(meal_1.foods[1].sugar, 3)

    def test_add_food(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2, self.food_3, self.food_4)
        info = {'name': 'new', 'ss': 28, 'unit': 'grams', 'cal': 200, 'carb': 12,
                  'fat': 7, 'protein': 12, 'fiber': 7, 'sugar': 2}
        new_food = FoodItem(info)
        self.assertTrue(meal_1.add_food(new_food))
        self.assertFalse(meal_1.add_food(self.food_1))
        self.assertFalse(meal_1.add_food(self.food_2))
        self.assertFalse(meal_1.add_food(self.food_3))
        self.assertFalse(meal_1.add_food(new_food))

        self.assertEqual(meal_1.foods[4].name, 'new')
        self.assertEqual(meal_1.foods[4].ss, 28)
        self.assertEqual(meal_1.foods[4].unit, 'grams')
        self.assertEqual(meal_1.foods[4].cal, 200)
        self.assertEqual(meal_1.foods[4].carb, 12)
        self.assertEqual(meal_1.foods[4].fat, 7)
        self.assertEqual(meal_1.foods[4].protein, 12)
        self.assertEqual(meal_1.foods[4].fiber, 7)
        self.assertEqual(meal_1.foods[4].sugar, 2)

    def test_food_count(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2, self.food_3, self.food_4)
        meal_2 = Meal('Meal2', self.food_2)
        self.assertEqual(meal_1.food_count(), 4)
        self.assertEqual(meal_2.food_count(), 1)

    def test_meal_info(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2)
        meal_2 = Meal('Meal2', self.food_3, self.food_4)
        meal_3 = Meal('Meal3', self.food_1, self.food_2,  self.food_3, self.food_4, )
        self.assertEqual(meal_1.meal_info['cal'], (self.food_1.cal + self.food_2.cal))
        self.assertEqual(meal_1.meal_info['carb'], (self.food_1.carb + self.food_2.carb))
        self.assertEqual(meal_1.meal_info['fat'], (self.food_1.fat + self.food_2.fat))
        self.assertEqual(meal_1.meal_info['protein'], (self.food_1.protein + self.food_2.protein))
        self.assertEqual(meal_1.meal_info['fiber'], (self.food_1.fiber + self.food_2.fiber))
        self.assertEqual(meal_1.meal_info['sugar'], (self.food_1.sugar + self.food_2.sugar))

        self.assertEqual(meal_2.meal_info['cal'], (self.food_3.cal + self.food_4.cal))
        self.assertEqual(meal_2.meal_info['carb'], (self.food_3.carb + self.food_4.carb))
        self.assertEqual(meal_2.meal_info['fat'], (self.food_3.fat + self.food_4.fat))
        self.assertEqual(meal_2.meal_info['protein'], (self.food_3.protein + self.food_4.protein))
        self.assertEqual(meal_2.meal_info['fiber'], (self.food_3.fiber + self.food_4.fiber))
        self.assertEqual(meal_2.meal_info['sugar'], (self.food_3.sugar + self.food_4.sugar))

        self.assertEqual(meal_3.meal_info['cal'], (self.food_1.cal + self.food_2.cal + self.food_3.cal + self.food_4.cal))
        self.assertEqual(meal_3.meal_info['carb'], (self.food_1.carb + self.food_2.carb + self.food_3.carb + self.food_4.carb))
        self.assertEqual(meal_3.meal_info['fat'], (self.food_1.fat + self.food_2.fat + self.food_3.fat + self.food_4.fat))
        self.assertEqual(meal_3.meal_info['protein'], (self.food_1.protein + self.food_2.protein + self.food_3.protein + self.food_4.protein))
        self.assertEqual(meal_3.meal_info['fiber'], (self.food_1.fiber + self.food_2.fiber + self.food_3.fiber + self.food_4.fiber))
        self.assertEqual(meal_3.meal_info['sugar'], (self.food_1.sugar + self.food_2.sugar + self.food_3.sugar + self.food_4.sugar))

    def test_set_foods_from_list(self):
        meal_1 = Meal('Meal1', self.food_1, self.food_2)
        meal_2 = Meal('Meal3')


        new_foods = [self.food_1, self.food_4]
        self.assertEqual(meal_2.foods, [])
        meal_2.set_foods_from_list(new_foods)
        self.assertEqual(meal_2.foods[0].name, 'apple')
        self.assertEqual(meal_2.foods[1].name, 'oats')
        self.assertEqual(meal_2.foods[0].ss, 30)
        self.assertEqual(meal_2.foods[1].ss, 40)
        self.assertEqual(meal_2.foods[0].unit, 'g')
        self.assertEqual(meal_2.foods[1].unit, 'g')
        self.assertEqual(meal_2.foods[0].cal, 75)
        self.assertEqual(meal_2.foods[1].cal, 150)
        self.assertEqual(meal_2.foods[0].carb, 30)
        self.assertEqual(meal_2.foods[1].carb, 35)
        self.assertEqual(meal_2.foods[0].fat, 1)
        self.assertEqual(meal_2.foods[1].fat, 5)
        self.assertEqual(meal_2.foods[0].protein, 3)
        self.assertEqual(meal_2.foods[1].protein, 4)
        self.assertEqual(meal_2.foods[0].fiber, 5)
        self.assertEqual(meal_2.foods[1].fiber, 6)
        self.assertEqual(meal_2.foods[0].sugar, 26)
        self.assertEqual(meal_2.foods[1].sugar, 2)

        with self.assertRaises(IndexError):
            meal_1.foods[2]

        meal_1.set_foods_from_list(new_foods)
        self.assertEqual(meal_1.foods[2].name, 'apple')
        self.assertEqual(meal_1.foods[3].name, 'oats')
        self.assertEqual(meal_1.foods[2].ss, 30)
        self.assertEqual(meal_1.foods[3].ss, 40)
        self.assertEqual(meal_1.foods[2].unit, 'g')
        self.assertEqual(meal_1.foods[3].unit, 'g')
        self.assertEqual(meal_1.foods[2].cal, 75)
        self.assertEqual(meal_1.foods[3].cal, 150)
        self.assertEqual(meal_1.foods[2].carb, 30)
        self.assertEqual(meal_1.foods[3].carb, 35)
        self.assertEqual(meal_1.foods[2].fat, 1)
        self.assertEqual(meal_1.foods[3].fat, 5)
        self.assertEqual(meal_1.foods[2].protein, 3)
        self.assertEqual(meal_1.foods[3].protein, 4)
        self.assertEqual(meal_1.foods[2].fiber, 5)
        self.assertEqual(meal_1.foods[3].fiber, 6)
        self.assertEqual(meal_1.foods[2].sugar, 26)
        self.assertEqual(meal_1.foods[3
                         ].sugar, 2)


if __name__ == '__main__':
    unittest.main()