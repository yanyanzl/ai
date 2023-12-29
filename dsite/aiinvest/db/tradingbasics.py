# this is a learning file for IB TWS connection

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

from ibapi.order import *
from pynput import keyboard
from pynput.keyboard import KeyCode

import pandas
import threading
import time
import os

# print(os.environ)
# print(os.get_exec_path())
         
from decimal import *

PLACE_BUY_ORDER = keyboard.Key.f9
PLACE_SELL_ORDER = keyboard.Key.f12

CANCEL_LAST_ORDER = KeyCode(char="c")


MULTIPLY = KeyCode(char="*")
ADD = KeyCode(char="+")
SEPARATOR = KeyCode(char=".")  # this is locale-dependent.
SUBTRACT = KeyCode(char="-")
DECIMAL = KeyCode(char=".")
DIVIDE = KeyCode(char="/")
NUMPAD0 = KeyCode(char="0")
NUMPAD1 = KeyCode(char="1")
NUMPAD2 = KeyCode(char="2")
NUMPAD3 = KeyCode(char="3")
NUMPAD4 = KeyCode(char="4")
NUMPAD5 = KeyCode(char="5")
NUMPAD6 = KeyCode(char="6")
NUMPAD7 = KeyCode(char="7")
NUMPAD8 = KeyCode(char="8")
NUMPAD9 = KeyCode(char="9")

BUY_LMT_PLUS = 0.05
SELL_LMT_PLUS = -0.05
ACCOUNT_COLUMNS=['key', 'value', 'currency']

class TestWrapper(EWrapper):

    # The API treats many items as errors even though they are not.
    def error(self, reqId, errorCode, errorMsg="", advancedOrderRejectJson=""):
         if errorCode == 202:
            print('order canceled - Reason ', errorMsg) 

class TestClient(EClient):
     def __init__(self, wrapper):
         EClient.__init__(self, wrapper)

class TestApp(TestWrapper, TestClient):
  
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.data = [] #Initialize variable to store data
        self.account = "" 
        #  account_info;` columns: key, value, currency`
        self.account_info = pandas.DataFrame()
        self.mkt_price = ""
        self.portfolio = []

    # overide the account Summary method. to get all the account summary information
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        # print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
        self.account = account
        if tag != None and tag != "":
             self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[tag, value, currency]],
                   columns=ACCOUNT_COLUMNS)])
            #  if not self.account_info.empty:
            #       self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[tag, value, currency]],
            #        columns=ACCOUNT_COLUMNS)])
            #  else: 
            #       self.account_info = pandas.DataFrame([[tag, value, currency]],
            #        columns=ACCOUNT_COLUMNS)

    # overide the account Summary end method. 
    # Notifies when all the accounts’ information has ben received.
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

    # Receiving Account Updates
    # Resulting account and portfolio information will be delivered via the IBApi.EWrapper.updateAccountValue, IBApi.EWrapper.updatePortfolio, IBApi.EWrapper.updateAccountTime and IBApi.EWrapper.accountDownloadEnd
        
    # Receives the subscribed account’s information. Only one account can be subscribed at a time. After the initial callback to updateAccountValue, callbacks only occur for values which have changed. This occurs at the time of a position change, or every 3 minutes at most. This frequency cannot be adjusted.
    def updateAccountValue(self, key: str, val: str, currency: str,accountName: str):
        # print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)
        if key != None and key != "":
            self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[key, val, currency]],
                   columns=ACCOUNT_COLUMNS)])
            # if not self.account_info.empty:
            #       self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[key, val, currency]],
            #        columns=ACCOUNT_COLUMNS)])
            # else: 
            #       self.account_info = pandas.DataFrame([[key, val, currency]],
            #        columns=ACCOUNT_COLUMNS)

    # Receives the subscribed account’s portfolio. This function will receive only the portfolio of the subscribed account. After the initial callback to updatePortfolio, callbacks only occur for positions which have changed.

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
         # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",contract.exchange, "Position:", position, "MarketPrice:", marketPrice,"MarketValue:", marketValue, "AverageCost:", averageCost, "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        #   to save those portfolio positions information to a dataset.
        self.portfolio.append([contract.symbol,contract.secType, contract.exchange,position,marketPrice,marketValue,averageCost, unrealizedPNL,realizedPNL])


    # Receives the last time on which the account was updated.
    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)

    # Notifies when all the account’s information has finished.
    def accountDownloadEnd(self, accountName: str):
        print("AccountDownloadEnd. Account:", accountName)

    # after reqMktData, this function is used to receive the data.
    def tickPrice(self, reqId, tickType, price, attrib):
            # for i in range(91):
            #     print(TickTypeEnum.to_str(i), i)
            print("reqID is ", reqId, "tickType is :", TickTypeEnum.to_str(tickType), " and the price is ", price)
            if price > 0:
                 self.mkt_price = price

    # after reqHistoricalData, this function is used to receive the data.
    def historicalData(self, reqId, bar):
            # print(f'Time: {bar.date} Close: {bar.close}')
            self.data.append([bar.date, bar.close])

    # To fire an order, we simply create a contract object with the asset details and an order object with the order details. Then call app.placeOrder to submit the order.
    # The IB API requires an order id associated with all orders and it needs to be a unique positive integer. It also needs to be larger than the last order id used. Fortunately, there is a built in function which will tell you the next available order id.
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    # order status, will be called after place/cancel order
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
             print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice, 'avgFullPrice:', avgFullPrice, 'mktCapPrice:', mktCapPrice)

    # will be called after place order
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, " at price ", order.lmtPrice, orderState.status)

    
    def execDetails(self, reqId, contract, execution):
         print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

