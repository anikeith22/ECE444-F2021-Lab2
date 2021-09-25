from flask import Flask, render_template, session, redirect, url_for, flash
from flask.signals import message_flashed
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'donut22'
moment = Moment(app)


class NameForm(Form):
	name = StringField('What is your name?', validators=[DataRequired()]) 
	email = StringField('What is your UofT Email address?', validators=[DataRequired(),Email()]) 
	submit = SubmitField('Submit')

	
@app.route('/', methods=['GET', 'POST']) 
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		old_email = session.get('email')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		if old_email is not None and old_email != form.email.data:
			flash('Looks like you have changed your email!')
		session['name'] = form.name.data
		if (not ("utoronto" in form.email.data)):
			session['email'] = None
		else:
			session['email'] = form.email.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
	app.run(debug=True)
