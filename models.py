from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db/inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'inventory'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_qty = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Last_Updated', Date)
    
    def __repr__(self):
        return f'Product Name: {self.product_name}, Product Quantity: {self.product_qty}, Product Price: ${self.product_price}, Last Updated: {self.date_updated}'
