# frontend.py
import streamlit as st
import requests

# 页面配置
st.set_page_config(
    page_title="ChatBot with Roles",
    page_icon="💬"
)

# 初始化聊天历史
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 角色描述
ROLE_DESCRIPTIONS = {
    "kids_teacher": "儿童编程教师 👶",
    "programmer": "资深程序员 💻",
    "professor": "大学教授 📚"
}

def send_message(message, role):
    """发送消息到后端"""
    try:
        response = requests.post(
            f"http://localhost:5000/chat/{role}",
            json={"message": message}
        )
        if response.status_code == 200:
            return response.json()['response']
        return f"Error: {response.json().get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

# 页面标题
st.title("💬 多角色聊天机器人 1.0")

# 角色选择
selected_role = st.selectbox(
    "选择你想对话的角色：",
    options=list(ROLE_DESCRIPTIONS.keys()),
    format_func=lambda x: ROLE_DESCRIPTIONS[x]
)

# 显示当前角色的描述
if selected_role == "kids_teacher":
    st.info("👶 我是一位善于用简单语言和生动例子教学的儿童编程老师！")
elif selected_role == "programmer":
    st.info("💻 我是一位经验丰富的程序员，可以提供专业的技术建议！")
else:
    st.info("📚 我是一位从理论角度解释问题的大学教授！")

# 显示聊天历史
for message in st.session_state.messages:
    if message["is_user"]:
        st.write("你: " + message['text'])
    else:
        st.write(f"{ROLE_DESCRIPTIONS[message['role']]}: {message['text']}")

# 用户输入
user_input = st.text_input("请输入你的问题:")

# 发送按钮
if st.button("发送"):
    if user_input:
        # 添加用户消息到历史
        st.session_state.messages.append({
            "is_user": True,
            "text": user_input,
            "role": selected_role
        })
        
        # 获取机器人响应
        bot_response = send_message(user_input, selected_role)
        
        # 添加机器人响应到历史
        st.session_state.messages.append({
            "is_user": False,
            "text": bot_response,
            "role": selected_role
        })
        
        # 重新加载页面显示新消息
        st.rerun()

# 添加清除聊天历史的按钮
if st.button("清除对话历史"):
    st.session_state.messages = []
    st.rerun()
