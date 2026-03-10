
from app.tools.tool_decorator import tool

@tool('test_task')
def test_task():
    return {'message':'Test Task executed successfully'}