#Function to create FX contract, by passing symbol of six letters like EURUSD
def fx_contract(symbol):
	contract = Contract()
	contract.symbol = symbol[:3]
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = symbol[3:]
	return contract

#Function to create stock contract, by passing ticker name
def stock_contract(symbol,pri_exchange="NASDAQ"):
    contract = Contract()
    contract.symbol = symbol
    # SecType [get, set]
 	# The security's type: STK - stock (or ETF) OPT - option FUT - future IND - index FOP - futures option CASH - forex pair BAG - combo WAR - warrant BOND- bond CMDTY- commodity NEWS- news FUND- mutual fund
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.primaryExchange = pri_exchange
    return contract


######## Order ##############
#Create buy order object,default quantity is 10
# order.OrderType = "LMT" , "MKT"
# order.action : Identifies the side. Generally available values are BUY and SELL. 
# For general account types, a SELL order will be able to enter a short position 
# automatically if the order quantity is larger than your current long position.
# order.AuxPrice Generic field to contain the stop price for STP LMT orders, trailing amount, etc. 
# order.Tif : The time in force.
    # DAY - Valid for the day only.
    # GTC - Good until canceled. The order will continue to work within the system and in the marketplace until it executes or is canceled. GTC orders will be automatically be cancelled under the following conditions: 
    # If a corporate action on a security results in a stock split (forward or reverse), exchange for shares, or distribution of shares. If you do not log into your IB account for 90 days. 
    # At the end of the calendar quarter following the current quarter. For example, an order placed during the third quarter of 2011 will be canceled at the end of the first quarter of 2012. If the last day is a non-trading day, the cancellation will occur at the close of the final trading day of that quarter. For example, if the last day of the quarter is Sunday, the orders will be cancelled on the preceding Friday.
    # Orders that are modified will be assigned a new “Auto Expire” date consistent with the end of the calendar quarter following the current quarter.
    # Orders submitted to IB that remain in force for more than one day will not be reduced for dividends. To allow adjustment to your order price on ex-dividend date, consider using a Good-Til-Date/Time (GTD) or Good-after-Time/Date (GAT) order type, or a combination of the two.
    # IOC - Immediate or Cancel. Any portion that is not filled as soon as it becomes available in the market is canceled.
    # GTD - Good until Date. It will remain working within the system and in the marketplace until it executes or until the close of the market on the date specified
    # OPG - Use OPG to send a market-on-open (MOO) or limit-on-open (LOO) order.
    # FOK - If the entire Fill-or-Kill order does not execute as soon as it becomes available, the entire order is canceled.
    # DTC - Day until Canceled. 
# order.GoodAfterTime [get, set]
    # Specifies the date and time after which the order will be active.
    # Format: yyyymmdd hh:mm:ss {optional Timezone}. 
# order.AutoCancelParent [get, set]
 	# Cancels the parent order if child order was cancelled.
# order.AlgoStrategy : The algorithm strategy.
    # As of API verion 9.6, the following algorithms are supported:
    # ArrivalPx - Arrival Price 
    # DarkIce - Dark Ice 
    # PctVol - Percentage of Volume 
    # Twap - TWAP (Time Weighted Average Price) 
    # Vwap - VWAP (Volume Weighted Average Price) 
    # For more information about IB's API algorithms, refer to https://interactivebrokers.github.io/tws-api/ibalgos.html 
