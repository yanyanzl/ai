# create virtual enviorenment by miniconda.
"""

step 1:
install miniconda https://docs.conda.io/projects/miniconda/en/latest/
After installing, initialize your newly-installed Miniconda.
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
If you are on macOS Catalina (or later versions), the default shell is zsh.
You will instead need to run source <path to conda>/bin/activate followed
by conda init zsh (to explicitly select the type of shell to initialize).
restart the terminal.

step 2: creat new virtural enviorenment for the new project
conda create -n financial-analysis
conda activate financial-analysis
conda install -c conda-forge numpy scipy pandas matplotlib sympy cython spyder-kernels requests multitasking lxml tqdm
pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance
pip install Historic-Crypto


step 3 change the interpreter on Spyder by Preference> Python interpreter to
/Users/yanyanzhou/miniconda3/envs/financial-analysis/bin/python

step 4 install pandas_datareader package and upgrade yfinance to the lastest version
pip install pandas_datareader
pip install yfinance --upgrade --no-cache-dir

Step 5 install any packages needed. and
when you restart computer, re activate financial-anlysis by
conda activate financial-analysis

"""


# =============================================================================
# to be added:
# output to websites, so to interactive
# plot Y = intercept + slope * X
#  > 2 assets portforlio?
#  compare the result with internet infomation
# =============================================================================

# About Correelation coefficient
# The correlation coefficient is particularly helpful in assessing and managing
# investment risks. For example, modern portfolio theory suggests diversification
# can reduce the volatility of a portfolio's returns, curbing risk.
# The correlation coefficient between historical returns can indicate whether
# adding an investment to a portfolio will improve its diversification.

# Correlation calculations are also a staple of factor investing, a strategy
# for constructing a portfolio based on factors associated with excess returns.
# Meanwhile, quantitative traders use historical correlations and correlation
# coefficients to anticipate near-term changes in securities prices

# proportion of the variation in the dependent variable is attributable to the
# independent variable. That's shown by the coefficient of determination,
# also known as R-squared, which is simply the correlation coefficient squared.

import pandas as pd

# pd.core.common.is_list_like = pd.api.types.is_list_like

# from pandas_datareader import data

from datetime import datetime
import statistics as st
import finlib
from finlib import format_excetpion_message
import yfinance as yf

# import matplotlib as inline
import warnings

warnings.filterwarnings("ignore")
# from datetime import timedelta

# from pandas_datareader.yahoo.headers import DEFAULT_HEADERS


yf.pdr_override()

start = datetime(datetime.now().year, 1, 2)
end = datetime.today()

# variables defined here could be get from the user's input in the
# future but not fixed
# target_price = "Close"
target_one_default = "GOLD"
target_two_default = "TSLA"

strong_correlation_po = 0.8
no_correlation = 0
moderate_correlation_po = 0.5
strong_correlation_ne = -0.8
moderate_correlation_ne = -0.5

default_asset = "SPX"
target_price = "Close"
test_mode = True


# Covariance for one and two. for targets sample Covariance
# (Sum of (Xi - meanX)(Yi - meanY)) / n
# =============================================================================
def get_covariance(data_list_x=list(), data_list_y=list()):
    try:
        # check the args are list
        if isinstance(data_list_x, list | tuple | pd.Series) and isinstance(
            data_list_y, list | tuple | pd.Series
        ):
            # check the list is not empty
            if len(data_list_x) != 0 and len(data_list_y) != 0:
                target_cova = st.covariance(data_list_x, data_list_y)

                # provide information for debug
                if test_mode:
                    print("Covariance is", round(target_cova, 3))

                return target_cova

            # input list is empty
            else:
                raise Exception("The input data list is empty for get_corr")

        # inputs are not list or tuple
        else:
            raise TypeError(
                f"list or tuple or Series expected, got'{type(data_list_x).__name__}'"
            )

    except Exception as ex:
        format_excetpion_message(ex)


# # liner regression for one and two. this will get the slope and intercept for
# # the linear relationship for x (one) and y (two). which is y = intercept + slope * x
# return target_linear. you can get target_linear.intercept
# target_linear.slope
def get_linear_regression(data_list_x=list(), data_list_y=list()):
    try:
        # check the args are list
        if isinstance(data_list_x, list | tuple | pd.Series) and isinstance(
            data_list_y, list | tuple | pd.Series
        ):
            # check the list is not empty
            if len(data_list_x) != 0 and len(data_list_y) != 0:
                target_linear = st.linear_regression(data_list_x, data_list_y)

                # provide information for debug
                if test_mode:
                    print(
                        "The intercept of the linear regression is",
                        round(target_linear.intercept, 3),
                        "and the slope of the regression is",
                        round(target_linear.slope, 3),
                    )

                    print(
                        "the linear relationship Y = ",
                        round(target_linear.intercept, 3),
                        "+",
                        round(target_linear.slope, 3),
                        "* X",
                    )

                return target_linear

            # input list is empty
            else:
                raise Exception("The input data list is empty for get_corr")

        # inputs are not list or tuple
        else:
            raise TypeError(
                "In function get_linear_regression: "
                + "list or tuple or Series expected,"
                + f" got'{type(data_list_x).__name__}'"
            )

    except Exception as ex:
        format_excetpion_message(ex)


