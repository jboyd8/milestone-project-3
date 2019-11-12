from flask import render_template, redirect, url_for
from app import app #imports the instance of the flask app created in __init__.py

@app.route('/')
@app.route('/index') # Both of these serves as routes to the homepage.
def index():
    return render_template('index.html', title='Home')