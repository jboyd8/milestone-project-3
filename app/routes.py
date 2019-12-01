from flask import render_template, redirect, url_for, request
from app import app, db  # imports the instance of the flask app created in __init__.py
import requests
from app.api import api_url, api_querystring, api_headers
import json


@app.route('/')
@app.route('/index')  # Both of these serves as routes to the homepage.
def index():
    return render_template('index.html', title='Home')


@app.route('/search_matches', methods=['POST', 'GET'])
def search_matches():
    """
    Search the database to see if matches against a particular opposition or season
    exist. If not, then a request to the API should be made to the API, and the relevant information
    should then be added to the db. Once added, the db should then be searched again and returned to the user.
    """
    if request.method == 'POST':
        selected = request.form.get('opposition-list')
        query = {'$or': [{'homeTeam': {'team_name': selected}}, {'awayTeam': {'team_name': selected}}]}
        matches = db.stats.find(query)
        count_docs = matches.count()

        print(count_docs)

        if not count_docs:
            response = requests.request(
                "GET", api_url, headers=api_headers, params=api_querystring)
            if response.status_code == 200:
                api_dict = json.loads(response.text)
                # access dict here to get values to add into db.

                filtered_dict = []
                
                for i in api_dict['api']['fixtures']:
                    if selected in i['homeTeam']['team_name'] or selected in i['awayTeam']['team_name']:
                        filtered_dict.append(i)
                
                db.stats.insert_many(filtered_dict)

    return render_template('matchlist.html', matches=matches)


@app.route('/match_list')
def match_list():
    return render_template('matchlist.html', title='Match List')


@app.route('/create_report')
def create_report():
    return render_template('createreport.html', title='Add Report')
