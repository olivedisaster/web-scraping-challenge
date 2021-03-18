from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# MongoDB connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

@app.route("/")
def index():

    mars_info_dict = mongo.db.mars_info_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_info_dict=mars_info_dict)

@app.route("/scrape")
def scrape():
    mars_info_dict = mongo.db.mars_info_dict
    mars_data = scrape_mars.scrape_info()

    mongo.db.mars_info_dict.update({}, mars_info_dict, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)