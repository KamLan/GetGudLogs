from flask import (
    Flask,
    flash,
    render_template,
    jsonify,
    request
)
import requests
import json
from flask_pymongo import PyMongo
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateField

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Create themongoDB instance
app.config['MONGO_DBNAME'] = 'gitgudlogs'
app.config["MONGO_URI"] = "mongodb://localhost:32768/gitgudlogs"
mongo = PyMongo(app)

#Forms checkers declaration 
class LogForm(Form):
  date = DateField('date:', validators=[validators.required()])
  category = TextField('category:', validators=[validators.required()])
  improvement = TextField('improvement:', validators=[validators.required()])
class TipForm(Form):
  date = DateField('date:', validators=[validators.required()])
  category = TextField('category:', validators=[validators.required()])
  tip = TextField('tip:', validators=[validators.required()])


# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')

#route for random logs or tips
@app.route('/rand')
def random():
    return render_template('random.html')

#route to log in your improvements
@app.route('/sLogs', methods=['GET', 'POST'])
def save_log():
  form = LogForm(request.form)
  if request.method == 'POST':
    date=request.form['date']
    category=request.form['category']
    improvement=request.form['improvement']
  if form.validate():
    # Save the log here.
    log = mongo.db.logs.insert_one({'date': date, 'category': category, 'improvement': improvement})
    flash('Thanks for this log about ' + category)
    return render_template('sLog.html', form=form)

  else:
    flash('Error: All the form fields are required. ')
    return render_template('sLog.html', form=form)

#route to see the daily logs
@app.route('/dLogs')
def daily_logs():
  return render_template('dLog.html')


#route to see every logs in the database
@app.route('/aLogs')
def all_logs():
    logs = list(mongo.db.logs.find())
    return render_template('allLogs.html', logs=logs)


#route to log in your improvements
@app.route('/sTips', methods=['GET', 'POST'])
def save_tip():
  form = TipForm(request.form)
  if request.method == 'POST':
    date=request.form['date']
    category=request.form['category']
    tip=request.form['tip']
  if form.validate():
    # Save the tip here.
    log = mongo.db.tips.insert_one({'date': date, 'category': category, 'tip': tip})
    flash('Thanks for this new tip about ' + category)
    return render_template('sTip.html', form=form)

  else:
    flash('Error: All the form fields are required. ')
    return render_template('sTip.html', form=form)

#route to see the daily tips
@app.route('/dTips')
def daily_tips():
    return render_template('dailyTips.html')

#route to see all the tips in the database
@app.route('/aTips')
def all_tips():
    tips = list(mongo.db.tips.find())
    return render_template('allTips.html', tips=tips)

#route to get all logs from the base and display it in json
@app.route('/getLogs', methods=['GET'])
def get_logs():
    log = mongo.db.logs
    output = []
    for l in log.find():
        output.append(
            {'date': l['date'], 'category': l['category'], 'improvement': l['improvement']})
    return jsonify({'result': output})


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
