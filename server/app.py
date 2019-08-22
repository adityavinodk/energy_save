import os
from flask import Flask, render_template, request
import json
import config as config
from inferences.main import createInference, createTipLinks
from api.dryer import predictDryer
from api.monitor import predictMonitor
from api.washing_machine import predictWashingMachine

app = Flask(__name__)
app.config.from_object(config.DevConfig)

def jsonResponse(prediction, appliance):
    info = app.config['PRODUCT_CATEGORIES'][int(prediction['category'])]
    correlatedParameters = prediction['inferences']
    category = prediction['category']
    starRange = prediction['starRange']
    links = createTipLinks(appliance)
    response = createInference(category, correlatedParameters)
    return json.dumps({'appliance': appliance, 'category': int(prediction['category']), 'info': info, 'correlatedParameters': correlatedParameters, 'text':response, 'starRange':starRange, 'idealEnergy': prediction['idealEnergy'], 'links': links})

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
    model = predictDryer(specifications, os.path.join(app.config['WEIGHTS_PATH'], 'dryer_weight.sav'), os.path.join(app.config['DATA_INFO_PATH'], 'dryer.json'))
    prediction = model.predict()
    return jsonResponse(prediction, 'Dryer')

@app.route('/api/predict/monitor', methods=["POST"])
def predict_monitor():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictMonitor(specifications, os.path.join(app.config['WEIGHTS_PATH'], 'monitor_weight.sav'), os.path.join(app.config['DATA_INFO_PATH'], 'monitor.json'))
    prediction = model.predict()
    return jsonResponse(prediction, 'Monitor')

@app.route('/api/predict/washing_machine', methods=["POST"])
def predict_washing_machine():
    req_data = request.get_json()
    specifications = req_data['specifications']
    model = predictWashingMachine(specifications, os.path.join(app.config['WEIGHTS_PATH'], 'washing_machine_weight.sav'), os.path.join(app.config['DATA_INFO_PATH'], 'washing_machine.json'))
    prediction = model.predict()
    return jsonResponse(prediction, 'Washing Machine')

app.run(debug=True)