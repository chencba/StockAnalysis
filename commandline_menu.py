
import datetime as dt
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import stock_analysis
import predictor
import warnings
warnings.filterwarnings("ignore")

class Main_Menu:
    """This is the command line interface of Stock Analyzer."""
    def __init__(self, manual_filename = "USER MANUAL.txt", df = pd.read_csv("stock_data.csv")):
        self.manual_filename = manual_filename
        self.df = df
    
    def get_user_manual(self):
        """Print the user manual."""
        with open(self.manual_filename, encoding = 'UTF-8') as f:
            print(f.read())
    
    def welcome(self):
        print("Welcome to stock analyzer!")   
    
    def show_options(self):
        print("There are four options: 1, User Manual; 2, Stock Analysis; 3, Stock Predictor; 4, Quit")
           
    def get_option(self):
        """Get user's input of choice."""
        return input("Please select your options (enter 1, 2, 3 or 4): ") 
    
    def convert_date(self, year, month, day):
        """Convert the year, month and day to a datetime."""
        return dt.datetime(year, month, day)
    
    def get_start_date(self):
        """Get user's input of start date."""
        start_date = None
        while start_date is None:
            try:
                start_year = int(input("Please input the start year: "))
                start_month = int(input("Please input the start month: "))
                start_day = int(input("Please input the start day: "))
                try:
                    start_date = self.convert_date(start_year, start_month, start_day)
                    return start_date
                except:
                    print("Please input valid date.")
                    start_date = None
            except ValueError:
                print("Invid date!")

    def get_end_date(self):
        """Get user's input of end date."""
        end_date = None
        while end_date is None:
            try:
                end_year = int(input("Please input the end year: "))
                end_month = int(input("Please input the end month: "))
                end_day = int(input("Please input the end day: "))
                try:
                    end_date = self.convert_date(end_year, end_month, end_day)
                    return end_date
                except:
                    print("Please input valid date.")
                    end_date = None
            except ValueError:
                print("Invid date!")
    
    def check_date(self, start_date, end_date):
        """Check the validity of the start date and end date."""
        signal = True
        while signal:
            # if start date is in the future or earlier than Jan 1, 2000, or end date
            # is in the future or earlier than Jan 1, 2000, or the start date is later
            # than the end date, user will be asked to input again.
            if start_date >= dt.datetime.now() or start_date < dt.datetime(2000,1,1) \
                or end_date <= dt.datetime(2000,1,1) or end_date > dt.datetime.now():
                print("Start date and end date must be between Jan 1, 2000 - today. Please input again.") 
                start_date = self.get_start_date()
                end_date = self.get_end_date()
            elif start_date >= end_date:
                print("Start date must be an earlier date than end date!!!")
                start_date = self.get_start_date()
                end_date = self.get_end_date()
            else:
                signal = False
                return start_date, end_date
  
    def get_ticker(self):
        """Get user's input of ticker. Must be available on Yahoo Finance."""
        ticker = None
        while ticker is None:
            ticker =  input("Please input ticker: ").upper()
            try:
                pdr.get_data_yahoo(ticker, start = dt.datetime(2021,11,23), end = dt.datetime(2021,11,24))
                return ticker
            except:
                print("No such ticker!")
                ticker = None
      
    def get_data(self, ticker, start_date, end_date):
        """Get the stock data of the given ticker and start & end date."""
        # It will first search in the local csv file, if it doesn't exist, then it will search
        # on Yahoo Finance.
        if self.df["Ticker"].str.contains(ticker).any():
            index = np.where((self.df.Ticker == ticker) & (self.df.Date >= start_date) & (self.df.Date <= end_date))
            if index[0].size:
                return self.df.iloc[index]
            else:
                return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()
        else:
            return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()
    
    def check_data(self):
        """Add another validity check for situations like the stock market is
           closed between start date and end date."""
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        ticker = self.get_ticker()
        
        signal = True
        while signal:
            start_date = self.get_start_date()
            end_date = self.get_end_date()
            self.check_date(start_date, end_date)
            
            try:
                data = self.get_data(ticker, start_date, end_date)
                signal = False
            except KeyError:      
                print("No stock information between chosen dates.")               
        return data
    
    def process_options(self, choice):
        """When users make choices, lead them to the corresponding sub-menu."""
        while choice != "4":            
            if choice == "1":
                self.get_user_manual()   
                
            elif choice == "2":
                print("Stock Analysis: Please select the ticker and start & end dates you would like to analyze.")
                data = self.check_data()
                analyzers = stock_analysis.StockAnalysis(data)
                analyzers.main()

            elif choice == "3":
                print("Stock Predictor: Please select the ticker and start & end dates you would like for training.")
                data = self.check_data()
                predictors = predictor.StockPredictor(data)
                predictors.main()
                
            else:
                print("Not an option. Please choose again!")
            choice = self.get_option()

    def main(self):
        self.welcome()
        self.show_options()
        choice = self.get_option()
        self.process_options(choice)

if __name__ == '__main__':
    menu = Main_Menu()
    menu.main()


