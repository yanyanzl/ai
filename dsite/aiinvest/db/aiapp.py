"""
Copyright (C) Steven Jiang. All rights reserved. This code is subject to the terms
 and conditions of the MIT Non-Commercial License, as applicable.
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader

from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.execution  import Execution
from datetime import datetime
import pandas

from ibapi.common import * # @UnusedWildImport
from ibapi.utils import * # @UnusedWildImport
from aiorder import *

BUY_LMT_PLUS = 0.05

ACCOUNT_COLUMNS=['key', 'value', 'currency']
PORTFOLIO_COLUMNS = ['symbol', 'sectype', 'exchange', 'position', 'marketprice', 'marketvalue', 'averagecost', 'unrealizedpnl', 'realizedpnl']

class AiWrapper(EWrapper):

    # The API treats many items as errors even though they are not.
    def error(self, reqId, errorCode, errorMsg="", advancedOrderRejectJson=""):
        super().error(reqId, errorCode, errorMsg, advancedOrderRejectJson)

        if errorCode == 202:
            print('order canceled - Reason ', errorMsg) 
        # else:
        #     print(f'errorcode {errorCode}, error message: {errorMsg}')

    # This function is fired when an order is filled or reqExcutions() called.
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
         super().execDetails(reqId,contract, execution)

         print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)    

    def openOrderEnd(self):
            super().openOrderEnd()
            print("OpenOrderEnd")
            # logging.debug("Received %d openOrders", len(self.permId2ord))     

class AiClient(EClient):
     def __init__(self, wrapper):
         EClient.__init__(self, wrapper)

class AiApp(AiWrapper, AiClient):
  
    def __init__(self):
        AiWrapper.__init__(self)
        AiClient.__init__(self, wrapper=self)
        self.data = [] #Initialize variable to store data
        self.account = "" 
        #  account_info;` columns: key, value, currency`
        self.account_info = pandas.DataFrame()
        # self.mkt_price = ""
        self.last_price = ""
        self.bid_price = ""
        self.ask_price = ""
        self.portfolio = pandas.DataFrame()
        # this is used for the cancel of the last order.
        self.lastOrderId = 0
        self.currentContract = Contract()

    # overide the account Summary method. to get all the account summary information
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        # print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
        self.account = account
        if tag != None and tag != "":
             self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[tag, value, currency]],
                   columns=ACCOUNT_COLUMNS)])
 

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
            # print(f"key is {key}. {val}")

            # if exist in the data list already. drop it firstly.
            if not self.account_info.loc[self.account_info['key'] == key].empty:
                # print("not empty. drop .... --- ")
                self.account_info = self.account_info.drop(index=self.account_info.loc[self.account_info['key'] == key].index)
                                                           
            self.account_info = pandas.concat([self.account_info,pandas.DataFrame([[key, val, currency]],
                   columns=ACCOUNT_COLUMNS)], ignore_index=True)


    # Receives the subscribed account’s portfolio. This function will receive only the portfolio of the subscribed account. After the initial callback to updatePortfolio, callbacks only occur for positions which have changed.

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
         # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",contract.exchange, "Position:", position, "MarketPrice:", marketPrice,"MarketValue:", marketValue, "AverageCost:", averageCost, "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        #   to save those portfolio positions information to a dataset.
        for _ in self.portfolio.index:
            # psoppcprint(f"portforlio {_}, symbol is {self.portfolio.iloc[_]['symbol']}")
            # if the symbol already in the portfolio. drop it.
            if contract.symbol == self.portfolio.iloc[_]['symbol']:
                #  print(f"droping {self.portfolio.iloc[_]}")
                 self.portfolio = self.portfolio.drop(index=_)
                 break

        self.portfolio = pandas.concat([self.portfolio, pandas.DataFrame([[contract.symbol,contract.secType, contract.exchange,position,marketPrice,marketValue,averageCost, unrealizedPNL,realizedPNL]],
                   columns= PORTFOLIO_COLUMNS)], ignore_index=True)

    # Receives the last time on which the account was updated.
    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)

    # Notifies when all the account’s information has finished.
    def accountDownloadEnd(self, accountName: str):
        print("AccountDownloadEnd. Account:", accountName)

    # after reqMktData, this function is used to receive the data.
    def tickPrice(self, reqId, tickType, price, attrib):
            super().tickPrice(reqId,tickType,price,attrib)
            # for i in range(91):
            #     print(TickTypeEnum.to_str(i), i)
            tickType = TickTypeEnum.to_str(tickType)
            
            print("reqID is ", reqId, "tickType is :", tickType, " and the price is ", price, "attrib is ", attrib)
            if price > 0:
                if tickType == "LAST":
                    print(f"price : {price} , tickType {tickType}")
                    self.last_price = price
                elif tickType == "BID":
                    print(f"price : {price} , tickType {tickType}")
                    self.bid_price = price
                elif tickType == "ASK":
                    print(f"price : {price} , tickType {tickType}")
                    self.ask_price = price


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
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
             super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
             print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice, 'avgFullPrice:', avgFillPrice, 'mktCapPrice:', mktCapPrice)

    # will be called after place order
    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)

        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, " at price ", order.lmtPrice, orderState.status)
        self.lastOrderId = orderId

    # tickByTickBidAsk function to receive the data.
    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float, bidSize: Decimal, askSize: Decimal, tickAttribBidAsk: TickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)

        print("BidAsk. ReqId:", reqId, "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"), "BidPrice:", floatMaxString(bidPrice), "AskPrice:", floatMaxString(askPrice), "BidSize:", decimalMaxString(bidSize), "AskSize:", decimalMaxString(askSize), "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:", tickAttribBidAsk.askPastHigh)

    def set_current_Contract(self, contract:Contract()):
        """ change the current contract. all functions use contract will be affected.
        """
        self.currentContract = contract


def place_lmt_order(app=AiApp(), action:str="", tif:str="DAY", increamental=BUY_LMT_PLUS, quantity=10, priceTickType="LAST"):
    """
    send limit order to server
    """
    ############ placing order started here
    price = 0
    if action != 'BUY' and action != 'SELL':
             raise ValueError(f"invalid  action {action} in place_lmt_order!")
    try:
        print(f"ask price {app.ask_price}, bid price {app.bid_price}, last price {app.last_price}")
        price = _get_order_price_by_type(app, priceTickType)
        if len(app.currentContract.symbol) > 0:

            order = lmt_order(str(price + increamental), action, quantity,tif)

            #Place order
            print(f'placing limit order now ...\n orderid {app.nextorderId}, action: {action}, symbol {app.currentContract.symbol}, quantity: {quantity}, tif: {tif} at price: {order.lmtPrice}'  )
            app.placeOrder(app.nextorderId, app.currentContract, order)
            # orderId used, now get a new one for next time
            app.reqIds(app.nextorderId)

        else:
            print(f"place order failed.:  symbol is {app.currentContract.symbol}, action is {action}")

    except Exception as ex:
         print(f"place order failed.: for price {price}, priceTickType: {priceTickType} symbol is {app.currentContract.symbol}, action is {action}")

def _get_order_price_by_type(app=AiApp(),priceTickType="LAST"): 
     """
     get the price for the order based on the priceTickType. inner function
     """
    #  print(f"prictTickType is {priceTickType}, app.lastprice is {app.last_price}")
     if priceTickType == "LAST" and app.last_price and float(app.last_price) > 0:
        #   print(f"prictTickType is {priceTickType}, app.lastprice is {app.last_price}")
          return app.last_price
     elif priceTickType == "ASK" and app.ask_price and float(app.ask_price) > 0:
        #   print(f"prictTickType is {priceTickType}, app.ask is {app.ask_price}")
          return app.ask_price
     elif priceTickType == "BID" and app.bid_price and float(app.bid_price) > 0:
        #   print(f"prictTickType is {priceTickType}, app.bid is {app.bid_price}")
          return app.bid_price
     else:
          raise ValueError(f"unexpected priceTickType {priceTickType} or no correspondont price availalbe.")
     
          
# cancel last order
def cancel_last_order(app=AiApp()):
     if app.lastOrderId > 0:
          print(f'placing orderId {app.lastOrderId} to server now ...')
          app.cancelOrder(app.lastOrderId,"")
     else:
          print('no order to be cancelled...')

# cancel all open orders
# IBApi::EClient::reqGlobalCancel will cancel all open orders, regardless of how they were originally placed.
def cancel_all_order(app=AiApp()):
     if app.isConnected():
          print('Cancelling all open orders to server now ...')
          app.reqGlobalCancel()
     else:
          print('calling all open orders failed. No connection ...')

# show the current portforlio 
def show_portforlio(app=AiApp()):

    if app.isConnected():
        print(f'current portforlio for account{app.account} are showing below ... \n {app.portfolio}')
        
    else:
        print('show portforlio failed. No connection ...')

# show the current account summary 
def show_summary(app=AiApp()):

    if app.isConnected():
        print(f'current portforlio for account{app.account} are showing below ... \n')
        print("all needed summary : ", app.account_info.loc[app.account_info['key'].isin(['UnrealizedPnL','RealizedPnL'])])

    else:
        print('show account summary failed. No connection ...')



def main():
     app = AiApp()

if __name__ == "__main__":
    main()