# Correlation coefficient for one and two. Pearson correlation. values can range from -1 to 1
# or Pearson's r
# measure of the strength of a linear relationship between two variables
# -1 describes a perfect negative, or inverse, correlation
# 1 shows a perfect positive correlation
# 0 means there is no linear relationship
# correlation coefficient for these variables based on market data reveals a moderate and inconsistent correlation over lengthy periods.


# Correlation coefficient ρ(x,y) = Cov(x,y) / (standard deviation x)(standard deviation y)
def get_corr(data_list_x=list(), data_list_y=list()):
    try:
        # check the args are list
        if isinstance(data_list_x, list | tuple | pd.Series) and isinstance(
            data_list_y, list | tuple | pd.Series
        ):
            # check the list is not empty
            if len(data_list_x) != 0 and len(data_list_y) != 0:
                target_corr = st.correlation(data_list_x, data_list_y)

                # provide information for debug
                if test_mode:
                    print(
                        "Pearson correlation coefficient is",
                        round(target_corr, 3),
                    )

                return target_corr

            # input list is empty
            else:
                raise Exception("The input data list is empty for get_corr")

        # inputs are not list or tuple
        else:
            raise TypeError(
                f"list or tuple or Series expected, got'{type(data_list_x).__name__}'"
            )

    except Exception as ex:
        format_excetpion_message(ex)


# coefficient of determination, also known as R-squared, which is simply the correlation coefficient squared.
# target_rsquare = target_corr ** 2
# =============================================================================
# target_corr = get_corr(target_one_data[target_price], target_two_data[target_price])
# target_rsquare = pow(target_corr, 2)
#
# print(
#     "the coefficient of determination, also known as R-squared is %.3f" % target_rsquare
# )
#
# =============================================================================


# portfolio expected return for two assest. unit: percentage; weight of asset 1
# is w1, expected return of asset1 is expectedreturn1;
# Expected Return = (Weight of A1 * Return of A1) + (Weight of A2 * Return of A2)
def pfreturn(w1=50, w2=50, expectedreturn1=10, expectedreturn2=10):
    try:
        w1 = float(w1) / 100
        w2 = float(w2) / 100
        expectedreturn1 = float(expectedreturn1)
        expectedreturn2 = float(expectedreturn2)

        # =============================================================================
        #         if test_mode:
        #             print(f'weight 1 is {w1:.3f}, weight 2 is {w2:.3f},expected return 1 is {expectedreturn1:.3f}, expected return 2 is {expectedreturn2:.3f}')
        #
        # =============================================================================

        portforlio_expected_return = (
            w1 * expectedreturn1 + w2 * expectedreturn2
        )

        # =============================================================================
        #         if test_mode:
        #             print(f'portfolio return is {portforlio_expected_return:.3f}')
        #
        # =============================================================================

        return format((portforlio_expected_return), ".1f")

    except Exception as ex:
        format_excetpion_message(ex)


# portfolio risk (standard deviation) for two assets. unit: percentage.
# Portfolio Risk σ = √ [(Weight of A12 * Standard Deviation of A12) +
# (Weight of A22 * Standard Deviation of A22) +
# (2 X W1 * W2 * Correlation Coefficient * Standard Deviation of A1 * Standard Deviation of A2)]


def pfrisk(w1=50, w2=50, sd1=10, sd2=10, corr=0.6):
    try:
        import math

        w1p = w1 / 100
        w2p = w2 / 100
        sd1p = sd1 / 100
        sd2p = sd2 / 100

        print(w1p, w2p, sd1p, sd2p, corr)

        portfolio_va = (
            pow(w1p, 2) * pow(sd1p, 2)
            + pow(w2p, 2) * pow(sd2p, 2)
            + 2 * w1p * w2p * sd1p * sd2p * corr
        )
        portfolio_risk = math.sqrt(portfolio_va) * 100  # percentage

        if test_mode:
            print(f"portfolio risk is {portfolio_risk:.3f}")

        return format(portfolio_risk, ".1f")
    except Exception as ex:
        format_excetpion_message(ex)


# build a set of combination for the return and risk. with different weight for two assets.
# The efficient frontier, or the portfolio frontier, describes the ideal
# portfolios predicted to produce the highest return with the lowest risk.
# It depicts the link between risk and returns for a portfolio, with
# expected return on the y-axis and standard deviation as a risk measurement on the x-axis.


