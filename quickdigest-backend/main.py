from fastapi import FastAPI, Query
from typing import List, Dict
import os
import httpx
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import asyncio

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
    # For now, just return first 25 chars + '...'
    return text[:25] + "..."

async def summarize(text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes news articles into 10 clear, non-opinionated bullet points. Do not include reasoning, internal thoughts, or tags."},
        {"role": "user", "content": f"Summarize this article in bullet points: {text}"}
    ]

    def stream_response():
        stream = client.chat.completions.create(
            messages=messages,
            model="llama3.1-8b",
            stream=True,
            max_completion_tokens=400,
            temperature=0.7,
            top_p=0.8
        )
        result_text = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            result_text += content
        return result_text

    summary = await asyncio.get_event_loop().run_in_executor(None, stream_response)
    return summary

async def fetch_articles(topic: str):
    params = {
        "apiKey": NEWSAPI_KEY,
        "category": topic,
        "language": "en",
        "pageSize": 5
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(NEWSAPI_URL, params=params)

        data = response.json()
        articles = data.get("articles", [])
        simplified = []
        for a in articles:
            # Simplify article content: if no content, fallback to description or title
            content = a.get("content") or a.get("description") or a.get("title")
            simplified.append({
                "title": a.get("title"),
                "content": content,
                "link": a.get("url")
            })
        return simplified

@app.get("/api/summaries")
async def get_summaries(topic: str = Query(...)):
    articles = await fetch_articles(topic)
    results = []
    for article in articles:
        summary = await summarize(article["content"])
        results.append({
            "title": article["title"],
            "summary": summary,
            "link": article["link"]
        })
    return results
