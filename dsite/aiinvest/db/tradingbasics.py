# this is a learning file for IB TWS connection

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

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

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
    
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

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
    app = TestApp()
    # print(app)
    # app.connect("127.0.0.1", 7497, clientId=123)
    # print(app.isConnected())
    # #  
    # app.run()
    # # tags = app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
    # print("tags: ", tags)
    # import time
    # time.sleep(6)

    app.connect('127.0.0.1', 7497, 133)
    print(app.isConnected())
    app.run()
    #Start the socket in a thread
    # api_thread = threading.Thread(target=app.run(), daemon=True)
    # api_thread.start()

    time.sleep(1) #Sleep interval to allow time for connection to server

    #Create contract object
    apple_contract = Contract()
    apple_contract.symbol = 'AAPL'
    apple_contract.secType = 'STK'
    apple_contract.exchange = 'SMART'
    apple_contract.currency = 'USD'

    #Request Market Data
    app.reqMktData(1, apple_contract, '', False, False, [])

    # from ibapi.ticktype import TickTypeEnum

    # for i in range(91):
    #     print(TickTypeEnum.to_str(i), i)

    #Request historical candles
    app.reqHistoricalData(1, apple_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])
    print(app.data)

    time.sleep(10) #Sleep interval to allow time for incoming price data

    app.disconnect()

    # app.accountSummary(9001,"yanzl6126", AccountSummaryTags.AllTags, 33, "USD")
    
    # contract = Contract()
    # contract.symbol = "AAPL"
    # contract.secType = "STK"
    # contract.exchange = "SMART"
    # contract.currency = "USD"
    # contract.primaryExchange = "NASDAQ"
    # # switch to delayed-frozen data if live is not available
    # app.reqMarketDataType(4)
    # app.reqMktData(1, contract, "", False, False, [])
    
if __name__ == "__main__":
    main()
