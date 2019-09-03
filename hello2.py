import os
from flask import Flask, url_for, render_template, request
import praw

app = Flask(__name__)

reddit = praw.Reddit(client_id='Q9UV2ZsbXF0K3w',
                     client_secret='DSh_JRQi563PWGayN1BHWmV89M8',
                     redirect_uri='http://secret-cove-59920.herokuapp.com/testit_result',
                     user_agent='SaltyGhio')

@app.route('/')
def render_main():
    return render_template('home.html')

@app.route('/testit')
def render_testit():
    return render_template('testit.html')

@app.route('/about')
def render_about():
    return render_template('about.html')

@app.route('/testit_result')
def checksubredtitles():
    for submission in reddit.subreddit('ucsd').hot(limit=1):
        firstprint = submission.title
        secondprint = reddit.user.me()
        
        return render_template('testit_result.html', whothetoken = firstprint, whotheuser=secondprint)
    
if __name__=="__main__":
    app.run(debug=False, port=54321)