# order.AlgoParams 
 	# The list of parameters for the IB algorithm.

# order.AlgoId [get, set]
 	# Identifies orders generated by algorithmic trading. 

def buy_order(price="",quantity:int=10):
    if price != "" and quantity > 0:
        order = Order()

        order.action = 'BUY'
        order.totalQuantity = quantity
        # 
        order.orderType = 'LMT'
        order.lmtPrice = price
        return order
    else:
         raise ValueError(f"invalid  price target {price}  or quantity {quantity}  in buy_order!")

#Create buy order object,default quantity is 10
def sell_order(price="",quantity:int=10):
    if price != "" and quantity > 0:
        order = Order()
        order.action = 'SELL'
        order.totalQuantity = quantity
        order.orderType = 'LMT'
        order.lmtPrice = price
        return order
    else:
         raise ValueError(f"invalid  price target {price}  or quantity {quantity}  in sell_order!")

# A Stop-Limit order is an instruction to submit a buy or sell limit order when the user-specified stop trigger price is attained or penetrated. The order has two basic components: the stop price and the limit price. When a trade has occurred at or through the stop price, the order becomes executable and enters the market as a limit order, which is an order to buy or sell at a specified price or better.
def stop_buy_lmt_order(stop_price="", limit_price="",quantity=10):
    if stop_price != "" and limit_price != "" and stop_price > 0 and limit_price >0  and quantity > 0:
        order = Order()
        order.Action = 'BUY'
        order.OrderType = "STP LMT"
        order.AuxPrice = stop_price
        order.lmtPrice = limit_price
        order.TotalQuantity = quantity;     
    else:
         raise ValueError(f"invalid  stop_price target {stop_price} , limit_price {limit_price} or quantity {quantity}  in stop_buy_lmt_order!")


# A sell trailing stop order sets the stop price at a fixed amount below the market price with an attached "trailing" amount. As the market price rises, the stop price rises by the trail amount, but if the stock price falls, the stop loss price doesn't change, and a market order is submitted when the stop price is hit. This technique is designed to allow an investor to specify a limit on the maximum possible loss, without setting a limit on the maximum possible gain. "Buy" trailing stop orders are the mirror image of sell trailing stop orders, and are most appropriate for use in falling markets.
# Note that Trailing Stop orders can have the trailing amount specified as a percent, as in the example below, or as an absolute amount which is specified in the auxPrice field.

def trailing_stop_buy_order(trailing_acount=0, stop_price=0, quantity = 10):
    if stop_price and trailing_acount and stop_price > 0 and trailing_acount >0  and quantity > 0:
        order = Order()
        order.Action = 'BUY'
        order.OrderType = "TRAIL"
        order.TrailStopPrice = stop_price
        order.auxPrice = trailing_acount
        order.TotalQuantity = quantity;  
       
    else:
         raise ValueError(f"invalid  stop_price target {stop_price} , trailing_acount {trailing_acount} or quantity {quantity}  in trailing_stop_buy_order!")

# Bracket Orders
# Bracket Orders are designed to help limit your loss and lock in a profit by "bracketing" an order with two opposite-side orders. 
# A BUY order is bracketed by a high-side sell limit order and a low-side sell stop order. 
# A SELL order is bracketed by a high-side buy stop order and a low side buy limit order. 
# Note how bracket orders make use of the TWS API's Attaching Orders mechanism.
# One key thing to keep in mind is to handle the order transmission accurately. Since a Bracket consists of three orders, 
# there is always a risk that at least one of the orders gets filled before the entire bracket is sent. 
# To avoid it, make use of the IBApi.Order.Transmit flag. When this flag is set to 'false', 
# the TWS will receive the order but it will not send (transmit) it to the servers. 
# In the example below, the first (parent) and second (takeProfit) orders will be send to the TWS but not transmitted to the servers. 
# When the last child order (stopLoss) is sent however and given that its IBApi.Order.Transmit flag is set to true, 
# the TWS will interpret this as a signal to transmit not only its parent order but also the rest of siblings, 
# removing the risks of an accidental execution.

