from flask import Flask, render_template
import dbManager

app = Flask(__name__)

dbm = dbManager.dbManager()

@app.route("/")
def landing():
    # return "<h1>Technical Difficulties</h1>"
    landingArt = dbm.get_random()
    return render_template("index.html", Artwork=landingArt)
    