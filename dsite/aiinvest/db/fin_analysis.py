
# financial analysis example from Spyeder. 
# mean-variance portfolio (MVP) theory or known as Modern Portfolio Theory (MPT)
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from datetime import datetime as dt

# The pprint module provides a capability to “pretty-print” arbitrary Python data structures in a form which can be used as input to the interpreter. If the formatted structures include objects which are not fundamental Python types, the representation may not be loadable. This may be the case if objects such as files, sockets or classes are included, as well as many other objects which are not representable as Python literals.
# The formatted representation keeps objects on a single line if it can, and breaks them onto multiple lines if they don’t fit within the allowed width. Construct PrettyPrinter objects explicitly if you need to adjust the width constraint.
import pprint

from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import HistoricalData
import yfinance as yf

netflix = yf.Ticker("NFLX")



# MPT : a method of constructing a portfolio that generates a maximum return for a given level of risk or a minimum risk for a stated return

pprint.pprint(netflix.info)
print("---------------------------")

hist = netflix.history(period="5y")
pprint.pprint(hist)

plt.style.use("fivethirtyeight")
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["font.family"] = "serif"
np.set_printoptions(precision=5, suppress=True, formatter={"float": lambda x: f"{x:6.3f}"})

# If you search for SYMBOLS_1 in Variable Explorer you will not find it: Python interprets this element not as a variable, but as a constant. This is because the name is written with uppercase letters (no letter is lowercase). By default, the Variable Explorer doesn’t show this, but actually you can change the settings in the Preferences to be able to see these constants.
SYMBOLS_1 = ["GOOG", "AAPL", "MSFT", "NFLX", "AMZN"]

RISK_FREE_RATE = 0.03

# The last argument (group_by="Ticker") groups the information mainly by stock. Otherwise, the primary grouping is done by the type of information (e.g., opening price, closing price, volume traded) of the transactions.
data_1 = yf.download(" ".join(SYMBOLS_1), start="2012-01-01", end=dt.today(), group_by="Ticker")


# Let’s change the formatting of the data a bit so that the symbols appear as the column names, and the Ticker moves from columns to rows. We will do this with the stack() operation of the DataFrame.
data_1 = data_1.stack(level=1).rename_axis(["Date", "Ticker"]).reset_index(level=1)

# From the Ticker we are only interested in the daily closing price. So we will leave only the values for "Close" and eliminate the Ticker column afterwards.
close_data_1 = data_1[data_1.Ticker == "Close"].drop("Ticker", inplace=False, axis=1)

# We want to see how our portfolio would have performed if we had invested in it from 2012 to early 2021. How could we obtain this measurement? Let’s look at the monthly closing prices of each stock. To do this we will do an automatic resample of the data. And then we will calculate the change in relative frequencies (percentages).

# The resampling will be performed with the resample("M") method and the calculation of percentages with the pct_change() method. The result will be stored in the monthly_data_1 variable.
monthly_data_1 = close_data_1.resample("M").ffill().pct_change()

# mean of the monthly growth. the higher the mean, the bigger the gain/return: Growth
pprint.pprint(monthly_data_1.mean())

# standard deviation of the monthly growth, the higher the SD, the higher the risk: Variability
pprint.pprint(monthly_data_1.std())

# To scale the values, we are going to divide the relative frequency of the closing price of the actions by the initial value it has in the dataframe close_data_1 (these initial values can be found with close_data_1.iloc[0])). The plot is drawn with the plot() method of the Pandas DataFrame (to which we pass as arguments the size of the plot and the plot title).
# Daily data chart
(close_data_1/close_data_1.iloc[0]).plot(figsize=(16, 10), title="Portfolio 1 daily stock price")


# We can also plot with the plot() method the DataFrame we already have with the monthly data. To do this, we will add 1 to all the values and calculate the accumulated product with the cumprod() method
# Monthly data chart (percentage to compound growth)
# This plot of the monthly data is “smoother” than the plot of the daily data.
(monthly_data_1 + 1).cumprod().plot(figsize=(16, 10), title="Portfolio 1 monthly stock price")

# plt.show()

