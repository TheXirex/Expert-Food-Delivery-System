from tabulate import tabulate as tb
import os

# done
class Dish:
    def __init__(self, name, dtype, vn, price, components):
        self.name = name
        self.dtype = dtype
        self.vn = vn
        self.price = price
        self.components = components
    def __str__(self) -> str:
        return f'Title: {self.name}\nComponents: {self.components}\nPrice: ${self.price}'

# done
def input_database(file_name):
    dishes = []
    with open(file_name) as text:
        for line in text:
            lst = line.split(':')

            name = lst[0][:-1]
            dtype = lst[1][2:-2]
            vn= lst[2][2:-2]
            price= float(lst[3][2:-2])
            components = [i.strip() for i in lst[4][2:-2].split(',')]

            obj = Dish(name, dtype, vn, price, components)
            dishes.append(obj)
    return dishes

# done
def select_types(dishes) -> list:
    types = []
    for dish in dishes:
        if dish.dtype not in types:
            types.append(dish.dtype)
    return types

# done    
def choose_dish_type(types):

    table = [[i + 1, types[i]] for i in range(len(types))]
    print(tb(table, ['Type'], tablefmt = 'simple_grid'))
    
    print('What type of dish do you want?')
    while True:
        try:
            number = int(input('Enter the number of dish type: ')) - 1
        except:
            print('The answer must be an integer number! Try again.')
        else:    
            if 0 <= number < len(types):
                return types[number]
            else:
                print('Choose a number from the above.')

# done
def print_ingridients(lst_ingridients) -> None:

    table = []
    row = []

    for i in range(len(lst_ingridients)):
        row.append(lst_ingridients[i])
        if i != len(lst_ingridients) - 1:
            if len(row) == 4:
                table.append(row)
                row = []
        else:
            table.append(row)
            break
    print(tb(table, tablefmt = 'simple_grid'))

# done
def input_lst_ingridients(dishes):

    set_ingridients = []

    for dish in dishes:
        for ingridient in dish.components:
            if ingridient not in set_ingridients:
                set_ingridients.append(ingridient)

    while True:
        flag = True
        input_ingridients = input('Enter your ingridients separated by "/": ')
        if input_ingridients == '':
            print('Empty line, please enter the ingredient(s).')
            flag = False
        elif '/' not in input_ingridients:
            if input_ingridients not in set_ingridients:
                print('Your ingredients are misspelled. Try again.')
                flag = False
            else:
                lst_ingridients = []
                lst_ingridients.append(input_ingridients)
        else:
            lst_ingridients = input_ingridients.split('/')
            for ingridient in lst_ingridients:
                if ingridient not in set_ingridients:
                    print('One or some of the ingredients on your list are misspelled (or you misspelled distributor). Try again.')
                    flag = False
                    break
        
        if not flag: continue

        set_dishes = []
        
        for ingridient in lst_ingridients:
            for dish in dishes:
                if dish not in set_dishes:
                    if ingridient in dish.components:
                        set_dishes.append(dish)

        return set_dishes, lst_ingridients

# done
def vegeterian():
    while True:
        try:
            ans = int(input('Are you a vegetarian? (<1> to confirm or <2> to reject): '))
        except:
            print('Incorrect value. Enter <1> to confirm or <2> to reject.')
        else:
            if ans == 1: return True
            elif ans == 2: return False
            else: print('Incorrect value. Enter <1> to confirm or <2> to reject.')
    
def search(dishes):
    if vegeterian(): dishes = [i for i in dishes if i.vn == 'V']
    else: dishes = [i for i in dishes if i.vn == 'N']
        
    set_ingridients = []

    for dish in dishes:
        for ingridient in dish.components:
            if ingridient not in set_ingridients:
                set_ingridients.append(ingridient)

    print_ingridients(set_ingridients)

    new_dishes, lst = input_lst_ingridients(dishes)

    lst_dishes = algorithm(new_dishes, lst)

    dish = choose_dish(lst_dishes)

    return dish


def algorithm(new_dishes, lst):

    dish_lst = new_dishes
    removed_ingridients = lst

    while True:

        set_ingridients = []

        for dish in dish_lst:
            for ingridient in dish.components:
                if ingridient not in lst and ingridient not in set_ingridients:
                    set_ingridients.append(ingridient)
        
        print(set_ingridients)

        while True:
            try:
                ans = int(input(f'Do you want to see {set_ingridients[0]} in a dish? (<1> to confirm or <2> to reject): '))
            except:
                print(set_ingridients[0])
                print('Incorrect value. Enter <1> to confirm or <2> to reject.3')

            else:
                if ans == 1 or ans == 2:
                    break
                else:
                    print('Incorrect value. Enter <1> to confirm or <2> to reject.4')

        removed_lst = []

        if ans == 1:
            for i in dish_lst:
                if set_ingridients[0] not in i.components:
                    removed_lst.append(i) 
        else:
            for i in dish_lst:
                if set_ingridients[0] in i.components:
                    removed_lst.append(i)

        for i in removed_lst:
            dish_lst.remove(i)
        
        removed_ingridients.append(set_ingridients[0])

        if len(dish_lst) == 1:
            print('\nYour dish is ' + dish_lst[0].name + '!')
            dish = [dish_lst[0]]
            return [dish, removed_lst]
        
        elif len(dish_lst) < 1 or len(set_ingridients) < 1:
            print('\nSorry, but there is not enough information about your dish in the database.')
            return [[], removed_lst]


def choose_dish(lst_dish):
    if len(lst_dish[0]) == 1:
        ans = int(input('Would you like to add that dish to the check? (<1> to confirm or <2> to reject): '))
        if ans == 1:
            return lst_dish[0][0]
        else:
            print('I can offer you alternatives with the ingredients you chose:')
            dish = choose_dish_in_removed_lst(lst_dish)
            return dish
    else:
        print('There are no dishes with a similar set of ingredients, but I can offer you alternatives with the ingredients of your choice:')
        dish = choose_dish_in_removed_lst(lst_dish)
        return dish

def choose_dish_in_removed_lst(lst_dish):
    for i in range(len(lst_dish[1])):
        print(f'{i+1}: {lst_dish[1][i]}')
        while True:
            try:
                number = int(input('Enter the number of dish type: ')) - 1
            except:
                print('The answer must be an integer number! Try again.')
            if number == -1:
                return None
            else:    
                if 0 <= number < len(lst_dish[1]):
                    return lst_dish[1][number]
                else:
                    print('Choose a number from the above.')
            
# not done
def add_check(check, dish):
    check.append([dish.name, dish.price])
    print(tb(check, ['Name', 'Price'], tablefmt = 'simple_grid'))
    return check

def print_final_check(check):
    if len(check) != 0:
        print(tb(check, ['Name', 'Price'], tablefmt = 'simple_grid'))

    else:
        print(tb(check, ['Name', 'Price'], tablefmt = 'simple_grid'))

# done
def next_position():
    while True:
        try:
            ans = int(input('Do you want to continue to choose? (<1> to confirm or <2> to reject): '))
        except:
            print('Incorrect value. Enter <1> to confirm or <2> to reject.5')
        else:
            if ans == 1: return True
            else: return False

def main():
    check = []
    while True:
        dishes = input_database('database.txt')
        types = select_types(dishes)
        dish_type = choose_dish_type(types)
        dish = search([i for i in dishes if i.dtype == dish_type])

        if dish != None:
            check = add_check(check, dish)
        
        os.system('cls')

        if not next_position():
            print_final_check(check)
            break
            

if __name__ == '__main__':
    main()