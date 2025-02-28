from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_greeting():
    conn = sqlite3.connect('greetings.db')
    c = conn.cursor()
    c.execute('SELECT message FROM greetings WHERE id = 1')
    greeting = c.fetchone()[0]
    conn.close()
    return greeting

def add_greeting(message):
    conn = sqlite3.connect('greetings.db')
    c = conn.cursor()
    c.execute('INSERT INTO greetings (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    greeting_message = get_greeting()
    return render_template('index.html', greeting=greeting_message)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_greeting = request.form['greeting']
        add_greeting(new_greeting)
        return redirect(url_for('index'))
    return render_template('add_greeting.html')

if __name__ == '__main__':
    app.run(debug=True)
