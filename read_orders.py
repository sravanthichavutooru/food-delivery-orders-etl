import csv
import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent
orders_file = project_folder / "data" / "orders.csv"

seen_order_ids = set()
unique_orders = []

with orders_file.open(newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, skipinitialspace=True)    
    print("Column names:", reader.fieldnames)

    for order in reader:
        order_id = order["order_id"].strip()

        if not order["customer_id"].strip():
            print("Missing customer ID for order:", order_id)
            continue

        if float(order["amount"]) < 0:
            print("Negative amount for order:", order_id)
            continue

        if order_id in seen_order_ids:
            print("Skipping duplicate:", order_id)
            continue

        seen_order_ids.add(order_id)
        unique_orders.append(order)

print("Orders kept:", len(unique_orders))
database_file = project_folder / "food_delivery.db"
connection = sqlite3.connect(database_file)

print("Database created:", database_file)


connection.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        order_date TEXT,
        restaurant_id TEXT,
        customer_id TEXT,
        amount REAL,
        status TEXT,
        delivery_min INTEGER
    )
""")

connection.commit()
connection.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        order_date TEXT,
        restaurant_id TEXT,
        customer_id TEXT,
        amount REAL,
        status TEXT,
        delivery_min INTEGER
    )
""")

connection.commit()
connection.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        order_date TEXT,
        restaurant_id TEXT,
        customer_id TEXT,
        amount REAL,
        status TEXT,
        delivery_min INTEGER
    )
""")

connection.commit()
print("Orders table is ready")
for order in unique_orders:
    connection.execute("""
        INSERT OR IGNORE INTO orders
        (order_id, order_date, restaurant_id, customer_id,
         amount, status, delivery_min)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order["order_id"].strip(),
        order["order_date"].strip(),
        order["restaurant_id"].strip(),
        order["customer_id"].strip(),
        float(order["amount"]),
        order["status"].strip(),
        order["delivery_minutes"].strip() or None
    ))

connection.commit()

count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print("Orders in database:", count)
print("\nOrders in the database:")

rows = connection.execute(
    "SELECT order_id, restaurant_id, amount, status FROM orders"
).fetchall()

for row in rows:
    print(row)
    connection.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id TEXT PRIMARY KEY,
        restaurant_name TEXT,
        city TEXT
    )
""")

connection.commit()
print("Restaurants table is ready")
restaurants_file = project_folder / "data" / "restaurants.csv"

with restaurants_file.open(newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, skipinitialspace=True)

    for restaurant in reader:
        connection.execute("""
            INSERT OR IGNORE INTO restaurants
            (restaurant_id, restaurant_name, city)
            VALUES (?, ?, ?)
        """, (
            restaurant["restaurant_id"].strip(),
            restaurant["restaurant_name"].strip(),
            restaurant["city"].strip()
        ))

connection.commit()

count = connection.execute(
    "SELECT COUNT(*) FROM restaurants"
).fetchone()[0]

print("Restaurants in database:", count)


connection.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id TEXT PRIMARY KEY,
        restaurant_name TEXT,
        city TEXT
    )
""")

connection.commit()
print("Restaurants table is ready")
print("\nOrders with restaurant names:")

rows = connection.execute("""
    SELECT orders.order_id,
           restaurants.restaurant_name,
           restaurants.city,
           orders.amount
    FROM orders
    JOIN restaurants
        ON orders.restaurant_id = restaurants.restaurant_id
""").fetchall()

for row in rows:
    print(row)
print("\nNumber of orders by restaurant:")

rows = connection.execute("""
    SELECT restaurants.restaurant_name,
           COUNT(*) AS order_count
    FROM orders
    JOIN restaurants
        ON orders.restaurant_id = restaurants.restaurant_id
    GROUP BY restaurants.restaurant_name
""").fetchall()

for row in rows:
    print(row)
    print("\nDelivered order amount by restaurant:")

rows = connection.execute("""
    SELECT restaurants.restaurant_name,
           SUM(orders.amount) AS total_amount
    FROM orders
    JOIN restaurants
        ON orders.restaurant_id = restaurants.restaurant_id
    WHERE orders.status = 'delivered'
    GROUP BY restaurants.restaurant_name
""").fetchall()

for row in rows:
    print(row)
print("\nAverage delivery time by restaurant:")

rows = connection.execute("""
    SELECT restaurants.restaurant_name,
           AVG(orders.delivery_min) AS average_minutes
    FROM orders
    JOIN restaurants
        ON orders.restaurant_id = restaurants.restaurant_id
    WHERE orders.status = 'delivered'
    GROUP BY restaurants.restaurant_name
""").fetchall()

for row in rows:
    print(row)


connection.close()