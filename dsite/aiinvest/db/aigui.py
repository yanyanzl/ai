
"""
Copyright (C) Steven Jiang. All rights reserved. This code is subject to the terms
 and conditions of the MIT Non-Commercial License, as applicable.
build the GUI for ai trading

Tkinter isn't thread safe, and the general consensus is that Tkinter doesn't work in a non-main thread
The main caveat is that the workers cannot interact with the Tkinter widgets. They will have to write data to a queue, and your main GUI thread will have to poll that queue.


"""

from tkinter import *

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from tkterminal import Terminal
from tkinter import messagebox
from aisettings import Aiconfig
from aitools import *
from aiapp import AiApp

import tkinter as tk

import numpy as np
import matplotlib
import pandas

matplotlib.use("TkAgg")


def get_plot(self, data:pandas.DataFrame=None):
    f = Figure(figsize=(4,4), dpi=100)
    a = f.add_subplot(111)
    t = arange(0.0,3.0,0.01)
    s = sin(2*pi*t)
    a.plot(t,s)
    return f

class AiGUIMenu(tk.Frame):
    def __init__(self, master = None) -> None:
            super().__init__(master)

            self.master = master
            self.pack()
            self.menu = None
            self.filemenu = None
            self.helpmenu = None
            self.create_menu(master)

    def create_menu(self, master:tk.Frame=None):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='New')
        self.filemenu.add_command(label='Open...')
        self.filemenu.add_separator()
        # self.filemenu.add_command(label='Exit', command=self.master.destroy)
        self.helpmenu = Menu( self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About')

class RightClickMenu(tk.Frame):

    menu = None
    def __init__(self, master = None) -> None:
            super().__init__(master)
        
            self.menu = None
            self.create_menu(master)

    def create_menu(self, master=None):
        
        self.menu = Menu(master, tearoff = 0) 
        self.menu.add_command(label ="Cut") 
        self.menu.add_command(label ="Copy") 
        self.menu.add_command(label ="Paste") 
        self.menu.add_command(label ="Reload") 
        self.menu.add_separator() 
        self.menu.add_command(label ="Rename")   

    def do_popup(self, event): 
        try: 
            self.menu.tk_popup(event.x_root, event.y_root) 
            display_message("popup menu...")
        finally: 
            self.menu.grab_release() 

class AIGUIFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.combo_box = None
        self.symbol_list = []
        self.message_area = None
        self.symbol_list_box = None
        self.initialized = False
        self.symbol_selected = ""

        self.draw_head_frame()
        self.draw_graph_frame()
        self.draw_message_frame()
        self.layout()
        self.style()
        # self.plot_graph()


    def check_input(self, event):
        value = event.widget.get()

        # change the input string to uppercase
        self.combo_str.set(self.combo_str.get().upper())
        print("value", self.combo_str.get())

        if value == '':
            self.combo_box['values'] = self.symbol_list
        else:
            data = []
            for item in self.symbol_list:
                if value.lower() in item.lower():
                    data.append(item)
            # print("data is :", data)
            self.combo_box['values'] = data
            # self.combo_box.current()
            # self.combo_box.configure(exportselection=True)

    def add_symbol(self, event):
        value = event.widget.get()
        message = f"the combox input value is : {value}"
        valid = True
        print(message)
        if value != '':
            if not value in self.symbol_list:
                if asset_is_valid(value):
                    message = message + "it is a valid asset symbol. adding to list below..."
                    self.symbol_list.append(value)
                    self.symbol_list_box.insert(len(self.symbol_list), value)
                    Aiconfig.set("ASSET_LIST", self.symbol_list)
                    
                    self.combo_box['values'] = self.symbol_list
                    
                else:
                    message = message + "it's not a valid asset symbol. please input again..."
                    valid = False
            self.combo_box.set('') 
            if valid:
                self._change_symbol_selected(value)
        else:
            message = message + "asset symbol input is empty. please input again..."
            valid = False
        if AiApp.has_message_queue():
            AiApp.message_q.put(message)  
        return valid
        

    # function to be called when button-2 of mouse is pressed
    def pressed2(event):
        print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))
    
    # function to be called when button-3 of mouse is pressed
    def pressed3(event):
        print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))
    
    ## function to be called when button-1 is double clocked
    def double_click(event):
        print('Double clicked at x = % d, y = % d'%(event.x, event.y))


    def select_symbol(self, event): 

        cs = self.symbol_list_box.curselection() 
        # the index of the selected element in the list
        print(cs)
        self._change_symbol_selected(self.symbol_list_box.selection_get())
        # the event , like : <ButtonPress event num=1 x=35 y=48>
        display_message(str(event), self.message_area)

    def _change_symbol_selected(self, symbol:str=""):
        # the selected element
        if symbol:
            self.symbol_selected = symbol
            if AiApp.has_message_queue():
                AiApp.message_q.put(Aiconfig.get("SYMBOL_CHANGED"))
            print(self.symbol_selected)


    def plot_graph(self, data=pandas.DataFrame([1,2,3,4])):

        # destroy previous one
        # self.graph.destroy()
        # draw a new frame and then plot
        # self.draw_graph_frame()
        self.figure = get_plot(pandas.DataFrame([1,2,3,4]))
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph)
        self.canvas.get_tk_widget().pack(side = 'top')


    def draw_graph_frame(self):
        self.graph = tk.LabelFrame(self, text='', 
                    font=("times new roman",16,"bold"),
                    bg="white",bd=1,relief=tk.GROOVE)
        self.graph.config(width=580,height=410)
        if not self.initialized:
            # self.figure = Figure(figsize=(6, 4), dpi=100)
            self.figure = get_plot(pandas.DataFrame([1,2,3,4]))
            self.canvas = FigureCanvasTkAgg(self.figure, self.graph)
            self.canvas.get_tk_widget().pack()
    
          
    def draw_head_frame(self):
        self.headframe = Frame(self)

        self.label_ai = Label(self.headframe, text='AI Invest')
        
        ourMessage ='This is our Message'
        self.messageVar = Message(self.headframe, text = ourMessage, width=180)
        
        self.button_frame = Frame(self.headframe)
        self.redbutton = Button(self.button_frame, text = 'Tick Data', fg ='green', width=10)
        self.bar_data_button = Button(self.button_frame, text = 'Realtime Bar Data', foreground ='green', width=10)
        self.order_button = Button(self.button_frame, text='Exit',foreground ='green', width=10)

        self.symbol_frame = Frame(self.headframe)

        self.scrollbar = Scrollbar(self.symbol_frame)
        self.symbol_list_box = Listbox(self.symbol_frame, yscrollcommand = self.scrollbar.set )

        self.symbol_list = Aiconfig.get("ASSET_LIST")
        i = 0
        for line in self.symbol_list:
            self.symbol_list_box.insert(i, line)
            i += 1

        self.symbol_list_box.bind('<Double-1>', self.select_symbol) 
        self.scrollbar.config( command = self.symbol_list_box.yview )

        self.combo_str = StringVar(self)
        # creating Combobox
        self. combo_box = ttk.Combobox(self.symbol_frame,textvariable=self.combo_str)
        self.combo_box['values'] = self.symbol_list

        self.combo_box.bind('<KeyRelease>', self.check_input)
        self.combo_box.bind('<Return>', self.add_symbol)
        self.combo_box.bind("<<ComboboxSelected>>", self.add_symbol)

    def draw_message_frame(self):
        self.message_frame = Frame(self)
        self.message_area = ScrolledText(self.message_frame, foreground="yellow", background='green')

    # add a terminal to the application
    # terminal = Terminal(pady=5, padx=5, background='green', height=10)
    # terminal.pack(side='bottom', expand=True, fill='both')
    # terminal.shell = True
    # terminal.configure(foreground='yellow')
    # terminal.basename = "AI$"

    def layout(self):
        ############# layout start here.
        self.headframe.pack(side=TOP,fill="x")
        self.label_ai.pack(side = 'top')
        # self.messageVar.pack(side = 'bottom')
        self.button_frame.pack(side='left')
        self.symbol_frame.pack(side = 'right')

        self.combo_box.pack(side = 'top')
        self.scrollbar.pack( side = 'bottom', fill = Y )
        # self.symbol_list_box.pack( side = 'bottom', fill = BOTH )
        self.symbol_list_box.pack( side = 'bottom' )

        self.redbutton.pack( side = 'top')
        self.bar_data_button.pack(side='top')
        self.order_button.pack(side = 'bottom')

        self.graph.pack(side = "top")
        # self.dataPlot.get_tk_widget().pack(side=TOP, fill="y", expand=1)

        self.message_frame.pack(side='bottom')
        self.message_area.pack()

    def style(self):
        ############# style : add styling to any widget which are available 
        style = ttk.Style() 
        style.configure('TButton', foreground = 'green') 
        self.symbol_list_box.configure(foreground='orange')
        self.configure(background='lightblue')
        self.messageVar.config(bg='lightgreen')

    # def _action(self):
    #     # add righ click menu to the app. those menu could bind different command.
    #     self.right_click_menu = RightClickMenu(self)
        
    #     # For most mice, this will be '1' for left button, '2' for middle, '3' for right.
    #     self.bind("<Button-2>", self.right_click_menu.do_popup) 

    #     # here we are binding keyboard with the main window
    #     self.bind('<Key>', self.key_press)




    ''' #
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.create_rectangle(30,30,100,100)
    canvas.pack()

    #   grid
    var1 = tk.IntVar()
    tk.Checkbutton(root, text='male', variable=var1).grid(row=0, sticky='W')
    var2 = tk.IntVar()
    tk.Checkbutton(root, text='female', variable=var2).grid(row=1, sticky='W')
    '''

    # This widget is directly controlled by the window manager. It don’t need any parent window to work on
    # top = Toplevel()
    # top.title('Python')
    # top.mainloop()

    # in after method 5000 milliseconds
    # is passed i.e after 5 seconds
    # a message will be prompted
    # root.after(5000, lambda : messagebox.showinfo('Title', 'Prompting after 5 seconds'))

if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('800x800')
    root.wm_title('AI Investment')

    mainframe = AIGUIFrame(root)

    # create menu of the application
    menu = AiGUIMenu(root)

    # add righ click menu to the app. those menu could bind different command.
    right_click_menu = RightClickMenu(root)
    # For most mice, this will be '1' for left button, '2' for middle, '3' for right.
    root.bind("<Button-2>", right_click_menu.do_popup) 


    # root.bind('<Key>', key_press)
    # app = AiGUI(master=root)
    root.mainloop()

