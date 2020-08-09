#utils
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import statistics
import dateutil.parser

#models
from sklearn.linear_model import LinearRegression, ElasticNetCV, Ridge
import sklearn
import pandas_datareader.data as web
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit
from pandas_datareader.data import DataReader
pd.options.mode.chained_assignment = None

#data
from app.settings.config import HIST_BTCUSD_1H_OHLC_PKL

import warnings
warnings.filterwarnings('ignore')


df = pd.read_pickle(HIST_BTCUSD_1H_OHLC_PKL)
df.index = df.Date
df.index = pd.to_datetime(df['Date'])
cols_drop = ['Date', 'Volume', 'Price_Average']
df.drop(cols_drop, inplace=True, axis=1)


#colums lower
df.columns = [x.lower() for x in df.columns]

#OHLC Average feature
df['ohlc_average'] = (df['open'] + df['high'] + df['low'] + df['close']) / len(df.columns)

#Normalize data
"""
Function to normalize each column, parameters take a dataframe and a specific column
We use the min-max normalize scale function to get a more accurate result as the values are all between 0 and 1.
"""
def normalizeColumn(df, column):
    x = df[column].values #returns a numpy array
    scaler = preprocessing.minmax_scale(x)
    return scaler

#Function to normalize each column separately
def normalizeDf(df):
    normalizedDf = pd.DataFrame()

    for column in df:
        normalizedDf[column] = normalizeColumn(df, column)

    return normalizedDf.set_index(df.index)

#replace all infinity values with nan
df = df.replace([np.inf, -np.inf], np.nan)
#create our normalized dataframe using the normalizeDf function that we created
normalizedDataFrame = normalizeDf(df)

#We shift the closeprice to make a LABEL column for us, which we then predict on.
"""
!!! We should not shift the price before we normalize the values, else the values will be wrong!
"""
#Shift close to create our label, also dropping NaN values
normalizedDataFrame['label'] = normalizedDataFrame['close'].shift(-1)
normalizedDataFrame = normalizedDataFrame.dropna()

#Splitting the dataframe into test/train
#We print them next to eachother to check that our label is correct.
normalizedDataFrame[['close', 'label']].tail(5)

#We split the dataframes to create our test and train dataframes
n = normalizedDataFrame.shape[0]
train_size = 0.8
train_dataframe = normalizedDataFrame.iloc[:int(n * train_size)]
test_dataframe = normalizedDataFrame.iloc[int(n * train_size):]

print("Amount of traindata rows: ", len(train_dataframe),'\n'
      "Amount of testdata rows: ", len(test_dataframe))
print("Rows in total:", len(normalizedDataFrame))


#### Using SVR, RandomForest, LinearRegression and MLP ####
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression


#regressionmodels
svr = SVR()
rf = RandomForestRegressor()
lr = LinearRegression()
mlp = MLPRegressor()

#We create our x and y train values
x_train = np.array(train_dataframe[['close', 'ohlc_average']])
y_train = np.array(train_dataframe['label'])

#and then we use our training data on the models
svr.fit(x_train, y_train)
lr.fit(x_train, y_train)
rf.fit(x_train, y_train)
mlp.fit(x_train, y_train)


#We define our test values
x_test = np.array(test_dataframe[['close', 'ohlc_average']])
y_test = np.array(test_dataframe['label'])

#Show the accuracy on our test values
print("svr score:", svr.score(x_test, y_test))
print("lr score:", lr.score(x_test, y_test))
print("rf score:", rf.score(x_test, y_test))
print("mlp score:", mlp.score(x_test, y_test))


#### Creating a decision  ####
"""
The decision function creates a True = buy, 
False = sell decision based on our predicted values.

Basically the function simply compares the forecast with our price close, 
if the forecast value is bigger then we want to buy, else we sell.

The actual decision compares label with price_close.
We can then compare the actual with our forecasted decision to 
figure out our hit/miss percentage using our hit_miss function.

With the hit/miss function we can see which model is has the highest percentage
"""

#decision function. if forecast value is higher than close = buy, else sell
def decision(model, df, x_test, model_name):
    df['actual'] = (df.label > df.close)
    df[model_name + '_forecast'] = model.predict(x_test)
    df[model_name + '_decision'] = (df[model_name + '_forecast'] > df.close) # True == buy, False == sell
    return df

