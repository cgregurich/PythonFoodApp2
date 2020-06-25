from fooditem import FoodItem
from meal import Meal
from fooditemdao import FoodItemDAO
from mealdao import MealDAO
import mealtextuserinterface as mealTUI
import foodtextuserinterface as foodTUI

def run():
    display_menu()
    command = get_command()
    while command:
        command = get_command()


def display_menu():
    print("\nHOME COMMANDS")
    print("FOODS - Switch to foods mode")
    print("MEALS - Switch to meals mode")
    print("HELP - Display this menu")
    print("QUIT - Quit program")


def get_command():
    command = (input("Enter command: ")).lower()
    if command == 'foods':
        foodTUI.run()
        return None
    if command == 'meals':
        mealTUI.run()
        return None
    if command == 'quit' or command == 'exit':
        return None
    if command == 'help':
        display_menu()
        return True
    else:
        print("\nInvalid command.\n")
        return get_command()


