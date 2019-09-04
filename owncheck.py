from flask import Flask, abort, request, url_for, render_template
from uuid import uuid4
import os
import requests
import requests.auth
import urllib
import urllib.parse
import json

CLIENT_ID = "Q9UV2ZsbXF0K3w"
CLIENT_SECRET = "DSh_JRQi563PWGayN1BHWmV89M8"
REDIRECT_URI = "http://localhost:54321/testit_callback"

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

@app.route('/testit')
#This part returns a text with link to authorize
#def homepage():
#    text = '<a href ="%s">Authenticate with Reddit</a>'
#    return text % make_authorization_url()


def make_authorization_url():
    #uuid = universal unique identifier
    #Creates a unique string for each authorization request
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
                    "response_type": "code",
                    "redirect_uri": REDIRECT_URI,
                    "duration": "permanent",
                    "scope": "identity " + "save " + "history",
                    "state": state}
    url = "https://reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    #Sends the data to the testit webpage with auth storing the authorize url
    return render_template('testit.html', auth = url)    

def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/testit_callback')
def testit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    
    return "Your reddit username is: %s" %get_username(access_token)

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

if __name__ == "__main__":
    app.run(debug=False, port=54321)