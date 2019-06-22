import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

class predictDryer():

    def __init__(self, specifications, dataset_path):
        self.specifications = specifications
        self.dataset_path = dataset_path
        self.problemFeatures = ['New CEC', 'Prog Time', 'Type', 'Cap']
        self.booleanFeatures = ['Combination']

    def predict(self):
        # Kindly refer ../../inferences/dryer.ipynb for the logic of the following code

        # order_of_training_data = ['Appliance Standard', 'Brand', 'Capacity', 'Combination', 'Control', 'Country', 'Depth','Height', 'Current Comparitive Energy Consumption', 'Program Name', 'Program Time', 'Type', 'Width']
        specifications = self.specifications
        dataset_path = self.dataset_path
        
        data = pd.read_csv(dataset_path)
        
        columns = ['Model No', 'Family Name', 'Sold_in', 'N-Standard', 'SubmitStatus', 'Submit_ID', 'GrandDate', 'Product Class', 'New SRI', 'Tot_Wat_Cons', 'Test_Moist_Remove',
                   'Product Website', 'Old Star Rating', 'Star Image Large', 'Star Image Small', 'Availability Status', 'Representative Brand URL', 'ExpDate']
        data.drop(columns, axis=1, inplace=True)

        # Converting New Star to different classes
        data['New Star'] = data['New Star'].astype(int)
        for index, rows in data.iterrows():
            star = data.at[index, 'New Star']
            if star == 1: value = 0
            elif star == 2: value = 1
            elif star >= 3: value = 2
            data.at[index, 'New Star'] = value

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

        # To fill missing values in Depth
        mode_depth_overall = data['Depth'].value_counts().index[0]
        data['Depth'] = data['Depth'].fillna(0)
        for index, row in data.iterrows():
            if int(row['Depth']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country'] == row['Brand_Country']]['Depth'].mode().values[0])
                country_mode = int(data.loc[data['Country'] == row['Country']]['Depth'].mode().values[0])
                if brand_country_mode != 0: depth = brand_country_mode
                elif country_mode != 0: depth = country_mode
                else: depth = mode_depth_overall
            else:
                depth = int(data.at[index, 'Depth'])

            if depth >= 60 and depth <= 550: value = 0
            elif depth == 555: value = 1
            elif depth >= 560 and depth <= 700: value = 2
            else: value = 3
            data.at[index, 'Depth'] = value

        data['Depth'] = data['Depth'].astype(int)

        # To fill missing values in Height
        mode_height_overall = data['Height'].value_counts().index[1]
        data['Height'] = data['Height'].fillna(0)
        for index, row in data.iterrows():
            if int(data.at[index, 'Height']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country'] == row['Brand_Country']]['Height'].mode().values[0])
                country_mode = int(data.loc[data['Country'] == row['Country']]['Height'].mode().values[0])
                if brand_country_mode != 0:
                    height = brand_country_mode
                elif country_mode != 0:
                    height = country_mode
                else:
                    height = mode_depth_overall
            else:
                height = int(data.at[index, 'Height'])

            if height >= 85 and height <= 550: value = 0
            elif height == 555: value = 1
            elif height >= 560 and height < 850: value = 2
            elif height == 850: value = 3
            else: value = 4
            data.at[index, 'Height'] = value
        data['Height'] = data['Height'].astype(int)

        # To fill missing values in Width
        mode_height_overall = data['Width'].value_counts().index[0]
        data['Width'] = data['Width'].fillna(0)
        for index, row in data.iterrows():
            if int(row['Width']) == 0:
                brand_country_mode = int(data.loc[data['Brand_Country'] == row['Brand_Country']]['Width'].mode().values[0])
                country_mode = int(data.loc[data['Country'] == row['Country']]['Width'].mode().values[0])
                if brand_country_mode != 0:
                    width = brand_country_mode
                elif country_mode != 0:
                    width = country_mode
                else:
                    width = mode_depth_overall
            else:
                width = int(data.at[index, 'Width'])

            if width >= 60 and width < 595: value = 0
            elif width == 595: value = 1
            elif width >= 600 and width < 850: value = 2
            data.at[index, 'Width'] = value
        data['Width'] = data['Width'].astype(int)

        # Setting Capacity under different integer classes
        for index, rows in data.iterrows():
            capacity = int(data.at[index, 'Cap'])
            if capacity >= 1 and capacity <= 6: value = 0
            elif capacity >= 7 and capacity <= 8: value = 1
            else: value = 2
            data.at[index, 'Cap'] = value
        data['Cap'] = data['Cap'].astype(int)

        # Setting Program Time under different integer classes
        data['Prog Time'] = data['Prog Time'].astype(int)
        for index, rows in data.iterrows():
            time = data.at[index, 'Prog Time']
            if time >= 50 and time <= 115: value = 0
            elif time > 115 and time <= 150: value = 1
            elif time > 150 and time <= 175: value = 2
            elif time > 175 and time <= 200: value = 3
            elif time > 200 and time <= 215: value = 4
            elif time > 215 and time <= 235: value = 5
            elif time > 235 and time <= 275: value = 6
            elif time > 275 and time <= 300: value = 7
            elif time > 300: value = 8
            data.at[index, 'Prog Time'] = value

        # Converting CEC into smaller integer classes using feature scaling
        data['New CEC'] = data['New CEC'].astype(int)
        cec_range = data['New CEC'].max() - data['New CEC'].min()
        cec_mean = data['New CEC'].mean()
        for index, rows in data.iterrows():
            cec = (data.at[index, 'New CEC'] - cec_mean)/cec_range
            if cec > -0.5 and cec <= -0.25: value = 0
            elif cec > -0.25 and cec <= -0.175: value = 1
            elif cec > -0.175 and cec <= -0.15: value = 2
            elif cec > -0.15 and cec <= -0.05: value = 3
            elif cec > -0.05 and cec <= 0: value = 4
            elif cec > 0 and cec <= 0.15: value = 5
            elif cec > 0.15 and cec <= 0.25: value = 6
            elif cec > 0.25 and cec <= 0.5: value = 7
            data.at[index, 'New CEC'] = value

        # We shall extract the features fro the Program Name and seperate them into different classes
        def return_features(data, i):
            program = data.at[i, 'Prog Name']
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
            return features

        for i, row in data.iterrows():
            features = return_features(data, i)
            if 'dry' in features and 'heat' in features: 
                data.at[i, 'Prog Name'] = 0
            elif 'heat' in features:
                data.at[i, 'Prog Name'] = 1
            elif 'dry' in features:
                data.at[i, 'Prog Name'] = 2
            else:
                data.at[i, 'Prog Name'] = 3

        data['Prog Name'] = data['Prog Name'].astype(int)

        # As we can see we have removed all the null values are removed, now we must convert all the other data type
        # to int type, by mapping boolean and objects to int
        ApplStandard_types = {'AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)': 0, 'Greenhouse and Energy Minimum Standards (Rotary Clothes Dryers) Determination 2012': 1,
                              'Greenhouse and Energy Minimum Standards (Rotary Clothes Dryers) Determination 2015': 2, 'AS/NZS 2442.2:2000/Amdt 2:2007': 3}
        data['ApplStandard'] = data['ApplStandard'].map(ApplStandard_types).astype(int)
        data['Combination'] = data['Combination'].map({False: 0, True: 1}).astype(int)
        data['Control'] = data['Control'].map({'Timer': 0, 'Autosensing': 1, 'Manual': 2}).astype(int)
        data['Type'] = data['Type'].map({'Condenser': 0, 'Vented': 1}).astype(int)

        # We have converted all the initial types into integer type
        # For now we shall not consider the effects of Brand_country, Brand and Country
        train_x = data.drop(['Brand_Country', 'Brand', 'Country'], axis=1)
        test_x = train_x.loc[len(data)-1]
        inputData = test_x
        test_x = pd.DataFrame([test_x.tolist()], columns = train_x.columns.values)
        train_x = train_x[:-1]
        realData = train_x.copy()
        realData['New Star'] = pd.Series(train_y.to_numpy(), index=train_x.index)

        # KNN Neighbours Classification
        # TODO: Fine tuning of hyper parameters
        knn = KNeighborsClassifier(n_neighbors = 3, leaf_size=5, algorithm='ball_tree')
        knn.fit(train_x, train_y)
        test_y = knn.predict(test_x)
        return self.inferenceBuilder(realData, inputData, test_y[0])

    def inferenceBuilder(self, data, inputData, category):
        issues = []
        booleanFeatureNames = ['Condensor Combination']
        featureNames = ['Comparative Energy Consumption', 'Time of usage of Appliance', 'Type of appliance', 'Capacity of appliance']
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
    specifications = ['AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)', 'ASKO', 8, True, 'Timer', 'Slovenia', 890, 650, 200, 'Heat and dry', 230, 'Vented', 650]
    ROOT_DIRECTORY_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    DATASET_PATH = os.path.join(ROOT_DIRECTORY_PATH, 'datasets')
    a = predictDryer(specifications, os.path.join(DATASET_PATH, 'dryer.csv'))
    print(a.predict())