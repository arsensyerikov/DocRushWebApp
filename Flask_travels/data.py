from flask import Flask, request, render_template
import request, make_response

app = Flask(__name__)

@app.route('/')
def index():


    return render_template('index.html',
        departures=data.departures,
        title=data.title,
        subtitle=data.subtitle,
        escription=data.description,
        ours=data.tours)


@app.route('/departures/<departure>')
def departure(departure):
    tours = dict(filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    if tours:
        return render_template('departure.html',departure=departure,
            title=data.title,
            departures=data.departures,
            tours=tours)
        abort(404)


@app.route('/departures/')
def departure_zero():
    return render_template('index.html')


@app.route('/tours/<int:id>/')
def tours(id):
    return render_template('tour.html',
        tour=data.tours[id],
        title=data.title,
        departures=data.departures)

import request, make_response


@app.route("/")
def index():
    return render_template("index.html",
                           departures=data.departures,
                           title=data.title,
                           subtitle=data.subtitle,
                           description=data.description,
                           tours=data.tours,
                           cookie=request.cookies.get('username'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if not request.cookies.get('username') and request.method == "POST":
        res = make_response("Setting a cookie")
        res.set_cookie('username', request.form.get("name"), max_age=60 * 60 * 24 * 365 * 2)
        return  res
    return render_template("login.html")


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('username') or request.cookies.get('username') == "None":
        return redirect(url_for("login"))
    else:
        res = make_response(f"Value of cookie is {request.cookies.get('username')}")
    return res


C