from flask import Flask, render_template, redirect, url_for, flash
import flask_wtf
import wtforms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Define the form
class SubscriptionForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Ваше ім\'я', validators=[wtforms.validators.DataRequired()])
    surname = wtforms.StringField('Ваше прізвище', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Продовжити')

# Home page route
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template("welcome_page.html")

# Route for handling form submission (linked to swim.html)
@app.route('/web', methods=['GET', 'POST'])
def web():
    form = SubscriptionForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        # Process the form data (e.g., save to database)
        flash('Операція пройшла успішно!', 'success')
        return redirect(url_for('web'))  # Redirect to avoid form resubmission
    return render_template("swim.html", form=form)

# Additional routes for other pages
@app.route('/web1')
def web1():
    return render_template("web1.html")

@app.route('/swim')
def swim():
    return render_template("swim.html")

@app.route('/swim1')
def swim1():
    return render_template("swim1.html")

# More routes can be added here as needed
# For example:
@app.route('/main_page')
def main_page():
    return render_template("main_page.html")

@app.route('/my_py_project')
def my_py_project():
    return render_template("my_py_project.html")

@app.route('/information')
def information():
    return render_template("information_page.html")

@app.route('/github')
def github():
    return render_template("github.html")

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
