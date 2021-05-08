from flask import Flask, render_template

# now create a flask instance
app = Flask(__name__)

#create a route decorate (it's how ...url.../home.html)
@app.route('/') # it works when there ins't route name

def index():
    return "<h1>Hello World!</h1>"

# localhost:5000/user/mary
@app.route('/user/<name>')

def user(name):
    return "<h1>Hello, {}!</h1>".format(name)
#set FLASK_APP=hello.py
#set FLASK_ENV=development