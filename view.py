from tkinter import *
import tkinter
from tkinter import messagebox
from tkinter.messagebox import *
import datetime as dt
from numpy.lib.function_base import insert
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import gui_predictor
import stock_analysis
import mat_form
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk #NavigationToolbar2TkAgg

# User Manual menu
class ManualFrame(Frame): # inherit the Frame class
    def __init__(self, master = None): 
        Frame.__init__(self, master) 
        self.root = master # define root
        self.createPage() 
  
    def createPage(self):
        Label(self, text = 'User Manual').pack()
        text = Text(self, width = 600, height = 400)  # create text area
        usermanual = open(r'USER MANUAL.txt', 'r', encoding = 'utf-8').read()
        text.insert("insert", usermanual)  # Show User Manual content
        text.config(state = DISABLED) # Disable User Manual to be modified
        text.pack()  

# Stock Analysis Sub-menu
class AnalyzerFrame(Frame): # inherit the Frame class 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master # define root
        self.df = pd.read_csv("stock_data.csv")  
        # define textbox and label type
        self.stockName = StringVar()
        self.startDateYear = StringVar()
        self.startDateMonth = StringVar()
        self.startDateDay = StringVar()
        self.endDateYear = StringVar()
        self.endDateMonth = StringVar()
        self.endDateDay = StringVar()     
        self.Entry_stockname =  Entry(self, textvariable = self.stockName)
        self.Entry_startDateYear =  Entry(self, textvariable = self.startDateYear)
        self.Entry_startDateMonth =  Entry(self, textvariable = self.startDateMonth)
        self.Entry_startDateDay =  Entry(self, textvariable = self.startDateDay)
        self.Entry_endDateYear =  Entry(self, textvariable = self.endDateYear)
        self.Entry_endDateMonth =  Entry(self, textvariable = self.endDateMonth)
        self.Entry_endDateDay =  Entry(self, textvariable = self.endDateDay)
        self.createPage() 
    
  
    def createPage(self):      
        Label(self, text = 'Stock Analysis', font=('Arial', 20)).grid(row = 2, column = 1, sticky = N + S, columnspan = 5, rowspan = 2) # Stock Analysis label

        Label(self, text = 'Ticker', font=('Arial', 15)).grid(row = 5, column = 1,sticky = N + S, columnspan = 5)  # Ticker label
        self.Entry_stockname.grid(row = 6, column = 1, stick= N + S, columnspan = 5)  # Ticker textbox

        Label(self, text = 'Start Date',font = ('Arial', 15)).grid(row = 7, column = 1, sticky = N + S, columnspan = 5, rowspan = 2)  # Start Date label
        Label(self, text = 'Year',font = ('Arial', 13)).grid(row = 9, column = 2,sticky = N + S)  # Start Year label
        Label(self, text = 'Month',font = ('Arial', 13)).grid(row = 9, column = 3,sticky = N + S)  # Start Month label
        Label(self, text = 'Day',font = ('Arial', 13)).grid(row = 9, column = 4,sticky = N + S)  # Start Day label
        self.Entry_startDateYear.grid(row = 10, column = 2, stick = N + S)  # Start Year textbox
        self.Entry_startDateMonth.grid(row = 10, column = 3, stick = N + S) # Start Month textbox
        self.Entry_startDateDay.grid(row = 10, column = 4, stick = N + S)  # Start Day textbox

        Label(self, text = 'End Date', font = ('Arial',15)).grid(row = 11, column = 1, sticky = N + S, columnspan = 5, rowspan = 2)  # End Date label
        Label(self, text = 'Year', font = ('Arial',13)).grid(row = 13, column = 2, sticky = N + S)  # End Year label
        Label(self, text = 'Month', font = ('Arial',13)).grid(row = 13, column = 3, sticky = N + S)  # End Month label
        Label(self, text = 'Day', font = ('Arial',13)).grid(row = 13, column = 4, sticky= N + S)  # End Day label
        self.Entry_endDateYear.grid(row = 14, column = 2, stick = N + S)  # End Year textbox
        self.Entry_endDateMonth.grid(row = 14, column = 3, stick = N + S) # End Month textbox
        self.Entry_endDateDay.grid(row = 14, column = 4, stick = N + S)  # End Date textbox

        Label(self).grid(row = 15, stick = W, pady = 10, rowspan = 3) 

        # Define button
        Button(self, text='Search', font = ('Arial', 20), command = self.main, width = 6, height = 1).grid(row = 19, column = 2, stick = N + S, columnspan = 3)
    
    # Get start date
    def get_start_date(self):
        start_date = None
        try:
            start_year = int(self.Entry_startDateYear.get())
            start_month = int(self.Entry_startDateMonth.get())
            start_day = int(self.Entry_startDateDay.get())
            start_date = dt.datetime(start_year, start_month, start_day)
            return start_date
        except:
            print('Invalid Start Date!')

    # Get end date
    def get_end_date(self):
        end_date = None
        try:
            end_year = int(self.Entry_endDateYear.get())
            end_month = int(self.Entry_endDateMonth.get())
            end_day = int(self.Entry_endDateDay.get())
            end_date = dt.datetime(end_year, end_month, end_day)
            return end_date
        except:
            print('Invalid End Date!')

    # check date
    def check_date(self):
        start_date = self.get_start_date()
        end_date = self.get_end_date()

        if start_date:  
            if end_date:  
                if start_date >= dt.datetime.now() or start_date < dt.datetime(2000,1,1) or end_date <= dt.datetime(2000,1,1) or end_date > dt.datetime.now():
                    # print("Start date and end date must be between Jan 1, 2000 - today. Please input again.")
                    messagebox.showinfo('Info','Start date and end date must be between Jan 1, 2000 - today. Please input again.') 
                    start_date = self.get_start_date()
                    end_date = self.get_end_date()
                elif start_date >= end_date:
                    # print("Start date must be an earlier date than end date!!!")
                    messagebox.showinfo('Info','Start date must be an earlier date than end date!!!') 
                    start_date = self.get_start_date()
                    end_date = self.get_end_date()
                return start_date, end_date
            else:
                messagebox.showinfo('Info','Invalid End Date!')
        else:
            messagebox.showinfo('Info','Invalid Start Date!')
    
    # Get ticker
    def get_ticker(self):
        ticker = self.Entry_stockname.get().upper()
        try:
            pdr.get_data_yahoo(ticker, start = dt.datetime(2021, 11, 23), end = dt.datetime(2021, 11, 24))
            return ticker
        except:
            # print("No Such Ticker!")
            messagebox.showinfo('Info','No Such Ticker!') 

    # Get data
    def get_data(self):
        ticker = self.get_ticker()
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        if self.df['Ticker'].str.contains(ticker).any():
            index = np.where((self.df.Ticker == ticker) & (self.df.Date >= start_date) & (self.df.Date <= end_date))
            if index[0].size:
                return self.df.iloc[index]
            else:
                return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()
        else:
            return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()

    # Check data
    def check_data(self):
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        if self.check_date() and self.get_ticker():
            try:
                data = self.get_data()
                return data
            except:
                messagebox.showinfo('Info','No stock information between chosen dates.')
  
    # Analysis function    
    def main(self):
        data = self.check_data()
        if not data.empty: # Analysis is performed only when the data is not empty
            form = mat_form.Form(data)
            f = form.create_matplotlib()
            canvas = FigureCanvasTkAgg(f, master=self.root)
            form.create_form(f)

