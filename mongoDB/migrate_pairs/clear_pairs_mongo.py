from pymongo import MongoClient

# Підключення до MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["university_db"]
mongo_pairs = mongo_db["Пари"]

# Очищаємо колекцію "Пари"
deleted_count = mongo_pairs.delete_many({}).deleted_count
print(f"Видалено {deleted_count} документів з колекції 'Пари'.")

# Закриваємо підключення
mongo_client.close()
