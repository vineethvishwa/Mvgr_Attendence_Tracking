import os
import requests
import xlrd,datetime
from flask import Flask, session,render_template,request,redirect,url_for,abort,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xjvdssytgwcteq:bc260046057550ec187f97fa96658b388508032d1092db9d367b6c955dec636b@ec2-54-221-198-156.compute-1.amazonaws.com:5432/d7qv2gdhp1aaef'

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    Idno = StringField('ID', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
class RegisterForm_s(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    Idno = StringField('ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm_f(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    Idno = StringField('ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    code = PasswordField('code',validators=[InputRequired() ,Length(min=6,max=6)])
    Student_1=StringField('S-ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    Student_2=StringField('S-ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    Student_3=StringField('S-ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    Student_4=StringField('S-ID' ,validators=[InputRequired(),Length(min=10,max=10)])
    Student_5=StringField('S-ID' ,validators=[InputRequired(),Length(min=10,max=10)])

@app.route("/")
def index():	
	return render_template("index.html")
@app.route("/about")
def about():
	return render_template("about.html")
@app.route('/login_s', methods=['GET', 'POST'])
def login_s():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(idno=form.Idno.data,user_type = 1).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard_s'))
        return '<h1>Invalid user ID or Password</h1>'        
    return render_template("login_s.html",form=form,title='Login')

@app.route('/login_f', methods=['GET', 'POST'])
def login_f():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(idno=form.Idno.data,user_type = 2).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard_f'))
        return '<h1>Invalid user ID or Password'        
    return render_template("login_f.html",form=form,title='Login')

@app.route('/login_a', methods=['GET', 'POST'])
def login_a():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(idno=form.Idno.data ,user_type = '3').first()
        if user:
            if User.query.filter_by(idno=form.Idno.data ,password=form.password.data).first(): 
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard_a'))
        return '<h1>Invalid user ID or Password'        
    return render_template("login_a.html",form=form,title='Login')
     

@app.route("/signUp",methods=['GET','POST'])
def signUp():
    form = RegisterForm_f()
    if form.validate_on_submit() :
        if int(form.code.data) == 666666 :
                if User.query.filter_by(idno=form.Idno.data ).first() == None and Students.query.filter_by(idno=form.Student_1.data).first()!=None and Students.query.filter_by(idno=form.Student_2.data).first()!=None and Students.query.filter_by(idno=form.Student_3.data).first()!=None and Students.query.filter_by(idno=form.Student_4.data).first()!=None and Students.query.filter_by(idno=form.Student_5.data).first()!=None :
                    hashed_password = generate_password_hash(form.password.data, method='sha256')
                    new_user = User(username=form.username.data,user_type=2, email=form.email.data, password=hashed_password,idno=form.Idno.data)
                    db.session.add(new_user)
                    db.session.execute("UPDATE students SET counseller =:coun where idno=:val ",{"coun":form.Idno.data,"val":form.Student_1.data})
                    db.session.execute("UPDATE students SET counseller =:coun where idno=:val ",{"coun":form.Idno.data,"val":form.Student_2.data})
                    db.session.execute("UPDATE students SET counseller =:coun where idno=:val ",{"coun":form.Idno.data,"val":form.Student_3.data})
                    db.session.execute("UPDATE students SET counseller =:coun where idno=:val ",{"coun":form.Idno.data,"val":form.Student_4.data})
                    db.session.execute("UPDATE students SET counseller =:coun where idno=:val ",{"coun":form.Idno.data,"val":form.Student_5.data})
                    db.session.commit()
                    return '<h1>New user has been created!</h1>'
                return '<h1>User already exsists or Added Ids are not Valid </h1>'
    return render_template("signUp_f.html",form =form,title='SignUp')
@app.route("/signup",methods=['GET','POST'])
def signup():
    m=False
    form = RegisterForm_s()
    if form.validate_on_submit():
        if User.query.filter_by(idno=form.Idno.data ).first() == None:       
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data,user_type=1, email=form.email.data, password=hashed_password,idno=form.Idno.data)
            db.session.add(new_user)
            db.session.commit()
            m = True
            return render_template("signup.html",form = form,title='SignUp',msg='Succesfully Signed Up, Please Login',msgs=m)
        return f'<h1>Account with user Id {form.Idno.data} already exsists</h1>'
    return render_template("signup.html",form = form,title='SignUp')
@app.route('/dashboard_s')
@login_required
def dashboard_s():
    return render_template('dashboard_s.html',name=current_user.username)

@app.route('/dashboard_f')
@login_required
def dashboard_f():
    return render_template('dashboard_f.html',name=current_user.username)

@app.route('/dashboard_a')
@login_required
def dashboard_a():
    return render_template('dashboard_a.html',name=current_user.username)

@app.route('/attendence_ai' ,methods =["POST","GET"])
@login_required
def attendence_ai():
     sec = 1
     z=list()
     suma=0
     sumb=0
     sumc=0
     if request.method == 'POST':
        
        e = request.form.get('n')
        f = request.files['inputfile']
        f.save(f.filename) 
        wb=xlrd.open_workbook(f.filename)
        ws=wb.sheet_by_index(0)
        for x in range(ws.nrows):
         if x==0:
            sec=1
         elif ws.cell(x,0).value == 'S.No.':
           x=x+1
           continue
         elif x == 1:
            for b in range(int(ws.cell_value(0,1))):
                z.append(ws.cell(x,b).value)
                s = Subjects(sub=(ws.cell(x,b).value),year=int(ws.cell_value(0,0)))
                db.session.add(s)
                db.session.commit()
         elif x == 2:
            j=0
            for a in z:
                db.session.execute("UPDATE subjects SET seca =:num WHERE sub =:val",{"num":(ws.cell(x,j).value),"val":a})
                j=j+1
                db.session.commit()
            suma=(ws.cell(x,int(ws.cell(x,b).value)).value)
         elif (ws.cell(x,0).value)== 'B':
            l=0
            sec=2
            for a in z:
                db.session.execute("UPDATE subjects SET secb =:num WHERE sub =:val",{"num":(ws.cell(x+1,l).value),"val":a})
                l=l+1
                db.session.commit()
            sumb=(ws.cell(x+1,l).value)
            x=x+1
         elif (ws.cell(x,0).value)== 'C':
            l=0
            sec=3
            for a in z:
                db.session.execute("UPDATE subjects SET secc =:num WHERE sub =:val",{"num":(ws.cell(x+1,l).value),"val":a})
                l=l+1
                db.session.commit()
            sumc=(ws.cell(x+1,l).value)
            x=x+1
         else :
          g=ws.cell(x-1,0).value
          if (g != 'S.No.') and (g != 'B') and (g != 'A') and (g != 'C'): 
            if sec ==1:
                if int(ws.cell(0,1).value)==8:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),tot=(ws.cell(x,11).value),per=(ws.cell(x,12).value),year=(ws.cell(0,0).value),sec='A')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,12).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==9:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),tot=(ws.cell(x,12).value),per=(ws.cell(x,13).value),year=(ws.cell(0,0).value),sec='A')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,13).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==10:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),tot=(ws.cell(x,13).value),per=(ws.cell(x,14).value),year=(ws.cell(0,0).value),sec='A')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,14).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==11:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),tot=(ws.cell(x,14).value),per=(ws.cell(x,15).value),year=(ws.cell(0,0).value),sec='A')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,15).value))
                    db.session.add(h)
                else:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),sub12=(ws.cell(x,14).value),tot=(ws.cell(x,15).value),per=(ws.cell(x,16).value),year=(ws.cell(0,0).value),sec='A')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,16).value))
                    db.session.add(h)
            if sec ==2:
                if ws.cell(0,1).value==8:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),tot=(ws.cell(x,11).value),per=(ws.cell(x,12).value),year=(ws.cell(0,0).value),sec='B')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,12).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==9:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),tot=(ws.cell(x,12).value),per=(ws.cell(x,13).value),year=(ws.cell(0,0).value),sec='B')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,13).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==10:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),tot=(ws.cell(x,13).value),per=(ws.cell(x,14).value),year=(ws.cell(0,0).value),sec='B')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,14).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==11:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),tot=(ws.cell(x,14).value),per=(ws.cell(x,15).value),year=(ws.cell(0,0).value),sec='B')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,15).value))
                    db.session.add(h)
                else:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),sub12=(ws.cell(x,14).value),tot=(ws.cell(x,15).value),per=(ws.cell(x,16).value),year=(ws.cell(0,0).value),sec='B')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,16).value))
                    db.session.add(h)
            if sec ==3:
                if ws.cell(0,1).value==8:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),tot=(ws.cell(x,11).value),per=(ws.cell(x,12).value),year=(ws.cell(0,0).value),sec='C')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,12).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==9:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),tot=(ws.cell(x,12).value),per=(ws.cell(x,13).value),year=(ws.cell(0,0).value),sec='C')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,13).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==10:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),tot=(ws.cell(x,13).value),per=(ws.cell(x,14).value),year=(ws.cell(0,0).value),sec='C')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,14).value))
                    db.session.add(h)
                elif ws.cell(0,1).value==11:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),tot=(ws.cell(x,14).value),per=(ws.cell(x,15).value),year=(ws.cell(0,0).value),sec='C')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,15).value))
                    db.session.add(h)
                else:
                    s=Students(idno=ws.cell_value(x, 1),name=ws.cell_value(x, 2),sub1=(ws.cell(x,3).value),sub2=(ws.cell(x,4).value),sub3=(ws.cell(x,5).value),sub4=(ws.cell(x,6).value),sub5=(ws.cell(x,7).value),sub6=(ws.cell(x,8).value),sub7=(ws.cell(x,9).value),sub8=(ws.cell(x,10).value),sub9=(ws.cell(x,11).value),sub10=(ws.cell(x,12).value),sub11=(ws.cell(x,13).value),sub12=(ws.cell(x,14).value),tot=(ws.cell(x,15).value),per=(ws.cell(x,16).value),year=(ws.cell(0,0).value),sec='C')
                    db.session.add(s)
                    h=History(idno=ws.cell_value(x, 1),first=(ws.cell(x,16).value))
                    db.session.add(h)
            db.session.commit()
        d=Dates(date=datetime.datetime(*xlrd.xldate_as_tuple((ws.cell(0,2).value), wb.datemode)),year=(ws.cell(0,0).value),tota=suma,totb=sumb,totc=sumc)
        w=Start(date=e,year=(ws.cell(0,0).value))
        db.session.add(d)
        db.session.add(w)
        db.session.commit()
        os.remove(f.filename)
        return f'<h1>success</h1>' 
     else:
      return render_template('attendence_ai.html',name=current_user.username)
