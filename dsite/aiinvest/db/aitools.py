
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from aisettings import Aiconfig
import pathlib

LOGGING_FILE_NAME = Aiconfig.get('LOGGING_FILE_NAME')

class Message_Area():
    messagearea = ""
    def __init__(self) -> None:
        pass

def display_message(message:str, st:ScrolledText=None):
    """
    Display message to a scrolledText if given. otherwise, output to the sys.stdout
    """
    if str and st and isinstance(st, ScrolledText):
        st.pack()
        st.insert(tk.END, message+"\n")
        st.see(tk.END)
    
    elif str:
        with open(LOGGING_FILE_NAME,'a') as file:
            file.writelines(f"{message}\n")
            if Aiconfig.get('DEBUG'):
                print(message)

# display_message("x lines now ...")