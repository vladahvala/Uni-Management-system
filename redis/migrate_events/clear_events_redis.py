import redis

# --- Підключення до Redis ---
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# --- Отримуємо всі ключі для заходів ---
keys = r.keys("event:*")

# --- Видалення ключів ---
if keys:
    deleted_count = r.delete(*keys)
    print(f"Видалено {deleted_count} записів з Redis.")
else:
    print("Записів для видалення не знайдено.")

r.close()
