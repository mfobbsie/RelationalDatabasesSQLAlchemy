from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create my connection
engine = create_engine('mysql+mysqlconnector://root:ellietteGrace22@localhost/intro_orms')

Base = declarative_base()
pass

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    
Base.metadata.create_all(engine)