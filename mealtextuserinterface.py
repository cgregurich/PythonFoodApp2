from meal import Meal
from mealdao import MealDAO
from fooditem import FoodItem
from fooditemdao import FoodItemDAO
from tabulate import tabulate
import foodtextuserinterface as FTUI

meal_dao = MealDAO()
food_dao = FoodItemDAO()

def run():
    display_menu()
    command = get_command()
    while command:
        command = get_command()

def display_menu():
    print("\nMEALS COMMANDS")
    print("(Enter x at any time to cancel command)")
    print("VIEW - View all meals")
    print("ADD - Add a new meal")
    print("DEL - Delete a meal by name")
    print("UPDATE - Update a meal")
    print("SORT - Sort all meals")
    print("HELP - Display this menu")
    print("MEALS - Switch to foods mode")
    print("QUIT - Quit the program")


def get_command():
    command = (input("\nEnter command: ")).lower()
    if command == 'view':
        view()
        return True
    if command == 'add':
        add_meal()
        return True
    if command == 'del':
        del_meal()
        return True
    if command == 'update':
        update_meal()
        return True
    if command == 'sort':
        print('todo sort')
        return True
    if command == 'calc':
        print('todo calc')
        return True
    if command == 'help':
        display_menu()
        return True
    if command == 'foods':
        FTUI.run()
        return None
    if command == 'quit' or command == 'exit' or command == 'x':
        return None
    else:
        print("\nInvalid command.")
        return get_command()


def is_db_empty():
    meals = meal_dao.retrieve_all_meals()
    if not meals:
        return True
    else:
        return False

def view():
    if is_db_empty():
        print("\nNo meals found. Use the ADD command to add a meal.")
        return None
    table_view(meal_dao.retrieve_all_meals())




def table_view(meals_list, headers=['', 'SS', 'UNIT', 'CAL', 'CARB', 'FAT', 'PROTEIN', 'FIBER', 'SUGAR']):
    data = []
    for meal in meals_list:
        data.append(meal.get_info_tuple())
        for food in meal.foods:
            data.append(food.get_tuple())
        data.append('')
    print(tabulate(data, headers))




def add_meal():
    foods = food_dao.retrieve_all_foods()
    if not foods:
        print("\nNo foods have been added yet.\nTo add foods, enter command 'foods' and then command 'add'.")
        return None
    meal = add_meal_user_input()
    if meal is None:
        return None
    meal_dao.insert_meal(meal)



def add_meal_user_input():
    """Handles calling user input methods and returns a Meal object"""
    meal_name = meal_name_user_input()
    if meal_name is None:
        return None


    view_all_foods()

    print("\nWhat foods are in the meal?\n(leave blank and hit enter if done)")
    food_names = []
    foods = []
    while True:
        food_name = add_food_user_input(food_names)
        if food_name is None:
            return None
        if food_name == '':
            break
        else:
            food_names.append(food_name)
            amount = food_amount_user_input(food_name)
            if amount is None:
                return None
            cur_food = food_dao.retrieve_food(food_name)
            cur_food.proportionalize(amount)
            foods.append(cur_food)
    meal = Meal(meal_name)
    meal.set_foods_from_list(foods)
    return meal



def meal_name_user_input():
    meal_name = ''
    while True:
        meal_name = input("Enter meal name: ").lower()
        if meal_name == 'x':
            return None
        if meal_name in meal_dao.retrieve_all_meal_names():
            print(f"\nMeal named '{meal_name}' already exists.\n")
        else:
            return meal_name

def add_food_user_input(food_names):
    food_name = ' '

    while True:
        food_name = input("\nEnter name of food to add to meal (leave blank and enter if done): ")
        if food_name == 'x':
            return None
        elif food_name == '':
            return ''
        elif food_name not in food_dao.retrieve_all_food_names():
            print(f"\nFood named '{food_name}' does not exist.")
        elif food_name in food_names:
            print(f"\n'{food_name}' has already been entered for this meal.")
        else:
            return food_name

def food_amount_user_input(food_name):
    amount = ''
    unit = food_dao.retrieve_food(food_name).unit
    while True:
        amount = input(f"Enter amount ({unit}): ")
        if amount == 'x':
            return None
        try:
            amount = float(amount)
            return amount
        except ValueError:
            print(f"\n{amount} is not a valid amount.\n")

def del_meal():
    if is_db_empty():
        print("\nNo meals found. Use the ADD command to add a meal.")
        return None
    name = del_meal_user_input()
    if name is None:
        return None
    meal_dao.delete_meal(name)
    if (meal_dao.c.rowcount >= 1):
        print(f"\n'{name}' was deleted.")
    else:
        print("\nSomething went wrong.")



def del_meal_user_input():
    print("\nDELETE MEAL")
    name = ''
    while True:
        name = input("Enter name of meal to delete: ")
        if name == 'x':
            return None
        meal_by_name = meal_dao.retrieve_meal(name)
        if meal_by_name is None:
            print(f"\nNo meal called '{name}' exists.\n")
        else:
            return name

def update_meal():
    if is_db_empty():
        print("\nNo meals found. Use the ADD command to add a meal.")
        return None
    new_old_names = update_meal_names_user_input()
    if new_old_names is None:
        return None
    if new_old_names[0] != '':
        meal_dao.update_meal_names_of_foods(new_old_names)





def update_meal_names_user_input():
    print("\nUPDATE MEAL")
    old_name = update_old_name_user_input()
    if old_name is None:
        pass
    new_name = update_new_name_user_input()
    if new_name is None:
        return None
    return new_name, old_name


def update_old_name_user_input():
    old = input("Enter name of meal to update: ").lower()
    if old == 'x':
        return None
    elif old not in meal_dao.retrieve_all_meal_names():
        print(f"\nNo food named '{old}' exists.\n")
        return update_old_name_user_input()
    else:
        return old


def update_new_name_user_input():
    name = input("Enter new name (leave blank if unchanged): ")
    if name == 'x':
        return None
    if name in meal_dao.retrieve_all_meal_names():
        print(f"\nMeal named '{name}' already exists.\n")
        return update_new_name_user_input()
    else:
        return name


def view_all_foods():
    FTUI.table_view()



