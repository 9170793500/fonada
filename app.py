from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
import smtplib

import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, template_folder='template')

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'gmail-user',
    MAIL_PASSWORD=  'gmail-password'
  
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contect(db.Model):

    sno = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phoneno = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Dataadd(db.Model):

    sno = db.Column(db.Integer(), primary_key=True)
    Username = db.Column(db.String(50), nullable=False , unique=True)
    Mothername = db.Column(db.String(20), nullable=False)
    Fathername = db.Column(db.String(20), nullable=False)
    Address = db.Column(db.String(100), nullable=True)
    Gender = db.Column(db.String(20), nullable=False)
    DOB = db.Column(db.Integer, nullable=False)
    Pincode = db.Column(db.Integer, nullable=False)
    EmailID = db.Column(db.String(40), nullable=False)


@app.route("/")
def home():
    return render_template('home.html',params=params)

@app.route("/login")
def login():
    return render_template('login.html',params=params)

@app.route("/farget")
def forget():
    return render_template('farget.html',params=params)

@app.route("/farget2")
def forge2t():
    return render_template('farget2.html',params=params)

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
        entry = Dataadd(Username=Username, Mothername = Mothername,
                         Fathername = Fathername, Address= 'Address',Gender= Gender,
                         DOB='DOB', Pincode='Pincode',EmailID='Email ID')
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
        datetime = request.form.get('date')
        data = Contect(name=name, phoneno = phone, msg = message, date= 'datetime.now()',email = email )
        db.session.add(data)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients =[params['gmail-user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', params=params)

app.run(debug=True )

