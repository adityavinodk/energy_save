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
        self.features = ['ApplStandard','Cap','Combination','Control','Depth','Height','New CEC','Prog Name','Prog Time','Type','Width']

    def predict(self):
        # Kindly refer ../../inferences/dryer.ipynb for the logic of the following code
        data = pd.DataFrame([self.specifications],columns=self.features)

        # Classify depth value
        depth = int(data.at[0, 'Depth'])
        if depth >= 60 and depth <= 550: value = 0
        elif depth == 555: value = 1
        elif depth >= 560 and depth <= 700: value = 2
        else: value = 3
        data.at[0, 'Depth'] = value
        data['Depth'] = data['Depth'].astype(int)

        # Classify height value
        height = int(data.at[0, 'Height'])
        if height >= 85 and height <= 550: value = 0
        elif height == 555: value = 1
        elif height >= 560 and height < 850: value = 2
        elif height == 850: value = 3
        else: value = 4
        data.at[0, 'Height'] = value
        data['Height'] = data['Height'].astype(int)
        
        # Classify width value
        width = int(data.at[0, 'Width'])
        if width >= 60 and width < 595: value = 0
        elif width == 595: value = 1
        elif width >= 600 and width < 850: value = 2
        data.at[0, 'Width'] = value
        data['Width'] = data['Width'].astype(int)

        # Classify capacity value
        capacity = int(data.at[0, 'Cap'])
        if capacity >= 1 and capacity <= 6: value = 0
        elif capacity >= 7 and capacity <= 8: value = 1
        else: value = 2
        data.at[0, 'Cap'] = value
        data['Cap'] = data['Cap'].astype(int)

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
        data['New CEC'] = data['New CEC'].astype(int)
        cec_range = data['New CEC'].max() - data['New CEC'].min()
        cec_mean = data['New CEC'].mean()
        cec = (data.at[0, 'New CEC'] - cec_mean)/cec_range
        if cec > -0.5 and cec <= -0.25: value = 0
        elif cec > -0.25 and cec <= -0.175: value = 1
        elif cec > -0.175 and cec <= -0.15: value = 2
        elif cec > -0.15 and cec <= -0.05: value = 3
        elif cec > -0.05 and cec <= 0: value = 4
        elif cec > 0 and cec <= 0.15: value = 5
        elif cec > 0.15 and cec <= 0.25: value = 6
        elif cec > 0.25 and cec <= 0.5: value = 7
        data.at[0, 'New CEC'] = value

        # We shall extract the features fro the Program Name and seperate them into different classes
        program = data.at[0, 'Prog Name']
        if '/' in program:
            types = program.split('/')
            program = ''
            for t in types:
                program += t+' '
        if ',' in program:
            types = program.split(',')
            program = ''
            for t in types:
                program += t+' '
        keywords = program.split(' ')
        features = []
        for i in keywords:
            i = i.strip()
            if i not in ['', '-']:
                features.append(i.lower())

        if 'dry' in features and 'heat' in features: 
            data.at[0, 'Prog Name'] = 0
        elif 'heat' in features:
            data.at[0, 'Prog Name'] = 1
        elif 'dry' in features:
            data.at[0, 'Prog Name'] = 2
        else:
            data.at[0, 'Prog Name'] = 3
        data['Prog Name'] = data['Prog Name'].astype(int)
        
        # map boolean objects to int
        ApplStandard_types = {'AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)': 0, 'Greenhouse and Energy Minimum Standards (Rotary Clothes Dryers) Determination 2012': 1,
                              'Greenhouse and Energy Minimum Standards (Rotary Clothes Dryers) Determination 2015': 2, 'AS/NZS 2442.2:2000/Amdt 2:2007': 3}
        data['ApplStandard'] = data['ApplStandard'].map(ApplStandard_types).astype(int)
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
        featureNames = {'New CEC':'Comparative Energy Consumption', 'Prog Time':'Usage Time', 'Type':'Type of appliance', 'Cap':'Capacity of appliance', 'Combination': 'Multi-Purpose Appliance'}
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