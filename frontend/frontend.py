# frontend.py
import streamlit as st
import requests

# 页面配置
st.set_page_config(
    page_title="AI 故事生成器",
    page_icon="📚",
    layout="wide"
)

# 故事风格选项
STORY_STYLES = {
    "adventure": "冒险故事 🗺️",
    "fantasy": "奇幻故事 🔮",
    "mystery": "悬疑故事 🔍",
    "scifi": "科幻故事 🚀",
    "fairytale": "童话故事 🏰"
}

# 故事长度选项
STORY_LENGTHS = ["短篇（500字左右）", "中篇（1000字左右）", "长篇（2000字左右）"]

# 初始化session state
if 'generated_stories' not in st.session_state:
    st.session_state.generated_stories = []

def generate_story(keywords, style, length):
    """发送请求到后端生成故事"""
    try:
        response = requests.post(
            "http://localhost:5000/generate-story",
            json={
                "keywords": keywords,
                "style": style,
                "length": length
            }
        )
        if response.status_code == 200:
            return response.json()['story']
        return f"Error: {response.json().get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

# 页面标题
st.title("📚 AI 故事生成器")
st.markdown("---")

# 创建两列布局
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("故事设置")
    
    # 关键词输入
    keywords_input = st.text_input("输入关键词（用逗号分隔）:", 
                                 placeholder="例如：森林,魔法,冒险")
    
    # 故事风格选择
    style = st.selectbox(
        "选择故事风格:",
        options=list(STORY_STYLES.keys()),
        format_func=lambda x: STORY_STYLES[x]
    )
    
    # 故事长度选择
    length = st.selectbox("选择故事长度:", STORY_LENGTHS)
    
    # 生成按钮
    if st.button("生成故事"):
        if keywords_input:
            keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
            story = generate_story(keywords, style, length)
            
            # 保存故事到历史记录
            st.session_state.generated_stories.append({
                "keywords": keywords,
                "style": STORY_STYLES[style],
                "length": length,
                "content": story
            })
            
            # 重新加载页面以显示新故事
            st.rerun()
        else:
            st.error("请输入至少一个关键词！")

with col2:
    st.subheader("生成的故事")
    
    if st.session_state.generated_stories:
        # 显示最新生成的故事
        latest_story = st.session_state.generated_stories[-1]
        
        # 创建一个带格式的故事展示区
        st.markdown("### 最新故事")
        st.info(f"""
        **关键词**: {', '.join(latest_story['keywords'])}  
        **风格**: {latest_story['style']}  
        **长度**: {latest_story['length']}
        """)
        st.markdown("---")
        st.markdown(latest_story['content'])
        
        # 显示历史故事
        if len(st.session_state.generated_stories) > 1:
            st.markdown("### 历史故事")
            for i, story in enumerate(reversed(st.session_state.generated_stories[:-1])):
                with st.expander(f"故事 {len(st.session_state.generated_stories) - i - 1}"):
                    st.info(f"""
                    **关键词**: {', '.join(story['keywords'])}  
                    **风格**: {story['style']}  
                    **长度**: {story['length']}
                    """)
                    st.markdown(story['content'])
    else:
        st.info("还没有生成任何故事，请在左侧设置参数并点击生成按钮！")

# 添加清除历史按钮
if st.session_state.generated_stories:
    if st.button("清除所有历史记录"):
        st.session_state.generated_stories = []
        st.rerun()

# 添加页脚
st.markdown("---")
st.markdown("### 使用说明")
st.markdown("""
1. 在左侧输入框中输入关键词，用逗号分隔
2. 选择想要的故事风格和长度
3. 点击"生成故事"按钮
4. 生成的故事会显示在右侧
5. 历史记录会保存本次会话中生成的所有故事
""")