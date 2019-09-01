import os
from flask import Flask, url_for, render_template, request
import praw

app = Flask(__name__)

reddit = praw.Reddit(client_id='Q9UV2ZsbXF0K3w',
                     client_secret='DSh_JRQi563PWGayN1BHWmV89M8',
                     redirect_uri='http://secret-cove-59920.herokuapp.com/',
                     user_agent='SaltyGhio')

@app.route('/')
def render_main():
    return render_template('home.html')

@app.route('/ftoc')
def render_ftoc():
    return render_template('ftoc.html')

@app.route('/testit')
def render_testit():
    return render_template('testit.html')

@app.route('/about')
def render_about():
    return render_template('about.html')
    
@app.route('/ftoc_result')
def render_ftoc_result():
    try:
        ftemp_result = float(request.args['fTemp'])
        ctemp_result = ftoc(ftemp_result)
        return render_template('ftoc_result.html', fTemp=ftemp_result, cTemp=ctemp_result)
    except ValueError:
        return "Sorry: something went wrong."

@app.route('/testit_result')
def checksubredtitles():
    for submission in reddit.subreddit('ucsd').hot(limit=1):
        firstprint = print(submission.title)
        return render_template('testit_result.html', testresult = firstprint)


def ftoc(ftemp):
   return (ftemp-32.0)*(5.0/9.0)
    
def ctof(ctemp):
   return (ctemp*(9.0/5.0) + 32.0) # replace with correct formula
    
if __name__=="__main__":
    app.run(debug=False, port=54321)
