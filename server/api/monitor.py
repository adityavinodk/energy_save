import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

class predictMonitor():

    def __init__(self, specifications, dataset_path):
        self.specifications = specifications
        self.dataset_path = dataset_path

    def predict(self):
        # Kindly refer ../../inferences/monitor.ipynb for the logic of the following code

        # order_of_training_data = ['Screen Size', 'Screen Technology', 'Active Standby Power']
        specifications = self.specifications
        dataset_path = self.dataset_path
        data = pd.read_csv(dataset_path)

        # Drop the unnecessary columns
        columns = ['Record ID', 'Status', 'Brand Name', 'Manufacturing Countries', 'Availability Status','Model Number', 'Family Name', 'Comparative Energy Consumption', 'Selling Countries', 'Product Website', 'Representative Brand URL', 'Star Rating Index', 'Expiry Date', 'Star Image Large', 'Star Image Small']
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

        # Mapping Screen Size to Integer Classes
        data['Screen Size'] = data['Screen Size'].astype(float)
        screen_size_range = data['Screen Size'].max() - data['Screen Size'].min()
        screen_size_mean = data['Screen Size'].mean()
        for index, rows in data.iterrows():
            screen_size = (data.at[index, 'Screen Size'] - screen_size_mean)/screen_size_range
            if screen_size>-0.4 and screen_size<=-0.08: value = 0
            elif screen_size>-0.08 and screen_size<=-0.07: value = 1
            elif screen_size>-0.07 and screen_size<=-0.03: value = 2
            elif screen_size>-0.03 and screen_size<=-0.027: value = 3
            elif screen_size>-0.027 and screen_size<=-0.01: value = 4
            elif screen_size>-0.01 and screen_size<=0.044: value = 5
            elif screen_size>0.044 and screen_size<=0.045: value = 6
            elif screen_size>0.045 and screen_size<=0.2: value = 7
            elif screen_size>0.2 : value = 8
            data.at[index, 'Screen Size'] = value
        data['Screen Size'] = data['Screen Size'].astype(int)

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
        test_x = pd.DataFrame([test_x.tolist()], columns = train_x.columns.values)
        train_x = train_x[:-1]

        # Fit the random forest classifier model and return prediction
        random_forest = RandomForestClassifier(n_estimators=200, criterion='entropy', oob_score=True)
        random_forest.fit(train_x, train_y)
        test_y = random_forest.predict(test_x)
        return test_y[0]

if __name__ == "__main__":
    specifications = [60.5, 'LCD (LED)', 0.35]
    ROOT_DIRECTORY_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    DATASET_PATH = os.path.join(ROOT_DIRECTORY_PATH, 'datasets')
    a = predictMonitor(specifications, os.path.join(DATASET_PATH, 'monitor.csv'))
    print(a.predict())