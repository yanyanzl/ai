"""
finance_agent.py - FinanceAgent v1.1

功能：
- fetch_market_data: 获取市场数据（本地模拟或 Yahoo Finance API）
- generate_strategy: 生成示例策略
- backtest_strategy: 回测策略
- task_finance_example: 整合任务，安全执行，返回完整结果
"""

from app.tools.tool_decorator import tool
from app.core.config import Config
from app.utils.logger import get_logger

import requests
import yfinance as yf  # pip install yfinance

logger = get_logger("finance_agent")

# --------------------------
# 获取市场数据
# --------------------------
@tool("fetch_market_data")
def fetch_market_data(symbol: str):
    """
    获取市场数据，返回 dict
    支持 test_mode 配置
    """
    try:
        test_mode = Config.get("finance.test_mode", True)
        if test_mode:
            # 本地模拟数据
            data = [
                {"date": "2026-03-10", "close": 150},
                {"date": "2026-03-09", "close": 152},
                {"date": "2026-03-08", "close": 148},
            ]
            logger.info(f"[fetch_market_data] 模拟数据 {symbol}")
            return {"symbol": symbol, "data": data}

        # Yahoo Finance 实时数据
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo", interval="1d")
        data = [{"date": str(idx.date()), "close": row["Close"]} for idx, row in hist.iterrows()]
        logger.info(f"[fetch_market_data] Yahoo Finance 数据 {symbol}")
        return {"symbol": symbol, "data": data}

    except Exception as e:
        logger.error(f"[fetch_market_data] 错误: {e}")
        return {"error": str(e)}


# --------------------------
# 生成交易策略
# --------------------------
@tool("generate_strategy")
def generate_strategy(symbol: str):
    try:
        strategy = {
            "symbol": symbol,
            "buy_signal": "MA50 > MA200",
            "sell_signal": "MA50 < MA200"
        }
        logger.info(f"[generate_strategy] {symbol} 策略生成成功")
        return {"strategy": strategy}
    except Exception as e:
        logger.error(f"[generate_strategy] {e}")
        return {"error": str(e)}


# --------------------------
# 策略回测
# --------------------------
@tool("backtest_strategy")
def backtest_strategy(strategy: dict, historical_data: list):
    try:
        profit = sum([d.get("close", 0) * 0.01 for d in historical_data])
        logger.info(f"[backtest_strategy] 回测收益 {profit}")
        return {"profit": profit}
    except Exception as e:
        logger.error(f"[backtest_strategy] 回测错误: {e}")
        return {"error": str(e)}


# --------------------------
# 示例金融任务
# --------------------------
@tool("task_finance_example")
def task_finance_example():
    symbol = "AAPL"
    result_summary = {}

    # 1. 获取市场数据
    res = fetch_market_data(symbol)
    result_summary["market_data"] = res
    if "error" in res:
        logger.error(f"[TASK ERROR] fetch_market_data: {res['error']}")
        return result_summary

    # 2. 生成策略
    strategy_res = generate_strategy(symbol)
    result_summary["strategy"] = strategy_res
    if "error" in strategy_res:
        logger.error(f"[TASK ERROR] generate_strategy: {strategy_res['error']}")
        return result_summary

    # 3. 回测策略
    backtest_res = backtest_strategy(strategy_res["strategy"], res["data"])
    result_summary["backtest"] = backtest_res
    if "error" in backtest_res:
        logger.error(f"[TASK ERROR] backtest_strategy: {backtest_res['error']}")
    else:
        logger.info(f"[TASK] {symbol} 策略回测收益: {backtest_res['profit']}")

    return result_summary