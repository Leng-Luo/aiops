# frontend.py
import streamlit as st
import requests
import json
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="智能简历分析助手",
    page_icon="📋",
    layout="wide"
)

# 初始化session state
if 'resume_analysis' not in st.session_state:
    st.session_state.resume_analysis = None
if 'optimization_history' not in st.session_state:
    st.session_state.optimization_history = []

def analyze_resume(resume_text, job_description=""):
    """发送简历到后端进行分析"""
    try:
        response = requests.post(
            "http://localhost:5000/analyze-resume",
            json={
                "resume_text": resume_text,
                "job_description": job_description
            }
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"分析失败: {str(e)}")
        return None

def optimize_section(section_text, section_type):
    """发送简历部分到后端进行优化"""
    try:
        response = requests.post(
            "http://localhost:5000/optimize-section",
            json={
                "section_text": section_text,
                "section_type": section_type
            }
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"优化失败: {str(e)}")
        return None

# 页面标题
st.title("📋 智能简历分析助手")
st.markdown("---")

# 创建标签页
tab1, tab2 = st.tabs(["简历分析", "历史记录"])

with tab1:
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 输入简历内容")
        resume_text = st.text_area(
            "粘贴您的简历内容:",
            height=300,
            placeholder="请将您的简历内容粘贴在这里..."
        )
        
        st.subheader("🎯 目标职位描述（可选）")
        job_description = st.text_area(
            "粘贴职位描述:",
            height=150,
            placeholder="粘贴目标职位的描述以获得更精准的建议..."
        )
        
        if st.button("开始分析"):
            if resume_text:
                with st.spinner("正在分析简历..."):
                    analysis_result = analyze_resume(resume_text, job_description)
                    if analysis_result:
                        st.session_state.resume_analysis = analysis_result
                        st.success("分析完成！")
                        st.rerun()
            else:
                st.error("请输入简历内容！")
    
    with col2:
        if st.session_state.resume_analysis:
            st.subheader("📊 分析结果")
            
            # 显示总体评分
            score = st.session_state.resume_analysis.get('overall_score', 0)
            st.progress(score/100)
            st.metric("总体评分", f"{score}/100")
            
            # 显示优势
            with st.expander("💪 简历优势"):
                for strength in st.session_state.resume_analysis.get('strengths', []):
                    st.markdown(f"- {strength}")
            
            # 显示需要改进的地方
            with st.expander("🔨 需要改进"):
                for improvement in st.session_state.resume_analysis.get('improvements', []):
                    st.markdown(f"- {improvement}")
            
            # 显示技能分析
            with st.expander("🎯 技能评估"):
                skills = st.session_state.resume_analysis.get('skills_analysis', {})
                for skill, rating in skills.items():
                    st.markdown(f"**{skill}**: {rating}")
            
            # 显示ATS优化建议
            with st.expander("🤖 ATS优化建议"):
                for suggestion in st.session_state.resume_analysis.get('ats_optimization', []):
                    st.markdown(f"- {suggestion}")
            
            # 显示关键词匹配
            with st.expander("🔑 关键词匹配"):
                keywords = st.session_state.resume_analysis.get('keyword_matches', [])
                st.write("匹配到的关键词：")
                st.write(", ".join(keywords))
            
            # 添加优化功能
            st.subheader("✨ 内容优化")
            section_type = st.selectbox(
                "选择要优化的部分:",
                ["工作经验", "技能描述", "教育背景", "个人简介"]
            )
            section_text = st.text_area(
                f"输入要优化的{section_type}内容:",
                height=150
            )
            
            if st.button("优化内容"):
                if section_text:
                    with st.spinner("正在优化..."):
                        optimization_result = optimize_section(section_text, section_type)
                        if optimization_result:
                            st.session_state.optimization_history.append({
                                'type': section_type,
                                'original': section_text,
                                'optimized': optimization_result['optimized_content']
                            })
                            st.success("优化完成！")
                            st.markdown("### 优化结果：")
                            st.markdown(optimization_result['optimized_content'])
                else:
                    st.error("请输入要优化的内容！")

with tab2:
    if st.session_state.optimization_history:
        st.subheader("📚 优化历史记录")
        for i, item in enumerate(st.session_state.optimization_history):
            with st.expander(f"{item['type']} - 优化记录 {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**原始内容：**")
                    st.markdown(item['original'])
                with col2:
                    st.markdown("**优化后内容：**")
                    st.markdown(item['optimized'])
        
        if st.button("清除历史记录"):
            st.session_state.optimization_history = []
            st.rerun()
    else:
        st.info("暂无优化历史记录")

# 添加页脚说明
st.markdown("---")
st.markdown("""
### 💡 使用说明
1. 在左侧输入框粘贴您的简历内容
2. 可选择添加目标职位描述以获得更精准的建议
3. 点击"开始分析"获取详细分析报告
4. 使用优化功能改进特定部分的内容
5. 在历史记录标签页查看之前的优化记录
""")