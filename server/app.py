import os
from flask import Flask, render_template, request
import json
from api.dryer import predictDryer
from api.monitor import predictMonitor

app = Flask(__name__)
app.secret_key = 'rishiisapain'
categories = ['Poor: The appliance seems to be using up a lot of energy',
                  'OK: The appliance seems to be operating just fine', 'Good: The appliance is in good condition']

# Serve React App
@app.route('/')
def my_index():
    return render_template("index.html")

@app.route('/api/predict/dryer', methods=["POST"])
def predict_dryer():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictDryer(
        specifications, os.path.abspath('../datasets/dryer.csv'))
    prediction = model.predict()
    return json.dumps({'category': int(prediction), 'info': categories[prediction]})

@app.route('/api/predict/monitor', methods=["POST"])
def predict_monitor():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictMonitor(
        specifications, os.path.abspath('../datasets/monitor.csv'))
    prediction = model.predict()
    return json.dumps({'category': int(prediction), 'info': categories[prediction]})

app.run(debug=True)