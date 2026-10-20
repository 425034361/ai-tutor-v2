import urllib.request
import json

url = "https://ai-tutor-backend.425034361.workers.dev/ask"
payload = {"error_msg": "IndexError: list index out of range"}
data = json.dumps(payload).encode('utf-8')

# 关键：加上 User-Agent 马甲
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, data=data, headers=headers, method='POST')

print("正在请求云端 Worker，请稍候...")
try:
    with urllib.request.urlopen(req) as response:
        print("状态码:", response.status)
        print("返回结果:\n", response.read().decode('utf-8'))
except Exception as e:
    print("请求失败:", e)