# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

STORY_STYLES = {
    "adventure": "一个充满冒险和刺激的故事，包含意外和转折",
    "fantasy": "一个包含魔法和奇幻元素的故事，有神奇生物和魔法世界",
    "mystery": "一个充满悬疑和谜题的故事，需要解开谜团",
    "scifi": "一个发生在未来或太空的科幻故事，包含先进科技",
    "fairytale": "一个童话风格的故事，适合儿童阅读，富含寓意"
}

def generate_story_prompt(keywords, style, length):
    """生成故事提示"""
    base_prompt = f"""请根据以下关键词创作一个{style}风格的{length}故事：
    关键词：{', '.join(keywords)}
    
    要求：
    1. 故事应该是{STORY_STYLES[style]}
    2. 故事长度应该是{length}
    3. 包含对话和描写
    4. 确保故事有完整的开端、发展、高潮和结局
    5. 使用生动的语言
    
    请直接开始讲述故事，不需要其他解释：
    """
    return base_prompt

@app.route('/generate-story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        style = data.get('style', 'adventure')
        length = data.get('length', '短篇')
        
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
            
        # 生成故事
        prompt = generate_story_prompt(keywords, style, length)
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的故事创作者，善于写作引人入胜的故事。"},
                {"role": "user", "content": prompt}
            ]
        )
        
        story = completion.choices[0].message.content
        
        return jsonify({
            'story': story,
            'style': style,
            'keywords': keywords
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)