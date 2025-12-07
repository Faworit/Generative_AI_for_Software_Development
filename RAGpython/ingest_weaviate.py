import json
import os
from dotenv import load_dotenv
import weaviate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY:", OPENAI_API_KEY)


WEAVIATE_URL = "http://localhost:8080"
DATASET_FILE = "data_dataset_hotels.json"

# Создаём клиент
client = weaviate.Client(WEAVIATE_URL)

if not client.is_ready():
    raise RuntimeError("Weaviate недоступен")

print("Weaviate подключён ✅")

# Создание класса (схемы)
hotel_class = {
    "class": "Hotel",
    "description": "Отель для туристов",
    "properties": [
        {"name": "name", "dataType": ["string"]},
        {"name": "city", "dataType": ["string"]},
        {"name": "country", "dataType": ["string"]},
        {"name": "stars", "dataType": ["int"]},
        {"name": "price_per_night_eur", "dataType": ["number"]},
        {"name": "amenities", "dataType": ["string[]"]},
        {"name": "description", "dataType": ["text"]},
        {"name": "url", "dataType": ["string"]},
        {"name": "latitude", "dataType": ["number"]},
        {"name": "longitude", "dataType": ["number"]}
    ]
}

# Удаляем старый класс (если есть)
try:
    client.schema.delete_class("Hotel")
except:
    pass

client.schema.create_class(hotel_class)
print("Схема Hotel создана ✅")

# Загружаем данные из JSON
with open(DATASET_FILE, "r", encoding="utf-8") as f:
    hotels = json.load(f)

for hotel in hotels:
    client.data_object.create(data_object=hotel, class_name="Hotel")

print(f"Загружено {len(hotels)} записей ✅")
