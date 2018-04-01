from flask import Flask, session, render_template, redirect, url_for, request,flash,abort
from flask import Markup
from rethinkdb.errors import RqlRuntimeError,RqlDriverError
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
#login#
#signup#
#otp#
#forgot Password#
#forgot ID#
#logout#
#profile
#Accounts
#dashboard
USER = None
#USERID = None
RDB_HOST =  'localhost'
RDB_PORT = 28015
cif = None
app = Flask(__name__)
app.secret_key = 'banking daww'
connection=None
# open connection before each request
@app.before_request
def before_request():
    try:
        global connection
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)

    except RqlDriverError:
        abort(503, "Database connection could be established.")

# close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        connection.close()
    except AttributeError:
        pass

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
        mail=request.args.get('mail')
        phone=request.args.get('phone')
        #add otp sending to phone code
        server.sendmail("codewars2k18@gmail.com", mail, msg)
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
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
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
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    #digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    bank=r.db('bank')
    customer=bank.table('customer')
    #b=password.encode('utf-8')
    #digest.update(b)
    #hashedpw=digest.finalize()
    #print(str(hashedpw))
    customer.filter(r.row["cif"]==cif).update({'username':uname,'password':password,'onlineAcc':True}).run(connection)
    customer.sync().run(connection)
    check=customer.filter({"cif":cif}).pluck('onlineAcc').run(connection)
    for each in check:
        if(each['onlineAcc']==True):
            created= True
        else:
            created= False
    print(created)
    #connection.close()
    return created
def foruid(cif,phone,mail):
    checked=False
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
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

def getUnameByCif(cif):
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    uname=customer.filter({'cif':cif}).pluck('username').run(connection)
    for each in uname:
        username=each['username']
    return username


@app.route('/otpuid',methods=['GET','POST'])
def otpuid():
    if request.method == 'GET':
        global co
        co=71234
        msg="Your OTP for The Bank is "+str(co)
        mail=request.args.get('mail')
        phone=request.args.get('phone')
        #add mobile too
        server.sendmail("codewars2k18@gmail.com", mail, msg)
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            cif=request.args.get('cif')
            mail=request.args.get('mail')
            phone=request.args.get('phone')
            username=getUnameByCif(cif)
            msg="Your User ID is "+username
            flash(msg)                          #remove flash
            server.sendmail("codewars2k18@gmail.com", mail, msg)
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
        phone=request.form['mobile']
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
            return render_template('forgotuid.html')
        else:
            if(foruid(cif,phone,mail) is True ):#include new function to check
                flash("Please enter the OTP sent to "+phone[0:2]+"XXXXXX"+phone[8:10]+"and to your Registered Mail ID")
                return redirect(url_for('otpuid',mail=mail,phone=phone,cif=cif))
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
        phone=request.form['mobile']
        mail=request.form['email']
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
                return redirect(url_for('otppass',userid=userid,mail=mail,phone=phone))
            else:
                error='Mismatch of Details. Please check Your Details'
                return render_template('forgotpass.html',error=error)
def forpass(userid,cif,phone,mail):
    checked=False
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    cif_exists=customer.filter({"cif":cif}).distinct().run(connection)
    #cif_exists=cif_result['cif']
    if(cif_exists!=None):
        for each_cus in cif_exists:
            if(each_cus['contact'][0]['mobile']==phone and each_cus['contact'][0]['email']==mail and each_cus['username']==userid):
                onlineAcc_exists=each_cus['onlineAcc']
                if(onlineAcc_exists==True):
                    checked=True
                else:
                    checked= False
    return checked
    #check db work return true or false
@app.route('/otppass',methods=['POST','GET'])
def otppass():
    if request.method=='GET':
        global co
        co=71234
        msg="Your OTP for The Bank is "+str(co)
        mail=request.args.get('mail')
        phone=request.args.get('phone')
        #add mobile too
        server.sendmail("codewars2k18@gmail.com", mail, msg)
        return render_template('otp.html')
    else:
        otp=request.form['otp']
        otp=int(otp)
        error=None
        if(otp-co==0):
            userid=request.args.get('userid')
            msg="ALERT! Your account password is being changed."
            mail=request.args.get('mail')
            server.sendmail("codewars2k18@gmail.com", mail, msg)
            return redirect(url_for('changepass',userid=userid))
        else:
            error='invalid OTP'
            return render_template('otp.html', error=error)
