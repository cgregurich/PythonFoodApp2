from fooditem import FoodItem
from fooditemdao import FoodItemDAO
from mealdao import MealDAO
from tabulate import tabulate
import mealtextuserinterface as MTUI

food_dao = FoodItemDAO()
meal_dao = MealDAO()

def run():
    display_menu()
    command = get_command()
    while command:
        command = get_command()


def display_menu():
    print("\nFOODS COMMANDS")
    print("(Enter x at any time to cancel command)")
    print("VIEW - View all foods")
    print("ADDM - Add as many foods as you want")
    print("ADD - Add a new food")
    print("DEL - Delete a food by name")
    print("UPDATE - Update a food")
    print("SORT - Sort all foods")
    print("CALC - Calculate macros for a given food")
    print("HELP - Display this menu")
    print("MEALS - Switch to meals mode")
    print("QUIT - Quit the program")


def get_command():
    command = (input("\nEnter commmand: ")).lower()
    if command == 'addm':
        add_multiple()
        return True
    if command == 'view':
        view()
        return True
    if command == 'add':
        add_food()
        return True
    if command == 'del':
        del_food()
        return True
    if command == 'update':
        update_food()
        return True
    if command == 'sort':
        sort_foods()
        return True
    if command == 'calc':
        calc()
        return True
    if command == 'help':
        display_menu()
        return True
    if command == 'meals':
        MTUI.run()
        return None
    if command == 'quit' or command == 'exit' or command == 'x':
        return None
    else:
        print("\nInvalid command.")
        return get_command()

def add_multiple():
    x = True
    while x is True:
        x = add_food()



def is_db_empty():
    foods = food_dao.retrieve_all_foods()
    if foods:
        return False
    else:
        return True

def view():
    if is_db_empty():
        print("\nNo foods found. Use the ADD command to add a food.")
        return None
    table_view(food_dao.retrieve_all_foods())

def add_food():
    food = add_user_input()
    if food is not None:
        food_dao.insert_food(food)
        return True
    else:
        return False


def add_user_input():
    print("\nADD FOOD")
    info = {'name': None, 'ss': 0, 'unit': None, 'cal': 0, 'carb': 0, 'fat': 0,
            'protein': 0, 'fiber': 0, 'sugar': 0}
    for key in info.keys():
        if key == 'name':
            name = add_name_user_input()
            if name is None:
                return None
            info[key] = name
        elif key == 'unit':
            unit = add_unit_user_input()
            if unit is None:
                return None
            info[key] = unit
        else:
            n = add_number_user_input(key)
            if n is None:
                return None
            info[key] = n
    return FoodItem(info)

def add_name_user_input():
    name = input("Enter name: ")
    if name == 'x':
        return None
    elif food_dao.retrieve_food(name):
        print(f"\nThere is already a food called '{name}'.\n")
        return add_name_user_input()
    else:
        return name

def add_unit_user_input():
    unit = input("Enter unit: ")
    if unit == 'x':
        return None
    else:
        return unit

def add_number_user_input(key):
    ans = input(f"Enter {key}: ")
    if ans == 'x':
        return None
    else:
        try:
            ans = float(ans)
            if ans < 0:
                print(f"\n{key} can't be negative.\n")
                return add_number_user_input(key)
            else:
                return ans
        except ValueError:
            print(f"\n{ans} is not a valid amount.\n")
            return add_number_user_input(key)




def del_food():
    if is_db_empty():
        print("\nNo foods found. Use the ADD command to add a food.")
        return None


    name = del_user_input()
    if name is None:
        return None
    food_dao.delete_food(name)
    meal_dao.delete_food_with_name(name)
    if (food_dao.c.rowcount == 1):
        print(f"\n'{name}' was deleted.")
        if meal_dao.c.rowcount > 0:
            print("Some meals were affected.")
        else:
            print("No meals were affected.")

    else:
        print("\nSomething went wrong.")


def del_user_input():
    print("\nDELETE FOOD")
    name = ''
    while True:
        name = input("Enter name of food to delete: ")
        if name == 'x':
            return None
        food_by_name = food_dao.retrieve_food(name)
        if food_by_name is None:
            print(f"\nNo food called '{name}' exists.\n")
        else:
            return name




def update_food():
    if is_db_empty():
        print("\nNo foods found. Use the ADD command to add a food.")
        return None

    update_tup = update_food_user_input()
    if update_tup is None:
        return None
    else:
        food_dao.update_food(update_tup[1], update_tup[0])
        if food_dao.c.rowcount == 1:
            print("Update successful.")
        else:
            print("Something went wrong.")



