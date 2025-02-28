import sqlite3

connection = sqlite3.connect('database.db')


with open('C:\\Users\\Mariy_Dell\\Desktop\\Сайт\\main\\schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
('First Post', 'Content for the first post')
)

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
('Second Post', 'Content for the second post')
)

connection.commit()
connection.close()
