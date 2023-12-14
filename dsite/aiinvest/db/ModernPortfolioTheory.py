#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:14:14 2023

@author: Yanyanzl
"""
"""
MPT
The modern portfolio theory (MPT) is a practical method for selecting 
investments in order to maximize their overall returns within an acceptable
level of risk
Any given investment's risk and return characteristics should not be viewed 
alone but should be evaluated by how it affects the overall portfolio's risk 
and return. That is, an investor can construct a portfolio of multiple assets 
that will result in greater returns without a higher level of risk.

The MPT assumes that investors are risk-averse, meaning they prefer a less 
risky portfolio to a riskier one for a given level of return.

As a practical matter, risk aversion implies that most people should invest 
in multiple asset classes

Return:
The expected return of the portfolio is calculated as a weighted 
sum of the returns of the individual assets.

Risk: Sigma, or standard deviation
The portfolio's risk is a function of the variances of each asset and the 
correlations of each pair of assets. To calculate the risk of a four-asset 
portfolio, an investor needs each of the four assets' variances and six 
correlation values, 4 * 3 / 2 = 6.  Because of the asset correlations, 
the total portfolio risk, or standard deviation, is lower than what would 
be calculated by a weighted sum.

For example, stock investors can reduce risk by putting a portion of their 
portfolios in government bond ETFs. The variance of the portfolio will be 
significantly lower because government bonds have a negative correlation 
with stocks. Adding a small investment in Treasuries to a stock portfolio 
will not have a large impact on expected returns because of this 
loss-reducing effect.

Looking for Negative Correlation

The modern portfolio theory allows investors to construct more efficient 
portfolios. Every possible combination of assets can be plotted on a graph, 
with the portfolio's risk on the X-axis and the expected return on the Y-axis


It is possible to draw an upward sloping curve to connect all of 
the most efficient portfolios. This curve is called the efficient frontier.

The modern portfolio theory (MPT) was a breakthrough in personal investing. 
It suggests that a conservative investor can do better by choosing a mix of 
low-risk and riskier investments than by going entirely with low-risk choices. 
More importantly, it suggests that the more rewarding option does not add 
additional overall risk

The modern portfolio theory can be used to diversify a portfolio in order to 
get a better return overall without a bigger risk.

Another benefit of the modern portfolio theory (and of diversification) is 
that it can reduce volatility. The best way to do that is to choose assets 
that have a negative correlation, such as U.S. treasuries and small-cap stocks.

Ultimately, the goal of the modern portfolio theory is to create the most 
efficient portfolio possible.

PMPT:
The post-modern portfolio theory (PMPT) attempts to improve modern portfolio 
theory by minimizing downside risk instead of variance.
Perhaps the most serious criticism of the MPT is that it evaluates portfolios 
based on variance rather than downside risk.
That is, two portfolios that have the same level of variance and returns are 
considered equally desirable under modern portfolio theory. One portfolio 
may have that variance because of frequent small losses. Another could have 
that variance because of rare but spectacular declines. Most investors would 
prefer frequent small losses, which would be easier to endure.

Limitations and assumptions:
1. tail risk, fat tail distribution but not normal distribution
2. investors are rational and avoid risk when possible, 
3. there are not enough investors to influence market prices, 
4. investors have unlimited access to borrowing and lending money at the 
risk-free interest rate


However, 
reality proves that the market includes irrational and risk-seeking investors, 
there are large market participants who could influence market prices, 
and there are investors who do not have unlimited access to borrowing and lending money.



"""

from coefficient import asset_return_his

asset_return_his("TSLA")



