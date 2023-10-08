from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.utilities.dalle_image_generator import DallEAPIWrapper

from src.app.flask_postgresql.configs import Config

from .current_stock_price import CurrentStockPriceTool
from .google_calendar import GoogleCalendarTool
from .stock_performance import StockPerformanceTool

# initialize LangChain services
search = SerpAPIWrapper(serpapi_api_key=Config.SERPAPI_API_KEY)
dalle = DallEAPIWrapper(openai_api_key=Config.OPENAI_API_KEY)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should \
        ask targeted questions",
    ),
    Tool(
        name="DallE",
        func=dalle.run,
        description="""Useful when you want to generate images.
        Translate description to English and invoke it to generate images.
        """,
    ),
    CurrentStockPriceTool(),
    StockPerformanceTool(),
    GoogleCalendarTool(),
]
