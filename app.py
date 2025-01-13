from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_idea', methods=['POST'])
def get_idea():
    query = request.json.get("message")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate 3 unique ideas for: {query} such that the content is a list of\
                 ideas and nothing else. Each idea contains not more than 10 words. The ideas must be short and crisp.\
                 The content must not include descriptions."}
            ],
            max_tokens=100,
        )
        idea = response
        print(idea)
        idea = response.choices[0].message.content.strip()
        return jsonify({'idea': idea})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
