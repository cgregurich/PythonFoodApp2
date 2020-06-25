import unittest
from fooditem import FoodItem


class TestFoodItem(unittest.TestCase):
    def setUp(self):
        self.food_1 = FoodItem()

        info_2 = {'name': 'apple', 'ss': 30, 'unit': 'g', 'cal': 75, 'carb': 30, 'fat': 1, 'protein': 3, 'fiber': 5, 'sugar': 26}
        self.food_2 = FoodItem(info_2)

    def test_init(self):
        self.assertEqual(None, self.food_1.name)
        self.assertEqual(None, self.food_1.ss)
        self.assertEqual(None, self.food_1.unit)
        self.assertEqual(None, self.food_1.cal)
        self.assertEqual(None, self.food_1.carb)
        self.assertEqual(None, self.food_1.fat)
        self.assertEqual(None, self.food_1.protein)
        self.assertEqual(None, self.food_1.fiber)
        self.assertEqual(None, self.food_1.sugar)

        self.assertEqual('apple', self.food_2.name)
        self.assertEqual(30, self.food_2.ss)
        self.assertEqual('g', self.food_2.unit)
        self.assertEqual(75, self.food_2.cal)
        self.assertEqual(30, self.food_2.carb)
        self.assertEqual(1, self.food_2.fat)
        self.assertEqual(3, self.food_2.protein)
        self.assertEqual(5, self.food_2.fiber)
        self.assertEqual(26, self.food_2.sugar)

    def test_set_info(self):
        info_1 = {'name': 'oats2', 'ss': 40, 'unit': 'g', 'cal': 120, 'carb': 30, 'fat': 5, 'protein': 6, 'fiber': 4, 'sugar': 2}
        self.food_1.set_info(info_1)
        self.assertEqual('oats2', self.food_1.name)
        self.assertEqual(40, self.food_1.ss)
        self.assertEqual('g', self.food_1.unit)
        self.assertEqual(120, self.food_1.cal)
        self.assertEqual(30, self.food_1.carb)
        self.assertEqual(5, self.food_1.fat)
        self.assertEqual(6, self.food_1.protein)
        self.assertEqual(4, self.food_1.fiber)
        self.assertEqual(2, self.food_1.sugar)

        info_2 = {'name': 'apple2', 'ss': 1, 'unit': 'apple', 'cal': 50, 'carb': 20, 'fat': 0, 'protein': 1, 'fiber': 4, 'sugar': 16}
        self.food_2.set_info(info_2)
        self.assertEqual('apple2', self.food_2.name)
        self.assertEqual(1, self.food_2.ss)
        self.assertEqual('apple', self.food_2.unit)
        self.assertEqual(50, self.food_2.cal)
        self.assertEqual(20, self.food_2.carb)
        self.assertEqual(0, self.food_2.fat)
        self.assertEqual(1, self.food_2.protein)
        self.assertEqual(4, self.food_2.fiber)
        self.assertEqual(16, self.food_2.sugar)

    def test_set_info_from_tuple(self):
        info_tup = ('oats', 30, 'g', 100, 30, 3, 5, 5, 2)
        food = FoodItem()
        food.set_info_from_tuple(info_tup)
        self.assertEqual(food.name, 'oats')
        self.assertEqual(food.ss, 30)
        self.assertEqual(food.unit, 'g')
        self.assertEqual(food.cal, 100)
        self.assertEqual(food.carb, 30)
        self.assertEqual(food.fat, 3)
        self.assertEqual(food.protein, 5)
        self.assertEqual(food.fiber, 5)
        self.assertEqual(food.sugar, 2)



    def test_str(self):
        self.assertEqual("name:None ss:None unit:None cal:None carb:None fat:None protein:None fiber:None sugar:None", self.food_1.__str__())
        self.assertEqual("name:apple ss:30 unit:g cal:75 carb:30 fat:1 protein:3 fiber:5 sugar:26", self.food_2.__str__())

    def test_proportionalize(self):
        self.assertRaises(TypeError, self.food_1.proportionalize, 70)

        self.food_2.proportionalize(60)
        self.assertEqual("name:apple ss:60 unit:g cal:150 carb:60 fat:2 protein:6 fiber:10 sugar:52", self.food_2.__str__())

        info_1 = {'name': 'oats', 'ss': 40, 'unit': 'g', 'cal': 120, 'carb': 30, 'fat': 5, 'protein': 6, 'fiber': 4, 'sugar': 2}
        self.food_1.set_info(info_1)
        self.food_1.proportionalize(125)
        self.assertEqual("name:oats ss:125 unit:g cal:375 carb:93.8 fat:15.6 protein:18.8 fiber:12.5 sugar:6.2", self.food_1.__str__())

    def test_is_info_same(self):
        info1 = {'name': 'first', 'ss': 100, 'unit': 'g', 'cal': 100, 'carb': 20, 'fat': 2, 'protein': 5, 'fiber': 3, 'sugar': 4}
        info2 = {'name':'second', 'ss': 100, 'unit': 'grams', 'cal': 100, 'carb': 20, 'fat': 4, 'protein': 3, 'fiber': 2, 'sugar': 1}
        info3 = {'name': 'first', 'ss': 100, 'unit': 'g', 'cal': 100, 'carb': 20, 'fat': 2, 'protein': 5, 'fiber': 3, 'sugar': 4}
        info4 = {'name': 'first2', 'ss': 100, 'unit': 'g', 'cal': 100, 'carb': 20, 'fat': 2, 'protein': 5, 'fiber': 3, 'sugar': 4}

        food1 = FoodItem(info1) #control
        food2 = FoodItem(info2) #most different
        food3 = FoodItem(info3) #all same
        food4 = FoodItem(info4) #all same but name

        self.assertFalse(food1.is_info_same(food2))
        self.assertFalse(food2.is_info_same(food3))
        self.assertTrue(food1.is_info_same(food3))
        self.assertFalse(food1.is_info_same(food4))

    def test_numberize_info(self):
        info1 = {'name': 'first', 'ss': '100', 'unit': 'g', 'cal': '100', 'carb': '20', 'fat': '2', 'protein': '5', 'fiber': '3', 'sugar': '4'}
        info2 = {'name':'second', 'ss': 100, 'unit': 'grams', 'cal': '100', 'carb': 20, 'fat': '4', 'protein': '3', 'fiber': 2, 'sugar': '1'}
        info3 = {'name': 'third', 'ss': 120, 'unit': 'g', 'cal': 59, 'carb': 24, 'fat': 4, 'protein': 5, 'fiber': 2, 'sugar': 4}
        info4 = {'name': 'third', 'ss': 'ffs', 'unit': 'g', 'cal': 59, 'carb': 24, 'fat': 4, 'protein': 5, 'fiber': 2, 'sugar': 4}

        food1 = FoodItem(info1) #all info is str
        food2 = FoodItem(info2) #some info is str
        food3 = FoodItem(info3) #only str info is str

        food4 = FoodItem(info4) #invalid info for numbers

        self.assertTrue(food1.numberize_info())
        self.assertTrue(food2.numberize_info())
        self.assertTrue(food3.numberize_info())
        self.assertFalse(food4.numberize_info())

    def test_is_missing_info(self):
        info1 = {'name': 'first', 'ss': '100', 'unit': 'g', 'cal': '100', 'carb': '20', 'fat': '2', 'protein': '5', 'fiber': '3', 'sugar': '4'}
        info2 = {'name':'second', 'ss': None, 'unit': 'grams', 'cal': '100', 'carb': 20, 'fat': '4', 'protein': '3', 'fiber': 2, 'sugar': '1'}
        info3 = {'name': 'third', 'ss': 120, 'unit': 'g', 'cal': 59, 'carb': 24, 'fat': None, 'protein': 5, 'fiber': 2, 'sugar': 4}
        info4 = {'name': '', 'ss': 'ffs', 'unit': 'g', 'cal': 59, 'carb': 24, 'fat': 4, 'protein': 5, 'fiber': 2, 'sugar': 4}

        food1 = FoodItem(info1)
        food2 = FoodItem(info2)
        food3 = FoodItem(info3)
        food4 = FoodItem(info4)

        self.assertFalse(food1.is_missing_info())
        self.assertTrue(food2.is_missing_info())
        self.assertTrue(food3.is_missing_info())
        self.assertTrue(food4.is_missing_info())

        

        
        



        
                



if __name__ == '__main__':
    unittest.main()

