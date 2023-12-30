
"""
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
"""

from ibapi.order import Order 
from decimal import Decimal


def lmt_order(price="", action:str="", quantity:int=10, tif:str='DAY'):
    """
    build a limit order
    """
    if action!="" and price != "" and quantity > 0:
        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.tif = tif
        order.orderType = 'LMT'
        order.lmtPrice = price
        return order
    else:
         raise ValueError(f"invalid  price target {price}, action {action}  or quantity {quantity}  in lmt_order()!")


# A Stop-Limit order is an instruction to submit a buy or sell limit order when the user-specified stop trigger price is attained or penetrated. The order has two basic components: the stop price and the limit price. When a trade has occurred at or through the stop price, the order becomes executable and enters the market as a limit order, which is an order to buy or sell at a specified price or better.
def stop_lmt_order(action:str, stop_price="", limit_price="", quantity=10):
    if stop_price != "" and limit_price != "" and stop_price > 0 and limit_price >0  and quantity > 0:
        if action != 'BUY' and action != 'SELL':
             raise ValueError(f"invalid  action {action} in stop_lmt_order!")
        order = Order()
        order.Action = action
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

#################### Order part end