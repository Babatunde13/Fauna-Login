from flask import Flask, redirect, url_for, render_template, request
from werkzeuug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.objects import Ref
from faunadb.errors import BadRequest, NotFound
from dotenv import load_dotenv
from typing import Dict
import os, secrets

app = Flask()
login_manager = LoginManager(app)

client = FaunaClient(secret=os.getenv('FAUNA_SECRET'))

@login_manager.user_loader
def get_user(_id):
	user = client.query(
		q.get(q.ref(q.collections('users')), _id)
	)
	return {}

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
	if request.method =='POST':
		# get the user details
		email = request.form['email']
		password = request.form['password']
		# verify if the user details exist
		user = {'email': email, 'password': password}		
		login_user(user)
		return redirect(url_for('dashboard'))
	return render_template('signin.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method =='POST':
		name = request.form['name']
		email = request.form['email']
		password = generate_password_hash(request.form['password'])
		user = {'name': name, 'email': email, 'password': password}
		# store user data to db
		login_user(user)
        return redirect(url_for('dashboard', user=user))
    return render_template('signup.html')


@app.route('/dashboard')
@login_required
def dashboard(current_user):
	return render_template('dashboard.html')