@staticmethod
def BracketOrder(parentOrderId:int, action:str, quantity:Decimal, 
                      limitPrice:float, takeProfitLimitPrice:float, 
                      stopLossPrice:float):
     
    #This will be our main or "parent" order
    parent = Order()
    parent.orderId = parentOrderId
    parent.action = action
    parent.orderType = "LMT"
    parent.totalQuantity = quantity
    parent.lmtPrice = limitPrice
    #The parent and children orders will need this attribute set to False to prevent accidental executions.
    #The LAST CHILD will have it set to True, 
    parent.transmit = False

    takeProfit = Order()
    takeProfit.orderId = parent.orderId + 1
    takeProfit.action = "SELL" if action == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = takeProfitLimitPrice
    takeProfit.parentId = parentOrderId
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.orderId = parent.orderId + 2
    stopLoss.action = "SELL" if action == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    #Stop trigger price
    stopLoss.auxPrice = stopLossPrice
    stopLoss.totalQuantity = quantity
    stopLoss.parentId = parentOrderId
    #In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True 
    #to activate all its predecessors
    stopLoss.transmit = True

    bracketOrder = [parent, takeProfit, stopLoss]
    return bracketOrder
# Example for using the bracketOrder 
# bracket = OrderSamples.BracketOrder(self.nextOrderId(), "BUY", 100, 30, 40, 20)
#     for o in bracket:
#     self.placeOrder(o.orderId, ContractSamples.EuropeanStock(), o)
#     self.nextOrderId()  # need to advance this we'll skip one extra oid, it's fine


# get the histroy data for a contract
def get_his_data(app=TestApp(),contract=Contract()):
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

def place_buy_lmt_order(app=TestApp(), contract=Contract(),increamental=BUY_LMT_PLUS,quantity=10):
    ############ placing order started here
    if app.mkt_price > 0 and len(contract.symbol) > 0:
        order = buy_order(str(app.mkt_price+increamental),quantity)
        #Place order
        print('placing order to server for  now ...')
        app.placeOrder(app.nextorderId, contract, order)
        #app.nextorderId += 1
        time.sleep(1)

        ############# creating order finished
    else:
         print(f"place order failed.: for app.mkt_price {app.mkt_price}, symbol is {contract.symbol}")


def place_sell_lmt_order(app=TestApp(), contract=Contract(),increamental=SELL_LMT_PLUS,quantity=10):
    ############ placing order started here
    if app.mkt_price > 0 and len(contract.symbol) > 0:
        order = sell_order(str(app.mkt_price+increamental),quantity)
        #Place order
        print(f'placing order to server for  now ... order price at  {order.lmtPrice}')
        app.placeOrder(app.nextorderId, contract, order)
        #app.nextorderId += 1
        time.sleep(1)

        ############# creating order finished
    else:
         print(f"place order failed.: for app.mkt_price {app.mkt_price}, symbol is {contract.symbol}")


# cancel last order
def cancel_last_order(app=TestApp()):
     if app.nextorderId:
          print('placing order to server now ...')
          app.cancelOrder(app.nextorderId,"")
     else:
          print('no order to be cancelled...')

def main():

    def run_loop():
        app.run()

    app = TestApp()
    print("program is starting ...")
    app.connect('127.0.0.1', 7497, 1)
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
    # print("app.account", app.account)

    app.reqAccountUpdates(True, app.account)
    

    #Create contract object
    apple_contract = stock_contract('AAPL')

    #Request Market Data. should be in market open time.
    app.reqMarketDataType(3)
    app.reqMktData(1, apple_contract, '', True, False, [])
    time.sleep(2)


    # transform data to Dataframe format. 
    app.portfolio = pandas.DataFrame(app.portfolio, columns=['symbol', 'sectype', 'exchange', 'position', 'marketprice', 'marketvalue', 'averagecost', 'unrealizedpnl', 'realizedpnl'])

    print("app.portfolio\n", app.portfolio)
    print("app.account_info\n", app.account_info)

    ################ keyboard input monitoring part start
    # monitoring the keyboard and make it available to control the order
    def on_press(key):
        try:
            # print('alphanumeric key {0} pressed'.format(key.char))
            if key == PLACE_BUY_ORDER:
                place_buy_lmt_order(app,apple_contract)

            elif key == PLACE_SELL_ORDER:
                place_sell_lmt_order(app,apple_contract)

            elif key == CANCEL_LAST_ORDER:
                 cancel_last_order(app)

            elif key == NUMPAD0:
                 print("Number 0 pressed...")

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            print("Stopping Listener...")

            # Once the subscription to account updates is no longer needed, it can be cancelled by invoking the IBApi.EClient.reqAccountUpdates method while specifying the susbcription flag to be False.
            app.reqAccountUpdates(False, app.account)
            time.sleep(1) 
            print("Exiting Program...")
            app.disconnect()
            return False
 
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
    ################ keyboard input monitoring part end
    
if __name__ == "__main__":
    main()
