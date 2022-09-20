import tkinter as tk
from tkinter import ttk
from turtle import width

from gui.BasicCalc import BasicCalc

class MainGUI:
  def __init__(self):


    # Main GUI window creation
    self.root = tk.Tk()
    self.root.geometry('600x400')
    self.root.wm_title('Engineering Calculator')

    # Create tab control
    tabCtrl = ttk.Notebook(self.root)
    tabCtrl.pack(expand=1, fill="both")
    # Create the tabs
    basicCalcTab = ttk.Frame(tabCtrl)
    tab2 = ttk.Frame(tabCtrl)
    # Add the tabs
    tabCtrl.add(basicCalcTab, text='Basic Calculator', padding=5)
    tabCtrl.add(tab2, text='Tab 2')

    # Add the widget for each tab
    self.basicCalc = BasicCalc(self.root, basicCalcTab)


  def start(self):
    """Start the app GUI"""
    self.root.mainloop()