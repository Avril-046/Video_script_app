
# video_script_app.py
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="视频脚本生成器")

st.title("🎬 视频脚本一键生成器")

st.sidebar.title("🔒 API设置")
st.sidebar.warning("请输入您的API密钥，不要分享给他人")
api_provider = st.sidebar.selectbox("API提供商", ["OpenAI", "DeepSeek"])
api_key = st.sidebar.text_input("API密钥", type="password")

if api_provider == "OpenAI":
    model = st.sidebar.selectbox("模型选择", ["gpt-4.1-mini", "gpt-4", "gpt-3.5-turbo"], index=0)
else:
        model = st.sidebar.selectbox("模型选择", ["deepseek-chat", "deepseek-llm"], index=0)

topic = st.text_input("请输入视频主题")
video_type = st.selectbox("视频类型", ["生活记录", "知识分享", "产品推荐", "娱乐搞笑", "教育学习", "其他"])
audience = st.selectbox("目标受众", ["普通大众", "年轻人", "职场人士", "学生", "家长", "专业人士"])
script_format = st.selectbox("脚本格式", ["标准格式", "分镜格式", "对话格式"])
duration = st.number_input("视频时长（分钟）", min_value=1, max_value=60, value=1)
temperature = st.slider("创造力（temperature）", 0.0, 1.0, 0.7)

if st.button("生成脚本"):
    if not api_key:
        st.warning("请输入API Key")
    elif not topic:
        st.warning("请输入主题")
    else:
        try:
            if api_provider == "OpenAI":
                client = OpenAI(api_key=api_key)
            else:  # DeepSeek
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com/v1"
                )

            prompt = f"""
你是一个专业短视频编剧，请生成一个完整的视频脚本：

主题：{topic}
视频类型：{video_type}
目标受众：{audience}
脚本格式：{script_format}
时长：{duration}分钟

要求：
1. 包含标题
2. 分为开头、中间、结尾
3. 适合{video_type}类型的短视频风格
4. 内容适合{audience}观看
5. 按照{script_format}格式输出
6. 有吸引力
"""

            with st.spinner("AI生成中..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                st.success("生成完成！")
                script_content = response.choices[0].message.content
                st.write(script_content)
                
                # 添加下载按钮
                st.download_button(
                    label="下载脚本",
                    data=script_content,
                    file_name=f"视频脚本_{topic}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"生成失败：{str(e)}")
            st.info("请检查API密钥是否正确，网络连接是否正常")