@app.route('/attendence_au' ,methods =["POST","GET"])
@login_required
def attendence_au():
    z=list()
    suma=0
    sumb=0
    sumc=0
    if request.method == 'POST':
        f = request.files['inputfile']
        f.save(f.filename) 
        wb=xlrd.open_workbook(f.filename)
        ws=wb.sheet_by_index(0)
        ws.cell_value(0, 0)
        p=Dates.query.filter_by(year=int(ws.cell_value(0, 0))).count()
        for x in range(ws.nrows):
         if x==0:
            sec=1
         elif ws.cell(x,0).value == 'S.No.':
           x=x+1
           continue
         elif x == 1:
            for b in range(int(ws.cell_value(0,1))):
                z.append(ws.cell(x,b).value)
         elif x == 2:
            j=0
            for a in z:
                db.session.execute("UPDATE subjects SET seca =:num WHERE sub =:val",{"num":(ws.cell(x,j).value),"val":a})
                j=j+1
                db.session.commit()
            suma=(ws.cell(x,int(ws.cell(x,b).value)).value)
         elif (ws.cell(x,0).value)== 'B':
            l=0
            sec=2
            for a in z:
                db.session.execute("UPDATE subjects SET secb =:num WHERE sub =:val",{"num":(ws.cell(x+1,l).value),"val":a})
                l=l+1
                db.session.commit()
            sumb=(ws.cell(x+1,l).value)
            x=x+1
         elif (ws.cell(x,0).value)== 'C':
            l=0
            sec=3
            for a in z:
                db.session.execute("UPDATE subjects SET secc =:num WHERE sub =:val",{"num":(ws.cell(x+1,l).value),"val":a})
                l=l+1
                db.session.commit()
            sumc=(ws.cell(x+1,l).value)
            x=x+1
         else :
          g=ws.cell(x-1,0).value
          if (g != 'S.No.') and (g != 'B') and (g != 'A') and (g != 'C'): 
                if int(ws.cell(0,1).value)==8:
                    db.session.execute("UPDATE students SET sub1 =:num1 ,sub2 =:num2 ,sub3 =:num3 ,sub4 =:num4 ,sub5 =:num5 ,sub6 =:num6 ,sub7 =:num7 ,sub8 =:num8 ,tot =:num9 ,per =:num10 WHERE idno =:val",{"num1":(ws.cell(x,3).value),"num2":(ws.cell(x,4).value),"num3":(ws.cell(x,5).value),"num4":(ws.cell(x,6).value),"num5":(ws.cell(x,7).value),"num6":(ws.cell(x,8).value),"num7":(ws.cell(x,9).value),"num8":(ws.cell(x,10).value),"num9":(ws.cell(x,11).value),"num10":(ws.cell(x,12).value),"val":ws.cell_value(x, 1)})
                    db.session.commit()
                    hist(p,(ws.cell(x,12).value),ws.cell_value(x, 1))
                elif ws.cell(0,1).value==9:
                    db.session.execute("UPDATE students SET sub1 =:num1 ,sub2 =:num2 ,sub3 =:num3 ,sub4 =:num4 ,sub5 =:num5 ,sub6 =:num6 ,sub7 =:num7 ,sub8 =:num8 ,sub9 =:num9 ,tot =:num10 ,per =:num11 WHERE idno =:val",{"num1":(ws.cell(x,3).value),"num2":(ws.cell(x,4).value),"num3":(ws.cell(x,5).value),"num4":(ws.cell(x,6).value),"num5":(ws.cell(x,7).value),"num6":(ws.cell(x,8).value),"num7":(ws.cell(x,9).value),"num8":(ws.cell(x,10).value),"num9":(ws.cell(x,11).value),"num10":(ws.cell(x,12).value),"num11":(ws.cell(x,13).value),"val":ws.cell_value(x, 1)})
                    db.session.commit()
                    hist(p,(ws.cell(x,13).value),ws.cell_value(x, 1))
                elif ws.cell(0,1).value==10:
                    db.session.execute("UPDATE students SET sub1 =:num1 ,sub2 =:num2 ,sub3 =:num3 ,sub4 =:num4 ,sub5 =:num5 ,sub6 =:num6 ,sub7 =:num7 ,sub8 =:num8 ,sub9 =:num9,sub10 =:num10  ,tot =:num11 ,per =:num12 WHERE idno =:val",{"num1":(ws.cell(x,3).value),"num2":(ws.cell(x,4).value),"num3":(ws.cell(x,5).value),"num4":(ws.cell(x,6).value),"num5":(ws.cell(x,7).value),"num6":(ws.cell(x,8).value),"num7":(ws.cell(x,9).value),"num8":(ws.cell(x,10).value),"num9":(ws.cell(x,11).value),"num10":(ws.cell(x,12).value),"num11":(ws.cell(x,13).value),"num12":(ws.cell(x,14).value),"val":ws.cell_value(x, 1)})
                    db.session.commit()
                    hist(p,(ws.cell(x,14).value),ws.cell_value(x, 1))
                elif ws.cell(0,1).value==11:
                    db.session.execute("UPDATE students SET sub1 =:num1 ,sub2 =:num2 ,sub3 =:num3 ,sub4 =:num4 ,sub5 =:num5 ,sub6 =:num6 ,sub7 =:num7 ,sub8 =:num8 ,sub9 =:num9,sub10 =:num10 ,sub11 =:num11 ,tot =:num12 ,per =:num13 WHERE idno =:val",{"num1":(ws.cell(x,3).value),"num2":(ws.cell(x,4).value),"num3":(ws.cell(x,5).value),"num4":(ws.cell(x,6).value),"num5":(ws.cell(x,7).value),"num6":(ws.cell(x,8).value),"num7":(ws.cell(x,9).value),"num8":(ws.cell(x,10).value),"num9":(ws.cell(x,11).value),"num10":(ws.cell(x,12).value),"num11":(ws.cell(x,13).value),"num12":(ws.cell(x,14).value),"num13":(ws.cell(x,15).value),"val":ws.cell_value(x, 1)})
                    db.session.commit()
                    hist(p,(ws.cell(x,15).value),ws.cell_value(x, 1))
                else:
                    db.session.execute("UPDATE students SET sub1 =:num1 ,sub2 =:num2 ,sub3 =:num3 ,sub4 =:num4 ,sub5 =:num5 ,sub6 =:num6 ,sub7 =:num7 ,sub8 =:num8 ,sub9 =:num9,sub10 =:num10 ,sub11 =:num11 ,sub12 =:num12 ,tot =:num13 ,per =:num14 WHERE idno =:val",{"num1":(ws.cell(x,3).value),"num2":(ws.cell(x,4).value),"num3":(ws.cell(x,5).value),"num4":(ws.cell(x,6).value),"num5":(ws.cell(x,7).value),"num6":(ws.cell(x,8).value),"num7":(ws.cell(x,9).value),"num8":(ws.cell(x,10).value),"num9":(ws.cell(x,11).value),"num10":(ws.cell(x,12).value),"num11":(ws.cell(x,13).value),"num12":(ws.cell(x,14).value),"num13":(ws.cell(x,15).value),"num14":(ws.cell(x,16).value),"val":ws.cell_value(x, 1)})
                    db.session.commit()
                    hist(p,(ws.cell(x,15).value),ws.cell_value(x, 1))
         db.session.commit()
        d=Dates(date=datetime.datetime(*xlrd.xldate_as_tuple((ws.cell(0,2).value), wb.datemode)),year=(ws.cell(0,0).value),tota=suma,totb=sumb,totc=sumc)
        db.session.add(d)
        db.session.commit()
        os.remove(f.filename)
        return f'<h1>sucessfully updated</h1>'
    else:
        return render_template('attendence_au.html',name=current_user.username)
