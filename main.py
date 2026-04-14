import requests
import os
from fastmcp import FastMCP
from dotenv import load_dotenv

SERP_URL = "https://serpapi.com/search"
JINA_URL = "https://r.jina.ai"


load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")


mcp = FastMCP("SearchAgent")

@mcp.tool()
def search_web(query: str, required_links: int = 10):
    """
    General search for websites, articles, and YouTube videos.
    The LLM should provide the query (e.g., 'YouTube explanation of Attention is All You Need').
    """
    required_links = min(required_links, 50)
    results = []
    start = 0
    
    while len(results) < required_links:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERP_API_KEY,
            "start": start,
        }
        try:
            res = requests.get(SERP_URL, params=params)
            res.raise_for_status()
            data = res.json()
            organic = data.get("organic_results", [])
            if not organic: break
            
            for item in organic:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                })
            start += 10
        except Exception as e:
            return {"error": f"Search failed: {e}"}
            
    return results[:required_links]

# --- 2. WEB CONTENT READER ---
@mcp.tool()
def fetch_web_content(url: str) -> str:
    """
    Extracts Markdown text from a URL. Does NOT work for YouTube links.
    """
    if "youtube.com" in url or "youtu.be" in url:
        return "Error: This tool cannot read YouTube videos. Please use a YouTube Transcript tool or summarize based on search snippets."

    reader_url = f"{JINA_URL}/{url}"
    headers = {"Authorization": f"Bearer {JINA_API_KEY}"}
    
    try:
        response = requests.get(reader_url, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text 
    except Exception as e:
        return f"Error accessing page: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")


