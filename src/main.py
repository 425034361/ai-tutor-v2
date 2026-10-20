import os
import json
from js import fetch
from fastapi import FastAPI, Request
from workers import asgi

# 1. 创建 FastAPI 实例
app = FastAPI()

# 2. 定义路由
@app.post("/ask")
async def ask_question(request: Request):
    try:
        body = await request.json()
        error_msg = body.get("error_msg", "")
    except Exception:
        return {"reply": "请求体解析失败，你是不是没传 JSON 数据过来？"}
    
    if not error_msg:
        return {"reply": "请提供 error_msg 参数，内容不能为空哦。"}

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        # 终极读取法：兼容 Cloudflare 的 JS 代理对象
        api_key = None
        env_obj = request.scope.get("env")
        
        if env_obj:
            try:
                # 方法一：直接作为属性访问（推荐）
                api_key = env_obj.DEEPSEEK_API_KEY
            except AttributeError:
                try:
                    # 方法二：用 getattr 兜底
                    api_key = getattr(env_obj, "DEEPSEEK_API_KEY", None)
                except Exception:
                    pass
                    
        # 方法三：如果都不行，再试 os.environ
        if not api_key:
            api_key = os.environ.get("DEEPSEEK_API_KEY")

        if not api_key:
            return {"reply": "完了，不管怎么拿，都拿不到 DEEPSEEK_API_KEY！"}
        
        api_key_str = str(api_key) 
    
    prompt = f"你是一个耐心的少儿编程老师，请用通俗易懂的语言，给一个初学者解释这个Python报错并提供修改建议：\n{error_msg}"
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = await fetch(
            "https://api.deepseek.com/chat/completions",
            {
                "method": "POST",
                "headers":  [
                    ["Content-Type", "application/json"],
                    ["Authorization", f"Bearer {api_key_str}"]
                ],
                "body": json.dumps(payload)
            }
        )
        
        data = await response.json()
        data_dict = data.to_py()
        
        if "choices" not in data_dict:
            return {"reply": f"大模型报错了，原话是：{data_dict}"}
            
        reply = data_dict["choices"][0]["message"]["content"]
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"底层网络或解析报错了：{e}"}

# 3. 暴露 ASGI 入口
Default = asgi.entrypoint(app)