from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create my connection
engine = create_engine('mysql+mysqlconnector://root:ellietteGrace22@localhost/intro_orms')

Base = declarative_base()
pass

Session = sessionmaker(bind=engine)
session = Session()

#Models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    
    orders = relationship('Order', backref='user')
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    
    orders = relationship('Order', backref='product')
    

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    
    users = relationship('User', backref='orders')
    products = relationship('Product', backref='orders')

# Insert data (2 Users, 3 Products, 4 Orders)
user1 = User(name='Alice', email='alice@example.com', is_active=True)
user2 = User(name='Bob', email='bob@example.com', is_active=True)

product1 = Product(name='Laptop', price='1000', is_active=True)
product2 = Product(name='Phone', price='500', is_active=True)
product3 = Product(name='Tablet', price='300', is_active=True)

order1 = Order(user_id=1, product_id=1, quantity=1, status=True)
order2 = Order(user_id=1, product_id=2, quantity=2, status=True)
order3 = Order(user_id=2, product_id=2, quantity=1, status=True)
order4 = Order(user_id=2, product_id=3, quantity=3, status=True)

session.add_all([user1, user2, product1, product2, product3, order1, order2, order3, order4])
session.commit()

# Queries
# 1. Get all users and print their information
users = session.query(User).all()
for user in users:
    print(f'User ID: {user.id}, Name: {user.name}, Email: {user.email}, Active: {user.is_active}')
    
# 2. Get all products and print their information
products = session.query(Product).all()
for product in products:
    print(f'Product ID: {product.id}, Name: {product.name}, Price: {product.price}, Active: {product.is_active}')

# 3. Get all orders and print user's name, product's name, quantity, and status
orders = session.query(Order).all()
for order in orders:
    print(f'Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}, Status: {order.status}')
    
#4. Update a product's price
product_to_update = session.query(Product).filter_by(name='Laptop').first()
if product_to_update:
    product_to_update.price = '1200'
    session.commit()
    print(f'Updated Product: {product_to_update.name}, New Price: {product_to_update.price}')
    
#5. Delete a user by ID
user_to_delete = session.query(User).filter_by(id=2).first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print(f'Deleted User: {user_to_delete.name}')
    
#7. Get all orders that are not shipped (status=False)
unshipped_orders = session.query(Order).filter_by(status=False).all()
for order in unshipped_orders:
    print(f'Unshipped Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}')
    
#8. Get the total number of orders for each user
order_counts = session.query(User.name, func.count(Order.id)).join(Order).group_by(User.id).all()
for name, count in order_counts:
    print(f'User: {name}, Total Orders: {count}')    
    
    
    
Base.metadata.create_all(engine)