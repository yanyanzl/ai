# this is a learning file for IB TWS connection

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.reader import EReader
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

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

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
    
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

def main():
    app = TestApp()
    print(app)
    app.connect("127.0.0.1", 7497, clientId=123)
    print(app.isConnected())
    #  
    app.run()
    tags = app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
    print("tags: ", tags)
    import time
    time.sleep(6)

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
