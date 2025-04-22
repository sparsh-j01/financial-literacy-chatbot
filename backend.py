# Extended MVP for Financial Literacy WhatsApp Chatbot (Multilingual + Voice Support + Voice Input + AI Integration)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
from collections import deque

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Rate limiting setup - 60 requests per minute
MAX_REQUESTS = 60
WINDOW_SIZE = timedelta(minutes=1)
requests_timestamps = deque()

# Configure Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=GOOGLE_API_KEY)

# List available models
try:
    for m in genai.list_models():
        print(f"Model: {m.name}")
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')  # Updated to use available model
except Exception as e:
    print(f"Error listing models: {str(e)}")
    raise

def is_rate_limited():
    current_time = datetime.now()
    # Remove timestamps older than the window size
    while requests_timestamps and current_time - requests_timestamps[0] > WINDOW_SIZE:
        requests_timestamps.popleft()
    # Check if we've hit the limit
    if len(requests_timestamps) >= MAX_REQUESTS:
        return True
    requests_timestamps.append(current_time)
    return False

def get_ai_response(prompt, lang='en'):
    try:
        # Check for Telugu language indicator
        is_telugu = lang == 'te'
        
        # Prepare the prompt with language instruction
        if is_telugu:
            system_prompt = "You are a helpful financial literacy assistant. Please respond in Telugu language using Telugu script. Answer this question: "
        else:
            system_prompt = "You are a helpful financial literacy assistant. Answer this question: "
        
        response = model.generate_content(system_prompt + prompt)
        return response.text
    except Exception as e:
        print(f"Error in get_ai_response: {str(e)}")
        return f"Error: {str(e)}"

@app.route("/webhook", methods=["POST"])
def webhook():
    # Check rate limit
    if is_rate_limited():
        return jsonify({
            "response": "Rate limit exceeded. Please wait a minute before trying again."
        }), 429

    incoming_msg = request.values.get("Body", "").strip()
    
    # Check for language preference
    lang = 'en'  # default to English
    if incoming_msg.endswith(" #te"):
        lang = 'te'
        incoming_msg = incoming_msg.replace(" #te", "").strip()
    
    bot_response = get_ai_response(incoming_msg, lang)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