# Remember that in the mean-variance portfolio theory what matters are the expected returns and variances. To calculate these returns, we will divide the price of the stock on one day by the price of the same stock on the previous day. We will do this by dividing the close_data_1 DataFrame by a version of itself in which we shift each record one date backwards (shift(1)). For example, if on the date 2012-01-03 a stock was valued at 1, and on the next day (2012-01-02), it was valued at 2, then in our shifted dataset, on the day 2012-01-03 the stock would be worth 1. In this way, we would divide 1 by 2. And so on with all the values of all the shares. We will also normalize the results by passing them to a logarithmic scale with np.log().
# numpy's logarithmic method and dropna() to drop any na values.
# This is the daily return normalized by logarithmic scale for each security
rets_1 = np.log(close_data_1/close_data_1.shift(1)).dropna()

# pprint.pprint("rets_1 ", lambda x: x in rets_1)

# In addition to the returns of each stock, we will need the specific weight of each stock in the portfolio
# This weight will be a vector (Python list) composed of the relative weight (between 0 and 1) of each stock in the portfolio. The sum of these weights has to be 1
weights_1 = [0.2, 0.2, 0.2, 0.2, 0.2]

# expected Return of the portfolio: E(Rp) = ∑ (E(Ri) * Wi)
# dot product of the portfolio weights vector and the vector of expected returns.
# annualised by 252 trading days.
def portfolio_return(returns, weights):
    return np.dot(returns.mean(), weights) * 252

p_return = portfolio_return(rets_1, weights_1) 

print("expected_return is : " ,p_return)

# Volatility : Variance of the portfolio : w12σ12 + w22σ22 + 2w1w2Cov1,2
# Portfolio variance looks at the co-variance or correlation co-efficients for the securities in a portfolio. Generally, a lower correlation between securities in a portfolio results in a lower portfolio variance.
# Portfolio variance is calculated by multiplying the squared weight of each security by its corresponding variance and adding twice the weighted average weight multiplied by the co-variance of all individual security pairs. co-variance with self is the standard deviation. 
# co-variance(x,y) = [∑ (Xi - X¯)(Yi - Y¯)] / (N - 1)
# First, the dot product of the annualized covariance of the returns (this is multiplied by the number of trading days in a year) and the weights is calculated. Then the dot product of the weights and the previous result is obtained. Finally, the square root of this result is extracted.
def portfolio_volatility(returns, weights):
    return np.dot(weights, np.dot(returns.cov() * 252, weights)) ** 0.5

p_risk = portfolio_volatility(rets_1, weights_1)

print("portfolio_risk is : " ,p_risk)


# The Sharpe ratio or index is a measure of portfolio performance. It relates the portfolio’s return to its volatility, comparing the expected/realized return with the expected/realized risk. It is calculated as the difference between the actual investment returns and the expected return in a zero-risk situation, divided by the volatility of the investment. It provides a model of the additional amount of returns received for each additional unit of risk.
def portfolio_sharpe(returns, weights):
    return (portfolio_return(returns, weights) - RISK_FREE_RATE) / portfolio_volatility(returns, weights)


p_sharpe = portfolio_sharpe(rets_1, weights_1)
print("p_sharpe is : " ,p_sharpe)



# Monte Carlo Simulation : 
# use a Monte Carlo simulation to randomize the weights of each stock in the portfolio so that we can see the range over which the Sharpe ratio can vary. In this way we can plot some scenarios that together will give us a good insight of the relationship between expected returns and expected volatility.
def monte_carlo_sharpe(returns, symbols, weights):

    # we create a numpy array of length 1,000 and width of the number of shares in the portfolio. 
    # random.Generator.random(size=None, dtype=np.float64, out=None), return is numpy.ndarray
    # sim_weights[999][4]
    sim_weights = np.random.random((1000, len(symbols)))

    # numpy.ndarray is a class. it has attribute T : ndarray View of the transposed array.
    # sim_weights is a two dimension array like sim_weights[x][y], sum(axis=0) meaning to sum all y for each x. sum(axis=1) meaning to sum all x for each y.
    # this line make sure Each row of the array has random weights that always add up to 1
    sim_weights = (sim_weights.T / sim_weights.sum(axis=1)).T

    # calculates the volatility and returns for the new random weights using a list comprehension. 
    # for 1000 array of weights (add up to 1 for each of them)
    # you get a array of 1000 volatility and return
    volat_ret = [(portfolio_volatility(returns[symbols], weights), portfolio_return(returns[symbols], weights)) for weights in sim_weights]

    # The resulting list is transformed back into a numpy array:
    volat_ret = np.array(volat_ret)

    # obtain the Sharpe ratio by dividing the index 1 (returns) by the index 0 ( volatilities) of the numpy array
    sharpe_ratio = volat_ret[:, 1] / volat_ret[:, 0]

    return volat_ret, sharpe_ratio


