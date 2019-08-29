import os
import numpy as np
import pandas as pd
import joblib
import json

class predictDryer():

    def __init__(self, specifications, weights_path, data_info_path):
        self.specifications = specifications
        self.weights_path = weights_path
        self.data_info_path = data_info_path
        self.features = ['Combination','Control','New CEC','Prog Time','Type']

    def predict(self):
        # Kindly refer ../../inferences/dryer.ipynb for the logic of the following code
        data = pd.DataFrame([self.specifications],columns=self.features)

        # Classify program time value
        time = data.at[0, 'Prog Time']
        if time >= 50 and time <= 115: value = 0
        elif time > 115 and time <= 150: value = 1
        elif time > 150 and time <= 175: value = 2
        elif time > 175 and time <= 200: value = 3
        elif time > 200 and time <= 215: value = 4
        elif time > 215 and time <= 235: value = 5
        elif time > 235 and time <= 275: value = 6
        elif time > 275 and time <= 300: value = 7
        elif time > 300: value = 8
        data.at[0, 'Prog Time'] = value
        data['Prog Time'] = data['Prog Time'].astype(int)

        # Converting CEC into smaller integer classes using feature scaling
        cec = data.at[0, 'New CEC']
        if cec > 21.89 and cec <= 130.14: value = 0
        elif cec > 130.14 and cec <= 162.61: value = 1
        elif cec > 162.61 and cec <= 173.44: value = 2
        elif cec > 173.44 and cec <= 216.74: value = 3
        elif cec > 216.74 and cec <= 238.39: value = 4
        elif cec > 238.39 and cec <= 303.34: value = 5
        elif cec > 303.34 and cec <= 346.64: value = 6
        elif cec > 346.64 and cec <= 454.89: value = 7
        else: value = 8
        data.at[0, 'New CEC'] = value
        
        # map boolean objects to int
        data['Combination'] = data['Combination'].map({False: 0, True: 1}).astype(int)
        data['Control'] = data['Control'].map({'Timer': 0, 'Autosensing': 1, 'Manual': 2}).astype(int)
        data['Type'] = data['Type'].map({'Condenser': 0, 'Vented': 1}).astype(int)

        model = joblib.load(self.weights_path)
        category = model.predict(data)[0]
        return self.inferenceBuilder(category, data)

    def inferenceBuilder(self, category, data):
        # This functions checks if the problematic features values are contributing to a low star rating, if they are they are considered to be issues
        inferences = {}
        file = open(self.data_info_path, 'r')
        full_data = json.load(file)
        featureNames = {'New CEC':'Comparative Energy Consumption', 'Prog Time':'Usage Time', 'Type':'Type of appliance'}
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
        ideal_energy_category = full_data['specifications_for_2']['New CEC'][0]
        responseData = {'category':category, 'inferences': inferences, 'starRange': starRange, 'idealEnergy': full_data['New CEC'][str(ideal_energy_category)]}
        print(responseData)
        return responseData