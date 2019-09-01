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

@app.route('/ctof')
def render_ctof():
    return render_template('ctof.html')

@app.route('/ftoc')
def render_ftoc():
    return render_template('ftoc.html')

@app.route('/mtokm')
def render_mtokm():
    return render_template('mtokm.html')

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

@app.route('/ctof_result')
def render_ctof_result():
    try:
        ctemp_result = float(request.args['cTemp'])
        ftemp_result = ctof(ctemp_result)
        return render_template('ctof_result.html', cTemp=ctemp_result, fTemp=ftemp_result)
    except ValueError:
        return "Sorry: something went wrong."

@app.route('/mtokm_result')
def render_mtokm_result():
    try:
        miledist_result = float(request.args['miledist'])
        kilodist_result = miletokm(miledist_result)
        return render_template('mtokm_result.html', miledist=miledist_result, kilodist=kilodist_result )
    except ValueError:
        return "Sorry: something went wrong."

@app.route('/testit')
def checksubredtitles():
    for submission in reddit.subreddit('ucsd').hot(limit=10):
        print(submission.url)
        print('\n')

def ftoc(ftemp):
   return (ftemp-32.0)*(5.0/9.0)
    
def ctof(ctemp):
   return (ctemp*(9.0/5.0) + 32.0) # replace with correct formula

def miletokm(miledist):
    return 1.609*miledist
    
if __name__=="__main__":
    app.run(debug=False, port=54321)
