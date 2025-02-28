from flask import Flask, render_template, request
from data import *
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def index():


    return render_template('index.html',
        departures=data.departures,
        title=data.title,
        subtitle=data.subtitle,
        escription=data.description,
        ours=data.tours)

@app.route('/departures/')
def departures():
    return render_template('departure.html')


@app.route('/tours/')
def list_tours():
    return render_template('tour.html')

@app.route('/agent/')
def agent():
    user_agent = request.headers.get('User-Agent')
    return f'<b>Your browser is {user_agent}</b>'



if __name__ == "__main__":
    app.run(debug=True)
