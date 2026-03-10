import requests
import json

# 局域网 Ollama 地址
url = "http://192.168.0.216:11434/"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3.1-optimized",
    "messages": [
        {"role": "user", "content": "帮我写一个 Python 函数计算阶乘"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print("请求失败:", e)