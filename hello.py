from flask import Flask, render_template

# now create a flask instance
app = Flask(__name__)

#create a route decorate (it's how ...url.../home.html)
@app.route('/') # it works when there ins't route name

def index():
    return "<h1>Hello World!</h1>"