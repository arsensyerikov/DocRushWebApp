from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next')
def index1():
    return render_template('index1.html')

@app.route('/next1')
def index2():
    return render_template('index2.html')

@app.route('/next2')
def index3():
    return render_template('index3.html')




if __name__ == '__main__':
    app.run(debug=True)