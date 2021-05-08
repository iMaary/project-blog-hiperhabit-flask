from flask import Flask, render_template

# now create a flask instance
app = Flask(__name__)

#create a route decorate (it's how ...url.../home.html)
@app.route('/') # it works when there ins't route name

#def index():
#    return "<h1>Hello World!</h1>"

def index():
    return render_template("index.html")

# localhost:5000/user/mary
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)
#set FLASK_APP=hello.py
#set FLASK_ENV=development