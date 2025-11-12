import redis

# --- Підключення до Redis ---
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# --- Отримуємо всі ключі пар ---
pair_keys = r.keys("pair:*")

# Видаляємо всі ключі
deleted_count = 0
if pair_keys:
    deleted_count = r.delete(*pair_keys)

print(f"Видалено {deleted_count} ключів з Redis.")

# --- Закриваємо підключення (не обов'язково для Redis) ---
r.close()
