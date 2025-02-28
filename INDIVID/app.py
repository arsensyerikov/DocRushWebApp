from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def name1():
    return render_template('index.html')

@app.route('/buy')
def name2():
    return render_template('example.html')

@app.route('/sell')
def name3():
    return render_template('sell.html')

@app.route('/balance')
def name4():
    return render_template('balance.html')

@app.route('/chart')
def name5():
    return render_template('chart.html')

@app.route('/trades')
def name6():
    return render_template('trades.html')

if __name__ == '__main__':
    app.run(debug=True)