#hit_miss function, basically checks how many times our models are the same as actual, giving us a percentage of hits
def hit_miss(df, model_name):
    df[model_name + '_hitmiss'] = (df.actual == df[model_name + '_decision'])
    print('Hit miss percentage', model_name,':', (df[model_name + '_hitmiss'].values == True).sum() / len(df), '%')


#creating our decision columns into the test_dataframe
decision(lr, test_dataframe, x_test, 'lr')
decision(mlp, test_dataframe, x_test, 'mlp')
decision(rf, test_dataframe, x_test, 'rf')
decision(svr, test_dataframe, x_test, 'svr')


#Hit/Miss percentages.. basically how many times our forecast is right
hit_miss(test_dataframe, 'mlp')
hit_miss(test_dataframe, 'lr')
hit_miss(test_dataframe, 'rf')
hit_miss(test_dataframe, 'svr')

#### Plotting our forecasts with label ####

import plotly.graph_objects as go
#plotting the forecasts and label
line1 = go.Scatter( x=test_dataframe.index, y=test_dataframe.mlp_forecast, name='MLP' )
line2 = go.Scatter( x=test_dataframe.index, y=test_dataframe.svr_forecast, name='SVR' )
line3 = go.Scatter( x=test_dataframe.index, y=test_dataframe.rf_forecast, name='RF' )
line4 = go.Scatter( x=test_dataframe.index, y=test_dataframe.lr_forecast, name='LR')
line5 = go.Scatter( x=test_dataframe.index, y=test_dataframe.label, name='Label' )

layout = go.Layout(
    title='Prediction',
    yaxis=dict(title='Price normalized'),
    xaxis=dict(title='Date')
)

data = [line1, line2, line3, line4, line5]

fig = go.Figure(data=data, layout=layout)

fig.show()

#### sMAPE and MASE calculations ####
# SMAPE - symmetric mean absolute percentage error

#this function is based on the formula shown above, which is from the paper/article found on itslearning "ErrorMeasurements.pdf"
def my_smape(label, forecast):
    return np.mean(200*(np.abs(label - forecast) / (label + forecast)))


#this function is striaght up copied from the internet (so i can test whether my own one gives same result)
def smape(label, forecast):
    return 100/len(label) * np.sum(2 * np.abs(forecast - label) / (np.abs(label) + np.abs(forecast)))


print("sMAPE for SVR:", my_smape(test_dataframe['label'], test_dataframe['svr_forecast']))
print("sMAPE for RandomForest:", my_smape(test_dataframe['label'], test_dataframe['rf_forecast']))
print("sMAPE for lr:", my_smape(test_dataframe['label'], test_dataframe['lr_forecast']))
print("sMAPE for MLP:", my_smape(test_dataframe['label'], test_dataframe['mlp_forecast']))

#### MASE - mean absolute scaled error ####
def mase(actual, predicted):
    # return np.mean(np.abs(actual - predicted)) / np.mean(np.abs(actual[1:] - actual[:-1]))

    # predicted error mean / naive prediction error mean
    return np.mean(np.abs(actual - predicted)) / np.mean(np.abs(np.diff(actual)))

print("MASE for SVR:", mase(test_dataframe['label'], test_dataframe['svr_forecast']))
print("MASE for RandomForest:", mase(test_dataframe['label'], test_dataframe['rf_forecast']))
print("MASE for lr:", mase(test_dataframe['label'], test_dataframe['lr_forecast']))
print("MASE for MLP:", mase(test_dataframe['label'], test_dataframe['mlp_forecast']))

#### We create a dataframe to display the comparison between our results from SMAPE and MASE ####
# Insert data for SMAPE and MASE
data = {'SMAPE': [my_smape(test_dataframe['label'], test_dataframe['svr_forecast']),
                  my_smape(test_dataframe['label'], test_dataframe['rf_forecast']),
                  my_smape(test_dataframe['label'], test_dataframe['lr_forecast']),
                  my_smape(test_dataframe['label'], test_dataframe['mlp_forecast'])],

        'MASE': [mase(test_dataframe['label'], test_dataframe['svr_forecast']),
                 mase(test_dataframe['label'], test_dataframe['rf_forecast']),
                 mase(test_dataframe['label'], test_dataframe['lr_forecast']),
                 mase(test_dataframe['label'], test_dataframe['mlp_forecast'])], }

# create a dataframe with our values
rankingDF = pd.DataFrame(data, index=['SVR', 'RF', 'LR', 'MLP'])

