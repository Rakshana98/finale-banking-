from flask import Flask, session, render_template, redirect, url_for, request,flash
import sqlite3
import random
import os
import subprocess
from functools import wraps
import rethinkdb as r
import json
connection=r.connect( "localhost", 28015).repl()
# Route for handling the login page logic
#TODO
#login
#signup->Check CIF check mobile
#otp
#forgot Password
#forgot ID
#logout
#profile
#Accounts
#dashboard
USER = None
USERID = None

app = Flask(__name__)
app.secret_key = 'any random string'

def login_required(f):
    @wraps(f)

    def wrap(*args, **kwargs):
        if 'logged_in' in session:

            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if 'username' in session:
        username=session['username']
        return render_template('dashboard.html',username=username)
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection=r.connect( "localhost", 28015).repl()
    error = None
    if request.method == 'POST':
        un=request.form['username']
        passw=request.form['pass']
        flash(un)
        try:
            pword=r.db('test').table('login').get(1)['details']['password'].run()
            if pword == passw:
                session['logged_in'] = True
                global USER
                USER = un
                session['username'] = un
                return redirect(url_for('index'))
            else:
                error = 'Invalid Credentials. Please try again.'
        except Exception as e:
            print (str(e))
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET' or request.method == 'POST':
        flash("heyeyey")
        return render_template('signup.html')
    else:
        email = request.form['email']
        username = request.form['usename']
        name=request.form['name']
        pword = request.form['password']
        accno=request.form['accno']
        phno=request.form['phno']
        error1 = None
        error2 = None
        error3 = None
        error4 = None
        error5 = None
        if len(username) == 0:
            error2 = "UserName cannot be empty"
        if len(name) == 0:
            error3 = "Name cannot be empty"
        if len(pword) <= 5:
            error4 = "Password must be more than 5 characters long"
        if len(phno) != 0:
            error5="phone number invalid"
        if error1 or error2 or error3 or error4 or error5:
            if str(error1) != 'None':
                flash(error1)
            if str(error2) != 'None':
                flash(error2)
            if str(error3) != 'None':
                flash(error3)
            if str(error4) != 'None':
                flash(error4)
            if str(error5) !='None':
                flash(error5)
            return render_template('signup.html')
        else:
            newCustomer(email, username, name, pword,accno,phno)
            flash("Account created! You can now login with your new credentials.")
            return redirect(url_for('login'))
def newCustomer(email, username, name, pword,accno,phno):
    c.execute("insert into login(uid,password) values(?,?)",
              (phno,pword))
    c.execute("insert into userlogin values(?,?,?)", (email, pword, custid))
    conn.commit()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
