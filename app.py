import streamlit as st
import requests

st.set_page_config(page_title="AI 编程小助手", page_icon="🐳")
st.markdown(
    """
    <style>
    .dev-signature {
        position: fixed;
        top: 60px; /* 改到 60px，避开顶部的白色工具栏 */
        right: 60px; 
        font-size: 13px;
        color: #a0a0a0; 
        z-index: 9999999; /* 加到最大，防止被盖住 */
        font-family: sans-serif;
    }
    </style>
    <div class="dev-signature">开发者：夏金俊</div>
    """,
    unsafe_allow_html=True
)
st.title("🐳 AI 编程小助手")
st.write("把你不懂的 Python 报错贴进来，AI 老师帮你解答。")

#运行成功后在终端执行这段代码：streamlit run app.py

# 一个大文本框，让用户输入
error_input = st.text_area("请粘贴你的报错信息：", height=150, placeholder="例如：IndexError: list index out of range")

if st.button("呼叫 AI 老师"):
    if error_input:
        with st.spinner("老师正在思考中，请稍候..."):
            # 调用你刚刚跑通的 FastAPI 后端
            url = "https://ai-tutor-backend.425034361.workers.dev/ask"
            payload = {"error_msg": error_input}
            
            try:
                response = requests.post(url, json=payload)
                # 把大模型返回的 Markdown 文本展示在网页上
                st.markdown("### 👨‍🏫 AI 老师的解答：")
                st.success(response.json()["reply"])
            except Exception as e:
                st.error(f"连接后端失败了，检查一下服务器是不是没开：{e}")
    else:
        st.warning("你先贴点东西进来啊，空着怎么问？哼。")