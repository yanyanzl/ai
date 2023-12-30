# this is a learning file for IB TWS connection


from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
# from ibapi.ticktype import TickTypeEnum
# from ibapi.execution  import Execution

from ibapi.common import * # @UnusedWildImport
from ibapi.utils import * # @UnusedWildImport
from ibapi.order import *
from pynput import keyboard
from pynput.keyboard import KeyCode

import pandas
import threading
import time

from aiapp import *
from aiorder import *
from aicontract import *
         
# from decimal import Decimal

DEBUG = True

PLACE_BUY_ORDER = keyboard.Key.f1
PLACE_SELL_ORDER = keyboard.Key.f5

CANCEL_LAST_ORDER = [{keyboard.Key.shift, KeyCode(char="c")},{keyboard.Key.shift, KeyCode(char="C")}]
CANCEL_ALL_ORDER = [{keyboard.Key.shift, keyboard.Key.backspace}, {keyboard.Key.shift, keyboard.Key.delete}]

PLACE_IOC_BUY = keyboard.Key.f9
PLACE_IOC_SELL = keyboard.Key.f12

PLACE_STOP_BUY = keyboard.Key.f10
PLACE_STOP_SELL = keyboard.Key.f11

PLACE_BRACKET_BUY = keyboard.Key.f7
PLACE_BRACKET_SELL  = keyboard.Key.f8

REQ_OPEN_ORDER = [{keyboard.Key.shift, KeyCode(char="o")},{keyboard.Key.shift, KeyCode(char="O")}]

TICK_BIDASK = [{keyboard.Key.shift, KeyCode(char="t")},{keyboard.Key.shift, KeyCode(char="T")}]
CANCEL_TICK_BIDASK = [{keyboard.Key.shift, KeyCode(char="r")},{keyboard.Key.shift, KeyCode(char="R")}]

SHOW_PORT = [{keyboard.Key.shift, KeyCode(char="p")},{keyboard.Key.shift, KeyCode(char="P")}]
SHOW_SUMMARY = [{keyboard.Key.shift, KeyCode(char="s")},{keyboard.Key.shift, KeyCode(char="S")}]

MULTIPLY = KeyCode(char="*")
ADD = KeyCode(char="+")
SEPARATOR = KeyCode(char=".")  # this is locale-dependent.
SUBTRACT = KeyCode(char="-")
DIVIDE = KeyCode(char="/")
NUMPAD0 = KeyCode(char="0")


BUY_LMT_PLUS = 0.05
SELL_LMT_PLUS = -0.05


# get the histroy data for a contract
def get_his_data(app=AiApp(),contract=Contract()):
    #Request historical candles
    app.reqHistoricalData(1, contract, '', '5 D', '1 hour', 'BID', 0, 2, False, [])

    #Sleep interval to allow time for incoming price data. 
    # without this sleep. the data will be empty
    time.sleep(2) 
    # transform data to Dataframe format. 
    df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
    df['DateTime'] = pandas.to_datetime(df['DateTime'],unit="s")

    # 20 SMA of the close price.
    df['20SMA'] = df['Close'].rolling(20).mean()
    # print(df.tail(10))


