from flask import Flask, jsonify
from scraper import login_and_scrape_attendance

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = login_and_scrape_attendance()
    return jsonify(data)

@app.route('/')
def home():
    return open('templates/index.html').read()

if __name__ == '__main__':
    app.run(debug=True)
