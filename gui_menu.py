
import tkinter as tk
from view import * # the menu bar corresponds to each subpage 
  
class MainPage(object): 
    def __init__(self, master = None): 
        self.root = master # define the internal variable root 
        self.root.geometry('%dx%d' % (1000, 800)) # Set the window size
        self.create_page() 
  
    def create_page(self): 
        """Create three pages for the three options."""
        self.ManualPage = ManualFrame(self.root) # create different Frames 
        self.analyzerPage = AnalyzerFrame(self.root) 
        self.predictorrPage = PredictorFrame(self.root) 
        self.ManualPage.pack() # Default display of data entry screen 
        menubar = Menu(self.root) 
        menubar.add_command(label = 'User Manual', command = self.user_manual) 
        menubar.add_command(label = 'Stock Analyzer', command = self.stock_analyzer) 
        menubar.add_command(label = 'Stock Predictor', command = self.stock_predictor) 
        self.root['menu'] = menubar # set menu bar 

    def user_manual(self): 
        self.ManualPage.pack() 
        self.analyzerPage.pack_forget() 
        self.predictorrPage.pack_forget() 
        
    def stock_analyzer(self): 
        self.ManualPage.pack_forget() 
        self.analyzerPage.pack() 
        self.predictorrPage.pack_forget()

    def stock_predictor(self): 
        self.ManualPage.pack_forget() 
        self.analyzerPage.pack_forget() 
        self.predictorrPage.pack() 

if __name__ == "__main__":
    root = tk.Tk() 
    root.title('Stock Analyzer and Stock Predictor') 
    MainPage(root) 
    root.mainloop() 