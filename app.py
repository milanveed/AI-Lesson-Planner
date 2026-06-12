from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Groq API Key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Generate Lesson Plan
@app.route('/generate', methods=['POST'])
def generate():

    subject = request.form['subject']
    topic = request.form['topic']
    duration = request.form['duration']
    difficulty = request.form['difficulty']

    prompt = f"""
    Generate a detailed lesson plan.

    Subject: {subject}
    Topic: {topic}
    Duration: {duration}
    Difficulty: {difficulty}

    Include:
    1. Learning Objectives
    2. Teaching Flow
    3. Activities
    4. Quiz Questions
    5. Homework
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    lesson_plan = completion.choices[0].message.content

    return render_template(
        'result.html',
        lesson=lesson_plan
    )

if __name__ == '__main__':
    app.run(debug=True)