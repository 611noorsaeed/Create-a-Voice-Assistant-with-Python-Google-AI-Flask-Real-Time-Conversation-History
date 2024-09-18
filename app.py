import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-pro")

# A global variable to store conversation history
conversation_history = []


# Voice assistance function
def voice_assistance(user_input):
    global conversation_history
    prompt = f"""
    Please provide a professional and concise solution or response to the following user query:
    '{user_input}'
    The answer should be brief, precise, and directly address the request.
    Don't hesitate to provide concise, dont' apologize, you must provide the details user looking for.
    """
    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response


# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle voice input and return model response with conversation history
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistance(user_input)

    # Return the updated conversation history
    return jsonify({'response': response, 'conversation_history': conversation_history})


if __name__ == '__main__':
    app.run(debug=True)
