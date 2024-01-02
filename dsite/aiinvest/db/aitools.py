
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from aisettings import Aiconfig
import logging
import threading

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


logging.basicConfig(filename='log/ailog.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    

import queue
def test():
    q = queue.Queue()

    def worker():
        while True:
            item = q.get()
            print(f'Working on {item}')
            print(f'Finished {item}')
            q.task_done()

    # Turn-on the worker thread.
    threading.Thread(target=worker, daemon=True).start()

    # Send thirty task requests to the worker.
    for item in range(30):
        q.put(item)

    # Block until all tasks are done.
    q.join()
    print('All work completed')