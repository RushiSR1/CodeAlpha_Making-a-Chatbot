import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.has_ai = True
        else:
            print("Warning: GEMINI_API_KEY not found. AI features disabled.")
            self.has_ai = False

        # Predefined patterns (Regex -> Response)
        self.patterns = {
            r"(?i)\b(hi|hello|hey|greetings)\b": "Hello! How can I assist you today?",
            r"(?i)\b(pricing|cost|price)\b": "Our basic plan starts at $10/month, and the pro plan is $50/month.",
            r"(?i)\b(contact|support|email)\b": "You can reach our support team at support@example.com.",
            r"(?i)\b(services|features)\b": "We offer AI integration, 24/7 chatbot support, and automated workflows.",
            r"(?i)\b(bye|goodbye|exit)\b": "Goodbye! Have a great day!",
            r"(?i)\b(help)\b": "I can help you with pricing, services, and contacting support. Just ask!"
        }

    def get_response(self, user_input: str) -> str:
        # 1. Check Predefined Patterns
        for pattern, response in self.patterns.items():
            if re.search(pattern, user_input):
                return response
        
        # 2. Hybrid/AI Fallback
        if self.has_ai:
            try:
                response = self.model.generate_content(user_input)
                return response.text
            except Exception as e:
                return f"I encountered an error connecting to my brain: {str(e)}"
        
        # 3. Default Fallback if no AI
        return "I'm not sure about that. Can you ask about our pricing, services, or contact info?"
