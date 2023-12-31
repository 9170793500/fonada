from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 


import json
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, template_folder='template')


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contect(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phoneno = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Ragistation(db.Model):
    
    sno = db.Column(db.Integer(), primary_key=True)
    Username = db.Column(db.String(50),nullable=False)
    Mothername = db.Column(db.String(20), nullable=False)
    Fathername = db.Column(db.String(20), nullable=False)
    Address = db.Column(db.String(100), nullable=True)
    Gender = db.Column(db.String(20), nullable=False)
    DOB = db.Column(db.Integer, nullable=False)
    Pincode = db.Column(db.Integer, nullable=False)
    EmailID = db.Column(db.String(40), nullable=False)

class Login(db.Model):
    sno = db.Column(db.Integer(), primary_key=True)
    Username = db.Column(db.String(50) )
    Password = db.Column(db.String(20), nullable=False)

@app.route("/home")
def home():
    return render_template('home.html',params=params)

@app.route("/login", methods = ['GET','POST'])
def login():
     if(request.method=='POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        entry = Login(Username=Username, Password = Password)
        db.session.add(entry)
        db.session.commit()
     return render_template('login.html', params=params )

@app.route("/farget")
def forget():
    return render_template('farget.html',params=params)

@app.route("/farget2")
def forge2t():
    return render_template('farget2.html')

@app.route("/layout")
def layout():
    return render_template('layout.html',params=params)


@app.route("/ragistation", methods = ['GET','POST'])
def ragistation():
     if(request.method=='POST'):
        Username = request.form.get('Username') 
        Mothername = request.form.get('Mothername')
        Fathername = request.form.get('Fathername')
        Address = request.form.get('Address')
        Gender = request.form.get('Gender')
        DOB = request.form.get('DOB')
        Pincode = request.form.get('Pincode')
        EmailID = request.form.get('EmailID')
    
        entry = Ragistation(Username= Username, Mothername = Mothername,
                         Fathername = Fathername, Address= Address,Gender= Gender,
                         DOB=DOB, Pincode=Pincode, EmailID = EmailID)
        db.session.add(entry)
        db.session.commit()
    
     return render_template('ragistation.html', params=params )

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
      
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
      
        entry = Contect(name=name, phoneno = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
      
    return render_template('contact.html', params=params)

app.run(debug=True )

