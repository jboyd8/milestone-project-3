from flask import render_template, redirect, url_for
from app import app, db #imports the instance of the flask app created in __init__.py
import requests



@app.route('/')
@app.route('/index') # Both of these serves as routes to the homepage.
def index():
    try:
        db.stats.find({'$or': [{'home-team':'Abderdeen'},{'away-team':'Aberdeen'}]})
    except:
        print('No games with matching criteria')
    return render_template('index.html', title='Home')


@app.route('/match_list')
def match_list():
    return render_template('matchlist.html', title='Match List')


@app.route('/match_stats')
def match_stats():
    return render_template('matchstats.html', title='Match Stats')


@app.route('/add_comment')
def add_comment():
    return render_template('addcomment.html', title='Add Comment')