"""
finance_agent.py

FinanceAgent：金融市场研究与投资示例
- 核心模块：MarketData、StrategyGenerator、Backtester
- 容错机制：网络错误、数据异常、策略异常
"""

from app.tools.tool_decorator import tool
import requests

@tool("fetch_market_data")
def task_finance_example():
    """每天示例金融任务"""
    symbol = "AAPL"
    res = fetch_market_data(symbol)
    if "error" in res:
        print(f"[TASK ERROR] fetch_market_data: {res['error']}")
        return

    strategy_res = generate_strategy(symbol)
    if "error" in strategy_res:
        print(f"[TASK ERROR] generate_strategy: {strategy_res['error']}")
        return

    # 假设历史数据模拟
    historical_data = [{"close": 150}, {"close": 152}, {"close": 148}]
    backtest_res = backtest_strategy(strategy_res["strategy"], historical_data)
    if "error" in backtest_res:
        print(f"[TASK ERROR] backtest_strategy: {backtest_res['error']}")
    else:
        print(f"[TASK] {symbol} 策略回测收益: {backtest_res['profit']}")

@tool("fetch_market_data")
def fetch_market_data(symbol: str):
    """
    获取市场数据（示例使用模拟接口）
    返回 dict
    """
    try:
        # 模拟请求，真实场景请接入行情API
        url = f"https://api.example.com/market/{symbol}"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return {"error": f"请求失败, 状态码: {response.status_code}"}

        data = response.json()
        return {"symbol": symbol, "data": data}
    except requests.RequestException as e:
        return {"error": f"网络错误: {e}"}
    except Exception as e:
        return {"error": str(e)}

@tool("generate_strategy")
def generate_strategy(symbol: str):
    """
    生成简单交易策略示例
    """
    try:
        # TODO: 用 AI 生成更复杂策略
        strategy = {
            "symbol": symbol,
            "buy_signal": "MA50 > MA200",
            "sell_signal": "MA50 < MA200"
        }
        return {"strategy": strategy}
    except Exception as e:
        return {"error": str(e)}

@tool("backtest_strategy")
def backtest_strategy(strategy: dict, historical_data: list):
    """
    回测策略示例
    """
    try:
        # 简单模拟收益
        profit = sum([d.get("close", 0) * 0.01 for d in historical_data])
        return {"profit": profit}
    except Exception as e:
        return {"error": str(e)}