def hist(p,q,r):
    if p==0:
       db.session.execute("UPDATE history SET first =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==1:
       db.session.execute("UPDATE history SET second =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==2:
       db.session.execute("UPDATE history SET third =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==3:
       db.session.execute("UPDATE history SET fourth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==4:
       db.session.execute("UPDATE history SET fifth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==5:
       db.session.execute("UPDATE history SET sixth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==6:
       db.session.execute("UPDATE history SET seventh =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==7:
       db.session.execute("UPDATE history SET eigth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==8:
       db.session.execute("UPDATE history SET nineth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
    elif p==9:
       db.session.execute("UPDATE history SET tenth =:num WHERE idno =:val",{"num":q,"val":r})
       db.session.commit()
@app.route('/dashboard_s/attendence_s')   
@login_required
def attendence_s():
    ove=0
    s=Students.query.filter_by(idno=current_user.idno).first()
    if s == None:
        return '<h1>No id no. found</h1>' 
    if s.sec=='A':
        t=Dates.query.filter_by(year=s.year).first()
        ove=t.tota
    elif s.sec=='B':
        t=Dates.query.filter_by(year=s.year).first()
        ove=t.totb
    else:
        t=Dates.query.filter_by(year=s.year).first()
        ove=t.totc 
    return render_template('attendence_s.html',idno=s.idno,name=current_user.username,sn=s.name,per=s.per,year=s.year,sec=s.sec,tot=s.tot,ove=ove,date=t.date)
@app.route('/not_available')   
@login_required
def not_available():
    return '<h1>Not Available yet !!</h1>'
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
