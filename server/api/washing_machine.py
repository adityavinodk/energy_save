import os
import numpy as np
import pandas as pd
import json
import joblib

class predictWashingMachine():

    def __init__(self, specifications, weights_path, data_info_path):
        self.specifications = specifications
        self.weights_path = weights_path
        self.data_info_path = data_info_path
        self.features = ['Cap', 'CEC_', 'Conn_Mode', 'delayStartMode', 'DetergentType', 'internal_heater', 'standbyPowerUsage', 'Type', 'Program Time']
        
    def predict(self):
        # Kindly refer ../../inferences/washing_machine.ipynb for the logic of the following code
        data = pd.DataFrame([self.specifications],columns=self.features)

        # Classify cec value
        cec = data.at[0, 'CEC_']
        if cec<=280: value = 0
        elif cec>280 and cec<=400: value = 1
        elif cec>400 and cec<=550: value = 2
        else: value = 3
        data.at[0, 'CEC_'] = value
        data.CEC_ = data.CEC_.astype(int)

        # Classify delayStartMode value value
        if not data.at[0, 'delayStartMode']:
            data.at[0, 'delayStartMode'] = 0
        else: 
            data.at[0, 'delayStartMode'] = 1
        data['delayStartMode'] = data['delayStartMode'].astype(int)

        # Classify detergentType value
        if data.at[0, 'DetergentType'] == 'Drum':
            value = 0
        else: value = 1
        data.at[0, 'DetergentType'] = value
        data.DetergentType = data.DetergentType.astype(int)

        # Classify internal_heater value
        if data.at[0, 'internal_heater']=='Yes on the warm wash program only':
            value = 0
        elif data.at[0, 'internal_heater']=='No':
            value = 1
        else: value = 2
        data.at[0, 'internal_heater'] = value
        data.internal_heater = data.internal_heater.astype(int)

        # Classify standby_power value
        standby_power = data.at[0, 'standbyPowerUsage']
        if standby_power<=0.25: value = 0
        elif standby_power>0.25 and standby_power<=0.5: value = 1
        elif standby_power>0.5 : value = 2
        data.at[0, 'standbyPowerUsage'] = value
        data.standbyPowerUsage = data.standbyPowerUsage.astype(int)

        # Setting these fields to their respective integer clases
        data['Conn_Mode'] = data['Conn_Mode'].map({'Dual':0, 'Cold': 1}).astype(int)
        data['Type'] = data['Type'].map({'Drum':0, 'Non-Drum': 1}).astype(int)

        # Classify cap value
        cap = data.at[0, 'Cap']
        if cap<7: value = 0
        elif cap>=7 and cap<8: value = 1
        elif cap>=8 and cap<9: value = 2
        else: value = 3
        data.at[0, 'Cap'] = value
        data.Cap = data.Cap.astype(int)

        # Classify program time value
        time = data.at[0, 'Program Time']
        if time<=125: value = 0
        elif time>125 and time<250: value = 1
        else: value = 2
        data.at[0, 'Program Time'] = value
        data['Program Time'] = data['Program Time'].astype(int)

        model = joblib.load(self.weights_path)
        category = model.predict(data)[0]
        return self.inferenceBuilder(category, data)

    def inferenceBuilder(self, category, data):
        # This functions checks if the problematic features values are contributing to a low star rating, if they are they are considered to be issues
        inferences = {}
        file = open(self.data_info_path, 'r')
        full_data = json.load(file)
        featureNames = {'Program Time':'Program Running Time','standbyPowerUsage':'Power usage in Standby Mode','Cap':'Capacity','CEC_':'Comparative Energy Consumption for Warm Use','Type':'Type of Appliance', 'Conn_Mode':'Connection Mode', 'delayStartMode': 'Delay Start Mode'}
        if category==0: starRange = "Less than or equal to 2 stars on 10"
        elif category==1: starRange = "Greater than 2 but lesser than 4 stars on 10"
        else: starRange = "More than or equal to 4 stars on 10"
        if category==0: 
            starRange = "Less than or equal to 4 stars on 10"
            for problemFeature in full_data['specifications_for_0']:
                if data.at[0,problemFeature] in full_data['specifications_for_0'][problemFeature]:
                    form = data.at[0,problemFeature]
                    print(problemFeature, form)
                    inferences[featureNames[problemFeature]] = full_data[problemFeature][str(form)]
        elif category==1: 
            starRange = "4-6 stars on 10"
            for problemFeature in full_data['specifications_for_1']:
                if data.at[0,problemFeature] in full_data['specifications_for_1'][problemFeature]:
                    form = data.at[0,problemFeature]
                    inferences[featureNames[problemFeature]] = full_data[problemFeature][str(form)]
        else: 
            starRange = "More than 6 stars on 10"
            for feature in full_data['specifications_for_2']:
                if data.at[0,feature] in full_data['specifications_for_2'][feature]:
                    form = data.at[0, feature]
                    inferences[featureNames[feature]] = full_data[feature][str(form)]
        ideal_energy_category = full_data['specifications_for_2']['CEC_'][0]
        responseData = {'category':category, 'inferences': inferences, 'starRange': starRange, 'idealEnergy': full_data['CEC_'][str(ideal_energy_category)]}
        print(responseData)
        return responseData