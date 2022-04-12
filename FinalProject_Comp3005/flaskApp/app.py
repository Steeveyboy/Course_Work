from flask import Flask, render_template, request, redirect
import dbManager

app = Flask(__name__)

dbm = dbManager.dbManager()

@app.route("/")
def landing():
    landingArt = dbm.get_by_title("Ocean Life")
    return render_template("index.html", results=[])

@app.route("/random")
def random():
    landingArt = dbm.get_random()
    print(landingArt)
    owners = dbm.get_owners(landingArt["Title"])
    results = {"Artwork": landingArt, "owners": owners}
    return render_template("ArtTemplate.html", results=results)

@app.route("/searchArt", methods=["POST"])
def getPieces():
    results = {"page": "searchArt"}
    if request.method == "POST":
        artList = dbm.get_many_by_attr("Artwork", request.form['searchText'])
        results["list"] = artList
        return render_template("index.html", results=results)
    else:
        return render_template("index.html", results=[])

@app.route("/searchGallery", methods=["POST"])
def getGalleries():
    results = {"page": "searchGallery"}
    if request.method == "POST":
        galleryList = dbm.get_many_by_attr("Gallery", request.form['searchText'])
        results["list"] = galleryList
        return render_template("index.html", results=results)
    else:
        return render_template("index.html", results=[])

@app.route("/searchGallery/<name>", methods=["GET"])
def viewGallery(name):
    artList = dbm.get_gallery_art(name)
    return render_template("GalleryTemplate.html", results=artList)

@app.route("/searchArt/<title>", methods=["GET"])
def viewPiece(title):
    landingArt = dbm.get_by_title(title)
    owners = dbm.get_owners(title)
    results = {"Artwork": landingArt, "owners": owners}
    return render_template("ArtTemplate.html", results=results)

@app.route("/user/<patron_id>", methods=["GET", "POST"])
def viewPatronCollection(patron_id):
    if(requests.method == "POST")
    contracts = dbm.get_patron_collection(patron_id)
    return render_template("PatronTemplate.html", results=contracts)

