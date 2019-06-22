import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

class predictMonitor():

    def __init__(self, specifications, dataset_path):
        self.specifications = specifications
        self.dataset_path = dataset_path
        self.problemFeatures = ['Screen Technology', 'Comparative Energy Consumption', 'Active Standby Power']

    def predict(self):
        # Kindly refer ../../inferences/monitor.ipynb for the logic of the following code

        # order_of_training_data = ['Screen Technology', 'Comparitive Energy Consumption', 'Active Standby Power']
        specifications = self.specifications
        dataset_path = self.dataset_path
        data = pd.read_csv(dataset_path)

        # Drop the unnecessary columns
        columns = ['Record ID', 'Status', 'Brand Name', 'Manufacturing Countries', 'Availability Status','Model Number', 'Family Name', 'Screen Size', 'Selling Countries', 'Product Website', 'Representative Brand URL', 'Star Rating Index', 'Expiry Date', 'Star Image Large', 'Star Image Small']
        data.drop(columns, axis=1, inplace=True)

        for index, row in data.iterrows():
            star = data.at[index, 'Star Rating']
            if star<=4 : value = 0
            elif star>4 and star<6: value = 1
            else: value = 2
            data.at[index, 'Star Rating'] = value
        data['Star Rating'] = data['Star Rating'].astype(int)

        # Setting train_y as New Star column
        train_y = data['Star Rating']
        data.drop('Star Rating', axis=1, inplace=True)

        # Concatenating the dataframe with the row to predict
        df2 = pd.DataFrame([specifications],columns=data.columns.values)
        data = pd.concat([data,df2], ignore_index = True)

        # Mapping Comparitive Energy Consumption to Integer Classes
        for index, row in data.iterrows():
            comp_energy = data.at[index, 'Comparative Energy Consumption']
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
            
            data.at[index, 'Comparative Energy Consumption'] = value
        data['Comparative Energy Consumption'] = data['Comparative Energy Consumption'].astype(int)

        # Mapping Screen Technology to Integer classes
        data['Screen Technology'] = data['Screen Technology'].map({'LCD (LED)': 0, 'LCD': 1, 'OLED': 2}).astype(int)

        # Mapping Active Standby Power to Integer classes
        for index, rows in data.iterrows():
            standby_power = data.at[index, 'Active Standby Power']
            if standby_power<=0.2: value = 0
            elif standby_power>0.2 and standby_power<=0.24: value = 1
            elif standby_power>0.24 and standby_power<=0.28: value = 2
            elif standby_power>0.28 and standby_power<=0.32: value = 3
            elif standby_power>0.32 and standby_power<=0.39: value = 4
            else: value = 5
            data.at[index, 'Active Standby Power'] = value
        data['Active Standby Power'] = data['Active Standby Power'].astype(int)

        # Split the data into train and test
        train_x = data
        test_x = train_x.loc[len(data)-1]
        inputData = test_x
        test_x = pd.DataFrame([test_x.tolist()], columns = train_x.columns.values)
        train_x = train_x[:-1]
        realData = train_x.copy()
        realData['Star Rating'] = pd.Series(train_y.to_numpy(), index=train_x.index)

        # Fit the random forest classifier model and return prediction
        random_forest = RandomForestClassifier(n_estimators=200, criterion='entropy', oob_score=True)
        random_forest.fit(train_x, train_y)
        test_y = random_forest.predict(test_x)
        return self.inferenceBuilder(realData, inputData, test_y[0])
    
    def inferenceBuilder(self, data, inputData, category):
        issues = []
        featureNames = ['Technology running the screen', 'Comparative Energy Consumption', 'Power used in Standby Mode']
        for i in range(len(self.problemFeatures)):
            feature = self.problemFeatures[i]
            if category==0 and inputData[feature] in data.loc[data['Star Rating']<=1, feature].value_counts().index[:2]:
                issues.append(featureNames[i])
            elif category==1 and inputData[feature] in data.loc[data['Star Rating']<=1, feature].value_counts().index[:1]:
                issues.append(featureNames[i])
        responseData = {'category':category, 'issues': issues}
        return responseData
            

if __name__ == "__main__":
    specifications = ['LCD (LED)', 100, 0.35]
    ROOT_DIRECTORY_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    DATASET_PATH = os.path.join(ROOT_DIRECTORY_PATH, 'datasets')
    a = predictMonitor(specifications, os.path.join(DATASET_PATH, 'monitor.csv'))
    print(a.predict())