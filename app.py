from flask import Flask
from config import Config
from flask_pymongo import PyMongo, MongoClient
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, url_for, request, session, flash
import requests
import json
from bson.objectid import ObjectId
import os
from os import path

if path.exists('api.py'):
    from api import api_url, api_querystring, api_headers


# initiates an instance of the flask and assigns it to app
app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

# Passes the MongoURI and assigns the correct collection to db to access it in routes.
client = MongoClient(Config.MONGO_URI)
db = client.hfc_stats


@app.route('/')
@app.route('/index')  # Both of these serves as routes to the homepage.
def index():
    """
    Check if a user is logged in, if so, redirect them  to the 'My Reports' page. If not, render the index template.
    """

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('index.html', title='Home', logged_in=logged_in)


@app.route('/register_page')
def register_page():
    """
    Check if user is logged in, if so, redirect to "my Reports". If not, render the register template.
    """

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('register.html', title='Register', logged_in=logged_in)


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    Check to see if method is post, if so, check to see if the username provided already exists in the db. If the user
    does not exist, then create a hash of the password provided and then store the hashed password and the username
    in the database. Add the new user to the session so that they are logged in once registered and redirect them to
    the "My Reports" page. If the username already exists, a message should be shown to the user saying so.
    """

    if request.method == 'POST':
        users = db.users
        user_exists = users.find_one({'username': request.form.get('username')})

        if not user_exists:
            pw_hash = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            users.insert({'username': request.form.get('username'), 'password': pw_hash})
            session['username'] = request.form.get('username')
            return redirect(url_for('user_reports'))
        else:
            flash('Username already exists. Please try another one.')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login_page')
def login_page():
    """
    Check if the user is logged in, if so redirect to "my Reports". If not, render the login form.
    """

    logged_in = True if 'username' in session else False

    if logged_in:
        return redirect(url_for('user_reports'))

    return render_template('login.html', title='Login', logged_in=logged_in)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Check is the username provided exists in the database. If so, check the hashed password. If it matches, add the
    user to the session and redirect to "my Reports".  If either the username doesnt exist, ot the password doesnt
    match, the flash a message to the user detailing the issue.
    """

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
    """
    Clear the session and redirect to the index page.
    """

    session.clear()
    return redirect(url_for('index'))


@app.route('/user_reports')
def user_reports():
    """
    Check if the user is logged in, if not, redirect them to the index page. If so, render a list of reports that
    have been created by the logged in user. Do a count on the cursor object so that I can return a message in the
    template if the user hasnt created any reports yet.
    """

    logged_in = True if 'username' in session else False

    if not logged_in:
        return redirect(url_for('index'))

    reports = db.stats.find({'author': session['username']})

    count = db.stats.count({'author': session['username']})

    return render_template('userreports.html', logged_in=logged_in, reports=reports, title='My Reports', count=count)


@app.route('/opposition_choice')
def opposition_choice():
    """
    Check if the user is logged in, if not, redirect to index page. If user is logged in, then render opposition
    choice page.
    """

    logged_in = True if 'username' in session else False

    if not logged_in:
        return redirect(url_for('index'))

    return render_template('oppositionchoice.html', logged_in=logged_in, title='Opposition Choice')


@app.route('/search_matches', methods=['POST', 'GET'])
def search_matches():
    """
    Check to see if the user is logged in. If not, redirect to index page.If logged in, check to see if method was post.
    If so, call the API and retrieve the data. If the api call is successful, then convert the JSON data into a python
    dictionary. Then, all the matches  involving the opposition team selected should be filtered into a seperate list.
    Render the matchlist page.
    """

    logged_in = True if 'username' in session else False

    if not logged_in:
        return redirect(url_for('index'))

    if request.method == 'POST':
        response = requests.request("GET", os.environ.get('api_url'), headers=os.environ.get('api_headers'),
                                    params=os.environ.get('api_querystring'))

        if response.status_code == 200:
            selected = request.form.get('opposition-list')
            api_dict = json.loads(response.text)

            matches = []
            for i in api_dict['api']['fixtures']:
                if selected in i['homeTeam']['team_name'] or selected in i['awayTeam']['team_name']:
                    if i['homeTeam']['team_name'] and i['awayTeam']['team_name'] and i['score']['fulltime'] and \
                            i['event_date'] and i['venue'] and i['league']['name']:
                        matches.append(i)
            return render_template('matchlist.html', matches=matches, logged_in=logged_in, title='Match List')
        else:
            flash('Sorry, we were unable to retrieve the data at this time. Please try again later.')
            return redirect('opposition_choice')


@app.route('/create_report/<ht>/<at>/<venue>/<date>/<league>/<score>')
def create_report(ht, at, venue, league, date, score):
    """
    Check to see if the user is logged in, if not, redirect to the index page. If logged in, then render the form to
    enter the report details. This function also should pass the details from the match over to the form so it can be
     pre-populated.
    """

    logged_in = True if 'username' in session else False

    if not logged_in:
        return redirect(url_for('index'))

    return render_template('createreport.html', logged_in=logged_in, title='Create Report', ht=ht, at=at, venue=venue,
                           league=league, date=date, score=score)


@app.route('/submit_report', methods=['POST', 'GET'])
def submit_report():
    """
    Enter the details provided in the form into the db. Then redirect to 'My reports'.
    """

    db.stats.insert({
        'home_team': request.form.get('home_team'),
        'away_team': request.form.get('away_team'),
        'score': request.form.get('score'),
        'venue': request.form.get('venue'),
        'date': request.form.get('date'),
        'league_name': request.form.get('league_name'),
        'match_report': request.form.get('match_report'),
        'author': session['username']
    })

    return redirect(url_for('user_reports'))


@app.route('/edit_report/<report_id>')
def edit_report(report_id):
    """
    Check to see if user is logged in. If not, redirect to index page. If logged in, render the edit report template
    with details pre-populated in the form.
    """

    logged_in = True if 'username' in session else False

    if not logged_in:
        return redirect(url_for('index'))

    report = db.stats.find_one({'_id': ObjectId(report_id)})
    return render_template('editreport.html', report=report, title='Edit Report', logged_in=logged_in)


@app.route('/update_report/<report_id>', methods=['POST', 'GET'])
def update_report(report_id):
    """
    Updated the report in the template with values provided in the form.
    """

    db.stats.update({'_id': ObjectId(report_id)},
                    {
                        'home_team': request.form.get('home_team'),
                        'away_team': request.form.get('away_team'),
                        'score': request.form.get('score'),
                        'venue': request.form.get('venue'),
                        'date': request.form.get('date'),
                        'league_name': request.form.get('league_name'),
                        'match_report': request.form.get('match_report'),
                        'author': session['username']
                    })
    return redirect(url_for('user_reports'))


@app.route('/delete_report/<report_id>')
def delete_report(report_id):
    """
    Delete the specific report from the database.
    """

    db.stats.remove({'_id': ObjectId(report_id)})
    return redirect(url_for('user_reports'))


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)


# has to be imported after the instance on the flask app has been created.
# from app import routes