import sqlite3

# Підключаємося до бази даних
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Вибираємо всі замовлення
cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()

# Виводимо результат
if orders:
    for order in orders:
        print(f"ID: {order[0]}, User ID: {order[1]}, Description: {order[2]}, Status: {order[3]}")
else:
    print("Немає замовлень.")

# Закриваємо з'єднання
conn.close()
