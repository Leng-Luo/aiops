# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def analyze_resume(resume_text, job_description=""):
    """分析简历内容并返回建议"""
    
    analysis_prompt = f"""请分析以下简历，并提供详细的反馈和建议。
    
    简历内容：
    {resume_text}
    
    {f'目标职位描述：{job_description}' if job_description else ''}
    
    请提供以下方面的分析：
    1. 简历强项
    2. 需要改进的地方
    3. 关键技能评估
    4. 经验匹配度分析
    5. 具体的改进建议
    6. ATS优化建议
    
    请以JSON格式返回，包含以下字段：
    - strengths: 优势列表
    - improvements: 需改进项列表
    - skills_analysis: 技能评估对象
    - experience_match: 经验匹配分析
    - specific_suggestions: 具体建议列表
    - ats_optimization: ATS优化建议列表
    - keyword_matches: 关键词匹配列表
    - overall_score: 总体评分(0-100)
    """
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位专业的HR和职业顾问，擅长简历分析和优化建议。"},
                {"role": "user", "content": analysis_prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Analysis failed: {str(e)}")

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume_endpoint():
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
            
        analysis_result = analyze_resume(resume_text, job_description)
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/optimize-section', methods=['POST'])
def optimize_section():
    """优化简历特定部分"""
    try:
        data = request.get_json()
        section_text = data.get('section_text', '')
        section_type = data.get('section_type', '')
        
        if not section_text or not section_type:
            return jsonify({'error': 'Section text and type are required'}), 400
        
        prompt = f"""请优化以下{section_type}部分的内容，使其更专业、更有影响力：
        
        原内容：
        {section_text}
        
        请提供：
        1. 优化后的内容
        2. 改进说明
        """
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位专业的简历优化专家。"},
                {"role": "user", "content": prompt}
            ]
        )
        
        return jsonify({
            'optimized_content': completion.choices[0].message.content,
            'section_type': section_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)