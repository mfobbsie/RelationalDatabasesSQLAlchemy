from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func, Float, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Create my connection
engine = create_engine('mysql+mysqlconnector://root:ellietteGrace22@localhost/intro_orms')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

#Association Table with relationships
users_orders_products = Table(
    'users_orders_products',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

#Models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    
    orders = relationship('Order', back_populates='product')
    

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

Base.metadata.create_all(engine)

# Insert data (2 Users, 3 Products, 4 Orders)
user_seed = [
    {'name': 'Alice', 'email': 'alice@example.com', 'is_active': True},
    {'name': 'Bob', 'email': 'bob@example.com', 'is_active': True},
]

product_seed = [
    {'name': 'Laptop', 'price': 1000.00, 'is_active': True},
    {'name': 'Phone', 'price': 500.00, 'is_active': True},
    {'name': 'Tablet', 'price': 300.00, 'is_active': True},
]

order_seed = [
    {'user_email': 'alice@example.com', 'product_name': 'Laptop', 'quantity': 1, 'status': True},
    {'user_email': 'alice@example.com', 'product_name': 'Phone', 'quantity': 2, 'status': True},
    {'user_email': 'bob@example.com', 'product_name': 'Phone', 'quantity': 1, 'status': True},
    {'user_email': 'bob@example.com', 'product_name': 'Tablet', 'quantity': 3, 'status': True},
]

users_by_email = {}
for user_data in user_seed:
    user = session.query(User).filter_by(email=user_data['email']).first()
    if not user:
        user = User(**user_data)
        session.add(user)
    users_by_email[user_data['email']] = user

products_by_name = {}
for product_data in product_seed:
    product = session.query(Product).filter_by(name=product_data['name']).first()
    if not product:
        product = Product(**product_data)
        session.add(product)
    products_by_name[product_data['name']] = product

session.commit()

if session.query(Order).count() == 0:
    order_seed = [
        {'user_email': 'alice@example.com', 'product_name': 'Laptop', 'quantity': 1, 'status': True},
        {'user_email': 'alice@example.com', 'product_name': 'Phone', 'quantity': 2, 'status': True},
        {'user_email': 'bob@example.com', 'product_name': 'Phone', 'quantity': 1, 'status': True},
        {'user_email': 'bob@example.com', 'product_name': 'Tablet', 'quantity': 3, 'status': True},
    ]

    for order_data in order_seed:
        session.add(
            Order(
                user=users_by_email[order_data['user_email']],
                product=products_by_name[order_data['product_name']],
                quantity=order_data['quantity'],
                status=order_data['status'],
            )
        )
    session.commit()

# Queries
# 1. Get all users and print their information
for user in session.query(User).all():
    print(f'User ID: {user.id}, Name: {user.name}, Email: {user.email}, Active: {user.is_active}')
    
# 2. Get all products and print their information
for product in session.query(Product).all():
    print(f'Product ID: {product.id}, Name: {product.name}, Price: {product.price}, Active: {product.is_active}')

# 3. Get all orders and print user's name, product's name, quantity, and status
for order in session.query(Order).all():
    print(f'Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}, Status: {order.status}')
    
#4. Update a product's price
product_to_update = session.query(Product).filter_by(name='Laptop').first()
if product_to_update:
    product_to_update.price = 1200.00
    session.commit()
    print(f'Updated Product: {product_to_update.name}, New Price: {product_to_update.price}')
    
#5. Delete a user by email
user_to_delete = session.query(User).filter_by(email='bob@example.com').first()
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