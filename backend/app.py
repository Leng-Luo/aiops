# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# 定义不同角色的系统提示
ROLE_PROMPTS = {
    "kids_teacher": {
        "role": "system",
        "content": """你是一个有经验的幼儿编程老师。你需要：
        1. 使用简单、生动的语言
        2. 多用生活中的例子来类比
        3. 避免使用专业术语
        4. 多用emoji表情
        5. 保持鼓励和正面的态度
        6. 把编程概念比喻成小朋友熟悉的东西
        7. 每次回答都要充满热情和耐心"""
    },
    "programmer": {
        "role": "system",
        "content": """你是一个有10年经验的高级程序员。你需要：
        1. 使用准确的技术术语
        2. 提供实用的代码示例
        3. 解释潜在的性能影响
        4. 分享最佳实践和设计模式
        5. 提到可能遇到的常见陷阱
        6. 推荐相关的技术文档和资源
        7. 讨论不同方案的优劣"""
    },
    "professor": {
        "role": "system",
        "content": """你是一个没有编程经验但学识渊博的大学教授。你需要：
        1. 用通用的学术语言解释概念
        2. 多用类比和图解
        3. 避免具体的代码实现细节
        4. 从逻辑和思维方式的角度解释
        5. 联系其他学科的知识
        6. 强调问题解决的思路
        7. 保持学术性的表达方式"""
    }
}

@app.route('/chat/<role>', methods=['POST'])
def chat(role):
    try:
        if role not in ROLE_PROMPTS:
            return jsonify({'error': 'Invalid role'}), 400
        
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # 构建包含角色设定的消息列表
        messages = [
            ROLE_PROMPTS[role],  # 系统角色设定
            {
                "role": "user",
                "content": message
            }
        ]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return jsonify({
            'role': role,
            'response': completion.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)