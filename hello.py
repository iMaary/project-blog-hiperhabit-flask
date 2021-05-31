from flask import Flask, render_template, flash, request
from flask.signals import request_finished
from flask_wtf import FlaskForm, form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from datetime import datetime

# now create a flask instance
app = Flask(__name__)

# Add database
#Old SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:62777999&aooa@localhost/our_users'

# Secret Key
app.config['SECRET_KEY'] = "senha muito secreta"

# The initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#Create A String
def __repr__(self):
    return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Usuário deletado com sucesso!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", name=name,
                                                form=form,
                                                our_users=our_users)
    except:
        flash("Opa, aconteceu algo de errado ao tentar deletar esse usuário... tente novamente!")
        return render_template("add_user.html", 
        name=name, form=form, our_users=our_users)

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email =  request.form['email']
        name_to_update.favorite_color =  request.form['favorite_color']
        try:
            db.session.commit()
            flash("Usuário Atualizado com Sucesso")
            return render_template("update.html",
                form=form,
                name_to_update = name_to_update)
        except:
            flash("ERRO! Parece que ocorreu algum problema... tente novamente")
            return render_template("update.html",
                form=form,
                name_to_update = name_to_update)
    else:
        return render_template("update.html",
                form=form,
                name_to_update = name_to_update,
                id=id)

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("Qual é o seu nome?", validators=[DataRequired()])
    submit = SubmitField("Submit")

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

#Create a route decorate (it's how ...url.../home.html)
@app.route('/') # it works when there ins't route name

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

# Local create user register 
@app.route('/user/add', methods=['GET', 'POST'])

def add_user():
    name = None
    form = UserForm()
    # Validate Form if it was Submited
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("Usuário Adicionado Com Sucesso!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", name=name,
                                            form=form,
                                            our_users=our_users)

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])

def name():
    name = None
    form = NamerForm()
    # Validate Form if it was Submited
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Formulário Submetido Com Sucesso!")

    return render_template("name.html", name = name,
                                        form = form)

# Create Custom Error Page

#invalid url
@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")

#internal server error
@app.errorhandler(500)
def page_not_fount(e):
    return render_template("500.html")