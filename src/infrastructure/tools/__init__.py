from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool

from .stock import CurrentStockPriceTool, StockPerformanceTool

# initialize LangChain services
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    CurrentStockPriceTool(),
    StockPerformanceTool()
]