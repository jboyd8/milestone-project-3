from flask import render_template, redirect, url_for, request, session, flash
from app import app, db, bcrypt  # imports the instance of the flask app created in __init__.py
import requests
from app.api import api_url, api_querystring, api_headers
import json
from bson.objectid import ObjectId


@app.route('/')
@app.route('/index')  # Both of these serves as routes to the homepage.
def index():

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('index.html', title='Home', logged_in=logged_in)


@app.route('/register_page')
def register_page():

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('register.html', title='Register', logged_in=logged_in)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        user_exists = users.find_one({'username': request.form.get('username')})

        if user_exists is None:
            pw_hash = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            users.insert({'username': request.form.get('username'), 'password': pw_hash})
            session['username'] = request.form.get('username')
            return redirect(url_for('index'))
        else:
            flash('Username already exists. Please try another one.')
            return redirect(url_for('register'))
        
    return render_template('register.html')


@app.route('/login_page')
def login_page():

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('login.html', title='Login', logged_in=logged_in)


@app.route('/login', methods=['POST', 'GET'])
def login():

    users = db.users
    login_user = users.find_one({'username': request.form.get('username')})

    if login_user:
        if bcrypt.check_password_hash(login_user['password'], request.form.get('password').encode('utf-8')):
            session['username'] = request.form.get('username')
            return redirect(url_for('user_reports'))
        else:
            flash('Invalid Username/Password Combination')
            return redirect('login_page')
    else:
        flash('Username does not exist')
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user_reports')
def user_reports():

    logged_in = True if 'username' in session else False

    return render_template('userreports.html', logged_in=logged_in)


@app.route('/opposition_choice')
def opposition_choice():

    logged_in = True if 'username' in session else False

    return render_template('oppositionchoice.html', logged_in=logged_in)


@app.route('/search_matches', methods=['POST', 'GET'])
def search_matches():
    """
    Search the database to see if matches against a particular opposition or season
    exist. If not, then a request to the API should be made, and the relevant information
    should then be added to the db. Once added, the db should then be searched again and returned to the user.
    """

    logged_in = True if 'username' in session else False

    if request.method == 'POST':
        response = requests.request("GET", api_url, headers=api_headers, params=api_querystring)

        if response.status_code == 200:
            selected = request.form.get('opposition-list')
            api_dict = json.loads(response.text)

            filtered_dict = []
            for i in api_dict['api']['fixtures']:
                if selected in i['homeTeam']['team_name'] or selected in i['awayTeam']['team_name']:
                    filtered_dict.append(i)

            matches = filtered_dict


    # if request.method == 'POST':
    #     selected = request.form.get('opposition-list')
    #     query = {'$or': [{'homeTeam.team_name': selected}, {'awayTeam.team_name': selected}]}
    #     matches = db.stats.find(query)
    #     count_docs = matches.count()
    #
    #     if not count_docs:
    #         response = requests.request(
    #             "GET", api_url, headers=api_headers, params=api_querystring)
    #         if response.status_code == 200:
    #             api_dict = json.loads(response.text)
    #             # access dict here to get values to add into db.
    #
    #             filtered_dict = []
    #
    #             for i in api_dict['api']['fixtures']:
    #                 if selected in i['homeTeam']['team_name'] or selected in i['awayTeam']['team_name']:
    #                     filtered_dict.append(i)
    #
    #             db.stats.insert_many(filtered_dict)
    #
    #             matches = db.stats.find(query)

    return render_template('matchlist.html', matches=matches, logged_in=logged_in)


@app.route('/create_report')
def create_report():

    logged_in = True if 'username' in session else False

    return render_template('createreport.html', title='Add Report', logged_in=logged_in)


@app.route('/submit_report', methods=['POST', 'GET'])
def submit_report():
    db.stats.insert({
        'home_team' : request.form.get('home_team'),
        'away_team' : request.form.get('away_team'),
        'score' : request.form.get('score'),
        'venue' : request.form.get('venue'),
        'date' : request.form.get('date'),
        'league_name' : request.form.get('league_name'),
        'match_report' : request.form.get('match_report')
    })

    return redirect(url_for('user_reports'))
#
#
# @app.route('/edit_report')
# def edit_report(match_id):
#     the_match = db.stats.find_one({'_id': ObjectId(match_id)})
#     return render_template('editreport.html', match=the_match, title='Edit Report')


# @app.route('/delete_report/<match_id>')
# def delete_report(match_id):
#     db.stats.remove({'_id': ObjectId(match_id)})
#     return redirect(url_for('index'))


