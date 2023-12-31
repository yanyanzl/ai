
"""
Copyright (C) Steven Jiang. All rights reserved. This code is subject to the terms
 and conditions of the MIT Non-Commercial License, as applicable.
build the GUI for ai trading
"""

from tkinter import *

import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from tkterminal import Terminal
from tkinter import messagebox
from aisettings import Aiconfig

# from matplotlib import colormaps
# print(list(colormaps))

#################### draw by matplotlib start here 


def main():

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


    def select_symbol(event): 

        cs = symbol_list_box.curselection() 
        # the index of the selected element in the list
        print(symbol_list_box.curselection())

        # the selected element
        print(symbol_list_box.selection_get())

        # the event , like : <ButtonPress event num=1 x=35 y=48>
        print(f"event: {event}")


    def do_popup(event): 
        try: 
            m.tk_popup(event.x_root, event.y_root) 
        finally: 
            m.grab_release() 

    # function to be called when
    # keyboard buttons are pressed
    def key_press(event):
        
        key = event.char
        print(key, 'is pressed')
        print(event, 'event')

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
    symbol_list_box = Listbox(middleframe, yscrollcommand = scrollbar.set )

    symbol_list = Aiconfig.get("ASSET_LIST")
    i = 0
    for line in symbol_list:
        symbol_list_box.insert(i, line)
        i += 1
    symbol_list_box.bind('<Double-1>', select_symbol) 
    scrollbar.config( command = symbol_list_box.yview )


    bottomframe = Frame(root)
    order_button = ttk.Button(bottomframe, text='Order', width=25, command=root.destroy)
    ourMessage ='This is our Message'
    messageVar = Message(bottomframe, text = ourMessage, width=180)
    messageVar.config(bg='lightgreen')

    # import os
    # term_frame = Frame(root, height=100, width=500)

    # term_frame.pack(side='bottom', fill=BOTH, expand=YES)
    # wid = term_frame.winfo_id()
    # # os.system('xterm -into %d -geometry 40x20 -sb &' % wid)    
    # os.system('sh -into %d' % wid) 
    terminal = Terminal(pady=5, padx=5, background='green', height=10)
    terminal.pack(side='bottom', expand=True, fill='both')
    terminal.shell = True
    terminal.configure(foreground='yellow')
    terminal.basename = "AI$"
    # terminal.linebar = True


    ############# layout start here.
    topframe.pack(side=TOP,fill="x")
    label_ai.pack(side = 'top')
    redbutton.pack( side = LEFT)
    greenbutton.pack( side = LEFT )
    bluebutton.pack( side = RIGHT )
    combo_box.pack(side = 'right')

    middleframe.pack(side = 'right')
    scrollbar.pack( side = RIGHT, fill = Y )
    symbol_list_box.pack( side = 'right', fill = BOTH )

    dataPlot.get_tk_widget().pack(side=TOP, fill="y", expand=1)

    bottomframe.pack( side = 'bottom' )
    order_button.pack(side = 'left')
    messageVar.pack(side = 'bottom')


    ############# style : add styling to any widget which are available 
    style = ttk.Style() 
    style.configure('TButton', foreground = 'green') 
    symbol_list_box.configure(foreground='orange')
    root.configure(background='lightblue')

    # add righ click menu to the app. those menu could bind different command.
    m = Menu(root, tearoff = 0) 
    m.add_command(label ="Cut") 
    m.add_command(label ="Copy") 
    m.add_command(label ="Paste") 
    m.add_command(label ="Reload") 
    m.add_separator() 
    m.add_command(label ="Rename") 
    
    # For most mice, this will be '1' for left button, '2' for middle, '3' for right.
    root.bind("<Button-2>", do_popup) 

    # here we are binding keyboard with the main window
    root.bind('<Key>', key_press)

    root.mainloop()



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

    # in after method 5000 milliseconds
    # is passed i.e after 5 seconds
    # a message will be prompted
    # root.after(5000, lambda : messagebox.showinfo('Title', 'Prompting after 5 seconds'))


if __name__ == "__main__":
    main()