from fooditemdao import FoodItemDAO
from fooditem import FoodItem
from mealdao import MealDAO
from meal import Meal

import startpage

# FONTS
LARGE_FONT = ("Verdana", 12)
BOLD_FONT = ("Verdana", 12, "bold")
ADD_FONT = ("Verdana", 8)
ERROR_FONT = ("Verdana", 8)
MONOSPACED_FONT = ("Consolas", 8)
HEADER_FONT = ("Verdana", 10)
BOLD_MONOSPACED = ("Consolas", 8, "bold")
BOLD_MONOSPACED_BIG = ("Consolas", 11, "bold")
MONOSPACED_BIG = ("Consolas", 11)

# DATA ACCESS OBJECTS
fooditemdao = FoodItemDAO()
mealdao = MealDAO()

