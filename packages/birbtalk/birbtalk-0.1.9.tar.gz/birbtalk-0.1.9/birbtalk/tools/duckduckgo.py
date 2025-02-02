import os
from duckduckgo_search import DDGS
from ..models import BirbTool

PROXY = os.getenv("PROXY")

# Search pages in duckduckgo
def duckduckgo_tool(max_results: int):
    # Define function
    def function(query: str, **kwargs):
        # Search
        try:
            ddgs = DDGS(proxy=PROXY.replace("socks5", "socks5h") if PROXY else None)
            results = ddgs.text(query, region='wt-wt', safesearch='off', timelimit='y', max_results=max_results)
        except:
            return "Nothing found!"
        # No results
        if len(results) == 0:
            return "Nothing found!"
        # Format texts
        texts = []
        for x in results:
            texts.append(f'Title: {x["title"]}\nSource: [{x["href"]}]({x["href"]})\nText: {x["body"]}')
        return "\n\n".join(texts)
    # Define tool
    return BirbTool(
        name = "web_search",
        description = "Search for information on the web",
        function = function,
        arguments = {
            "query": {
                "type": "string",
                "description": "Short query for search engine that reflects the user's intentions. Should be rich with keywords."
            }
        },
        required = ["query"]
    )

# Search news in duckduckgo
def duckduck_news_tool(max_results: int):
    # Define function
    def function(keywords: str, **kwargs):
        # Search
        try:
            ddgs = DDGS(proxy=PROXY.replace("socks5", "socks5h") if PROXY else None)
            results = ddgs.news(keywords, region='wt-wt', safesearch='off', timelimit='y', max_results=max_results)
        except:
            return "Nothing found!"
        # No results
        if len(results) == 0:
            return "Nothing found!"
        # Format texts
        texts = []
        for x in results:
            texts.append(f'Title: {x["title"]}\nSource: [{x["source"]}]({x["url"]})\nText: {x["body"]}')
        return "\n\n".join(texts)
    # Define tool
    return BirbTool(
        name = "get_news",
        description = "Search for news by keywords",
        function = function,
        arguments = {
            "keywords": {
                "type": "string",
                "description": "List of keywords separated by semicolons."
            }
        },
        required = ["keywords"]
    )