# new
def update_food_user_input():
    print("\nUPDATE FOOD")
    updated_info = {'name': None, 'ss': 0, 'unit': None, 'cal': 0, 'carb': 0, 'fat': 0,
                    'protein': 0, 'fiber': 0, 'sugar': 0}
    old_name = update_old_name_user_input()
    if old_name is None:
        return None
    old_food = food_dao.retrieve_food(old_name)
    for key in updated_info.keys():
        if key == 'name':
            name = update_name_user_input()
            if name is None:
                return None
            if name == '':
                name = old_food.name
            updated_info[key] = name
        elif key == 'unit':
            unit = update_unit_user_input()
            if unit is None:
                return None
            if unit == '':
                unit = old_food.unit
            updated_info[key] = unit
        else:
            n = update_number_user_input(key)
            if n is None:
                return None
            if n == '':
                n = old_food.info[key]
            updated_info[key] = n
    return old_name, FoodItem(updated_info)

def update_old_name_user_input():
    old = input("Enter name of food to update: ")
    if old == 'x':
        return None
    elif old not in food_dao.retrieve_all_food_names():
        print(f"\nNo food named '{old}' exsits.\n")
        return update_old_name_user_input()
    else:
        return old


def update_name_user_input():
    name = input("Enter new name (leave blank if unchanged): ")
    if name == 'x':
        return None
    if name in food_dao.retrieve_all_food_names():
        print(f"\nFood named '{name}' already exists.\n")
        return update_name_user_input()
    else:
        return name


def update_unit_user_input():
    unit = input("Enter new unit (leave blank if unchanged): ")
    if unit == 'x':
        return None
    else:
        return unit


def update_number_user_input(key):
    ans = input(F"Enter new {key} (leave blank if unchanged): ")
    if ans == 'x':
        return None
    if ans == '':
        return ''
    else:
        try:
            ans = float(ans)
            if ans < 0:
                print(f"\n{key} can't be negative.\n")
                return update_number_user_input(key)
            else:
                return ans
        except ValueError:
            print(f"\n{ans} is not a valid amount.\n")
            return update_number_user_input(key)


def sort_foods():
    if is_db_empty():
        print("\nNo foods found. Use the ADD command to add a food.")
        return None

    sort_info = sort_user_input()
    if None in sort_info:
        return None
    sorted_foods = food_dao.sort_foods(sort_info[0], sort_info[1])
    table_view(sorted_foods)


def sort_user_input():
    print("\nSORT FOODS")
    valid = ('name', 'ss', 'unit', 'cal', 'carb', 'fat', 'protein', 'fiber', 'sugar')
    sort_type = ''

    while sort_type not in valid:
        print("\nSort by what?")
        sort_type = input("(name ss unit cal carb fat protein fiber sugar): ").lower()
        if sort_type == 'x':
            return None, None
        if sort_type not in valid:
            print("\nInvalid input.")
    order = ''
    while order != 'ASC' and order != 'DESC':

        print("\nAscending or descending?")
        order = input("(ASC or DESC): ").upper()
        if order == 'X':
            return None, None
        if order != 'ASC' and order != 'DESC':
            print("\nInvalid input.")
    return sort_type, order

def calc():
    if is_db_empty():
        print("\nNo foods found. Use the ADD command to add a food.")
        return None

    calc_info = calc_user_input()
    if calc_info is None:
        return None
    food = calc_info[0]
    food.proportionalize(calc_info[1])
    foods = [food]
    table_view(foods)




def calc_user_input():
    print("\nCALCULATE FOODS")
    name = input("Enter name of food to calculate: ")
    if name == 'x':
        return None
    food_by_name = food_dao.retrieve_food(name)
    if food_by_name is None:
        print(f"\nNo food called {name} exists.")
        return calc_user_input()

    amount = input("Enter amount to calculate: ")
    if amount == 'x':
        return None
    else:
        amount = float(amount)

    return food_by_name, amount

def table_view(foods_list=None, headers=['NAME', 'SS', 'UNIT', 'CAL', 'CARB', 'FAT', 'PROTEIN', 'FIBER', 'SUGAR']):
    data = []
    if foods_list is None:
        foods_list = food_dao.retrieve_all_foods()
    for food in foods_list:
        data.append(food.get_tuple())
    print("\nDISPLAYING ALL FOODS")
    print(tabulate(data, headers))


