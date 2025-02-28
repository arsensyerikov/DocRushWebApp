import flask
import flask_wtf
import wtforms

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Add a secret key for CSRF protection

class SubscriptionForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Імя')
    pasword = wtforms.PasswordField('Пароль')
    submit = wtforms.SubmitField('Відправити')

@app.route('/ent/', methods=['GET', 'POST'])
def subscribe():
    form = SubscriptionForm()
    if flask.request.method == "POST" and form.validate_on_submit():
        return "Form submitted successfully"
    return flask.render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change port to 5001
