
import pandas as pd
import json
import pandas_datareader as pdr
import datetime as dt

class StoreStockData:
    """Download the stock data from Yahoo Finance and save to a csv file."""
    def __init__(self, t_filename = "tickers_companynames.txt", filename = "stock_data.csv", start_date = dt.datetime(2000,1,1)):
        self.t_filename = t_filename
        self.filename = filename
        self.start_date = start_date

    def get_ticker(self):
        """Read the ticker data from a txt file."""
        with open (self.t_filename) as f:
            data = f.readlines()
        return (json.loads(i) for i in data)    
        
    def get_stockprice(self, ticker):
        """Download the stock data from Yahoo Finance using the ticker data."""
        try:
            return pdr.get_data_yahoo(ticker, start = self.start_date)
        except:
            print("Cannot find this stock!")
    
    def add_ticker_companyname(self, data, ticker, company_name):
        """Add the ticker name and company name to the data."""
        data["Ticker"] = ticker
        data["Company_Name"] = company_name
        return data
        
    def save_to_csv(self, df):
        """Save the data to a csv file."""
        df.to_csv(self.filename)
    
    def main(self):
        df = pd.concat([self.add_ticker_companyname(self.get_stockprice(line["ticker"]), \
                                                  line["ticker"], line["company_name"]) \
                        for line in self.get_ticker()]).reset_index()
        self.save_to_csv(df)
        

if __name__ == '__main__':
    stock_data = StoreStockData()
    stock_data.main()
    
    