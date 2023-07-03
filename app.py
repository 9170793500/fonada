from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
import smtplib

import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, template_folder="template")

app.config.update(
    MAIL_SERVER = 'smtp.google.com',
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

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phoneno = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Post(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)
    paragraph = db.Column(db.String(1000), nullable=False)

@app.route("/home")

def home():
    post = Post.query.filter_by().all()[0 : params['no_of_post']]
    return render_template('home.html',params=params, post=post)

@app.route("/login")
def login():
    return render_template('login.html',params=params)

@app.route("/layout")
def layout():
    return render_template('layout.html',params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,  post=post)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        datetime = request.form.get('date')
        entry = Contect(name=name, phoneno = phone, msg = message, date= 'datetime.now()',email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients =[params['gmail-user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', params=params)

app.run(debug=True )

