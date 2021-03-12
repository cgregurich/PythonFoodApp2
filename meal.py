class Meal:
    def __init__(self, meal_name='', *foods):
        """Takes a variable number of FoodItem arguments
        Each FoodItem arg is put in the list self.foods"""
        if not isinstance(meal_name, str):
            raise TypeError("meal_name is not a String. Did you forget to include "
                            "the meal name?")
        self.meal_name = meal_name

        self.foods = []
        for food in foods:
            self.foods.append(food)

    def set_foods_from_list(self, foods_list):
        for food in foods_list:
            self.foods.append(food)

    def get_foods(self):
        """Returns the list of FoodItems self.foods"""
        return self.foods

    def del_food(self, name):
        """Deletes the FoodItem from Meal's list of FoodItems whose name matches
        the param name. Assumes FoodItems in foods are uniquely named"""
        for food in self.foods:
            if food.name == name:
                self.foods.remove(food)
                return True
        return False

    def add_food(self, new_food):
        """Adds the FoodItem param food to self.foods if new_food's name is unique
        Returns True if it is unique and was added, otherwise returns False"""
        for food in self.foods:
            if food.name == new_food.name:
                return False
        self.foods.append(new_food)
        return True

    def __str__(self):
        str = f"{self.meal_name.upper()}\n"
        for food in self.foods:
            str += f"{food.__str__()}\n"
        return str

    def food_count(self):
        return len(self.foods)

    @property
    def meal_info(self):
        info_dict = {'cal': 0, 'carb': 0, 'fat': 0, 'protein': 0, 'fiber': 0, 'sugar': 0}
        for food in self.foods:
            for key in info_dict.keys():
                info_dict[key] += food.info[key]
        return info_dict

    def get_info_tuple(self):
        macros = tuple(self.meal_info.values())
        return (self.meal_name.upper(),'-', '-') + macros

    @property
    def formatted_meal_info(self):
        meal_info = self.meal_info
        for key in meal_info.keys():


            val = meal_info[key]
            if key == 'cal': # cal should be whole number
                meal_info[key] = round(int(meal_info[key]))
                continue

            if val == int(val):
                meal_info[key] = int(meal_info[key])
            else:
                meal_info[key] = round(meal_info[key], 1)
        return meal_info

    def get_widths_of_info(self):
        """Returns a list of the widths of each piece of data in the meal's foods"""
        widths = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        headers = ('name', 'ss', 'unit', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
        for i in range(len(headers)):
            for food in self.foods:
                widths[i] = max(widths[i], len(str(food.info[headers[i]])))
        return widths




