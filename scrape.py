from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
# mars = client.marsDB.marsInfo.find()

@app.route('/')
def index():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    mars = client.marsDB.marsInfo.find()
    mars = mars
    print (mars)
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    mars = client.marsDB.marsInfo.find()
    mars = mars
    data = scrape_mars.scrape()
    print (mars)
    print (data)
    mars.update(
        {},
        data,
        upsert = True
    )
    return redirect('http://localhost:5000', code=302)

if __name__ == "__main__":
    app.run(debug=True)