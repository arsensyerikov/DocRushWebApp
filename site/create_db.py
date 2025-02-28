import sqlite3

# Створення бази даних і таблиці
conn = sqlite3.connect('greetings.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS greetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL
    )
''')

# Додавання привітання
c.execute('''
    INSERT INTO greetings (message)
    VALUES ('Вітаю вас на нашій сторінці!')
''')

conn.commit()
conn.close()
