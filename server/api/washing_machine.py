import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

class predictWashingMachine():

    def __init__(self, specifications, dataset_path):
        self.specifications = specifications
        self.dataset_path = dataset_path
        # Adding problematic features
        self.problemFeatures = ['Program Time', 'standbyPowerUsage', 'powerConsMode', 'Cap', 'CEC Cold', 'CEC_', 'Cold Wat Cons']
        self.booleanFeatures = ['Type', 'delayStartMode', 'Conn_Mode']

    def predict(self):
        # Kindly refer ../../inferences/washing_machine.ipynb for the logic of the following code
        # specifications = ['AS/NZS 2040.2:2005', 'WHIRLPOOL', 7, 150, 400, 100, True, 'Dual', 'India', True, 565, 'Non Drum', 850, 'No', 0.4, 'normal', 0.45, 'Drum', 600, 120]

        # order_of_training_data = ['ApplStandard', 'Brand', 'Cap', 'CEC Cold', 'CEC_', 'Cold Water Cons', 'Combination', 'Conn_Mode', 'Country', 'delayStartMode', 'Depth', 'DetergentType', 'Height', 'internal_heater', 'powerConsMode', 'Prog Name', 'standbyPowerUsage', 'Type', 'Width', 'Program Time']
        specifications = self.specifications
        dataset_path = self.dataset_path
        
        data = pd.read_csv(dataset_path)
        columns = ['Cold Prog', 'Family Name', 'Tot Wat Cons', 'Loading', 'Model No', 'WEI', 'Hot Water (L)', 'postProgenergy', 'New SRI', 'Registration Number', 'MachineAction', 'Hot Wat Cons', 'Test Prog Time', 'Cold Water (L)', 'N-Standard', 'Sold_in', 'Submit_ID', 'GrandDate', 'SubmitStatus', 'Product Class', 'Product Website', 'Star Rating (old)', 'Star Image Large', 'ExpDate', 'Star Image Small', 'Availability Status', 'Representative Brand URL']
        data.drop(columns, axis=1, inplace=True)

        # Converting New Star to different classes
        for index, rows in data.iterrows():
            star = data.at[index, 'New Star']
            if star<=2: value = 0
            elif star>2 and star<4: value = 1
            else: value = 2
            data.at[index, 'New Star'] = value
        data['New Star'] = data['New Star'].astype(int)

        # Setting train_y as New Star column
        train_y = data['New Star']
        data.drop('New Star', axis=1, inplace=True)

        # Concatenating the dataframe with the row to predict
        df2 = pd.DataFrame([specifications],columns=data.columns.values)
        data = pd.concat([data,df2], ignore_index = True)

        # Firstly we shall combine Brand and Country into a single column
        Brand_Country = []
        for index, row in data.iterrows():
            if len(row['Country']) > 1:
                Brand_Country.append((row['Brand'][:2] + row['Country'][0][:1] + row['Country'][1][:1]).upper())
            else:
                Brand_Country.append((row['Brand'][:2] + row['Country'][0][:1]).upper())
        data['Brand_Country'] = Brand_Country

        # Setting the Value of CEC Cold
        mode_cec_cold_overall = data['CEC Cold'].value_counts().index[1]
        mean = data['CEC Cold'].mean()
        std = data['CEC Cold'].std()
        null_count = data["CEC Cold"].isnull().sum()
        null_random = np.random.randint(mean - std, mean + std, size=null_count)
        data['CEC Cold'][np.isnan(data['CEC Cold'])] = null_random
        data['CEC Cold'] = data['CEC Cold'].astype(int)
        for index, row in data.iterrows():
            cec_cold = data.at[index, 'CEC Cold']
            if cec_cold>=0 and cec_cold<75: value = 0
            elif cec_cold>=75 and cec_cold<125: value = 1
            elif cec_cold>=125 and cec_cold<175: value = 2
            elif cec_cold>=175: value = 3
            data.at[index, 'CEC Cold'] = value
        data['CEC Cold'] = data['CEC Cold'].astype(int)

        # Setting the value of CEC Warm wash
        for index, rows in data.iterrows():
            cec = data.at[index, 'CEC_']
            if cec<=280: value = 0
            elif cec>280 and cec<=400: value = 1
            elif cec>400 and cec<=550: value = 2
            else: value = 3
            data.at[index, 'CEC_'] = value
        data.CEC_ = data.CEC_.astype(int)

        # Setting the value of Cold Water Consumed
        cold_water_cons_mode = data['Cold Wat Cons'].value_counts().index[1]
        mean = data['Cold Wat Cons'].mean()
        std = data['Cold Wat Cons'].std()
        null_count = data['Cold Wat Cons'].isnull().sum()
        null_random = np.random.randint(mean - std, mean + std, size=null_count)
        data['Cold Wat Cons'][np.isnan(data['Cold Wat Cons'])] = null_random
        data['Cold Wat Cons'] = data['Cold Wat Cons'].astype(int)
        for index, row in data.iterrows():
            cold_wat_cons = data.at[index, 'Cold Wat Cons']
            if cold_wat_cons>=0 and cold_wat_cons<50: value = 0
            elif cold_wat_cons>=50 and cold_wat_cons<80: value = 1
            elif cold_wat_cons>=80: value = 2
            data.at[index, 'Cold Wat Cons'] = value
        
        # Setting the type of Combination
        combination_mode = data.Combination.value_counts().index[0]
        data.Combination = data.Combination.fillna(0)
        for index, row in data.iterrows():
            if not data.at[index, 'Combination']:
                data.at[index, 'Combination'] = 0
            else: 
                data.at[index, 'Combination'] = 1
        data['Combination'] = data['Combination'].astype(int)

        # Setting type of delayStartMode
        delayStart_mode = data.delayStartMode.value_counts().index[0]
        data.delayStartMode = data.delayStartMode.fillna(0)
        for index, row in data.iterrows():
            if not data.at[index, 'delayStartMode']:
                data.at[index, 'delayStartMode'] = 0
            else: 
                data.at[index, 'delayStartMode'] = 1
        data['delayStartMode'] = data['delayStartMode'].astype(int)

        # Setting value of depth
        depth_mode = data['Depth'].value_counts().index[0]
        data.Depth = data.Depth.fillna(0)
        for index, row in data.iterrows():
            if int(data.at[index, 'Depth']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country']==row['Brand_Country']]['Depth'].mode().values[0])
                country_mode = int(data.loc[data['Country']==row['Country']]['Depth'].mode().values[0])
                if brand_country_mode!=0:
                    depth = brand_country_mode
                elif country_mode!=0:
                    depth = country_mode
                else: 
                    depth = depth_mode
            else: 
                depth = int(data.at[index, 'Depth'])
            
            if depth>=292 and depth<565: value = 0
            elif depth==565: value = 1
            elif depth>=570 and depth<700: value = 2
            elif depth>=700: value = 3
                
            data.at[index, 'Depth'] = value
        data.Depth = data.Depth.astype(int)

        # Setting type of Detergent Type
        mode_detergentType = data.DetergentType.value_counts().index[0]
        data.DetergentType = data.DetergentType.fillna(mode_detergentType)
        for index, row in data.iterrows():
            if data.at[index, 'DetergentType'] == 'Drum':
                value = 0
            else: value = 1
            data.at[index, 'DetergentType'] = value
        data.DetergentType = data.DetergentType.astype(int)

        # Setting value of Height   
        height_mode = data['Height'].value_counts().index[0]
        data.Height = data.Height.fillna(0)
        for index, row in data.iterrows():
            if int(data.at[index, 'Height']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country']==row['Brand_Country']]['Height'].mode().values[0])
                country_mode = int(data.loc[data['Country']==row['Country']]['Height'].mode().values[0])
                if brand_country_mode!=0:
                    height = brand_country_mode
                elif country_mode!=0:
                    height = country_mode
                else: 
                    height = height_mode
            else: 
                height = int(data.at[index, 'Height'])
            
            if height>=515 and height<850: value = 0
            elif height==850: value = 1
            else: value = 2
            
            data.at[index, 'Height'] = value
        data.Height = data.Height.astype(int)

        # Setting mode of Internal Heater
        mode_internal_heater = data.internal_heater.value_counts().index[0]
        data.internal_heater.fillna(mode_internal_heater)
        for index, rows in data.iterrows():
            if data.at[index, 'internal_heater']=='Yes on the warm wash program only':
                value = 0
            elif data.at[index, 'internal_heater']=='No':
                value = 1
            else: value = 2
            data.at[index, 'internal_heater'] = value
        data.internal_heater = data.internal_heater.astype(int)

        # Setting value of powerConsMode
        data.powerConsMode = data.powerConsMode.fillna(0.0)
        for index, rows in data.iterrows():
            powerConsMode = data.at[index, 'powerConsMode']   
            if powerConsMode<=0.4: value = 0
            elif powerConsMode>0.4 and powerConsMode<=0.75: value = 1
            elif powerConsMode>0.75 and powerConsMode<=1.4: value = 2
            elif powerConsMode>1.4: value = 3
            data.at[index, 'powerConsMode'] = value
        data.powerConsMode = data.powerConsMode.astype(int)

        # Return features of the program
        def return_features(data, index):
            program = data.at[index, 'Prog Name']
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
                if i not in ['', '-']: features.append(i.lower())
            return features

        # General categories - Normal, Heavy, Eco
        for index, row in data.iterrows():
            names = return_features(data, index)
            if 'normal' in names: value = 0
            elif 'eco' in names: value = 1
            elif 'cotton' in names: value = 2
            else: value = 3
            data.at[index, 'Prog Name'] = value
        data['Prog Name'] = data['Prog Name'].astype(int)

        # Setting values for Standby Power Consumed
        mode_standby_power = data.standbyPowerUsage.value_counts().index[1]
        mean = data.standbyPowerUsage.mean()
        std = data.standbyPowerUsage.std()
        null_count = data.standbyPowerUsage.isnull().sum()
        null_random = np.random.randint(mean - std, mean + std, size=null_count)
        data.standbyPowerUsage[np.isnan(data.standbyPowerUsage)] = null_random
        for index, rows in data.iterrows():
            standby_power = data.at[index, 'standbyPowerUsage']
            if standby_power<=0.25: value = 0
            elif standby_power>0.25 and standby_power<=0.5: value = 1
            elif standby_power>0.5 : value = 3
            data.at[index, 'standbyPowerUsage'] = value
        data.standbyPowerUsage = data.standbyPowerUsage.astype(int)

        # Setting values of width
        width_mode = data['Width'].value_counts().index[0]
        data.Width = data.Width.fillna(0)
        for index, row in data.iterrows():
            if int(data.at[index, 'Width']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country']==row['Brand_Country']]['Width'].mode().values[0])
                country_mode = int(data.loc[data['Country']==row['Country']]['Width'].mode().values[0])
                if brand_country_mode!=0:
                    width = brand_country_mode
                elif country_mode!=0:
                    width = country_mode
                else: 
                    width = depth_mode
            else: 
                width = int(data.at[index, 'Width'])
            
            if width<=565: value = 0
            elif width>=570 and width<600: value = 1
            elif width>=600: value = 2
            data.at[index, 'Width'] = value
        data.Width = data.Width.astype(int)

        # Setting these fields to their respective integer clases
        ApplStandard_types = {'AS/NZS 2040.2:2005': 0, 'AS/NZS 2040.2:2005 (Legacy)': 1, 'AS/NZS 2040.2:2000 (Legacy)': 2, 'Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2015': 3, 'Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2012': 4}
        data['ApplStandard'] = data['ApplStandard'].map(ApplStandard_types).astype(int)
        data['Conn_Mode'] = data['Conn_Mode'].map({'Dual':0, 'Cold': 1}).astype(int)
        data['Type'] = data['Type'].map({'Drum':0, 'Non-Drum': 1}).astype(int)

        # Setting values for Cap
        for index, row in data.iterrows():
            cap = data.at[index, 'Cap']
            if cap<7: value = 0
            elif cap>=7 and cap<8: value = 1
            elif cap>=8 and cap<9: value = 2
            else: value = 3
            data.at[index, 'Cap'] = value
        data.Cap = data.Cap.astype(int)

        # Setting values for Program Time
        for index, rows in data.iterrows():
            time = data.at[index, 'Program Time']
            if time<=125: value = 0
            elif time>125 and time<250: value = 1
            else: value = 2
            data.at[index, 'Program Time'] = value
        data['Program Time'] = data['Program Time'].astype(int)

        train_x = data.drop(['Brand_Country', 'Brand', 'Country'], axis=1)
        test_x = train_x.loc[len(data)-1]
        inputData = test_x
        test_x = pd.DataFrame([test_x.tolist()], columns = train_x.columns.values)
        train_x = train_x[:-1]
        realData = train_x.copy()
        realData['New Star'] = pd.Series(train_y.to_numpy(), index=train_x.index)

        knn = KNeighborsClassifier(n_neighbors = 3, leaf_size=5, algorithm='auto')
        knn.fit(train_x, train_y)  
        test_y = knn.predict(test_x)
        return self.inferenceBuilder(realData, inputData, test_y[0])

    def inferenceBuilder(self, data, inputData, category):
        # This functions checks if the problematic features values are contributing to a low star rating, if they are they are considered to be issues
        issues = []
        booleanFeatureNames = ['Type of Appliance being Non-Drum', 'Delay Start Mode being False', 'Connection Mode being Drum']
        featureNames = ['Program Running Time', 'Power usage in Standby Mode', 'Power Consumption in Mode', 'Capacity', 'Comparative Energy Consumption for Cold Use', 'Comparative Energy Consumption for Warm Use', 'Cold Water Consumption']
        for i in range(len(self.booleanFeatures)):
            feature = self.booleanFeatures[i]
            if category!=2 and inputData[feature] in data.loc[data['New Star']<=1, feature].value_counts().index[:1]:
                issues.append(booleanFeatureNames[i])
        for i in range(len(self.problemFeatures)):
            feature = self.problemFeatures[i]
            if category==0 and inputData[feature] in data.loc[data['New Star']<=1, feature].value_counts().index[:2]:
                issues.append(featureNames[i])
            elif category==1 and inputData[feature] in data.loc[data['New Star']<=1, feature].value_counts().index[:1]:
                issues.append(featureNames[i])
        responseData = {'category':category, 'issues': issues}
        return responseData

if __name__ == "__main__":
    specifications = ['AS/NZS 2040.2:2005', 'WHIRLPOOL', 7, 150, 400, 100, True, 'Dual', 'India', True, 565, 'Non Drum', 850, 'No', 0.4, 'normal', 0.45, 'Drum', 600, 120]
    ROOT_DIRECTORY_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    DATASET_PATH = os.path.join(ROOT_DIRECTORY_PATH, 'datasets')
    a = predictWashingMachine(specifications, os.path.join(DATASET_PATH, 'washing_machine.csv'))
    print(a.predict())