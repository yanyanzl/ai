# scheduler.py
"""
任务调度器
- 支持每天/每小时/定时任务
- 使用 APScheduler
- 完全支持 config.yaml 配置化
"""

from apscheduler.schedulers.background import BackgroundScheduler
import traceback
from app.core.config import Config
from app.utils.logger import get_logger

logger = get_logger("scheduler")

def wrap_task(func, name: str):
    """统一任务执行封装"""
    def wrapper():
        try:
            res = func()
            if not isinstance(res, dict):
                res = {"message": str(res)}
            if "error" in res:
                logger.warning(f"[TASK ERROR] {name}: {res['error']}")
                return {"task": name, "status": "error", "result": res["error"]}
            logger.info(f"[TASK OK] {name}: {res.get('message', res)}")
            return {"task": name, "status": "ok", "result": res.get("message", res)}
        except Exception as e:
            logger.error(f"[TASK EXCEPTION] {name}: {e}")
            return {"task": name, "status": "error", "result": str(e)}
    return wrapper


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
    trigger: interval / cron
    trigger_args: APScheduler 支持的参数
    """
    # 支持旧配置 interval_minutes / interval_seconds -> 自动映射
    if "interval_minutes" in trigger_args:
        trigger_args["minutes"] = trigger_args.pop("interval_minutes")
    if "interval_seconds" in trigger_args:
        trigger_args["seconds"] = trigger_args.pop("interval_seconds")

    # interval 默认值
    if trigger == "interval" and not any(k in trigger_args for k in ["seconds", "minutes", "hours"]):
        trigger_args["minutes"] = 1

    try:
        scheduler.add_job(safe_run, trigger, args=[func], **trigger_args)
        print(f"[INFO] 任务 {func.__name__} 已添加, trigger={trigger}, args={trigger_args}")
    except Exception as e:
        print(f"[ERROR] 添加任务 {func.__name__} 失败: {e}")
        traceback.print_exc()


def add_jobs_from_config(task_funcs: dict):
    """
    从配置文件添加所有任务
    task_funcs: dict，key=任务名, value=任务函数
    配置示例 (config.yaml):
    
    scheduler:
      tasks:
        demo_task:
          trigger: interval
          minutes: 1
        scan_desktop:
          trigger: interval
          minutes: 2
        clean_temp:
          trigger: interval
          minutes: 3
        task_finance_example:
          trigger: cron
          hour: 0
          minute: 30
    """
    tasks_config = Config.get("scheduler.tasks", {})
    for task_name, func in task_funcs.items():
        cfg = tasks_config.get(task_name, {})
        trigger = cfg.get("trigger", "interval")
        trigger_args = {k: v for k, v in cfg.items() if k != "trigger"}

        # 自动映射 interval_minutes -> minutes, interval_seconds -> seconds
        if "interval_minutes" in trigger_args:
            trigger_args["minutes"] = trigger_args.pop("interval_minutes")
        if "interval_seconds" in trigger_args:
            trigger_args["seconds"] = trigger_args.pop("interval_seconds")

        if not trigger_args:
            trigger_args = {"minutes": 1} if trigger == "interval" else {}

        add_job(func, trigger=trigger, **trigger_args)

def start_scheduler():
    """
    启动调度器
    """
    scheduler.start()
    print("[INFO] 调度器启动成功")