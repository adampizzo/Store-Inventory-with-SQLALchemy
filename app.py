from datetime import datetime
from models import (Base, session, Inventory, engine)
import datetime
import csv
import time
import logging

logging.basicConfig(filename='log\store.log', encoding='utf-8', level=logging.DEBUG)

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




def add_csv():
    with open('store-inventory\inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        # Modified from code at: https://linuxhint.com/skip-header-row-csv-python/
        next(data)
        for row in data:
            item_in_db = session.query(Inventory).filter(Inventory.product_name==row[0]).one_or_none()
            if item_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                qty = int(row[2])
                date = clean_date(row[3])
                new_item = Inventory(product_name=name, product_price=price, product_qty=qty, date_updated=date)
                session.add(new_item)
            elif item_in_db.date_updated > clean_date(row[3]):
                logging.info(
                    f'"{item_in_db.product_name}" already exists in the database and a more recent item exists in the database. Discarding item {datetime.datetime.now(datetime.timezone.utc).strftime("%m-%d-%Y %H:%M %Z")}.')
                time.sleep(1)
            elif item_in_db.date_updated < clean_date(row[3]):
                print(f'''
                    \n***** REPLACING ENTRY *****
                    \rOld Item:
                    \rName: {item_in_db.product_name}
                    \rID: {item_in_db.product_id}
                    \rPrice: {item_in_db.product_price}
                    \rQuantity: {item_in_db.product_qty}
                    \rDate Updated: {item_in_db.date_updated}
                    \r
                    \rNew Item:
                    \rName: {row[0]}
                    \rID: {item_in_db.product_id}
                    \rPrice: {clean_price(row[1])}
                    \rQuantity: {int(row[2])}
                    \rDate Updated: {clean_date(row[3])}
                    ''')
                
                item_in_db.product_name = row[0]
                item_in_db.product_price = clean_price(row[1])
                item_in_db.product_qty = int(row[2])
                item_in_db.date_updated = clean_date(row[3])
                logging.info(f'{item_in_db.product_name} successfully updated at {datetime.datetime.now(datetime.timezone.utc).strftime("%m-%d-%Y %H:%M %Z")}.')
            else:
                logging.info(f'"{item_in_db.product_name}" already exists in the database and no other entries detected. Discarding item at {datetime.datetime.now(datetime.timezone.utc).strftime("%m-%d-%Y %H:%M %Z")}.')
        session.commit()




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()