# Stock Predictor Sub-menu
class PredictorFrame(Frame): 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master 
        self.df = pd.read_csv("stock_data.csv") 

        self.stockName = StringVar()
        self.startDateYear = StringVar()
        self.startDateMonth = StringVar()
        self.startDateDay = StringVar()
        self.endDateYear = StringVar()
        self.endDateMonth = StringVar()
        self.endDateDay = StringVar() 
        self.predictionDateYear = StringVar()
        self.predictionDateMonth = StringVar()
        self.predictionDateDay = StringVar()
        self.predictionResult = StringVar()
        self.Entry_stockname =  Entry(self, textvariable = self.stockName)
        self.Entry_startDateYear =  Entry(self, textvariable = self.startDateYear)
        self.Entry_startDateMonth =  Entry(self, textvariable = self.startDateMonth)
        self.Entry_startDateDay =  Entry(self, textvariable = self.startDateDay)
        self.Entry_endDateYear =  Entry(self, textvariable = self.endDateYear)
        self.Entry_endDateMonth =  Entry(self, textvariable = self.endDateMonth)
        self.Entry_endDateDay =  Entry(self, textvariable = self.endDateDay)
        self.Entry_predictionDateYear =  Entry(self, textvariable = self.predictionDateYear)
        self.Entry_predictionDateMonth =  Entry(self, textvariable = self.predictionDateMonth)
        self.Entry_predictionDateDay =  Entry(self, textvariable = self.predictionDateDay)
        self.Entry_predictionResult =  Entry(self, textvariable=self.predictionResult)
        self.createPage() 
  
    def createPage(self): 
        Label(self, text = 'Stock Prediction',font = ('Arial', 20)).grid(row = 2, column = 1, sticky = N + S, columnspan = 5, rowspan = 2) # Stock Prediction

        Label(self, text = 'Ticker',font = ('Arial', 15)).grid(row = 5, column = 1, sticky = N + S,columnspan = 5)  # Ticker label
        self.Entry_stockname.grid(row = 6, column = 1, stick= N + S,columnspan = 5)  # Ticker textox

        Label(self, text = 'Start Date of Training Data',font=('Arial',15)).grid(row=7, column = 1, sticky = N + S, columnspan = 5, rowspan = 2)  # Start Date label
        Label(self, text = 'Year',font=('Arial', 13)).grid(row = 9, column = 2, sticky = N + S)  # Start Year label
        Label(self, text = 'Month',font=('Arial', 13)).grid(row = 9, column = 3, sticky = N + S)  # Start Month label
        Label(self, text = 'Day',font=('Arial', 13)).grid(row = 9, column = 4, sticky = N + S)  # Start Day label

        self.Entry_startDateYear.grid(row = 10, column = 2, stick = N + S)  # Start Year textbox
        self.Entry_startDateMonth.grid(row = 10, column = 3, stick = N + S) # Start Month textbox
        self.Entry_startDateDay.grid(row = 10, column = 4, stick = N + S)  # Start Day textbox

        Label(self, text = 'End Date of Training Data',font=('Arial',15)).grid(row = 11, column = 1,sticky = N + S, columnspan = 5, rowspan = 2)  # End Date label
        Label(self, text = 'Year',font=('Arial', 13)).grid(row = 13, column = 2,sticky = N + S)  # End Year label
        Label(self, text = 'Month',font=('Arial', 13)).grid(row = 13, column = 3,sticky = N + S)  # End Month label
        Label(self, text = 'Day',font=('Arial', 13)).grid(row = 13, column = 4,sticky = N + S)  # End Day label

        self.Entry_endDateYear.grid(row = 14, column = 2, stick = N + S)  # End Year textbox
        self.Entry_endDateMonth.grid(row = 14, column = 3, stick = N + S) # End Month textbox
        self.Entry_endDateDay.grid(row = 14, column = 4, stick = N + S)  # End Date textbox

        Label(self, text = 'Prediction Date', font=('Arial', 15)).grid(row = 17, column = 1, sticky = N + S, columnspan = 5, rowspan = 2)  # Prediction Date label
        Label(self, text = 'Year', font=('Arial', 13)).grid(row = 20, column = 2,sticky = N + S)  # Prediction Year label
        Label(self, text = 'Month', font=('Arial', 13)).grid(row = 20, column = 3,sticky = N + S)  # Prediction Month label
        Label(self, text = 'Day', font=('Arial', 13)).grid(row = 20, column = 4, sticky = N + S)  # Prediction Day label

        self.Entry_predictionDateYear.grid(row = 21, column = 2, stick = N + S)  # Prediction Year textbox
        self.Entry_predictionDateMonth.grid(row = 21, column = 3, stick = N + S) # Prediction Month textbox
        self.Entry_predictionDateDay.grid(row = 21, column = 4, stick = N + S)  # Prediction Date textbox

        self.text_Result = Text(self, width = 60, height = 20)  # create result text area

        # Label(self).grid(row = 22, stick = W, pady = 10,rowspan = 5) 
        Label(self, text = 'Prediction Result', font=('Arial', 15)).grid(row = 23, column = 1, sticky = N + S, columnspan = 5, rowspan = 2)  # Prediction Result label
        # create text result area
        self.text_Result.grid(row = 30 , column = 2, stick = N + S ,columnspan = 5)
        # define button
        Button(self, text = 'Predict', font=('Arial', 20),command = self.main, width = 6, height = 1).grid(row = 28, column = 2, stick = N + S, columnspan = 3)

    # get start date
    def get_start_date(self):
        start_date = None
        try:
            start_year = int(self.Entry_startDateYear.get())
            start_month = int(self.Entry_startDateMonth.get())
            start_day = int(self.Entry_startDateDay.get())
            start_date = dt.datetime(start_year,start_month,start_day)
            return start_date
        except:
            messagebox.showinfo('Info','Invalid Date!') 

    # get end date
    def get_end_date(self):
        end_date = None
        try:
            end_year = int(self.Entry_endDateYear.get())
            end_month = int(self.Entry_endDateMonth.get())
            end_day = int(self.Entry_endDateDay.get())
            end_date = dt.datetime(end_year,end_month,end_day)
            return end_date
        except:
            messagebox.showinfo('Info','Invalid Date!') 

    # get prediction date
    def get_prediction_date(self):
        try:
            prediction_year = int(self.Entry_predictionDateYear.get())
            prediction_month = int(self.Entry_predictionDateMonth.get())
            prediction_day = int(self.Entry_predictionDateDay.get())
            prediction_date = np.array([prediction_year, prediction_month, prediction_day]).reshape(1, -1)
            return prediction_date
        except:
            messagebox.showinfo('Info','Invalid Date!') 

    # check date
    def check_date(self):
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        if start_date >= dt.datetime.now() or start_date < dt.datetime(2000,1,1) or end_date <= dt.datetime(2000,1,1) or end_date > dt.datetime.now():
            # print("Start date and end date must be between Jan 1, 2000 - today. Please input again.")
            messagebox.showinfo('Info','Start date and end date must be between Jan 1, 2000 - today. Please input again.') 
            start_date = self.get_start_date()
            end_date = self.get_end_date()
        elif start_date >= end_date:
            # print("Start date must be an earlier date than end date!!!")
            messagebox.showinfo('Info','Start date must be an earlier date than end date!!!') 
            start_date = self.get_start_date()
            end_date = self.get_end_date()
        return start_date, end_date
    
    # get ticker
    def get_ticker(self):
        ticker = self.Entry_stockname.get().upper()
        try:
            pdr.get_data_yahoo(ticker, start = dt.datetime(2021,11,23), end = dt.datetime(2021,11,24))
            return ticker
        except:
            messagebox.showinfo('Info','No Such Ticker!') 

    # get data
    def get_data(self):
        ticker = self.get_ticker()
        if ticker:
            start_date = self.get_start_date()
            end_date = self.get_end_date()
            if self.df['Ticker'].str.contains(ticker).any():
                index = np.where((self.df.Ticker == ticker) & (self.df.Date >= start_date) & (self.df.Date <= end_date))
                if index[0].size:
                    return self.df.iloc[index]
                else:
                    return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()
            else:
                return pd.DataFrame(pdr.get_data_yahoo(ticker, start = start_date, end = end_date)).reset_index()

    # check data
    def check_data(self):
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        if self.check_date():
            try:
                data = self.get_data()
                return data
            except:
                messagebox.showinfo('Info','No stock information between chosen dates.')
    
    # prediction functions   
    def main(self):
        data = self.check_data()
        if not data.empty:  # Prediction is performed only when the data is not empty
            predictors = gui_predictor.GUIPredictor(data, self.get_prediction_date())
            p = predictors.main()
            self.text_Result.insert('insert', p)






