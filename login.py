from flask import Flask, session, render_template, redirect, url_for, request,flash
from flask import Markup
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
message=None
RDB_HOST =  'localhost'
RDB_PORT = 28015
cif = None
app = Flask(__name__)
app.secret_key = 'any random string'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            global message
            message='You need to login first.'
            return redirect(url_for('login'))
    return wrap
@app.route('/', methods=['GET','POST'])
def start():
    return render_template('index.html')
@app.route('/validatesignup',methods=['GET','POST'])
def validatesignup():
    if request.method == 'GET':
        global co
        co=1111
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            return redirect(url_for('credset'))
        else:
            error='invalid OTP'
            return render_template('otp.html', error=error)
def checkdetails(cif,phone,mail):
    checked=False
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    cif_exists=customer.filter({"cif":cif}).distinct().run(connection)
    #cif_exists=cif_result['cif']
    if(cif_exists!=None):
        for each_cus in cif_exists:
            if(each_cus['contact'][0]['mobile']==phone and each_cus['contact'][0]['email']==mail):
                onlineAcc_exists=each_cus['onlineAcc']
                if(onlineAcc_exists==False):
                    checked=True
                else:
                    checked= False
    return checked

def createLogin(uname,password):
    created=False
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    customer.filter(r.row["cif"]==cif).update({'username':uname,'password':password,'onlineAcc':True}).run(connection)
    if(customer.filter({"cif":cif}).pluck('onlineAcc').run(connection)==True):
        created= True
    else:
        created= False
    connection.close()
    return created
    

    
@app.route('/credset',methods=['GET','POST'])
def credset():
    if request.method == 'GET':
        return render_template('setpass.html')
    else:
        user = request.form['username']
        password = request.form['pass']
        conf_pass=request.form['conf_pass']
        error1 = None
        error2 = None
        error3 = None
        error4 = None
        if len(user) == 0:
            error1 = "Username cannot be empty"
        if len(password) == 0:
            error2 = "Pass cannot be empty"
        if len(conf_pass) == 0:
            error3 = "Confirm password cant be empty"
        if (password!=conf_pass):
            error4="Passwords dont match"
        if error1 or error2 or error3 or error4:
            if str(error1) != 'None':
                flash(error1)
            if str(error2) != 'None':
                flash(error2)
            if str(error3) != 'None':
                flash(error3)
            if str(error4) !='None':
                flash(error4)
            return render_template('setpass.html')
        else:
            if(createLogin(user,password) is True):
                flash("Account has been created. You can now login")
                return redirect(url_for('login'))
            else:
                error='Mismatch of Details or Account already exists. Please check Your Details'
                return render_template('setpass.html',error=error)



            

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if 'username' in session:
        username=session['username']
        return render_template('dashboard.html',username=username)
    global message
    message='You need to login first2.'
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    error = None
    if request.method == 'POST':
        un=request.form['username']
        passw=request.form['pass']
        flash(error)
        try:
            user=customer.filter({"username":un}).run(connection)
            for each in user: 
                if(each['username']!=None):
                    pword=each['password']
                    if pword == passw:
                        session['logged_in'] = True
                        global USER
                        USER = un
                        session['username'] = un
                        return redirect(url_for('index'))
                    else:
                        error='Invalid Credentials1. Please try again'
                        flash(error)
                        return render_template('login.html', error=error)
                else:
                    error = 'Invalid Credentials2. Please try again.'
                    flash(error)
                    return render_template('login.html', error=error)
        except Exception as e:
            print (str(e))
            error = 'Invalid Credentials3. Please try again.'
            flash(error)
            return render_template('login.html', error=error)
    #if message:
    #    flash(message)
    else:
        return render_template('login.html', error=error)
@app.route('/logout')
@login_required
def logout():
    global message
    message=None
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        global cif
        cif = request.form['cif']
        phone = request.form['mobile']
        mail=request.form['email']
        error1 = None
        error2 = None
        error3 = None
        if len(cif) == 0:
            error1 = "CIF cannot be empty"
        if len(phone) == 0:
            error2 = "Phone cannot be empty"
        if len(mail) == 0:
            error3 = "Email cant be empty"
        if error1 or error2 or error3:
            if str(error1) != 'None':
                flash(error1)
            if str(error2) != 'None':
                flash(error2)
            if str(error3) != 'None':
                flash(error3)
            return render_template('signup.html')
        else:
            if(checkdetails(cif,phone,mail) is True):
                flash("Please enter the OTP sent to "+phone[0:2]+"XXXXXX"+phone[8:10])
                return redirect(url_for('validatesignup'))
            else:
                error='Mismatch of Details or Account already exists. Please check Your Details'
                return render_template('signup.html',error=error)



if __name__ == '__main__':
    app.debug = True
    app.run()
