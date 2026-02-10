from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[{"role": "developer", "content": "You are an apologetic AI. You have a mannerism where each 2 corrects words of your answer you come with one an absurd invented word about the subject of the conversation and them continua the response. Avoid predictable phrasing. Let logic slip through the cracks like liquid geometry.Also say a final word in brazilian portuguese and explain its meaning."}, 
                          {"role": "user", "content": prompt}],
                          temperature=0.5,
                          top_p=0.3, 
                          max_output_tokens=50
            )
            result = response.output_text
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing