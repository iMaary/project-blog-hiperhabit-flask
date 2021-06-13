from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets.core import TextArea

# Create a Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Senha", validators=[DataRequired(), EqualTo('password_hash2', message='As senhas devem combinar')])
    password_hash2 = PasswordField("Confirmar Senha", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class PasswordForm(FlaskForm):
    email = StringField("Qual é o seu email?", validators=[DataRequired()])
    password_hash = PasswordField("Qual é a sua senha?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("Qual é o seu nome?", validators=[DataRequired()])
    submit = SubmitField("Submit")