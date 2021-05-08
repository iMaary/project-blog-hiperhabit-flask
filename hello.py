from flask import Flask, render_template

# now create a flask instance
app = Flask(__name__)

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
    first_name = "Mary"
    stuff = "This is <strong>Bold</strong> tag"
    favorites_pizza = ["Mussarela", "Calabresa", "Marguetira", "4 Queijos", 41]
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