def pf_efficient_frontier(er1=10, er2=10, asd1=10, asd2=10, corra=0.6):
    try:
        pf_return = list()
        pf_risk = list()

        # for percentage of the weight from 0 to 100, get return and risk
        for i in range(0, 101):
            # print(i)

            # return of the portfolio when asset1's weight is i
            pf_return.append(
                pfreturn(
                    w1=i, w2=100 - i, expectedreturn1=er1, expectedreturn2=er2
                )
            )

            # risk of the portfolio when asset1's weight is i
            pf_risk.append(
                pfrisk(w1=i, w2=100 - i, sd1=asd1, sd2=asd2, corr=corra)
            )

        return pf_return, pf_risk

    except Exception as ex:
        format_excetpion_message(ex)


# =============================================================================
# # get the date of years ago relative the date dt. this will be the first day
# # of that year. default dt is current date. default years is one year.
# def date_of_years_ago(dt=datetime.today(), years=1):
#     try:
#         return datetime(dt.year - years, month=1, day=1)
#
#     except ValueError as ex:
#         format_excetpion_message(ex)
# =============================================================================


# plot the efficient frontier of two lists for two asset's risk and return
def pf_efrontier_plot(pf_return_list=list(), pf_risk_list=list()):
    try:
        # pf1, pf2 = pf_efficient_frontier(15,10,target_one_sd,target_two_sd,0.5)

        if test_mode:
            print(pf_return_list)
            print(pf_risk_list)

        import matplotlib.pyplot as plt

        # naming the x axis
        plt.xlabel("Risk")
        # naming the y axis
        plt.ylabel("Return")
        # giving a title
        plt.title("Efficient Frontier")

        plt.xscale("linear")

        # Convert contents of lists to numbers (so the )
        new_x = [float(i) for i in pf_risk_list]
        new_y = [float(j) for j in pf_return_list]

        plt.plot(
            new_x,
            new_y,
            color="green",
            marker="o",
            linestyle="dashed",
            linewidth=2,
        )

        # plt.ylim(bottom=0)
        # plt.xlim(left=0)

        # showing legend
        # plt.legend()
        plt.show()

    except Exception as ex:
        format_excetpion_message(ex)


def main():
    try:
        asset1 = finlib.Asset(target_one_default)
        asset2 = finlib.Asset(target_two_default)

        pf_return, pf_risk = pf_efficient_frontier(
            asset1.get_return_his(period=5),
            asset2.get_return_his(period=5),
            asset1.cal_price_sd(),
            asset2.cal_price_sd(),
            get_corr(
                asset1.his_price[target_price], asset2.his_price[target_price]
            ),
        )

        pf_efrontier_plot(pf_return, pf_risk)

    except Exception as ex:
        format_excetpion_message(ex)


# the following code Allows You to Execute Code When the File Runs as a Script,
# but Not When It’s Imported as a Module.
if __name__ == "__main__":
    main()

"""
# plot the relationship between one and two
import matplotlib.pyplot as plt
plt.plot(target_one_data[target_price],target_two_data[target_price])
plt.show()

"""

"""
# using the history() method we can get the share price of the stock over 
# a certain period of time. Using the period parameter we can set how far 
# back from the present to get data. The options for period are 1 day (1d), 
# 5d, 1 month (1mo) , 3mo, 6mo, 1 year (1y), 2y, 5y, 10y, ytd, and max.
target_one_info = yf.Ticker(target_one)
target_one_history = target_one_info.history(period='1y')


# The format that the data is returned in is a Pandas DataFrame. With the Date as the index
# We can reset the index of the DataFrame with the reset_index function
target_one_history.reset_index(inplace=True)

# We can plot the Open price against the Date
# kind of the diagram could be :str scatter, line, area, bar, pie,  
# kde, density (distribution), box (quartile ox and whisker plot or diagram)
# hist (histogram)
# A kernel density estimate (KDE) plot is a method for visualizing the 
# distribution of observations in a dataset, analogous to a histogram.

# target_one_history.plot(x="Date", y=target_price, kind='hist', title=target_one, grid=True)

# plot 8 diagrams (2 * 4), ylabel=target_price will fix y axes to a specific array.
#axes = target_one_history.plot(subplots=True,layout=(2,4),figsize=(10, 6), secondary_y=False, kind='line', title=target_one, grid=True, logy=False, fontsize=12, table=False)

# extract the figure object; only used for tight_layout in this example



# set the individual titles
import matplotlib.pyplot as plt
# The zip object yields n-length tuples, where n is the number of iterables 
# passed as positional arguments to zip(). The i-th element in every tuple 
# comes from the i-th iterable argument to zip(). This continues until the 
#shortest argument is exhausted. list(zip('abcdefg', range(3), range(4))) >>> [('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]
fig, axes = plt.subplots(nrows=3, ncols=2)

for ax, title in zip(axes.ravel(), target_one_history.columns):
    ax.set_title(title)
    ax.plot(target_one_history['Date'],target_one_history[title], color='blue')
fig.tight_layout()
plt.show()

"""

"""
# plot different y on the same x.
axes = target_one_history.plot(x='Date',y=['Open','Close','High'],title='Price Trend chart')
"""
