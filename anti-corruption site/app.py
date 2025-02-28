from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Для flash-повідомлень

# Ініціалізація бази даних
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT UNIQUE,
                phone TEXT
            )
        ''')
        conn.commit()

# Головна сторінка входу
@app.route('/')
def home():
    return render_template('login.html')

# Вхід
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    
    if user:
        if user[2] == password:  # Перевірка пароля (індекс 2 - це пароль)
            return redirect(url_for('main_page'))
        else:
            flash("Невірний пароль. Спробуйте ще раз.")
            return redirect(url_for('home'))
    else:
        flash("Користувача не знайдено. Будь ласка, зареєструйтесь.")
        return redirect(url_for('register'))

# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        
        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)', (username, password, email, phone))
                conn.commit()
            flash("Успішна реєстрація! Ви можете увійти.")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("Користувач з таким ім'ям або електронною поштою вже існує.")
            return redirect(url_for('register'))
    
    return render_template('register.html')

# Головна сторінка після входу
@app.route('/main')
def main_page():
    return render_template('main_page.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
