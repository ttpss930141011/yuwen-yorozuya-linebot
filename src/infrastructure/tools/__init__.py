from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper

from src.app.flask_postgresql.configs import Config

from .stock import CurrentStockPriceTool, StockPerformanceTool

# initialize LangChain services
search = SerpAPIWrapper(serpapi_api_key=Config.SERPAPI_API_KEY)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should \
        ask targeted questions",
    ),
    CurrentStockPriceTool(),
    StockPerformanceTool(),
]
