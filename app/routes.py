from flask import render_template, redirect, url_for, request
from app import app, db #imports the instance of the flask app created in __init__.py
import requests



@app.route('/')
@app.route('/index') # Both of these serves as routes to the homepage.
def index(): 
    return render_template('index.html', title='Home')

@app.route('/search_matches', methods=['GET'])
def search_matches():
    """
    Search the database to see if matches against a particular opposition or season
    exist. If not, then a request to the API should be made to the API, and the relevant information
    should then be added to the db. Once added, the db should then be searched again and returned to the user.
    """
    # try:
    #     db.stats.find({'$or': [{'home-team':'Abderdeen'},{'away-team':'Aberdeen'}]})
    # except:
    #     print('No games with matching criteria')
    # else:
    #     # Make request to API here and add
    print('Match List')
    return redirect(url_for('match_list'))


@app.route('/match_list')
def match_list():
    return render_template('matchlist.html', title='Match List')


@app.route('/match_stats')
def match_stats():
    return render_template('matchstats.html', title='Match Stats')


@app.route('/add_comment')
def add_comment():
    return render_template('addcomment.html', title='Add Comment')