def main():

    def run_loop():
        app.run()

    app = AiApp()
    print("program is starting ...")
    app.connect('127.0.0.1', 7497, 16)
    # app.connect('192.168.1.146', 7497, 1)
    
    print(app.isConnected())

    app.nextorderId = None
    
    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    #Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            print('connected')
            break
        else:
            print('waiting for connection')
            time.sleep(1)

    time.sleep(1) #Sleep interval to allow time for connection to server

    # requre all the 
    app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)

    #Sleep interval to allow time for response data from server
    time.sleep(2) 

    # The IBApi.EClient.reqAccountUpdates function creates a subscription to the TWS through which account and portfolio information is delivered. This information is the exact same as the one displayed within the TWS’ Account Window. Just as with the TWS’ Account Window, unless there is a position change this information is updated at a fixed interval of three minutes.
    app.reqAccountUpdates(True, app.account)

    #Create contract object
    contract = stock_contract('AAPL')

    #Request Market Data. should be in market open time.
    app.reqMarketDataType(3) # -1 is real time stream. 3 is delayed data.
    app.reqMktData(1, contract, '', True, False, [])
    # time.sleep(2)


    ################ keyboard input monitoring part start
    # monitoring the keyboard and make it available to control the order
    combo_key = set()

    def on_press(key):
        try:
            
            # print('alphanumeric key pressed', key.char.lower())

            # place limit buy order Tif = day
            if key == PLACE_BUY_ORDER:
                place_lmt_order(app,contract, "BUY", increamental=BUY_LMT_PLUS)

            # place limit buy order Tif = day
            elif key == PLACE_SELL_ORDER:
                place_lmt_order(app,contract, "SELL", increamental=SELL_LMT_PLUS)
            
            # cancel last order
            elif any([key in COMBO for COMBO in CANCEL_LAST_ORDER]): # Checks if pressed key is in any combinations
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in CANCEL_LAST_ORDER): # Checks if every key of the combination has been pressed
                    cancel_last_order(app)
                    combo_key.clear()

            # cancel all orders
            elif any([key in COMBO for COMBO in CANCEL_ALL_ORDER]): # Checks if pressed key is in any combinations
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in CANCEL_ALL_ORDER): # Checks if every key of the combination has been pressed
                    cancel_all_order(app)
                    combo_key.clear()

            elif key == PLACE_IOC_BUY:
                 place_lmt_order(app,contract, "BUY", tif="IOC", increamental=BUY_LMT_PLUS, priceTickType="ASK")
            
            elif key ==  PLACE_IOC_SELL:
                 place_lmt_order(app,contract, "SELL", tif="IOC", increamental=SELL_LMT_PLUS, priceTickType="BID")
            
            ########### to be completed
            elif key ==  PLACE_STOP_SELL:
                 pass
            
            elif key ==  PLACE_STOP_BUY:
                 pass
            
            elif key ==  PLACE_BRACKET_BUY:
                 pass
            
            elif key ==  PLACE_BRACKET_SELL:
                 pass
            
            elif any([key in COMBO for COMBO in REQ_OPEN_ORDER]): #  Requests all current open orders in associated accounts at the current moment. The existing orders will be received via the openOrder and orderStatus events. Open orders are returned once; this function does not initiate a subscription.
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in REQ_OPEN_ORDER): # Checks if every key of the combination has been pressed
                    print("requesting all Open orders from server now ...")
                    app.reqAllOpenOrders()

                    combo_key.clear()

            elif any([key in COMBO for COMBO in TICK_BIDASK]): 
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in TICK_BIDASK): # Checks if every key of the combination has been pressed
                    print("requesting tick by tick bidask data from server now ...")
                    app.reqTickByTickData(19003, contract, "BidAsk", 0, True)
                    combo_key.clear()

            elif any([key in COMBO for COMBO in CANCEL_TICK_BIDASK]): 
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in CANCEL_TICK_BIDASK): # Checks if every key of the combination has been pressed
                    print("cancelling tick by tick bidask data from server now ...")
                    app.cancelTickByTickData(19003)
                    combo_key.clear()

            elif any([key in COMBO for COMBO in SHOW_PORT]): 
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in SHOW_PORT): # Checks if every key of the combination has been pressed
                    show_portforlio(app)
                    combo_key.clear()

            elif any([key in COMBO for COMBO in SHOW_SUMMARY]): 
                combo_key.add(key)
                if any(all (k in combo_key for k in COMBO) for COMBO in SHOW_SUMMARY): # Checks if every key of the combination has been pressed
                    show_summary(app)
                    combo_key.clear()

            else:
                 if DEBUG:
                      print(f"{key} is not defined for any function now ...")

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        # print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            print("Stopping Listener...")

            # Once the subscription to account updates is no longer needed, it can be cancelled by invoking the IBApi.EClient.reqAccountUpdates method while specifying the susbcription flag to be False.
            app.reqAccountUpdates(False, app.account)
            time.sleep(1) 
            print("Exiting Program...")
            app.disconnect()
            return False
        
        # in case only part of the key pressed. those key should be removed from combo_key.
        elif any([key in combo_key]):
             combo_key.remove(key)
             print(f"removing...{key}")


    # in a non-blocking fashion:
    # A keyboard listener is a threading.Thread, and all callbacks will be invoked from the thread.
    # Call pynput.keyboard.Listener.stop from anywhere, raise StopException or return False from a callback to stop the listener.
    # The key parameter passed to callbacks is a pynput.keyboard.Key, for special keys, a pynput.keyboard.KeyCode for normal alphanumeric keys, or just None for unknown keys.
    # When using the non-blocking version above, the current thread will continue executing. This might be necessary when integrating with other GUI frameworks that incorporate a main-loop, but when run from a script, this will cause the program to terminate immediately.
    listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
    listener.start()
    # app.disconnect()
 
    # def on_activate_h():
    #     print('<ctrl>+<alt>+h pressed')

    # def on_activate_i():
    #     print('<ctrl>+<alt>+i pressed')

    # print("before hotkeys start() ... ")
    # hotkeys_listener =  
    # try:
    #     # with keyboard.GlobalHotKeys({
    #     #         '<ctrl>+<alt>+h': on_activate_h,
    #     #         '<ctrl>+<alt>+i': on_activate_i}) as hotkeys_listener:
    #     #     hotkeys_listener.join()
    #     def on_activate():
    #         print('Global hotkey activated!')

    #     def for_canonical(f):
    #         return lambda k: f(l.canonical(k))

    #     hotkey = keyboard.HotKey(
    #         keyboard.HotKey.parse('<ctrl>+<alt>+h'),
    #         on_activate)
    #     with keyboard.Listener(
    #             on_press=for_canonical(hotkey.press),
    #             on_release=for_canonical(hotkey.release)) as l:
    #         l.join() 
    # except Exception as ex:
    #      print(f"starting hotkeys failed. {type(ex).__name__}, {ex.args}")

    # hotkeys_listener.start()

    ################ keyboard input monitoring part end
    
if __name__ == "__main__":
    main()
