# this is a learning file for IB TWS connection

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

from ibapi.order import *

import pandas
import threading
import time
import os

# print(os.environ)
# print(os.get_exec_path())

class TestWrapper(EWrapper):
    def test():
        print("This is test")

    # The API treats many items as errors even though they are not.
    def error(self, reqId, errorCode, errorString):
         if errorCode == 202:
            print('order canceled - Reason ', errorString) 

class TestClient(EClient):
     def __init__(self, wrapper):
         EClient.__init__(self, wrapper)
         
         
from decimal import *

class TestApp(TestWrapper, TestClient):
  
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.data = [] #Initialize variable to store data
        self.account = ""
        self.mkt_price = ""

    # overide the account Summary method. to get all the account summary information
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
        self.account = account

    # overide the account Summary end method. 
    # Notifies when all the accounts’ information has ben received.
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

    # Receiving Account Updates
    # Resulting account and portfolio information will be delivered via the IBApi.EWrapper.updateAccountValue, IBApi.EWrapper.updatePortfolio, IBApi.EWrapper.updateAccountTime and IBApi.EWrapper.accountDownloadEnd
        
    # Receives the subscribed account’s information. Only one account can be subscribed at a time. After the initial callback to updateAccountValue, callbacks only occur for values which have changed. This occurs at the time of a position change, or every 3 minutes at most. This frequency cannot be adjusted.
    def updateAccountValue(self, key: str, val: str, currency: str,accountName: str):
        print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    # Receives the subscribed account’s portfolio. This function will receive only the portfolio of the subscribed account. After the initial callback to updatePortfolio, callbacks only occur for positions which have changed.

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType)
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",contract.exchange, "Position:", position, "MarketPrice:", marketPrice,"MarketValue:", marketValue, "AverageCost:", averageCost, "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        # ########  need to save those portfolio positions information to a dataset.


    # Receives the last time on which the account was updated.
    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)

    # Notifies when all the account’s information has finished.
    def accountDownloadEnd(self, accountName: str):
        print("AccountDownloadEnd. Account:", accountName)

    # after reqMktData, this function is used to receive the data.
    def tickPrice(self, reqId, tickType, price, attrib):
            if tickType == 2 and reqId == 1:
                print('The current ask price is: ', price)
            else:
                print("tickType is :", tickType, " and the price is ", price, "the attrib is ", attrib)
            self.mkt_price = price

    # after reqHistoricalData, this function is used to receive the data.
    def historicalData(self, reqId, bar):
            print(f'Time: {bar.date} Close: {bar.close}')
            self.data.append([bar.date, bar.close])

    # To fire an order, we simply create a contract object with the asset details and an order object with the order details. Then call app.placeOrder to submit the order.
    # The IB API requires an order id associated with all orders and it needs to be a unique positive integer. It also needs to be larger than the last order id used. Fortunately, there is a built in function which will tell you the next available order id.
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    # order status, will be called after place/cancel order
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
             print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    # will be called after place order
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    
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


#Create buy order object,default quantity is 10
def buy_order(price="",quantity:int=10):
    if price != "":
        order = Order()
        order.action = 'BUY'
        order.totalQuantity = quantity
        order.orderType = 'LMT'
        order.lmtPrice = price
        return order
    else:
         raise ValueError("No price target given in buy_order!")


def main():

    def run_loop():
        app.run()

    app = TestApp()

    # app.connect('127.0.0.1', 7497, 155)
    app.connect('192.168.1.146', 7497, 176)
    
    # print(app.isConnected())

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
    print("app.account", app.account)

    app.reqAccountUpdates(True, app.account)
    
    time.sleep(2) 
    # Once the subscription to account updates is no longer needed, it can be cancelled by invoking the IBApi.EClient.reqAccountUpdates method while specifying the susbcription flag to be False.
    app.reqAccountUpdates(False, app.account)

    #Create contract object
    apple_contract = stock_contract('AAPL')

    #Request Market Data. should be in market open time.
    app.reqMarketDataType(3)
    app.reqMktData(1, apple_contract, '', True, False, [])
    time.sleep(2)

    ############ placing order started here
    order = buy_order(str(app.mkt_price),10)
    #Place order
    app.placeOrder(app.nextorderId, apple_contract, order)
    #app.nextorderId += 1

    time.sleep(3)

    #Cancel order 
    print('cancelling order')

    app.cancelOrder(app.nextorderId,"")
    ############# creating order finished


    # from ibapi.ticktype import TickTypeEnum

    # for i in range(91):
    #     print(TickTypeEnum.to_str(i), i)

    #Request historical candles
    app.reqHistoricalData(1, apple_contract, '', '5 D', '1 hour', 'BID', 0, 2, False, [])

    #Sleep interval to allow time for incoming price data. 
    # without this sleep. the data will be empty
    time.sleep(5) 

    # transform data to Dataframe format. 
    df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
    df['DateTime'] = pandas.to_datetime(df['DateTime'],unit="s")
    # 20 SMA of the close price.
    df['20SMA'] = df['Close'].rolling(20).mean()
    print(df.tail(10))


    app.disconnect()

    
if __name__ == "__main__":
    main()
