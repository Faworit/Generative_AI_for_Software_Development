from openai import OpenAI

client = OpenAI()

MODEL = "text-embedding-3-small"

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Возвращает список векторов для списка текстов
    """
    resp = client.embeddings.create(
        model=MODEL,
        input=texts
    )
    return [item.embedding for item in resp.data]
