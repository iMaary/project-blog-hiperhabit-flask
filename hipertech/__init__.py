from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "senha muito secreta"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import hipertech.models
import hipertech.routes
import hipertech.forms


