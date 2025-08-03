from fastapi import FastAPI, Query
from typing import List, Dict
import os
import httpx
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
app = FastAPI()

load_dotenv()
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")

client = Cerebras(api_key=CEREBRAS_API_KEY)

@app.get("/")
async def root():
    return {"message": "QuickDigest backend running"}

# Dummy articles
DUMMY_ARTICLES = [
    {
        "title": "Tech breakthrough in AI",
        "content": "Artificial intelligence is advancing rapidly...",
        "link": "https://example.com/tech1"
    },
    {
        "title": "New gadget released",
        "content": "The latest gadget has many features...",
        "link": "https://example.com/tech2"
    }
]

def dummy_summarize(text: str) -> str:
    # For now, just return first 10 chars + '...'
    return text[:10] + "..."

@app.get("/api/summaries")
async def get_summaries(topic: str = Query(..., description="Topic to summarize news for")) -> List[Dict]:
    # For MVP, ignore topic and return dummy articles with dummy summaries
    results = []
    for article in DUMMY_ARTICLES:
        summary = dummy_summarize(article["content"])
        results.append({
            "title": article["title"],
            "summary": summary,
            "link": article["link"]
        })
    return results
