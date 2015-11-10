from flask import Flask, render_template, redirect, session, request
from mysqlconnection import MySQLConnector

import bcrypt
import re

app = Flask(__name__)

app.secret_key = "Thisisthesecretkey"

mysql = MySQLConnector('loginandreg')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# MODEL FUNCTIONS

def show(param):
    print "Show individual"
    print param
    query = "SELECT * FROM users where email = '{}'".format(param)
    print query
    user = mysql.fetch(query)
    print user
    return user

def create(param):
    # the param is the entire request object
    #password_hash = bcrypt.hashpw(str(param['password']),bcrypt.gensalt());
    password_hash = 'temp'
    
    print 'Creating the user'
    query = "INSERT into users (first_name, last_name, email, password) VALUES ('{}', '{}', '{}', '{}')".format(param['first_name'], param['last_name'], param['email'], password_hash)
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
	except:
		session['loginid'] = ''
	print session['loginid']
	return render_template('login.html')

@app.route('/<email>', methods=['GET'])
def logged(email):
	print 'Logged in'
	print email
	print session['loginid']
	session['loginid'] = email
	print session['loginid']	
	return redirect('/')

@app.route('/registration', methods=['GET'])
def registration():
	print 'Displaying registration page'
	return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def register():
	print 'Check if registration information is valid'
	print request.form
	create(request.form)
	return redirect('/'+ request.form['email'])


app.run(debug=True)	