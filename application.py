import sqlite3 as sql
import os, math
from flask import Flask, render_template,request,session,redirect, url_for, flash
# from flask.ext.session import Session
from flask import url_for
from datetime import datetime,date,timedelta
from werkzeug.utils import secure_filename
import random,uuid

app = Flask(__name__)
app.secret_key = '%jsdj!@'
UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
admin = "vikash"
passWord = "vikash1234"

def uniqueid():
    seed = random.randint(1,100000)
    while True:
        yield seed
        seed += 1
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def main():
    return render_template('index.html')

    # return redirect(url_for('login'))

def validate_user(username,flag):
    con = sql.connect('database.db')
    validate = False
    
    if(flag==1):
        with con:
            cur = con.cursor()
            cur.execute('select w_id from employee')
            rows = cur.fetchall()
            for row in rows:
                dUser = row[0]
                if(dUser == username):
                    validate = True
        return validate

    if(flag==2):
        with con:
            cur = con.cursor()
            cur.execute('select hr_id from employee')
            rows = cur.fetchall()
            for row in rows:
                dUser = row[0]
                if(dUser == username):
                    validate = True
        return validate
@app.route('/userlogin', methods =['GET','POST'])
def userlogin():
    error = None
    
    if request.method == 'POST':
        w_id = request.form['w_id']
        # password = request.form['password']
        validate = validate_user(w_id,1)
        if validate == False:
            error = 'Invalid credentials. Please try again'
        else:
            session['username'] = w_id
            return redirect('/viewleave')
    if 'username' in session:
        return redirect('/viewleave')
    return render_template('userlogin.html',error=error)




@app.route('/usersignup',methods=['GET','POST'])
def usersignup():
    con = sql.connect('database.db')
    cur = con.cursor()
    error = None
    if request.method == 'POST':
        # username = request.form['username']
        #add all form data
        name = request.form['name']
        w_id = request.form['w_id']
        hr_id = request.form['hr_id']
        age = request.form['age']
        gender = request.form['gender']
        family_history = request.form['family_history']
        

        cur.execute('select w_id from employee')
        rows = cur.fetchall()
        for row in rows:
            if(row[0] == w_id):
                error = 'Username already exist! Try other username'
                return render_template('usersignup.html',error=error)
        session['username'] = w_id
        ##edit here
        #
        #
        #       
        cur.execute("insert into employee values(?,?,?,?,?,?)",(w_id,hr_id,name,age,gender,family_history))
        con.commit()
        return redirect('/viewleave')
    if 'username' in session:
        return redirect('/viewleave')
    return render_template('usersignup.html',error=error)


@app.route('/viewleave', methods=['GET','POST'])
def viewleave():
    if 'username' in session:
        con = sql.connect('database.db')
        cur = con.cursor()
        w_id = session['username']

        cur.execute("select e.*,f.* from employee e, fe_em fe, features f where e.w_id = fe.w_id and f.field_id = fe.field_id and e.w_id = (?)",(w_id,))
        rows = cur.fetchall()
        return render_template('viewleave.html',rows = rows)
    return redirect('/userlogin')

@app.route('/requestleave',methods=['GET','POST'])
def requestleave():
    con = sql.connect('database.db')

    if request.method == 'POST':
        #All the features to be added here like this:
        #family_history = request.form
        cur = con.cursor()
        #insert into table
        field_id = uniqueid()
        w_id = session['username']
        work_interface = request.form['work_interface']
        remote_work = request.form['remote_work']
        care_options = request.form['care_options']
        wellness = request.form['wellness']
        anonimity = request.form['anonimity']
        leave = request.form['leave']
        mental_health = request.form['mental_health']
        phy_health = request.form['phy_health']
        supervisor = request.form['supervisor']
        ment_vs_phy = request.form['ment_vs_phy']
        obs = request.form['obs']

        cur.execute("insert into features(field_id,work_interface,remote_work,care_options,wellness,anonimity,leave,mental_health,phy_health,supervisor,ment_vs_phy,obs) values(?,?,?,?,?,?,?,?,?,?,?,?)",(field_id,work_interface,remote_work,care_options,wellness,anonimity,leave,mental_health,phy_health,supervisor,ment_vs_phy,obs))
        con.commit()
        
        hr_id = cur.execute("select hr_id from employee e where e.w_id = (?)",(w_id,))
        cur.execute("insert into fe_em values(?,?,?)",(field_id,w_id,hr_id,))
        con.commit()



        return redirect('/viewleave')
    if 'username' in session:
        return render_template('requestleave.html')
    return redirect('/userlogin')






