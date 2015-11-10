from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)

app.secret_key = "Thisisthesecretkey"

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

@app.route('/process', methods=['POST'])
def check_password():
	print 'Checking Password'
	print request.form['pswd']
	print request.form['email']
	if len(request.form['pswd']) > 1 and len(request.form['email']) > 1:
		return redirect('/'+ request.form['email'])
	return render_template('/')


@app.route('/registration', methods=['GET'])
def registration():
	print 'Displaying registration page'
	return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def register():
	print 'Check if registration information is valid'
	if len(request.form['pswd']) > 1 and len(request.form['email']) > 1:
		return redirect('/'+ request.form['email'])


app.run(debug=True)	