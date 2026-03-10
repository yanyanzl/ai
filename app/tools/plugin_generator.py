import os
import json

PLUGIN_BASE_DIR = "app/plugins"

PLUGIN_PY_TEMPLATE = '''import os
from app.utils.logger import get_logger

logger = get_logger("{plugin_name}_plugin")

class Plugin:
    name = "{plugin_name}"

    def register(self, router):
        """
        将工具注册到系统的 tool_router
        """
        router.register_tool(self.name, self.run)

    def run(self, args: dict):
        """
        工具执行入口，args 中包含用户传入参数
        """
{param_parse}
        try:
            # TODO: 插入你的业务逻辑
            result = {{}}
            return result
        except Exception as e:
            logger.error(f"{{self.name}} failed: {{e}}")
            return {{"error": str(e)}}
'''

PLUGIN_JSON_TEMPLATE = '''{{
  "name": "{plugin_name}",
  "description": "{description}",
  "version": "1.0",
  "enabled": true,
  "parameters": {{
{param_schema}
  }}
}}
'''


def create_plugin(plugin_name, description="新插件", parameters=None):
    parameters = parameters or {}
    plugin_dir = os.path.join(PLUGIN_BASE_DIR, plugin_name)
    os.makedirs(plugin_dir, exist_ok=True)

    # 生成参数解析代码
    param_parse_lines = []
    for k, v in parameters.items():
        default_val = repr(v.get("default"))
        param_parse_lines.append(f"        {k} = args.get('{k}', {default_val})  # {v.get('description','')}")
    param_parse_code = "\n".join(param_parse_lines) if param_parse_lines else "        pass  # no parameters"

    # 写 plugin.py
    plugin_py = PLUGIN_PY_TEMPLATE.format(
        plugin_name=plugin_name,
        param_parse=param_parse_code
    )
    with open(os.path.join(plugin_dir, "plugin.py"), "w", encoding="utf-8") as f:
        f.write(plugin_py)

    # 生成参数 schema JSON
    param_schema_lines = []
    for k, v in parameters.items():
        line = f'    "{k}": {{"type": "{v.get("type","string")}", "default": {json.dumps(v.get("default"))}, "description": "{v.get("description","")}"}}'
        param_schema_lines.append(line)
    param_schema_text = ",\n".join(param_schema_lines)

    plugin_json = PLUGIN_JSON_TEMPLATE.format(
        plugin_name=plugin_name,
        description=description,
        param_schema=param_schema_text
    )
    with open(os.path.join(plugin_dir, "plugin.json"), "w", encoding="utf-8") as f:
        f.write(plugin_json)

    print(f"插件 '{plugin_name}' 已生成在 {plugin_dir}")


# ---------------------------
# 批量生成插件
# ---------------------------
def batch_generate_from_json(config_path="plugins_config.json"):
    """
    JSON 配置示例：
    [
        {
            "name": "scan_desktop",
            "description": "扫描桌面文件",
            "parameters": {
                "folder": {"type": "string", "default": "C:/Users/Public/Desktop", "description": "扫描路径"},
                "include_hidden": {"type": "boolean", "default": false, "description": "是否包含隐藏文件"}
            }
        },
        {
            "name": "clean_temp",
            "description": "清理临时文件",
            "parameters": {}
        }
    ]
    """
    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        plugins = json.load(f)

    for p in plugins:
        create_plugin(
            plugin_name=p.get("name"),
            description=p.get("description", "新插件"),
            parameters=p.get("parameters", {})
        )


# ---------------------------
# 交互式生成单个插件
# ---------------------------
def interactive():
    print("=== 插件生成器 ===")
    plugin_name = input("输入插件名: ").strip()
    description = input("输入插件描述: ").strip()

    parameters = {}
    while True:
        add_param = input("添加参数? (y/n): ").strip().lower()
        if add_param != "y":
            break
        param_name = input("  参数名: ").strip()
        param_type = input("  参数类型 (string/int/boolean): ").strip()
        default_val = input("  默认值: ").strip()
        try:
            if param_type == "int":
                default_val = int(default_val)
            elif param_type == "boolean":
                default_val = default_val.lower() in ["true", "1", "yes"]
        except Exception:
            pass
        param_desc = input("  参数描述: ").strip()
        parameters[param_name] = {"type": param_type, "default": default_val, "description": param_desc}

    create_plugin(plugin_name, description, parameters)


# ---------------------------
# 示例用法
# ---------------------------
if __name__ == "__main__":
    print("选择模式:")
    print("1. 交互式生成单个插件")
    print("2. 批量生成插件（从 plugins_config.json）")
    mode = input("选择 (1/2): ").strip()
    if mode == "1":
        interactive()
    elif mode == "2":
        batch_generate_from_json()
    else:
        print("无效选择")


# if __name__ == "__main__":
#     interactive()

    # create_plugin(
    #     plugin_name="scan_desktop",
    #     description="扫描桌面文件",
    #     parameters={
    #         "folder": {"type": "string", "default": "C:/Users/Public/Desktop", "description": "需要扫描的文件夹路径"},
    #         "include_hidden": {"type": "boolean", "default": False, "description": "是否包含隐藏文件"}
    #     }
    # )