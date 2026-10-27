# Food Delivery Orders ETL

This is a personal  project inspired by food delivery operations.
It uses sample data to demonstrate Python, SQL, and data quality checks.

## What the project does

1. Reads order and restaurant data from CSV files.
2. Checks orders for duplicate IDs, missing customer IDs, and negative amounts.
3. Loads accepted orders and restaurant details into a SQLite database.
4. Uses SQL to explore orders by restaurant.

## SQL reports

- Orders with restaurant names and cities
- Number of orders by restaurant
- Total delivered order amount by restaurant
- Average delivery time by restaurant

## Tools used

- Python
- SQLite
- SQL
- CSV files

## How to run

Open a terminal in the project folder and run:

    py .\read_orders.py

The script creates a database file called `food_delivery.db`.
