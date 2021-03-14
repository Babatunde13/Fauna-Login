import re
from flask import Flask, flash, redirect, url_for, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.objects import Ref
from faunadb.errors import BadRequest, NotFound
from dotenv import load_dotenv
import os, secrets

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

client = FaunaClient(secret=os.getenv('FAUNA_SECRET'))

@app.route('/')
def home():
	if session.get('user_id'):
			flash('You are logged in!', 'warning')
			return redirect(url_for('dashboard'))
	return render_template('home.html')


@app.route('/signin/', methods=['POST', 'GET'])
def signin():
	if session.get('user_id'):
			flash('You are logged in!', 'warning')
			return redirect(url_for('dashboard'))
	if request.method =='POST':
		# get the user details
		email = request.form['email']
		password = request.form['password']
		# verify if the user details exist
		try:
			user = client.query(
					q.get(q.match(q.index('user_by_email'), email))
			)
		except NotFound:
			flash('Invalid email or password', category='warning')
		else:
			if check_password_hash(user['data']['password'], password):
				session['user_id'] = user['ref'].id()
				flash('Signed in successfully', 'success')
				return redirect(url_for('dashboard'))
			else:
				flash('Invalid email or password', 'warning')
	return render_template('signin.html')

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if session.get('user_id'):
			flash('You are logged in!', 'warning')
			return redirect(url_for('dashboard'))
	if request.method =='POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if not re.search(email_regex, email) or not 6 < len(password) < 20:
			flash('Invalid email or password!, password needs to be between 6 and 20 characters', 'warning')
			return render_template('signup.html')
		if password != request.form['confirm_password']:
			flash('password fields not equal', 'warning')
			return render_template('signup.html')
		password = generate_password_hash(password)
		user = {'name': name, 'email': email, 'password': password}
		try:
			# store user data to db
			new_user = client.query(q.create(
				q.collection('user'),
				{'data': user}
			))
		except BadRequest:
			flash('Email already exists')
		else:
			session['user_id'] = new_user['ref'].id()
			flash('Account created successfully', 'success')
			return redirect(url_for('dashboard'))
	return render_template('signup.html')


@app.route('/dashboard/')
def dashboard():
	if not session.get('user_id'):
			flash('You need to be logged in to view this page!', 'warning')
			return redirect(url_for('signin'))
	user = client.query(
		q.get(q.ref(q.collection("user"), session['user_id']))
	)['data']
	return render_template('dashboard.html', current_user=user)

@app.route("/signout/")
def signout():
	if not session.get('user_id'):
		flash('You need to be logged in to do this!', 'warning')
	else:
		session.pop('user_id', None)
		flash('Signed out successfully', 'success')
	return redirect(url_for('home'))
	

if __name__ == '__main__':
	app.run(debug=True)