from flask import Flask, abort, request, url_for, render_template
from uuid import uuid4
import os
import requests
import requests.auth
import urllib
import urllib.parse
import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

CLIENT_ID = "Q9UV2ZsbXF0K3w"
CLIENT_SECRET = "DSh_JRQi563PWGayN1BHWmV89M8"
REDIRECT_URI = "http://secret-cove-59920.herokuapp.com/subredditkarma_callback"

def user_agent():
    return "oauth2-owncheck by /u/spis19av"
    raise NotImplementedError()

def base_headers():
    return {"User-Agent": user_agent()}

app = Flask(__name__)

@app.route('/')
def render_main():
    return render_template('home.html')

#@app.route('/testit')
#def render_testit():
#    return render_template('testit.html')

@app.route('/about')
def render_about():
    return render_template('about.html')

@app.route('/testit_callback')
def render_testit_callback():
    render_template('/testit_callback.html')

@app.route('/testit')
def make_authorization_url():
    #uuid = universal unique identifier
    #Creates a unique string for each authorization request
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
                    "response_type": "code",
                    "redirect_uri": REDIRECT_URI,
                    "duration": "permanent",
                    "scope": "identity " + "save " + "history " + "mysubreddits",
                    "state": state}
    url = "https://reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    #Sends the data to the testit webpage with auth storing the authorize url
    return render_template('testit.html', auth = url)    

def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/subredditkarma_callback')
def karma_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    karmascore = get_karma(access_token)
    
    return render_template('subredditkarma_callback.html', karmascore = karmascore)

@app.route('/username_callback')
def username_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    username = get_username(access_token)

    return render_template('username_callback.html', username = username)

#function that gets access code using code granted from user's grant of permission on reddit
def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                            auth = client_auth,
                            headers=headers,
                            data = post_data)
    token_json = response.json()
    return token_json["access_token"]

def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers = headers)
    me_json = response.json()
    return me_json['name']

def get_karma(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/user/spis19av/saved", headers = headers)
    me_json = str(response.json())
    urlsearch = re.compile("'https://www.reddit.com(?:.*?)',")
    urlresults = urlsearch.findall(me_json)
    return urlresults
    #return response.json()


#me_json configure only print urls


@app.route('/teamoffense')
def render_teamOffense():
    return render_template('team_offense.html')

@app.route('/team_offense_result')
def render_team_offense_result():
    try:
        offense_result = request.args['school']
        attack_result = getOffenseStats(offense_result)
        return render_template('team_offense_result.html', attack_form = attack_result)
    except ValueError:
        return "Sorry: invalid team"

def getOffenseStats(school): 
    url = "https://www.sports-reference.com/cfb/years/2018-team-offense.html"
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    soup.findAll('tr')
    tableHead = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
    otherTableHead = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]
    tableHead = tableHead[1:]
    #print(otherTableHead)
    rows = soup.findAll('tr')[1:]
    teamStats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    stats = pd.DataFrame(teamStats, columns = tableHead)
    #print(stats)
    statsCols = stats.columns
    statsSize = stats.size
    name = school
    statsRows = int(statsSize//len(statsCols))
    while statsRows > 0:
        statsRows -= 1
        university = stats.loc[statsRows]['School']
        if university != None and university == name:
            index = 0
            string = ""
            string += otherTableHead[index]
            index += 1
            string += str(stats.iloc[statsRows,0:3])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index] +"\n"
            index += 1
            string += str(stats.iloc[statsRows,3:8])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index] +"\n"
            index += 1
            string += str(stats.iloc[statsRows,8:12])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index] +"\n"
            index += 1
            string += str(stats.iloc[statsRows,12:15])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index] +"\n"
            index += 1
            string += str(stats.iloc[statsRows,15:19])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index] +"\n"
            index += 1
            string += str(stats.iloc[statsRows,19:21])+"/\/\/\/\/\/\/\/\/"
            string += otherTableHead[index]+"\n"
            string += str(stats.iloc[statsRows,21:len(tableHead)])
            return string
getOffenseStats("UCLA")

if __name__ == "__main__":
    app.run(debug=False, port=54321)