# use the function to get the simulated returns and volatility of portfolio 1 (port_1_vr) and the related Sharpe ratios (port_1_sr).
# With this we obtain two arrays with 1,000 simulated cases for our portfolio
port_1_vr, port_1_sr = monte_carlo_sharpe(rets_1, SYMBOLS_1, weights_1)

# he best way to explore this is with a plot.
# A roughly linear relationship can be observed between returns and volatility: the higher the volatility, the higher the gains. And the Sharpe ratio shows an important amount of variability (it is noticeable in the “width” of the line drawn).
plt.figure(figsize=(16, 10))
fig = plt.scatter(port_1_vr[:, 0], port_1_vr[:, 1], c=port_1_sr, cmap="turbo")
CB = plt.colorbar(fig)
CB.set_label("Sharpe ratio")
plt.xlabel("expected volatility")
plt.ylabel("expected return")
plt.title(" | ".join(SYMBOLS_1))

# you can get all the colormaps value by the following 
# from matplotlib import colormaps
# print(list(colormaps))

# plt.show()

# Optimal portfolio weights
# use the data obtained to calculate the optimal weights for the portfolio by year
start_year, end_year = (2012, dt.today().year)

# calculate these optimal weights
def optimal_weights(returns, symbols, actual_weights, start_y, end_y):

    # bounds will be like n * (0,1) : [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]
    bounds = len(symbols) * [(0, 1), ]

    # constraints is a function that ensures that the sum of the weights of all actions always adds up to 1. 
    constraints = {"type": "eq", "fun": lambda weights: weights.sum() - 1}

    # a loop is initialized that will segment the data for each year. 
    opt_weights = {}

    for year in range(start_y, end_y):
        # In the variable _rets the returns for the specified year are obtained
        _rets = returns[symbols].loc[f"{year}-01-01":f"{year}-12-31"]

        # scipy.optimize.minimize : Minimization of scalar function of one or more variables.
            # parameters 1: fun: callable
                # The objective function to be minimized.
                # fun(x, *args) -> float
                # where x is a 1-D array with shape (n,) and args is a tuple of the fixed parameters needed to completely specify the function.

            # parameters 2: x0 : ndarray, shape (n,)
                # Initial guess. Array of real elements of size (n,), where n is the number of independent variables.
        
            # parameters 3: bounds : sequence or Bounds, optional
                # Bounds on variables for Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell, trust-constr, and COBYLA methods. There are two ways to specify the bounds:
                    # Instance of Bounds class.
                    # Sequence of (min, max) pairs for each element in x. None is used to specify no bound.

            # constraints{Constraint, dict} or List of {Constraint, dict}, optional
            # Constraints definition. Only for COBYLA, SLSQP and trust-constr.

            # Constraints for ‘trust-constr’ are defined as a single object or a list of objects specifying constraints to the optimization problem. Available constraints are:
                # LinearConstraint
                # NonlinearConstraint

            # Constraints for COBYLA, SLSQP are defined as a list of dictionaries. Each dictionary with fields:
                # typestr
                    # Constraint type: ‘eq’ for equality, ‘ineq’ for inequality.
                # fun: callable
                    # The function defining the constraint.
        
        _opt_w = minimize(lambda weights: -portfolio_sharpe(_rets, weights), actual_weights, bounds=bounds, constraints=constraints)["x"]
        # In _opt_w the portfolio_shape() function is used to calculate the weights that maximize the Sharpe ratio. This is done with the minimize() function of SciPy (which takes as arguments the portfolio_shape function, the actual weights of our stocks in the portfolio, and the bounds and the constraints variables). Notice the - sign before portfolio_sharpe? It’s because minimize() aims to find the minimum value of a function relative to a parameter, but we are interested in the maximum, so we make the result of portfolio_sharpe a negative one.
        # Returns: res : OptimizeResult
        # The optimization result represented as a OptimizeResult object. Important attributes are: x the solution array, success a Boolean flag indicating if the optimizer exited successfully and message which describes the cause of the termination. See OptimizeResult for a description of other attributes.

        # appendix year x's optimal weights to the dictionary
        opt_weights[year] = _opt_w
    return opt_weights


# We will use the function we just defined to calculate the optimal weights for each year, and we are going to save the result in a Pandas DataFrame to take advantage of the Variable Explorer display options.

opt_weights_1 = optimal_weights(rets_1, SYMBOLS_1, weights_1, start_year, end_year)

