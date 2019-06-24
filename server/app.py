import os
from flask import Flask, render_template, request
import json
import config as config
from inferences.main import createInference
from api.dryer import predictDryer
from api.monitor import predictMonitor
from api.washing_machine import predictWashingMachine

app = Flask(__name__)
app.config.from_object(config.DevConfig)

def jsonResponse(prediction):
    info = app.config['PRODUCT_CATEGORIES'][int(prediction['category'])]
    issues = prediction['issues']
    category = prediction['category']
    inferences = createInference(category, issues)
    return json.dumps({'category': int(prediction['category']), 'info': info, 'inference':inferences})

# Serve React App
@app.route('/')
@app.route('/dryer')
@app.route('/monitor')
@app.route('/washing_machine')
def my_index():
    return render_template("index.html")

@app.route('/api/predict/dryer', methods=["POST"])
def predict_dryer():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictDryer(specifications, os.path.join(app.config['DATASET_PATH'], 'dryer.csv'))
    prediction = model.predict()
    return jsonResponse(prediction)

@app.route('/api/predict/monitor', methods=["POST"])
def predict_monitor():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictMonitor(specifications, os.path.join(app.config['DATASET_PATH'], 'monitor.csv'))
    prediction = model.predict()
    return jsonResponse(prediction)

@app.route('/api/predict/washing_machine', methods=["POST"])
def predict_washing_machine():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictWashingMachine(specifications, os.path.join(app.config['DATASET_PATH'], 'washing_machine.csv'))
    prediction = model.predict()
    return jsonResponse(prediction)
app.run(debug=True)