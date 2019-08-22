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
        self.features = ['ApplStandard', 'Cap', 'CEC Cold', 'CEC_', 'Cold Wat Cons', 'Combination', 'Conn_Mode', 'delayStartMode', 'Depth', 'DetergentType', 'Height', 'internal_heater', 'powerConsMode', 'Prog Name', 'standbyPowerUsage', 'Type', 'Width', 'Program Time']
        
    def predict(self):
        # Kindly refer ../../inferences/washing_machine.ipynb for the logic of the following code
        data = pd.DataFrame([self.specifications],columns=self.features)

        # Classify cec_cold value
        cec_cold = data.at[0, 'CEC Cold']
        if cec_cold>=0 and cec_cold<75: value = 0
        elif cec_cold>=75 and cec_cold<125: value = 1
        elif cec_cold>=125 and cec_cold<175: value = 2
        elif cec_cold>=175: value = 3
        data.at[0, 'CEC Cold'] = value
        data['CEC Cold'] = data['CEC Cold'].astype(int)

        # Classify cec value
        cec = data.at[0, 'CEC_']
        if cec<=280: value = 0
        elif cec>280 and cec<=400: value = 1
        elif cec>400 and cec<=550: value = 2
        else: value = 3
        data.at[0, 'CEC_'] = value
        data.CEC_ = data.CEC_.astype(int)

        # Classify cold_water_cons value
        cold_wat_cons = data.at[0, 'Cold Wat Cons']
        if cold_wat_cons>=0 and cold_wat_cons<50: value = 0
        elif cold_wat_cons>=50 and cold_wat_cons<80: value = 1
        elif cold_wat_cons>=80: value = 2
        data.at[0, 'Cold Wat Cons'] = value
        
        # Classify combination value
        if not data.at[0, 'Combination']:
            data.at[0, 'Combination'] = 0
        else: 
            data.at[0, 'Combination'] = 1
        data['Combination'] = data['Combination'].astype(int)

        # Classify delayStartMode value value
        if not data.at[0, 'delayStartMode']:
            data.at[0, 'delayStartMode'] = 0
        else: 
            data.at[0, 'delayStartMode'] = 1
        data['delayStartMode'] = data['delayStartMode'].astype(int)

        # Classify depth value
        depth = int(data.at[0, 'Depth'])
        if depth>=292 and depth<565: value = 0
        elif depth==565: value = 1
        elif depth>=570 and depth<700: value = 2
        elif depth>=700: value = 3
        data.at[0, 'Depth'] = value
        data.Depth = data.Depth.astype(int)

        # Classify detergentType value
        if data.at[0, 'DetergentType'] == 'Drum':
            value = 0
        else: value = 1
        data.at[0, 'DetergentType'] = value
        data.DetergentType = data.DetergentType.astype(int)

        # Classify height value
        height = int(data.at[0, 'Height'])
        if height>=515 and height<850: value = 0
        elif height==850: value = 1
        else: value = 2
        data.at[0, 'Height'] = value
        data.Height = data.Height.astype(int)

        # Classify internal_heater value
        if data.at[0, 'internal_heater']=='Yes on the warm wash program only':
            value = 0
        elif data.at[0, 'internal_heater']=='No':
            value = 1
        else: value = 2
        data.at[0, 'internal_heater'] = value
        data.internal_heater = data.internal_heater.astype(int)

        # Classify powerConsMode value
        powerConsMode = data.at[0, 'powerConsMode']   
        if powerConsMode<=0.4: value = 0
        elif powerConsMode>0.4 and powerConsMode<=0.75: value = 1
        elif powerConsMode>0.75 and powerConsMode<=1.4: value = 2
        elif powerConsMode>1.4: value = 3
        data.at[0, 'powerConsMode'] = value
        data.powerConsMode = data.powerConsMode.astype(int)

        # Extract features from program name
        program = data.at[0, 'Prog Name']
        if isinstance(program, float): return []
        if '/' in program:
            types = program.split('/')
            program = ''
            for t in types:
                program+=t+' '
        if ',' in program:
            types = program.split(',')
            program = ''
            for t in types:
                program+=t+' '
        keywords = program.split(' ')
        features = []
        for i in keywords: 
            i = i.strip()
            if i not in ['', '-']: 
                features.append(i.lower())

        if 'normal' in features: value = 0
        elif 'eco' in features: value = 1
        elif 'cotton' in features: value = 2
        else: value = 3
        data.at[0, 'Prog Name'] = value
        data['Prog Name'] = data['Prog Name'].astype(int)

        # Classify standby_power value
        standby_power = data.at[0, 'standbyPowerUsage']
        if standby_power<=0.25: value = 0
        elif standby_power>0.25 and standby_power<=0.5: value = 1
        elif standby_power>0.5 : value = 2
        data.at[0, 'standbyPowerUsage'] = value
        data.standbyPowerUsage = data.standbyPowerUsage.astype(int)

        # Classify width value
        width = int(data.at[0, 'Width'])
        if width<=565: value = 0
        elif width>=570 and width<600: value = 1
        elif width>=600: value = 2
        data.at[0, 'Width'] = value
        data.Width = data.Width.astype(int)

        # Setting these fields to their respective integer clases
        ApplStandard_types = {'AS/NZS 2040.2:2005': 0, 'AS/NZS 2040.2:2005 (Legacy)': 1, 'AS/NZS 2040.2:2000 (Legacy)': 2, 'Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2015': 3, 'Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2012': 4}
        data['ApplStandard'] = data['ApplStandard'].map(ApplStandard_types).astype(int)
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
        featureNames = {'Program Time':'Program Running Time','standbyPowerUsage':'Power usage in Standby Mode','powerConsMode':'Power Consumption in Mode','Cap':'Capacity','CEC Cold':'Comparative Energy Consumption for Cold Use','CEC_':'Comparative Energy Consumption for Warm Use','Cold Wat Cons':'Cold Water Consumption', 'Type':'Type of Appliance', 'Conn_Mode':'Connection Mode', 'delayStartMode': 'Delay Start Mode'}
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