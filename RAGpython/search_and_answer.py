"""
search_and_answer.py
Пример поиска по Weaviate + отправки контекста в LLM для ответа (RAG).
"""
import os
from embeddings_client import embed_texts
import weaviate
import json
from pathlib import Path

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_FILE = Path(__file__).parent / "data_dataset_hotels.json"

client = weaviate.Client(WEAVIATE_URL)

# Simple function: given query text, return top-k hotel descriptions
def search(query: str, top_k=4):
    q_emb = embed_texts([query])[0]
    res = client.query.get("Hotel", ["name","city","country","stars","price_per_night_eur","description","url"]).with_near_vector({"vector": q_emb, "certainty":0.0}).with_limit(top_k).do()
    # response parsing is client-version dependent
    try:
        hits = res['data']['Get']['Hotel']
        return hits
    except Exception:
        return []

def build_prompt(query: str, docs):
    context = "\n\n".join([f"{d.get('name')} ({d.get('city')}, {d.get('country')}): {d.get('description')}" for d in docs])
    prompt = f"""You are an assistant that helps users pick hotels. Use the context below (hotel descriptions) to answer the user's question.

Context:\n{context}\n\nUser question: {query}\n\nAnswer concisely and mention which hotels from the context you used."""
    return prompt

def call_llm(prompt: str):
    # use OpenAI ChatCompletion if available
    try:
        from openai import OpenAI
        client_openai = OpenAI(api_key=OPENAI_API_KEY)
        resp = client_openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=400)
        return resp.choices[0].message.content
    except Exception as e:
        return f"LLM call failed: {e}"

if __name__ == '__main__':
    q = input("Enter user query: ")
    docs = search(q, top_k=4)
    if not docs:
        print("No relevant docs found.")
    else:
        prompt = build_prompt(q, docs)
        print("--- PROMPT SENT TO LLM ---\n", prompt)
        answer = call_llm(prompt)
        print("\n--- LLM ANSWER ---\n", answer)
