"""
scheduler.py

任务调度器示例
- 支持每天/每小时/定时任务
- 使用 APScheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler
import traceback

scheduler = BackgroundScheduler()

def safe_run(func, *args, **kwargs):
    """
    包装任务函数，捕获异常，防止调度器崩溃
    """
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"[ERROR] 任务执行失败: {e}")
        traceback.print_exc()

def add_job(func, trigger: str = "interval", **trigger_args):
    """
    添加任务到调度器
    trigger: "interval" 或 "cron"
    trigger_args: 传递给 APScheduler trigger 的参数
    """
    scheduler.add_job(safe_run, trigger, args=[func], **trigger_args)
    print(f"[INFO] 任务 {func.__name__} 已添加")

def start_scheduler():
    """
    启动调度器
    """
    scheduler.start()
    print("[INFO] 调度器启动成功")