## HR_FORM

@app.route('/hrlogin', methods =['GET','POST'])
def hrlogin():
    error = None
    
    if request.method == 'POST':
        hr_id = request.form['hr_id']
        # password = request.form['password']
        validate = validate_user(hr_id,2)
        if validate == False:
            error = 'Invalid credentials. Please try again'
        else:
            session['username'] = hr_id
            return redirect('/hrviewform')
    if 'username' in session:
        return redirect('/hrviewform')
    return render_template('hrlogin.html',error=error)




@app.route('/hrsignup',methods=['GET','POST'])
def hrsignup():
    con = sql.connect('database.db')
    cur = con.cursor()
    error = None
    if request.method == 'POST':
        name = request.form['name']
        hr_id = request.form['hr_id']
        emp_num = request.form['empnum']
        tech_comp = request.form['tech']
        benefits = request.form['benefits']
        seek_help = request.form['seek_help']

        #add all form data
        ##form data
        # name = request.form['name']
        # age = request.form['ph_no']
        cur.execute('select hr_id from employer')
        rows = cur.fetchall()
        for row in rows:
            if(row[0] == hr_id):
                error = 'Username already exist! Try other username'
                return render_template('hrsignup.html',error=error)
        session['username'] = hr_id
        ##edit here
        #
        #
        #       
        cur.execute("insert into employer values(?,?,?,?,?,?)",(name,hr_id,emp_num,tech_comp,benefits,seek_help))
        con.commit()
        #edit till here
        
        return redirect('/hrviewform')
        
    if 'username' in session:
        return redirect('/hrviewform')
    return render_template('hrsignup.html',error=error)


@app.route('/hrviewform', methods=['GET','POST'])
def hrviewform():
    con = sql.connect('database.db')
    cur = con.cursor()
    if 'username' in session:
        hr_id = session['username']
        #query to view name of employer and the details with prediction 
        cur.execute("select hr.name,e.name,e.w_id,f.* from employee e, fe_em fe, features f, employer hr where e.w_id = fe.w_id and f.field_id = fe.field_id and e.hr_id = hr.hr_id and hr.hr_id = (?)",(hr_id,))
        rows = cur.fetchall()
        return render_template('hrviewform.html',rows= rows)

    return redirect('/hrlogin')

@app.route('/predict', methods= ['GET','POST'])
def predict():
    if 'username' in session:
        field_id = request.args.get('field_id')
        hr_id = session['username']
        w_id = request.args.get('w_id')

        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("select f.*,e.age,e.gender,e.family_history,hr.tech_company,hr.benefits,hr.no_employees,hr.seek_help from employee e, fe_em fe, features f, employer hr where e.w_id = fe.w_id and f.field_id = fe.field_id and e.hr_id = hr.hr_id and fe.field_id = (?)",(field_id,))
        rows = cur.fetchall()
        rows.pop(0)
        rows.pop(11)

        model = pickle.load(open('decision.pkl','rb'))

        scaler = pickel.load(open('scaler.sav','rb'))
        x = scaler.transform(rows)
        result = model.predict(x)

        cur.execute("update features set treatment =(?) where field_id =(?)",(result,field_id))
        con.commit()
        return redirect('/hrviewform')


        #write a query to get all the data

        #make prediction using ML model

        #set the value and return the /hrviewform
    return redirect('/hrlogin')







## create usersignup
#
#
#
#
#




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(('/'))


if __name__ == "__main__":
    app.run()