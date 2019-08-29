from flask import Flask
app = Flask(__name__)


@app.route('/addstring/<a>/<b>/<c>')

def addstring(a,b,c):
    first = a
    second = b
    third = c

    try:
        return "first is " + first + " second is " + second + " third is " + third
    except ValueError:
        return "That's an unfortunate input"
if __name__ == "__main__":
    app.run(port=5306)
