from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# now create a flask instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# secret key
app.config['SECRET_KEY'] = "senha muito secreta"

# The initialize the database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("Qual é o seu nome?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a route decorate (it's how ...url.../home.html)
@app.route('/') # it works when there ins't route name

#def index():
#    return "<h1>Hello World!</h1>"

# FILTERS:
# safe
# capitalize
# lower 
# upper 
# title
# trim
# spritags

def index():
    first_name = "Maria"
    stuff = "Essa é minha <strong>Lista</strong>"
    flash("Seja Bem Vindo(a)!")
    favorites_pizza = ["Caminhar", "Diminuir Sal", "Dormir 8h+", "Beber água"]
    return render_template("index.html",
                            first_name=first_name,
                            stuff=stuff,
                            favorites_pizza=favorites_pizza)

# localhost:5000/user/mary
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)
#set FLASK_APP=hello.py
#set FLASK_ENV=development

# Create Custom Error Page

#invalid url
@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")

#internal server error
@app.errorhandler(500)
def page_not_fount(e):
    return render_template("500.html")

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])

def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Formulário Submetido Com Sucesso!")

    return render_template("name.html",
                            name = name,
                            form = form)