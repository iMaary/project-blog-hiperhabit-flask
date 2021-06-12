from operator import pos
from flask import Flask, render_template, flash, request
from flask.signals import request_finished
from flask_wtf import FlaskForm, form
from werkzeug.wrappers import AuthorizationMixin
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets.core import TextArea

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

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # It's what will stay after of the route
    slug = db.Column(db.String(255))

# Create a Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash('Postado com Sucesso!')

    # Redirect to Webpage
    return render_template("add_post.html", form=form)


# JASON Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "Mary": "4 Queijos",
        "Carla": "Calabresa"
    }
    return favorite_pizza
    # return {"Date": date.today()}


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("a senha não pode ser lida")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    password_hash = PasswordField("Senha", validators=[DataRequired(), EqualTo('password_hash2', message='As senhas devem combinar')])
    password_hash2 = PasswordField("Confirmar Senha", validators=[DataRequired()])
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
class PasswordForm(FlaskForm):
    email = StringField("Qual é o seu email?", validators=[DataRequired()])
    password_hash = PasswordField("Qual é a sua senha?", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
            # Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data  = ''
        flash("Usuário Adicionado Com Sucesso!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", name=name,
                                            form=form,
                                            our_users=our_users)

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])

def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    # Validate Form if it was Submited
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        # Clear Form
        form.email.data = ''
        form.password_hash.data = ''

        # Look Up User By Email Adress
        pw_to_check = Users.query.filter_by(email=email).first()
        
        # Check Hash Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html", email=email,
                                           password=password,
                                           pw_to_check=pw_to_check,
                                           passed=passed,
                                           form=form)

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