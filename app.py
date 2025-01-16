from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

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
                 ideas and nothing else. These ideas must must be software engineering related. Each idea contains not\
                 more than 10 words. The ideas must be short and crisp. The content must not include descriptions."}
            ],
            max_tokens=100,
        )
        idea = response.choices[0].message.content.strip().split("\n")
        print(idea, type(idea))
        return jsonify({'idea': idea})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_detailed_description', methods=['POST'])
def get_detailed_description():
    options = request.json.get("options")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Elaborate the following ideas {options} in detail such that the contents does not\
                 exceed 100 words per idea and nothing else."}
            ],
            max_tokens=100,
        )
        idea_description = response.choices[0].message.content
        return jsonify({'detailed_description': idea_description})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
