from datetime import datetime
from models import (Base, session, Inventory, engine)
import datetime
import csv
import time
import logging

logging.basicConfig(filename='log\store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %H:%M UTC')
logging.Formatter.converter = time.gmtime # From https://docs.python.org/3/library/logging.html


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
        print('''
            \n***** STORE INVENTORY SYSTEM *****
            \r1) Add Book
            \r2) View all books
            \r3) Search for book by ID
            \r4) Book Analysis
            \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ['a', 'v', 'b']:
            return choice
        else:
            input('''
                \rPlease choose of the options above.
                \rA number from 1-5.
                \rPress enter to try again.''')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()