def changepword(uname,pword):
    changed=False
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    #digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    bank=r.db('bank')
    customer=bank.table('customer')
    #ins_pw=pword
    #b=ins_pw.encode('utf-8')
    #digest.update(b)
    #hashedpw=digest.finalize()
    check_ins=customer.filter(r.row["username"]==uname).update({'password':pword}).run(connection)
    check_pw=customer.filter({"username":uname}).pluck('password').run(connection)
    #print(check_pw)
    for each in check_pw:
        print(each)
        print(each['password'],check_ins['replaced'])
        if(each['password']==pword and check_ins['replaced']==1 ):
            changed=True
        else:
            changed=False
    customer.sync().run(connection)
    #connection.close()
    #print(changed)
    return changed

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
            uname=request.args.get('userid')
            if(changepword(uname,password) is True):
                flash('Password successfully resetted. Your can login Now')
                return redirect(url_for('login'))
            else:
                error='Mismatch of Details or Account already exists. Please check Your Details'
                return render_template('changepass.html',error=error)


@app.route('/editprof', methods=['GET', 'POST'])
@login_required
def editprof():
    if request.method=='POST':
        #update Database
        return redirect(url_for('profile'))
    else:
        return render_template('editprof.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method=='GET':
        #db get data
        return render_template('profile.html')
    else:
        return redirect(url_for('editprof'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if 'username' in session:
        username=session['username']
        return render_template('dash2.html',username=username)
    global message
    message='You need to login first.'
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    #connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    bank=r.db('bank')
    customer=bank.table('customer')
    error = None
    if request.method == 'POST':
        #digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        un=request.form['username']
        passw=request.form['pass']
        i=0
        #flash(error)
        try:
            user=customer.filter({"username":un}).run(connection)
            for each in user:
                if(each['username']!=None):
                    i=1
                    #b=passw.encode('utf-8')
                    #digest.update(b)
                    #hashedpw=digest.finalize()
                    pword=each['password']
                    if pword == passw:
                        session['logged_in'] = True
                        global USER
                        USER = un
                        session['username'] = un
                        return redirect(url_for('index'))
                    else:
                        error='Invalid Password. Please try again'
                        flash(error)
                        return render_template('login.html', error=error)
                else:
                    error = 'Invalid Credentials2. Please try again.'
                    flash(error)
                    return render_template('login.html', error=error)
            if(i==0):
                error="Invalid User ID"
                flash(error)
                return render_template('login.html',error=error)
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
                return redirect(url_for('validatesignup',mail=mail,phone=phone))
            else:
                error='Mismatch of Details or Account already exists. Please check Your Details'
                return render_template('signup.html',error=error)

@app.route('/accountdash', methods=['POST', 'GET'])
@login_required
def accountdash():
    if request.method=='GET':
        bank=r.db('bank')
        customer=bank.table('customer')
        #uname=customer.filter({'username':session['username']}).pluck('username').run(connection)
        #acc=customer.filter({'username':session['username']}).pluck({'account':[{'number','balance'}]}).run(connection)
        cust_list=customer.filter({'username':session['username']}).distinct().run(connection)
        uname=cust_list[0]['username']
        num=[]
        bal=[]
        for each in cust_list:
            e=[]
            x=len(each['account'])
            for i in range(0,x):
                e.append(i)
                print(e)
            print(e)
            for i in e:
                q=each['account'][i]['balance']
                w=each['account'][i]['number']
                print(w)
                print(q)
                bal.append(q)
                num.append(w)


        print(uname)
        # print(acc)
        return render_template('accountdash.html',username=uname,bal=bal,num=num)
    else:
	    return render_template('accountdash.html')


@app.route('/messages', methods=['POST', 'GET'])
@login_required
def messagedash():
    if request.method=='GET':
        bank=r.db('bank')
        customer=bank.table('customer')
        cust_list=customer.filter({'username':session['username']}).distinct().run(connection)
        uname=cust_list[0]['username']
        return render_template('complaint.html')
    else:
        return render_template('complaint.html')



@app.route('/trans_list/<int:accno>', methods=['POST', 'GET'])
@login_required
def trans_list(accno):
    if request.method=='GET':
        bank=r.db('bank')
        customer=bank.table('customer')
        cust_list=customer.filter({'username':session['username']}).distinct().run(connection)
        uname=cust_list[0]['username']
        tran=[]
        q=[]
        e=[]
        f=[]
        dat=[]
        toacc=[]
        fromacc=[]
        amt=[]

        for each in cust_list:
            x=len(each['account'])
            y=0
            for i in range(0,x):
                    e.append(i)
            for i in e:
                if each['account'][i]['number']==str(accno):
                    q=each['account'][i]['transaction']
                    y=len(q)
                    for i in range(0,y):
                        f.append(i)
                    for i in f:
                        dat.append(q[i]['date'])
                        toacc.append(q[i]['toacc'])
                        fromacc.append(q[i]['fromacc'])
                        amt.append(q[i]['amt'])



        sz=len(dat)
        print(q)
        print(amt)
        print(dat)









        return render_template('transaction_page.html',uname=uname,dat=dat,toacc=toacc,fromacc=fromacc,amt=amt,sz=sz)
    else:
        return render_template('transaction_page.html')







if __name__ == '__main__':
    app.debug = True
    app.run()
