
import numpy as np
import datetime as dt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA

class GUIPredictor:
    """
    Provide preditive functions using three models: Linear Regression Model,
    Non-linear Regression Model and ARIMA model.
    Users will input the date (year, month and day) on which they would like
    to predict a particular stock.
    Outputs are the predicted price on that day and the evaluation scores
    (MSE, R2) of each model.    
    """   
    def __init__(self, df, pred_date):  # The predicted time is passed in from the interface
        self.df = df
        self.pred_date = pred_date
    
    def get_features(self):
        """Get the features (Year, Month, Day) from df["Date"]"""
        self.df.loc[:,"Year"] = self.df["Date"].dt.year
        self.df.loc[:,"Month"] = self.df["Date"].dt.month
        self.df.loc[:,"Day"] = self.df["Date"].dt.day
        
    def split(self):
        """Split the dataset into train set and test set."""
        return train_test_split(self.df[["Year","Month","Day"]], self.df["Close"], test_size = 0.3, random_state = 42)

    def arima(self, y_train):
        """ARIMA model"""
        p = 3  # Number of time lags (Auto-Regresive coefficient)
        d = 1  # Degree of differencing (I)
        q = 3  # Number of Moving Average terms (MA coefficient)
        model = ARIMA (y_train, order = (p, d, q))
        results =  model.fit()
        return results

    def linear_regression(self, x_train, y_train):
        """Linear Regression Model"""
        model = linear_model.LinearRegression()
        model.fit(x_train, y_train)
        return model
    
    def to_integer(self, dt_time):
        """Convert the datetime to an integer."""
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day
          
    def evaluate(self, y_test, y_pred):
        """Evaluate the model and output the MSE and R2 scores."""
        return (mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred))
    
    def main(self):
        self.get_features() # get the year, month, day from df["Date"] and use them as features
        x_train, x_test, y_train, y_test = self.split() # split the dataset as train set and test set
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_test = np.array(x_test)
        y_test = np.array(y_test).reshape(-1, 1)

        pred_date = self.pred_date  # Calling its own properties

        # Linear Regression Model
        model1 = self.linear_regression(x_train, y_train) #instantiate the linear regression model
        prediction1 = model1.predict(pred_date) # predicted price for the prediction date
        y_pred1 = model1.predict(x_test)
        mse1, r21 = self.evaluate(y_test, y_pred1) # evaluation scores for model1
        
        # Non-linear Regression Model
        PF = PolynomialFeatures(2) # transform the features to non-linear
        xfit1 = PF.fit_transform(x_train)
        xfit2 = PF.fit_transform(x_test)
        model2 = self.linear_regression(xfit1, y_train) #instantiate the non-linear regression model
        prediction2 = model2.predict(PF.fit_transform(pred_date)) # predicted price for the prediction date
        y_pred2 = model2.predict(xfit2)
        mse2, r22 = self.evaluate(y_test, y_pred2) # evaluation scores for model2

        # ARIMA Model
        l = len(self.df)
        l1 = l // 3
        l2 = l - l1
        train = self.df[:l2].Close
        test = self.df[l2:].Close
        model3 = self.arima(train) #instantiate the ARIMA model
        y_pred3 = model3.predict(start = l2, end = l - 1)
        # calculate the number of days between the last train date and the prediction date
        last_train_date = self.df.iloc[-1,:].Date
        fsteps = self.to_integer(dt.datetime(*pred_date[0])) - self.to_integer(last_train_date) # Number of future steps
        prediction3 = model3.get_forecast(fsteps) # predicted price for the prediction date
        prediction3 = prediction3.predicted_mean.values[-1] #Forecast (ARIMA) for 'Close' values
        mse3, r23 = self.evaluate(test, y_pred3)

        result_text = """
        Linear Regression Model:\n
        Predicted Price:{}\n
        MSE: {}      R2:{}\n
        Non-linear Regression Model:\n
        Predicted Price:{}\n
        MSE: {}      R2:{}\n
        ARIMA model:\n
        Predicted Price:{}\n
        MSE: {}
        """.format(*prediction1, mse1, r21, *prediction2, mse2, r22, prediction3, mse3, r23)
        return result_text


