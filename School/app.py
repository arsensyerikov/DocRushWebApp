from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    teacher_name = db.Column(db.String(100), nullable=False)

# Тільки 1-9 класи
class_list = ["1 клас", "2 клас", "3 клас", "4 клас", "5 клас", "6 клас", "7 клас", "8 клас", "9 клас"]
# 9 випадкових класних керівників
teacher_list = [
    "Олександр Петрович", "Марина Іванівна", "Сергій Олегович", 
    "Наталія Володимирівна", "Ігор Миколайович", "Ганна Сергіївна", 
    "Василь Степанович", "Юлія Олександрівна", "Михайло Андрійович"
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not all(k in request.form for k in ('first_name', 'last_name', 'password', 'class_name', 'teacher_name')):
            return "Всі поля повинні бути заповнені!", 400
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        class_name = request.form['class_name']
        teacher_name = request.form['teacher_name']
        
        user = User.query.filter_by(first_name=first_name, last_name=last_name, password=password, class_name=class_name, teacher_name=teacher_name).first()
        if user:
            session['first_name'] = first_name
            session['last_name'] = last_name
            return redirect('/welcome')
        else:
            return redirect('/register')
    
    return render_template('login.html', class_list=class_list, teacher_list=teacher_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not all(k in request.form for k in ('first_name', 'last_name', 'password', 'class_name', 'teacher_name')):
            return "Всі поля повинні бути заповнені!", 400
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        class_name = request.form['class_name']
        teacher_name = request.form['teacher_name']
        
        new_user = User(first_name=first_name, last_name=last_name, password=password, class_name=class_name, teacher_name=teacher_name)
        db.session.add(new_user)
        db.session.commit()
        
        session['first_name'] = first_name
        session['last_name'] = last_name
        return redirect('/welcome')
    
    return render_template('register.html', class_list=class_list, teacher_list=teacher_list)

@app.route('/welcome')
def welcome():
    if 'first_name' in session and 'last_name' in session:
        return render_template('welcome.html', first_name=session['first_name'], last_name=session['last_name'])
    return redirect('/')

@app.route('/homework')
def homework():
    return render_template('homework.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/absence')
def absence():
    return render_template('absence.html')

@app.route('/class')
def class_page():
    return render_template('class.html')

@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)