
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(4, 1, figsize=(14, 14))
fig.subplots_adjust(hspace = 0.4)

class StockAnalysis:
    """
    Provide the stock analytics functions.
    Shows the descriptive analysis.
    Plot the graphs of time trend, MA10 and MACD.
    """
    def __init__(self, df):
        self.df = df       
        
    def descr_analysis(self):
        """Get the mean, median, max, min, 1st quartile, 3rd quartile of stock close price and volume."""
        data = self.df[["Close", "Volume"]]
        print(data.describe())        
    
    def plot_trend(self):
        """Plot the time trend line on close price."""
        ax[0].plot(self.df["Date"], self.df["Close"])
        ax[0].set_xlabel("Date")
        ax[0].set_ylabel("Close Price")
        ax[0].set_title("Close Price Over Time")
        
    def ma(self):
        """Plot the MA5/10/20 lines on close price."""
        data = self.df["Close"]
        self.df.loc[:, "MA5"] = data.rolling(window = 5).mean()
        self.df.loc[:, "MA10"] = data.rolling(window = 10).mean()
        self.df.loc[:, "MA20"] = data.rolling(window = 20).mean()
        ax[1].plot(self.df["Date"], self.df["MA5"])
        ax[1].plot(self.df["Date"], self.df["MA10"])
        ax[1].plot(self.df["Date"], self.df["MA20"])
        ax[1].legend(["MA5", "MA10", "MA20"])
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("Average Price")
        ax[1].set_title("Moving Average (5, 10, 20 days)")
        
    def macd(self):
        """Plot the DIFF, DEA and MACD graphs."""
        data = self.df["Close"]
        ndata = len(data)
        m, n, T = 12, 26, 9
        EMA1 = np.copy(data)
        EMA2 = np.copy(data)
        f1 = (m-1)/(m+1)
        f2 = (n-1)/(n+1)
        f3 = (T-1)/(T+1)
        for i in range(1, ndata):
            EMA1[i] = EMA1[i-1]*f1 + EMA1[i]*(1-f1)
            EMA2[i] = EMA2[i-1]*f2 + EMA2[i]*(1-f2)
        self.df.loc[:, "ma1"] = EMA1
        self.df.loc[:, "ma2"] = EMA2
        diff = EMA1 - EMA2
        self.df.loc[:, "DIFF"] = diff
        DEA = np.copy(diff)
        for i in range(1, ndata):
            DEA[i] = DEA[i-1]*f3 + DEA[i]*(1-f3)
        self.df.loc[:, "DEA"] = DEA
        self.df.loc[:, "MACD"] = (self.df["DIFF"] - self.df["DEA"])*2
        ax[2].plot(self.df["Date"], self.df["DIFF"])
        ax[2].plot(self.df["Date"], self.df["DEA"])
        ax[2].bar(self.df["Date"], self.df["MACD"])
        ax[2].legend(["DIFF", "DEA", "MACD"])
        ax[2].set_xlabel("Date")
        ax[2].set_title("MACD")
    
    def plot_volume(self):
        """Plot the time trend bar on volume."""
        ax[3].bar(self.df["Date"], self.df["Volume"])
        ax[3].set_xlabel("Date")
        ax[3].set_ylabel("Volume")
        ax[3].set_title("Volume Over Time")
   
    def main(self):
        self.descr_analysis()
        self.plot_trend()
        self.ma()
        self.macd()
        self.plot_volume()
        plt.show()

