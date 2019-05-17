import pymongo
import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.marsDB
collection = db.mars

# mars_data = list(db.mars.find())

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    mars_data = db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)
# def index():
#     return render_template('index.html', mars_data=mars_data)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    mars = db.mars
    mars_data = scrape_mars.scrape()
    db.mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

    
if __name__ == '__main__':
    app.run(debug=True)