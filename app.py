from datetime import datetime
from models import (Base, session, Inventory, engine)
import datetime
import csv
import time
import logging

logging.basicConfig(filename='log\store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %H:%M UTC')
logging.Formatter.converter = time.gmtime # From https://docs.python.org/3/library/logging.html

class NotInListError(Exception):
    pass

def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        return_int = int(float(split_price[1]) * 100)
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number without a current symbol.
            \rEx: 10.99
            \rPress enter to try again.
            \r*************************''')
        return
    else:
        return return_int


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR ******
            \rThe date format should include a valid Month/Day/Year from the past.
            \rEx: 10/14/1980
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return return_date


def clean_id(id_str, id_options):
    try:
        item_id = int(id_str)
        if item_id not in id_options:
            raise NotInListError
    except ValueError:
        input('''
            \n****** ID ERROR ******
            \rThe ID should be a number.
            \rEx: 10
            \rPress enter to try again.
            \r*************************''')
        return
    except NotInListError:
        input(f'''
            \n****** ID ERROR ******
            \rThe ID should be one that is in the following list.
            \rOptions: {id_options}
            \rPress enter to try again.
            \r*************************''')
        return
    else:
        return item_id


def compare_items(db_item, other_item):
    if db_item == None:
        name = other_item[0]
        price = clean_price(other_item[1])
        qty = int(other_item[2])
        date = clean_date(other_item[3])
        new_item = Inventory(product_name=name, product_price=price, product_qty=qty, date_updated=date)
        session.add(new_item)
        session.commit()
        logging.info(f'New item added to database: {new_item}.')
    elif db_item.date_updated > clean_date(other_item[3]):
        logging.info(
            f'"{db_item.product_name}" already exists in the database and a more recent item exists in the database. Discarding item.')
    elif db_item.date_updated < clean_date(other_item[3]):
        logging.info(f'***** REPLACING Item *****')
        logging.info(f'\tOld Item: Name: {db_item.product_name}, ID: {db_item.product_id}, Price: {db_item.product_price}, Quantity: {db_item.product_qty}, Date Updated: {db_item.date_updated}.')
        logging.info(f'\tNew Item: Name: {other_item[0]}, ID: {db_item.product_id}, Price: {clean_price(other_item[1])}, Quantity: {int(other_item[2])}, Date Updated: {clean_date(other_item[3])}.')
        db_item.product_name = other_item[0]
        db_item.product_price = clean_price(other_item[1])
        db_item.product_qty = int(other_item[2])
        db_item.date_updated = clean_date(other_item[3])
        session.commit()
        logging.info(
            f'{db_item.product_name} successfully updated.')
    else:
        logging.info(f'"{db_item.product_name}" already exists in the database and no other entries detected. Discarding item.')


def display_inventory():
    print()
    for item in session.query(Inventory):
        print(f'{item.product_id} | {item.product_name}')
        time.sleep(.05)
    input('\nPress enter to return to the main menu...')


def search_inventory_by_id():
    id_list = []
    for item in session.query(Inventory):
        id_list.append(item.product_id)
    id_error = True
    while id_error:
        print(f'The IDs of items in the store are:\n{id_list}\n')
        id_choice = input('Please enter the ID of an item: ')
        id_choice = clean_id(id_choice, id_list)
        if type(id_choice) == int:
            id_error = False
    the_item = session.query(Inventory).filter(Inventory.product_id == id_choice).first()
    print(f'''
        \n{the_item.product_name} -
        \rPrice: {the_item.product_price/100}
        \rQuantity: {the_item.product_qty}
        \rLast Updated: {the_item.date_updated.strftime("%m-%d-%Y")}\n''')
    input('Press enter to return to the main menu...')


def add_product_to_inventory():
    pass


def backup_inventory():
    pass


def add_csv():
    with open('store-inventory\inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        # Modified from code at: https://linuxhint.com/skip-header-row-csv-python/
        next(data)
        for row in data:
            item_in_db = session.query(Inventory).filter(Inventory.product_name==row[0]).one_or_none()
            compare_items(item_in_db, row)

def menu():
    while True:
        valid_choices = ['p', 'v', 'a', 'b', 'x']
        print('''
            \n***** STORE INVENTORY SYSTEM *****
            \rp) Print all items in the database
            \rv) View a single product's inventory
            \ra) Add a new product to the database
            \rb) Make a backup of the entire inventory
            \rx) Exit''')
        choice = input('What would you like to do? ')
        if choice in valid_choices:
            return choice
        else:
            input(f'''
                \rPlease only choose items from the following list:
                \r{valid_choices}
                \rPress enter to try again.''')


def app():
    app_running = True
    while app_running:
        user_choice = menu()
        if user_choice == 'p':
            # "View all items in the database"
            display_inventory()

        elif user_choice == 'v':
            # "View a single product's inventory"
            search_inventory_by_id()
            
        elif user_choice == 'a':
            # "Add a new product to the database"
            pass
        elif user_choice == 'b':
            # "Make a backup of the entire inventory"
            pass
        elif user_choice == 'x':
            # "Exit Program"
            print("Thank you for utilizing the store inventory system. Have a good day!")
            time.sleep(2)
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #add_csv()
    app()