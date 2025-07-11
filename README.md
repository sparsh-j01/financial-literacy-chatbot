# Financial Literacy Chatbot

A bilingual (English/Telugu) financial literacy chatbot using Google's Gemini AI.

## Features
- Real-time chat interface
- Bilingual support (English and Telugu)
- Rate limiting to ensure free tier usage
- Clean, WhatsApp-like UI
- No credit card required

## Setup
1. Clone the repository:
```bash
git clone [your-repository-url]
cd financial-literacy-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your-api-key-here
```

4. Run the backend:
```bash
python backend.py
```

5. Open `index.html` in your browser or serve it using a simple HTTP server:
```bash
python -m http.server 8000
```
Then visit: `http://localhost:8000`

## Usage
- Type your financial questions in English
- For Telugu responses, check the "Use Telugu (తెలుగు)" checkbox
- The chatbot will respond appropriately in the selected language

## Technical Details
- Backend: Python/Flask
- Frontend: HTML/CSS/JavaScript
- AI: Google Gemini API
- Rate Limiting: 60 requests per minute

## Note
This project uses Google's Gemini API free tier, which has a generous limit and doesn't require a credit card.
