# SQLAlchemy ORM Practice Project
## Author
Mary Fobbs‑Guillory

## Overview
This project is a hands‑on exploration of SQLAlchemy ORM, focusing on modeling relational data, creating tables, seeding initial records, and performing common database operations. It demonstrates how to build and manage relationships between Users, Products, and Orders using SQLAlchemy’s declarative syntax.

The project uses MySQL as the database backend, with MySQL Workbench used to visualize and inspect the schema. All interactions with the database—creating tables, inserting data, querying, updating, and deleting—are performed through SQLAlchemy ORM.

## Features
SQLAlchemy declarative models for Users, Products, and Orders

One‑to‑many relationship between Users and Orders

One‑to‑many relationship between Products and Orders

Association table defined for potential many‑to‑many expansion

Automatic table creation using Base.metadata.create_all()

Seed data insertion for users, products, and orders

Multiple example queries demonstrating ORM usage

Update and delete operations using SQLAlchemy session

Aggregate queries using SQL functions (func.count)

## Technologies Used
Python 3.x

SQLAlchemy ORM

MySQL

MySQL Workbench (for database inspection and validation)

## Database Structure
### Users Table
id (Primary Key)

name

email (unique)

is_active

Relationship: orders → One‑to‑many with Orders

### Products Table
id (Primary Key)

name

price

is_active

Relationship: orders → One‑to‑many with Orders

### Orders Table
id (Primary Key)

user_id (Foreign Key → Users)

product_id (Foreign Key → Products)

quantity

status

Relationship: belongs to both User and Product

### Association Table (Defined but not used in this version)
users_orders_products

user_id

order_id

product_id

This table is included to demonstrate how a many‑to‑many relationship could be implemented.

## Installation
1. Clone the repository
bash
git clone https://github.com/yourusername/your-repo-name
cd your-repo-name
2. Install dependencies
bash
pip install sqlalchemy mysql-connector-python
3. Configure MySQL connection
Update the connection string in the script:

python
engine = create_engine('mysql+mysqlconnector://root:yourpassword@localhost/intro_orms')
4. Create the database
In MySQL Workbench:

sql
CREATE DATABASE intro_orms;
Running the Script
Run the Python file to:

Create tables

Insert seed data

Execute queries

Print results to the console

bash
python main.py
## Queries Demonstrated in This Project
The script includes several example ORM queries:

Retrieve all users

Retrieve all products

Retrieve all orders with joined user/product info

Update a product’s price

Delete a user by email

Retrieve unshipped orders (status=False)

Count total orders per user using func.count

These examples show how SQLAlchemy handles CRUD operations, relationships, and aggregate functions.

## Using MySQL Workbench
MySQL Workbench was used to:

Create and inspect the intro_orms database

View tables and relationships

Verify inserted seed data

Confirm updates and deletions

Run manual SQL queries for comparison

## Project Purpose
This project was created to strengthen understanding of:

SQLAlchemy ORM modeling

Declarative base classes

Relationships and foreign keys

Session management

Query building

Database seeding

CRUD operations

Integrating Python with MySQL

It serves as a foundational exercise for building more advanced APIs and backend systems.

## Collaborators
Coding Temple, CoPilot
