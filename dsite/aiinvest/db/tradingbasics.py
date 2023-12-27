# this is a learning file for IB TWS connection

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

import pandas
import threading
import time
import os

# print(os.environ)
# print(os.get_exec_path())

class TestWrapper(EWrapper):
    def test():
        print("This is test")


class TestClient(EClient):
     def __init__(self, wrapper):
         EClient.__init__(self, wrapper)

class TestApp(TestWrapper, TestClient):
  
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.data = [] #Initialize variable to store data

    # overide the account Summary method. to get all the account summary information
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)

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
    def updatePortfolio(self, contract: Contract, position: Decimal,marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",contract.exchange, "Position:", decimalMaxString(position), "MarketPrice:", floatMaxString(marketPrice),"MarketValue:", floatMaxString(marketValue), "AverageCost:", floatMaxString(averageCost), "UnrealizedPNL:", floatMaxString(unrealizedPNL), "RealizedPNL:", floatMaxString(realizedPNL), "AccountName:", accountName)

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
                print("the price is ", price)

    # after reqHistoricalData, this function is used to receive the data.
    def historicalData(self, reqId, bar):
            print(f'Time: {bar.date} Close: {bar.close}')
            self.data.append([bar.date, bar.close])


def main():

    def run_loop():
        app.run()

    app = TestApp()

    app.connect('127.0.0.1', 7497, 155)
    print(app.isConnected())

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    time.sleep(1) #Sleep interval to allow time for connection to server

    # requre all the 
    app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)

    #Sleep interval to allow time for response data from server
    time.sleep(2) 

    # The IBApi.EClient.reqAccountUpdates function creates a subscription to the TWS through which account and portfolio information is delivered. This information is the exact same as the one displayed within the TWS’ Account Window. Just as with the TWS’ Account Window, unless there is a position change this information is updated at a fixed interval of three minutes.
    app.reqAccountUpdates(True, app.account)


    #Create contract object
    apple_contract = Contract()
    apple_contract.symbol = 'AAPL'
    apple_contract.secType = 'STK'
    apple_contract.exchange = 'SMART'
    apple_contract.currency = 'USD'
    apple_contract.primaryExchange = "NASDAQ"

    #Request Market Data. should be in market open time.
    # app.reqMktData(1, apple_contract, '', False, False, [])

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
