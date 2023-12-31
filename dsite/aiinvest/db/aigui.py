
"""
Copyright (C) Steven Jiang. All rights reserved. This code is subject to the terms
 and conditions of the MIT Non-Commercial License, as applicable.
build the GUI for ai trading
"""

from tkinter import *

import matplotlib, sys
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

# from matplotlib import colormaps
# print(list(colormaps))


root = Tk()
'''
widgets are added here
'''
root.title("AI Invest APP")

#  menu start here
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

#################### draw by matplotlib start here 
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)
a.plot(t,s)

dataPlot = FigureCanvasTkAgg(f, master=root)

#################### draw by matplotlib start here 

lst = ['C', 'C++', 'Java',
       'Python', 'Perl',
       'PHP', 'ASP', 'JS']


def check_input(event):
    value = event.widget.get()

    if value == '':
        combo_box['values'] = lst
    else:
        data = []
        for item in lst:
            if value.lower() in item.lower():
                data.append(item)

        combo_box['values'] = data

# function to be called when button-2 of mouse is pressed
def pressed2(event):
    print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))
 
# function to be called when button-3 of mouse is pressed
def pressed3(event):
    print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))
 
## function to be called when button-1 is double clocked
def double_click(event):
    print('Double clicked at x = % d, y = % d'%(event.x, event.y))

topframe = Frame(root)
redbutton = Button(topframe, text = 'Red', fg ='red')
greenbutton = Button(topframe, text = 'Brown', fg='brown')
bluebutton = Button(topframe, text ='Blue', fg ='blue')
label_ai = Label(topframe, text='AI Invest')

# these lines are binding mouse buttons with the button widget
redbutton.bind('<Button-2>', pressed2)
redbutton.bind('<Button-3>', pressed3)
redbutton.bind('<Double 1>', double_click)

# creating Combobox
combo_box = ttk.Combobox(topframe)
combo_box['values'] = lst
combo_box.bind('<KeyRelease>', check_input)

middleframe = Frame(root)
scrollbar = Scrollbar(middleframe)
mylist = Listbox(middleframe, yscrollcommand = scrollbar.set )

for line in range(10):
   mylist.insert(END, 'This is line number' + str(line))

scrollbar.config( command = mylist.yview )


def go(event): 
    cs = Lb.curselection() 
      
    # Setting Background Colour 
    for list in cs: 
          
        if list == 0: 
            middleframe.configure(background='red') 
        elif list == 1: 
            middleframe.configure(background='green') 
        elif list == 2: 
            middleframe.configure(background='yellow') 
        elif list == 3: 
            middleframe.configure(background='white') 

# Creating Listbox 
Lb = Listbox(middleframe, height=6) 
# Inserting items in Listbox 
Lb.insert(0, 'Red') 
Lb.insert(1, 'Green') 
Lb.insert(2, 'Yellow') 
Lb.insert(3, 'White') 
   
# Binding double click with left mouse button with go function 
Lb.bind('<Double-1>', go) 



bottomframe = Frame(root)
order_button = Button(bottomframe, text='Order',fg = 'black', activebackground="green", bg="red", width=25, command=root.destroy)
ourMessage ='This is our Message'
messageVar = Message(bottomframe, text = ourMessage, width=180)
messageVar.config(bg='lightgreen')


# layout start here.
topframe.pack(side=TOP,fill="x")
label_ai.pack(side = 'top')
redbutton.pack( side = LEFT)
greenbutton.pack( side = LEFT )
bluebutton.pack( side = RIGHT )
combo_box.pack(side = 'right')

dataPlot.get_tk_widget().pack(side=TOP, fill="x", expand=1)

middleframe.pack(side = 'top')
scrollbar.pack( side = RIGHT, fill = Y )
mylist.pack( side = 'right', fill = BOTH )
Lb.pack(side='left') 

bottomframe.pack( side = BOTTOM )
order_button.pack(side = 'left')
messageVar.pack(side = 'bottom')

# add righ click menu to the app. those menu could bind different command.
m = Menu(root, tearoff = 0) 
m.add_command(label ="Cut") 
m.add_command(label ="Copy") 
m.add_command(label ="Paste") 
m.add_command(label ="Reload") 
m.add_separator() 
m.add_command(label ="Rename") 
  
def do_popup(event): 
    try: 
        m.tk_popup(event.x_root, event.y_root) 
    finally: 
        m.grab_release() 

# For most mice, this will be '1' for left button, '2' for middle, '3' for right.
root.bind("<Button-2>", do_popup) 


# function to be called when
# keyboard buttons are pressed
def key_press(event):
    
    key = event.char
    print(key, 'is pressed')
    print(event, 'event')

# here we are binding keyboard
# with the main window
root.bind('<Key>', key_press)

''' #
canvas = tk.Canvas(root, width=600, height=600)
canvas.create_rectangle(30,30,100,100)
canvas.pack()

var1 = tk.IntVar()
checkbox1 = tk.Checkbutton(root, text='male', variable=var1)
checkbox1.pack()

var2 = tk.IntVar()
checkbox2 = tk.Checkbutton(root, text='female', variable=var2)
checkbox2.pack()

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

root.mainloop()