port_1_ow = pd.DataFrame.from_dict(opt_weights_1, orient='index')

# give every columns a name according to the orders in the SYMBOLS_1
port_1_ow.columns = SYMBOLS_1

port_1_ow.plot(figsize=(16, 10), title="Optimal weights to maximise the Sharpe Ratio of the portfolio for each year")
print(port_1_ow.columns)
print(port_1_ow)



# Comparison of expected and realized returns
# use the optimal weights to calculate the expected returns and compare them with the actual returns.


def exp_real_rets(returns, opt_weights, symbols, start_year, end_year):

    _rets = {}
    for year in range(start_year, end_year):
        # all returns data for previous year.
        prev_year = returns[symbols].loc[f"{year}-01-01":f"{year}-12-31"]
        # all returns data for current year.
        current_year = returns[symbols].loc[f"{year + 1}-01-01":f"{year + 1}-12-31"]

        # The returns from applying the optimal weights of the previous year’s stocks to the data for that same year (expected_pr).
        expected_pr = portfolio_return(prev_year, opt_weights[year])

        # The returns from applying the optimal weights of the previous year’s stocks to the following year’s data
        realized_pr = portfolio_return(current_year, opt_weights[year])
        _rets[year + 1] = [expected_pr, realized_pr]

    return _rets

# apply this function to the data in portfolio 1 and store the results in a DataFrame that we can review in the Variable
# It can be seen that there are notable differences in some years. Let’s look at this in a plot.
port_1_exp_real = pd.DataFrame.from_dict(exp_real_rets(rets_1, opt_weights_1, SYMBOLS_1, start_year, end_year), orient='index')
port_1_exp_real.columns = ["expected", "realized"]

port_1_exp_real.plot(kind="bar", figsize=(16, 10),title="Expected vs. realized Portfolio Returns")


# optimal weight model offered us a profit of around 40%, but the profit we would have obtained, due to real market fluctuations, would have been almost 20%. Not bad, but the mean-variance portfolio model we have applied for annual calculations is not very accurate, is it?
print("Mean of expected and Real return are :", port_1_exp_real.mean())


# As we can see, the correlations are negative -0.48, which warns us that we should be cautious when using this type of modeling.
print("correlation of expected and Real return are :", port_1_exp_real[["expected", "realized"]].corr())



# Second portfolio
SYMBOLS_2 = ["PFE", "AZN", "JNJ"]  # Pfizer, Astra Zeneca, Johnson N Johnson

data_2 = yf.download(" ".join(SYMBOLS_2), start="2012-01-01", end=dt.today(), group_by="Ticker")
data_2 = data_2.stack(level=1).rename_axis(["Date", "Ticker"]).reset_index(level=1)

close_data_2 = data_2[data_2.Ticker == "Close"].drop("Ticker", inplace=False, axis=1)

# Mean and standard deviation
monthly_data_2 = close_data_2.resample("M").ffill().pct_change()

print("Mean:")
print(monthly_data_2.mean())
print("STD:")
print(monthly_data_2.std())

rets_2 = np.log(close_data_2[SYMBOLS_2] / close_data_2[SYMBOLS_2].shift(1)).dropna()

(close_data_2[SYMBOLS_2] / close_data_2[SYMBOLS_2].iloc[0]).plot(figsize=(16, 10), title="Portfolio 2 daily stock price")

(monthly_data_2 + 1).cumprod().plot(figsize=(16, 10), title="Portfolio 2 monthly stock price")

# These two plots show a steady growth over the years, but also a high variability in each year. This seems to be a good portfolio only if taken as a long-term investment.

# this form a equal weights for each columns like 3 * [0.33333] = [0.33333, 0.33333, 0.33333]
weights_2 = len(close_data_2.columns) * [1 / len(close_data_2.columns)]

# print("weights_2 is ", weights_2)
print(f"Portfolio 2 returns: {portfolio_return(rets_2, weights_2):.4f}")
print(f"Portfolio 2 volatility: {portfolio_volatility(rets_2, weights_2):.4f}")
print(f"portfolio 2 Sharpe: {portfolio_sharpe(rets_2, weights_2):.4f}")


# The return of this portfolio is significantly lower than that of the previous portfolio (0.0809 < 0.2859). Its volatility (0.1637 < 0.2370) is also lower, but to a lesser extent. This is reflected in a lower Sharpe ratio as well (0.4940 < 1.2062)
# This means, within the mean-variance theory approach, that the first portfolio is a better investment than the second one.


