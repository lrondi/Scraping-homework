import pymongo
import scrape_mars
from flask import Flask, render_template, redirect

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_dataDB
collection = db.mars_data

mars_data = list(db.mars_data.find())

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    return render_template('index.html', mars_data=mars_data)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    db.mars_data.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run(debug=True)