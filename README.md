# Problem Statement
The aim of this project is to build Machine Learning models to create energy consumption profiles for household and identify probable 
areas to plug wastage of energy in household. 

The objective of this application is to help households in 2 main ways - 
1. Predict the Energy Star Rating of old or vampire appliances without a energy star rating
2. Predict reasons for high energy consumption using the valuable insights provided 

## Starting App 
Firstly, add `chromedriver` to your system path. This is needed to ensure complete advantage of the UI/UX we offer.

Run the following in the root folder of the repository
```shell
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ../server
python app.py
```
Then open `localhost:5000` your browser to start the application. Test the API's using the inputs from `sample_inputs.txt` file.

## About the Project
We have used Jupyter Notebook for visualization and making inferences of the data. We are running the web application using Flask server and using React for the front-end of the application. We have REST API calls to all the predictions are made currently using simple supervised learning classifier models and average around 85% accuracy. 
- `datasets` folder consists of all the datasets along with their label files
- `data_infereces` folder consists of Jupyter files containing the prediction as well as the different inferences made based on the data from the datasets
- `frontend` folder consists the source files of the front-end of the web application
- `server` consists of all the server code, along with the REST API for making the predictions based on the input data

## Team Members
- [Rishi Ravikumar](https://github.com/RRK1000)
- [Aditya Vinod Kumar](https://github.com/adityavinodk)

## OpenSource Contribution 
We would like the developer community to contribute to this project - 
- Move to real-time data prediction, which will be easier to scale in the future
- Add more useful datasets which provide a larger idea of the usage of the appliances at households like seasonal data.
- Provide visualitzation of the inferences made on the website through charts and plots.

Send Pull Requests and we shall review them!