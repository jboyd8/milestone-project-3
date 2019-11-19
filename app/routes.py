from flask import render_template, redirect, url_for, request
from app import app, db  # imports the instance of the flask app created in __init__.py
import requests


@app.route('/')
@app.route('/index')  # Both of these serves as routes to the homepage.
def index():
    matches = db.stats.find()
    return render_template('index.html', title='Home', matches=matches)


@app.route('/search_matches', methods=['POST', 'GET'])
def search_matches():
    """
    Search the database to see if matches against a particular opposition or season
    exist. If not, then a request to the API should be made to the API, and the relevant information
    should then be added to the db. Once added, the db should then be searched again and returned to the user.
    """
    if request.method == 'POST':
        try:
            selected = request.form.get('opposition-list')
            matches = db.stats.find(
                {'$or': [{'home_team': selected}, {'away_team': selected}]})
            # return redirect(url_for('match_list'), matches=matches)
        except:
            print('No Matches found')
        # else:
        #     url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/249"
        #     querystring = {"timezone": "Europe/London"}
        #     headers = {
        #     'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        #     'x-rapidapi-key': "2fb5aa3fd7mshe3fb9b490c8acf2p198b7fjsnb482b6b374aa"}
        #     response = requests.request("GET", url, headers=headers, params=querystring)
        #     print(response.text)

    return render_template('matchlist.html', matches=matches)


@app.route('/match_list')
def match_list():
    return render_template('matchlist.html', title='Match List')


@app.route('/match_stats')
def match_stats():
    return render_template('matchstats.html', title='Match Stats')


@app.route('/add_comment')
def add_comment():
    return render_template('addcomment.html', title='Add Comment')
