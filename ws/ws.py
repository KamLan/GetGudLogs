from flask import (
    Flask,
    render_template,
    jsonify,
    request
)
import requests
import json
from flask_pymongo import PyMongo

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create themongoDB instance
app.config['MONGO_DBNAME'] = 'gitgudlogs'
app.config["MONGO_URI"] = "mongodb://localhost:32768/gitgudlogs"
mongo = PyMongo(app)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/r')
def random():
    return render_template('random.html')

@app.route('/dailyLog')
def log():
    return render_template('log.html')

@app.route('/aLogs')
def all_logs():
  logs = list(mongo.db.logs.find())
  return render_template('allLogs.html', logs = logs)

@app.route('/getLogs', methods=['GET'])
def get_logs():
  log = mongo.db.logs
  output = []
  for l in log.find():
    output.append({'date' : l['date'], 'category' : l['category'], 'improvement' : l['improvement']})
  return jsonify({'result' : output})

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)