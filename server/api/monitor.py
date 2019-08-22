import os
import numpy as np
import pandas as pd
import json
import joblib

class predictMonitor():

    def __init__(self, specifications, weights_path, data_info_path):
        self.specifications = specifications
        self.weights_path = weights_path
        self.data_info_path = data_info_path
        self.features = ['Screen Technology', 'Comparative Energy Consumption', 'Active Standby Power']

    def predict(self):
        # Kindly refer ../../inferences/monitor.ipynb for the logic of the following code
        data = pd.DataFrame([self.specifications],columns=self.features)

        # Mapping Comparitive Energy Consumption to Integer Classes
        comp_energy = data.at[0, 'Comparative Energy Consumption']
        if comp_energy<=50: value = 0
        elif comp_energy>50 and comp_energy<=60: value = 1
        elif comp_energy>60 and comp_energy<=67: value = 2
        elif comp_energy>67 and comp_energy<=75: value = 3
        elif comp_energy>75 and comp_energy<=82: value = 4
        elif comp_energy>82 and comp_energy<=92: value = 5
        elif comp_energy>92 and comp_energy<=102: value = 6
        elif comp_energy>102 and comp_energy<=112: value = 7
        elif comp_energy>112 and comp_energy<=125: value = 8
        elif comp_energy>125 and comp_energy<=150: value = 9
        elif comp_energy>150 and comp_energy<=180: value = 10
        else: value = 11
        data.at[0, 'Comparative Energy Consumption'] = value
        data['Comparative Energy Consumption'] = data['Comparative Energy Consumption'].astype(int)

        # Mapping Screen Technology to Integer classes
        data['Screen Technology'] = data['Screen Technology'].map({'LCD (LED)': 0, 'LCD': 1, 'OLED': 2}).astype(int)

        # Mapping Active Standby Power to Integer classes
        standby_power = data.at[0, 'Active Standby Power']
        if standby_power<=0.2: value = 0
        elif standby_power>0.2 and standby_power<=0.24: value = 1
        elif standby_power>0.24 and standby_power<=0.28: value = 2
        elif standby_power>0.28 and standby_power<=0.32: value = 3
        elif standby_power>0.32 and standby_power<=0.39: value = 4
        else: value = 5
        data.at[0, 'Active Standby Power'] = value
        data['Active Standby Power'] = data['Active Standby Power'].astype(int)

        model = joblib.load(self.weights_path)
        category = model.predict(data)[0]
        return self.inferenceBuilder(category, data)
    
    def inferenceBuilder(self, category, data):
        # This functions checks if the problematic features values are contributing to a low star rating, if they are they are considered to be inferences
        inferences = {}
        file = open(self.data_info_path, 'r')
        full_data = json.load(file)
        featureNames = {'Screen Technology': 'Technology running the screen', 'Comparative Energy Consumption': 'Comparative Energy Consumption', 'Active Standby Power': 'Power used in Standby Mode'}
        if category==0: 
            starRange = "Less than or equal to 4 stars on 10"
            for problemFeature in full_data['specifications_for_0']:
                if data.at[0,problemFeature] in full_data['specifications_for_0'][problemFeature]:
                    form = data.at[0,problemFeature]
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
        ideal_energy_category = full_data['specifications_for_2']['Comparative Energy Consumption'][0]
        responseData = {'category':category, 'inferences': inferences, 'starRange': starRange, 'idealEnergy': full_data['Comparative Energy Consumption'][str(ideal_energy_category)]}
        print(responseData)
        return responseData