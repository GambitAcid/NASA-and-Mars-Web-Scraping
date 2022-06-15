from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up our mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    # Finding one document from mongo db and returning it.
    mars = mongo.db.mars.find_one()
    # Passing to render_template
    return render_template("index.html", mars=mars)

# Path to /scrape
@app.route("/scrape")
def scraper():
    # Create an mars listings database
    mars = mongo.db.mars
    # Call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape_all()
    # Then we update our listings with the data that is being scraped.
    mars.update({}, mars_data, upsert=True)
    # Return a message if it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
