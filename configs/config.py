""" Configuration file
"""

import os
from dotenv import load_dotenv

load_dotenv(encoding='utf8')

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', None)
PORT = os.getenv("PORT")
SERPAPI_API_KEY=os.getenv("SERPAPI_API_KEY", None)
POSTGRES_URL=os.getenv("POSTGRES_URL", None)
CHATBOT_DESCRIPTION = os.getenv('CHATBOT_DESCRIPTION', None)
CHATBOT_LANGUAGE = os.getenv('CHATBOT_LANGUAGE', None)
