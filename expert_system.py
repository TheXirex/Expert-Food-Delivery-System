from tabulate import tabulate as tb

check = []

class Dish:
    def __init__(self, name, dtype, vn, price, components):
        self.name = name
        self.dtype = dtype
        self.vn = vn
        self.price = price
        self.components = components
    def __str__(self) -> str:
        return f'Name: {self.name}\nType of dish: {self.dtype}\nV/N: {self.vn}\nPrice: {self.price}\nComponents: {self.components}\n'

def input_database(file_name):
    dishes = []
    with open(file_name) as text:
        for line in text:
            lst = line.split(':')

            name = lst[0]
            dtype = lst[1][2:-2]
            vn= lst[2][2:-2]
            price= float(lst[3][2:-2])
            components = [i.strip() for i in lst[4][2:-2].split(',')]

            obj = Dish(name, dtype, vn, price, components)
            dishes.append(obj)
    return dishes

def select_types(dishes):
    return list(set([i.dtype for i in dishes]))
        
def choose_dish_type(types):
    table = [[i + 1, types[i]] for i in range(len(types))]
    headers = ['Type']
    print(tb(table, headers, tablefmt = 'simple_grid'))
    print('What type of dish do you want?')
    while True:
        try:
            number = int(input('Enter the number of type: ')) - 1
        except:
            print('The answer must be an integer number! Try again.')
        else:    
            if 0 <= number < len(types):
                return types[number]
            else:
                print('Choose a number from the above.')

def print_ingridients(lst_ingridients):
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


def input_lst_ingridients(dishes):
    lst = input('Enter your ingridients separated by "/": ').split('/')
    set_dishes = set()
    for i in lst:
        for j in dishes:
            if i in j.components:
                set_dishes.add(j)
    return set_dishes, lst

def vn():
    ans = int(input('You ar vegan? 1 (meat) or 2 (vegan)'))
    if ans == 1:
        return False
    else:
        return True
    

def search(dishes):
    if vn(): dishes = [i for i in dishes if i.vn == 'V']
    else: dishes = [i for i in dishes if i.vn == 'N']
        
    set_ingridients = set()
    for dish in dishes:
        for ingridient in dish.components:
            set_ingridients.add(ingridient)
    lst_ingridients = sorted(list(set_ingridients))
    print_ingridients(lst_ingridients)
    new_dishes, lst = input_lst_ingridients(dishes)
    
    algorithm(new_dishes, lst)

def algorithm(new_dishes, lst):
    r_sidhes = list(new_dishes)
    while True:
        set_ingridients = set()
        for dish in r_sidhes:
            for ingridient in dish.components:
                if ingridient not in lst:
                    set_ingridients.add(ingridient)
        lst_ingridients = sorted(list(set_ingridients))
        while True:
            try:
                answer = int(input('Does your dish contain ' + lst_ingridients[0] + '?\n'))
                
                break
            except:
                print('Enter the number: 1 or 2.')
        
        removed_lst = []
        if answer == 1:
            for i in r_sidhes:
                if lst_ingridients[0] not in i.components:
                    removed_lst.append(i)
                    print(1)
            for i in removed_lst:
                r_sidhes.remove(i)
        else:
            for i in r_sidhes:
                if lst_ingridients[0] in i.components:
                    removed_lst.append(i)
                    print(2)
            for i in removed_lst:
                r_sidhes.remove(i)
        
        lst_ingridients.remove(lst_ingridients[0])

        if len(r_sidhes) == 1:
            print('\nYour dish is ' + r_sidhes[0] + '!\n\nIf you riddle another dish, it means that this dish is not in the database.'
                '\nAdd it and make the system better!')
            break
        elif len(r_sidhes) < 1 or len(lst_ingridients) < 1:
            print('\nSorry, but there is not enough information about your dish in the database.')
            break
        

    
    



def main():
    dishes = input_database('database.txt')
    types = select_types(dishes)
    dish_type = choose_dish_type(types)
    dish = search([i for i in dishes if i.dtype == dish_type])

    

if __name__ == '__main__':
    main()
               

    

