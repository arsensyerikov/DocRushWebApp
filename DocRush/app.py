from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_user():
    return render_template('main_user.html')

@app.route('/admin')
def main_admin():
    return render_template('main_admin.html')
    
@app.route('/my_order_user')
def my_order_user():
    return render_template('my_order_user.html')

@app.route('/order_admin')
def order_admin():
    return render_template('order_admin.html')

@app.route('/order_user')
def order_user():
    return render_template('order_user.html')

@app.route('/payment_admin')
def payment_admin():
    return render_template('payment_admin.html')

@app.route('/payment_user')
def payment_user():
    return render_template('payment_user.html')

