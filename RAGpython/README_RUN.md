# Hotel RAG Project - Запуск локально

Файлы в этом каталоге: /mnt/data/hotel_rag_project

## 1) Установите зависимости
Создайте виртуальное окружение и установите зависимости:
```
python -m venv .venv
source .venv/bin/activate   # или .\.venv\Scripts\activate в Windows
pip install -r requirements.txt
```

## 2) Запустите Weaviate (docker)
```
docker-compose up -d
```
Weaviate будет слушать на http://localhost:8080

## 3) Установите переменные окружения
```
export OPENAI_API_KEY=your_key_here
export WEAVIATE_URL=http://localhost:8080
```

## 4) Загрузите данные в Weaviate
```
python ingest_weaviate.py
```

## 5) Запустите Streamlit UI
```
streamlit run app_streamlit.py
```

## Примечания
- Скрипты используют OpenAI API (ключ обязателен). Можно адаптировать для других эмбедингов/LLM.
- Если вы не хотите запускать Weaviate, вы можете заменить поиск на локальный поиск с помощью FAISS и сохранить эмбединги в файл.
