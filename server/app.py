import os
from flask import Flask, render_template, request
import json
import config as config
from api.dryer import predictDryer
from api.monitor import predictMonitor

app = Flask(__name__)
app.config.from_object(config.DevConfig)

# Serve React App
@app.route('/')
def my_index():
    return render_template("index.html")

@app.route('/api/predict/dryer', methods=["POST"])
def predict_dryer():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictDryer(
        specifications, os.path.join(app.config['DATASET_PATH'], 'dryer.csv'))
    prediction = model.predict()
    return json.dumps({'category': int(prediction), 'info': app.config['PRODUCT_CATEGORIES'][prediction]})

@app.route('/api/predict/monitor', methods=["POST"])
def predict_monitor():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictMonitor(
        specifications, os.path.join(app.config['DATASET_PATH'], 'monitor.csv'))
    prediction = model.predict()
    return json.dumps({'category': int(prediction), 'info': app.config['PRODUCT_CATEGORIES'][prediction]})

app.run(debug=True)