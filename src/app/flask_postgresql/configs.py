""" Configuration file
"""


import os
import sys
from dotenv import load_dotenv

load_dotenv(encoding='utf8')

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_RECYCLE = 300
    SQLALCHEMY_POOL_TIMEOUT = 300
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 300,
        "pool_size": 10,
        "max_overflow": 20
    }

    SERVICE_PREFIX = os.environ.get('SERVICE_PREFIX', '')
    CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
    CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
    PORT = os.getenv("PORT")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    CHATBOT_DESCRIPTION = os.getenv('CHATBOT_DESCRIPTION')
    CHATBOT_LANGUAGE = os.getenv('CHATBOT_LANGUAGE')
    MEMORY_KEY = "chat_history"

    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            print('Specify SQLALCHEMY_DATABASE_URI as environment variable.')
            sys.exit(1)
        if self.CHANNEL_SECRET is None:
            print('Specify LINE_CHANNEL_SECRET as environment variable.')
            sys.exit(1)
        if self.CHANNEL_ACCESS_TOKEN is None:
            print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
            sys.exit(1)
        if self.SERPAPI_API_KEY is None:
            print('Specify SERPAPI_API_KEY as environment variable.')
            sys.exit(1)
        if self.PORT is None:
            print('Specify PORT as environment variable.')
            sys.exit(1)
        if self.CHATBOT_DESCRIPTION is None:
            print('Specify CHATBOT_DESCRIPTION as environment variable.')
            sys.exit(1)
        if self.CHATBOT_LANGUAGE is None:
            print('Specify CHATBOT_LANGUAGE as environment variable.')
            sys.exit(1)
        
    
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]
    