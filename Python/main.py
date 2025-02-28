from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__, template_folder="//Users//arsensyerikov//Desktop//Python//templates")

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content, created FROM posts')
    posts = [{'id': row[0], 'title': row[1], 'content': row[2], 'created': row[3]} for row in cursor.fetchall()]
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        content = request.form['content']
        title = request.form.get('title', None)

        if not content.strip():
            return "Вміст публікації не може бути порожнім."

        conn = sqlite3.connect('database.db')
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO posts (content, title) VALUES (?, ?)", (content, title))
        conn.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cur.fetchone()
    conn.close()

    if request.method == 'GET':
        if not post:
            return "Публікація не знайдена."
        return render_template('edit.html', post=post)
    else:
        content = request.form['content']
        title = request.form.get('title', None)

        if not content.strip():
            return "Вміст публікації не може бути порожнім."

        conn = sqlite3.connect('database.db')
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE posts SET content = ?, title = ? WHERE id = ?", (content, title, post_id))
        conn.close()

        return redirect(url_for('index', post_id=post_id))
    
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
