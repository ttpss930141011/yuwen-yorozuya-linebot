from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', None)
PORT = os.getenv("PORT", 5000)
SERPAPI_API_KEY=os.getenv("SERPAPI_API_KEY", None)
POSTGRES_URL=os.getenv("POSTGRES_URL", None)
CHATBOT_DESCRIPTION = os.getenv('CHATBOT_DESCRIPTION', None)
