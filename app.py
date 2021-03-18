from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

#flask setup
from flask import Flask, render_template, redirect
app = Flask(__name__)

# app.config['MONGO_URI'] = "mongodb://localhost:27017/mission_to_mars"
# mongo = PyMongo(app)
# MongoDB connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def home():

    #Find one record of data from mongo database
    mars_data = mongo.db.marscollection.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_data)

#Route that will trigger scrape function
@app.route("/scrape")
def scrape():
    
    #Run the scrape function
    mars_dict = scrape_mars.scrape_info()

    #Update the mongo database using update and upsert=True
    mongo.db.marscollection.update({}, mars_dict, upsert=True)

    #Redirect back to home page
    return redirect("/")

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), 
        port=int(os.getenv('PORT', 4444)))
    app.run(debug=True)