# The different behavior is clearly observed if we apply a Monte Carlo simulation and visualize it with a graph
# High volatility does not correspond in most cases with high returns. In fact, there are scenarios in the simulation in which higher expected returns are related to lower expected volatility.

port_2_vr, port_2_sr = monte_carlo_sharpe(rets_2, SYMBOLS_2, weights_2)

plt.figure(figsize=(16, 10))
fig = plt.scatter(port_2_vr[:, 0], port_2_vr[:, 1], c=port_2_sr, cmap="cool")
CB = plt.colorbar(fig)
CB.set_label("Sharpe ratio")
plt.xlabel("expected volatility")
plt.ylabel("expected return")
plt.title(" | ".join(SYMBOLS_2))



# Third portfolio
# Our third portfolio will consist of three cryptocurrencies: bitcoin (BTC), ethereum (ETH) and litecoin (LTC). To access historical data, we are going to use a library called Historic-Crypto

# use the Cryptocurrencies class to obtain a list of available cryptocurrencies.
crypto_list = Cryptocurrencies(coin_search="", extended_output=True).find_crypto_pairs()
# pprint.pprint("crypto_list is ", crypto_list.columns) 


crypto_list.loc[crypto_list.base_currency == "ETH"]


# Download and format ETC data:
# Download and format ETC data:
ETC_HIST = HistoricalData("ETH-USD", 3600 * 24, "2016-01-01-00-00", dt.today().strftime('%Y-%m-%d-%H-%M')).retrieve_data()
ETC_HIST.rename(columns={"close": "ETC"}, inplace=True)
ETC_HIST.drop(["low", "high", "open", "volume"], axis=1, inplace=True)


# Download and format BTC data:
BTC_HIST = HistoricalData("BTC-USD", 3600 * 24, "2016-01-01-00-00", dt.today().strftime('%Y-%m-%d-%H-%M')).retrieve_data()
BTC_HIST.rename(columns={"close": "BTC"}, inplace=True)
BTC_HIST.drop(["low", "high", "open", "volume"], axis=1, inplace=True)


# Download and format LTC data:
LTC_HIST = HistoricalData("LTC-USD", 3600 * 24, "2016-01-01-00-00", dt.today().strftime('%Y-%m-%d-%H-%M')).retrieve_data()
LTC_HIST.rename(columns={"close": "LTC"}, inplace=True)
LTC_HIST.drop(["low", "high", "open", "volume"], axis=1, inplace=True)

# merge the resulting dataframes to have all the data in a single table.
close_data_3 = pd.merge(BTC_HIST, ETC_HIST, on=["time"])
close_data_3 = pd.merge(close_data_3, LTC_HIST, on=["time"])

# Mean and standard deviation
monthly_data_3 = close_data_3.resample("M").ffill().pct_change()
SYMBOLS_3 = ["BTC", "ETC", "LTC"] 

print("Mean:")
print(monthly_data_3.mean())
print("STD:")
print(monthly_data_3.std())

rets_3 = np.log(close_data_3[SYMBOLS_3] / close_data_3[SYMBOLS_3].shift(1)).dropna()

(close_data_3[SYMBOLS_3] / close_data_3[SYMBOLS_3].iloc[0]).plot(figsize=(16, 10), title="Portfolio 3 daily stock price")

(monthly_data_3 + 1).cumprod().plot(figsize=(16, 10), title="Portfolio 3 monthly stock price")

# this form a equal weights for each columns like 3 * [0.33333] = [0.33333, 0.33333, 0.33333]
weights_3 = len(close_data_3.columns) * [1 / len(close_data_3.columns)]


print(f"Portfolio 2 returns: {portfolio_return(rets_3, weights_3):.4f}")
print(f"Portfolio 2 volatility: {portfolio_volatility(rets_3, weights_3):.4f}")
print(f"portfolio 2 Sharpe: {portfolio_sharpe(rets_3, weights_3):.4f}")

port_3_vr, port_3_sr = monte_carlo_sharpe(rets_3, SYMBOLS_3, weights_2)

plt.figure(figsize=(16, 10))
fig = plt.scatter(port_3_vr[:, 0], port_3_vr[:, 1], c=port_3_sr, cmap="cool")
CB = plt.colorbar(fig)
CB.set_label("Sharpe ratio")
plt.xlabel("expected volatility")
plt.ylabel("expected return")
plt.title(" | ".join(SYMBOLS_3))


plt.show()