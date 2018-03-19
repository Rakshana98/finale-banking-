from flask import Flask, session, render_template, redirect, url_for, request,flash
from flask import Markup
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import sqlite3
import random
import os
import subprocess
from functools import wraps
import rethinkdb as r
import json
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login("codewars2k18@gmail.com", "ullepodude")
#connection=r.connect( "localhost", 28015).repl()
# Route for handling the login page logic
#TODO
#check mail ids
#add sms
#format it
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
#USERID = None
mail=None
phone=None
message=None
RDB_HOST =  'localhost'
RDB_PORT = 28015
cif = None
app = Flask(__name__)
app.secret_key = 'any random string'

def getmail():
    #function to set global variable mail from db
    global mail
    mail=None
def getphone():
    #function to set global variable phone from db
    global phone
    phone=None
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
        co=71234
        msg="Your OTP for The Bank is "+str(co)
        server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            #msg="Your User ID for The Bank is "+str()#add the user ID here from DB
            #server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
            #flash("User ID has been sent to Your Registered Mail ID")
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
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    bank=r.db('bank')
    customer=bank.table('customer')
    b=password.encode('utf-8')
    digest.update(b)
    hashedpw=digest.finalize()
    #print(str(hashedpw))
    customer.filter(r.row["cif"]==cif).update({'username':uname,'password':r.binary(hashedpw),'onlineAcc':True}).run(connection)
    customer.sync().run(connection)
    check=customer.filter({"cif":cif}).pluck('onlineAcc').run(connection)
    for each in check:
        if(each['onlineAcc']==True):
            created= True
        else:
            created= False
    print(created)
    connection.close()
    return created
def foruid(cif,phone,mail):
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
                if(onlineAcc_exists==True):
                    session['mailid']=mail
                    checked=True
                else:
                    checked= False
    return checked

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



@app.route('/otpuid',methods=['GET','POST'])
def otpuid():
    if request.method == 'GET':
        global co
        co=71234
        msg="Your OTP for The Bank is "+str(co)
        #add mobile too
        server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            #send your userid from DB
            server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
            return redirect(url_for('login'))
        else:
            error='invalid OTP'
            return render_template('otp.html', error=error)

@app.route('/forgotuid',methods=['GET','POST'])
def forgotuid():
    if(request.method=='GET'):
        return render_template('forgotuid.html')
    else:
        cif=request.form['cif']
        mobile=request.form['mobile']
        email=request.form['email']
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
            return render_template('forgotuid.html')
        else:
            if(foruid(cif,phone,mail) is True ):#include new function to check
                flash("Please enter the OTP sent to "+phone[0:2]+"XXXXXX"+phone[8:10]+"and to your Registered Mail ID")
                return redirect(url_for('otpuid'))
            else:
                error='Mismatch of Details. Please check Your Details'
                return render_template('forgotuid.html',error=error)

            #include new function for otp old one is not generic

@app.route('/forgotpass',methods=['GET','POST'])
def forgotpass():
    if request.method=='GET':
        return render_template('forgotpass.html')
    else:
        userid=request.form['userid']
        cif=request.form['cif']
        mobile=request.form['mobile']
        email=request.form['email']
        error1 = None
        error2 = None
        error3 = None
        error4 = None
        if len(userid) == 0:
            error1 ="User ID cannot be empty"
        if len(cif) != 10:
            error2 = "Invalid CIF"
        if len(phone) != 10:
            error3 = "Invalid Phone Number"
        if len(mail) == 0:
            error4 = "Email cant be empty"
        if error1 or error2 or error3 or error4:
            if str(error1) != 'None':
                flash(error1)
            if str(error2) != 'None':
                flash(error2)
            if str(error3) != 'None':
                flash(error3)
            if str(error4) != 'None':
                flash(error4)
            return render_template('forgotpass.html')
        else:
            if(forpass(userid,cif,phone,mail) is True ):#include new function to check
                flash("Please enter the OTP sent to "+phone[0:2]+"XXXXXX"+phone[8:10]+"and to your Registered Mail ID")
                return redirect(url_for('otppass'))
            else:
                error='Mismatch of Details. Please check Your Details'
                return render_template('forgotpass.html',error=error)
def forpass(userid,cif,phone,mail):
    return True
    #check db work return true or false
@app.route('/otppass',methods=['POST','GET'])
def otppass():
    if request.method=='GET':
        global co
        co=71234
        msg="Your OTP for The Bank is "+str(co)
        #add mobile too
        server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            #server.sendmail("codewars2k18@gmail.com", "eshwar.muthusamy7@gmail.com", msg)
            return redirect(url_for('changepass'))
        else:
            error='invalid OTP'
            return render_template('otp.html', error=error)
@app.route('/changepass',methods=['POST','GET'])
def changepass():
    if request.method=='GET':
        return render_template('changepass.html')
    else:
        password = request.form['pass']
        conf_pass=request.form['conf_pass']
        error1 = None
        error2 = None
        error3 = None
        if len(password) == 0:
            error1 = "Password cannot be empty"
        if len(conf_pass) == 0:
            error2 = "Confirm password cant be empty"
        if (password!=conf_pass):
            error3="Passwords dont match"
        if error1 or error2 or error3:
            if str(error1) != 'None':
                flash(error1)
            if str(error2) != 'None':
                flash(error2)
            if str(error3) != 'None':
                flash(error3)
            return render_template('changepass.html')
        else:#remove this
            if(True):
                flash('Password successfully resetted. Your can login Now')
                return redirect(url_for('login'))
            else:
                error='Mismatch of Details or Account already exists. Please check Your Details'
                return render_template('changepass.html',error=error)



@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if 'username' in session:
        username=session['username']
        return render_template('dashboard.html',username=username)
    global message
    message='You need to login first.'
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    error = None
    if request.method == 'POST':
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        un=request.form['username']
        passw=request.form['pass']
        #flash(error)
        try:
            user=customer.filter({"username":un}).run(connection)
            for each in user:
                if 'username' not in each:
                    error='Invalid User name!'
                    flash(error)
                    return render_template('login.html', error=error)
                if(each['username']!=None):
                    print(each['username'])
                    b=passw.encode('utf-8')
                    digest.update(b)
                    hashedpw=digest.finalize()
                    pword=each['password']
                    if pword == hashedpw:
                        session['logged_in'] = True
                        global USER
                        USER = un
                        session['username'] = un
                        return redirect(url_for('index'))
                    else:
                        error='Invalid Credentials. Please try again'
                        flash(error)
                        return render_template('login.html', error=error)
                else:
                    error = 'Invalid Credentials. Please try again.'
                    flash(error)
                    return render_template('login.html', error=error)
        except Exception as e:
            #print (str(e))
            error = 'Invalid Credentials. Please try again.'
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
