from flask import Flask, render_template, redirect, session, request
from mysqlconnection import MySQLConnector

import bcrypt
import re

app = Flask(__name__)

app.secret_key = "Thisisthesecretkey"

mysql = MySQLConnector('loginandreg')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


def show(param):
    print "Show individual"
    print param
    if EMAIL_REGEX.match(param):
    	query = "SELECT * FROM users where email = '{}'".format(param)
    	print query
    	user = mysql.fetch(query)
    	print user
    return user

def create(param):
    # the param is the entire request object
    password_hash = bcrypt.hashpw(str(param['password']),bcrypt.gensalt());
   
    print 'Creating the user'
    query = "INSERT into users (first_name, last_name, email, password_hash) VALUES ('{}', '{}', '{}', '{}')".format(param['first_name'], param['last_name'], param['email'], password_hash)
    print "Query string"
    print query
    mysql.run_mysql_query(query) #runs
    query_result = show(param['email']) #run
    if len(query_result) == 1:
        return query_result
    return []

@app.route('/', methods=['GET'])
def index():
	print 'Default Screen'
	try:
		session['loginid']
		session['user']
	except:
		session['loginid'] = ''
		session['user'] = []
	print session['loginid']
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	current_user = show(request.form['email'])
	if len(current_user) == 1 and bcrypt.hashpw(str(request.form['password']),current_user[0]['password_hash']) == current_user[0]['password_hash']:
		session['user'] = current_user[0]
		return render_template('/success.html')
	return redirect('/')


@app.route('/registration', methods=['GET'])
def registration():
	print 'Displaying registration page'
	return render_template('registration.html')


@app.route('/regt', methods=['POST'])
def register():
	print 'registration ......'
	print 'Check if registration information is valid'
	print request.form
	user = create(request.form)
	if len(user) == 1:
		session['user']
		return render_template('/success.html')
	
	return redirect('/')


app.run(debug=True)	