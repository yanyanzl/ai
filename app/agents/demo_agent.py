
from app.tools.tool_decorator import tool

@tool('demo_task')
def demo_task():
    try:
        return {'message': 'Demo Task 执行成功'}
    except Exception as e:
        return {'error': str(e)}
