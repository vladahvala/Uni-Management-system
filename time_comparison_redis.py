import time
import json
from datetime import datetime, timedelta
import mysql.connector
import redis

# --- Підключення до SQL ---
sql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="14768967H&ab",
    database="university"
)
sql_cursor = sql_conn.cursor(dictionary=True)

# --- Підключення до Redis ---
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# --------------------------- Базові дані ---------------------------
base_pair_data = {
    "Дата": "2025-11-12",
    "Час_початку": "15:00:00",
    "Предмет": "Математика",
    "Тривалість": "01:30:00",
    "Тип": "Лекція",
    "Деталі_типу": {"Розглянутий_матеріал": "Інтеграли"},
    "Викладачі": [{"Паспорт": "A12345", "ПІБ": "Іваненко І.І.", "Предмет": "Математика", "Науковий_ступінь": "к.ф-м.н."}],
    "Групи": [{"Номер": 1, "Кількість_студентів": 20, "Спеціальність": "Фізика"}],
    "Студенти": [{"Паспорт": "S001", "ПІБ": "Петренко П.П.", "Номер_групи": 1, "Курс_навчання": 2, "Форма_навчання": "денна"}]
}

pairs_data = []

base_date = datetime.strptime("2025-11-12 10:00:00", "%Y-%m-%d %H:%M:%S")
pair_duration = timedelta(hours=1, minutes=30)

# --------------------------- ВСТАВКА ---------------------------
start_sql = time.time()
for i in range(10):
    pair_data = base_pair_data.copy()
    start_time = (base_date + i * pair_duration).time()
    pair_data["Час_початку"] = start_time.strftime("%H:%M:%S")
    cabin_number = 401 + i
    pair_data["Номер_кабінету"] = cabin_number
    pairs_data.append(pair_data)

    # Створення кабінету (якщо його ще немає)
    sql_cursor.execute("SELECT * FROM Кабінет WHERE Номер=%s", (cabin_number,))
    if not sql_cursor.fetchone():
        sql_cursor.execute(
            "INSERT INTO Кабінет (Номер, Поверх, Кількість_місць, Тип, ID_університету) VALUES (%s,%s,%s,%s,%s)",
            (cabin_number, 2, 30, "Лекційний", 1)
        )

    # Вставка пари
    sql_cursor.execute(
        "INSERT INTO Пара (Дата, Час_початку, Номер_кабінету, Предмет, Тривалість) VALUES (%s,%s,%s,%s,%s)",
        (pair_data["Дата"], pair_data["Час_початку"], cabin_number, pair_data["Предмет"], 90)
    )

sql_conn.commit()
end_sql = time.time()

# --- Redis вставка ---
start_redis = time.time()
for pair_data in pairs_data:
    key = f"Пара:{pair_data['Дата']}:{pair_data['Час_початку']}:{pair_data['Номер_кабінету']}"
    redis_client.set(key, json.dumps(pair_data))
end_redis = time.time()

print(f"Час SQL ВСТАВКИ 10 пар: {end_sql - start_sql:.6f} сек")
print(f"Час Redis ВСТАВКИ 10 пар: {end_redis - start_redis:.6f} сек")



# --------------------------- ЧИТАННЯ ---------------------------
sql_cursor.execute("SELECT * FROM Пара ORDER BY RAND() LIMIT 1")
row = sql_cursor.fetchone()

start_sql = time.perf_counter()
if row:
    sql_cursor.execute("SELECT * FROM Пара WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s",
                       (row["Дата"], row["Час_початку"], row["Номер_кабінету"]))
    _ = sql_cursor.fetchone()
end_sql = time.perf_counter()

keys = redis_client.keys("Пара:*")
random_key = keys[0] if keys else None

start_redis = time.perf_counter()
if random_key:
    _ = json.loads(redis_client.get(random_key))
end_redis = time.perf_counter()

print(f"\nЧас SQL ЧИТАННЯ 1 пари: {end_sql - start_sql:.6f} сек") 
print(f"Час Redis ЧИТАННЯ 1 пари: {end_redis - start_redis:.6f} сек")



# --------------------------- ОНОВЛЕННЯ ---------------------------
if row:
    start_sql_update = time.perf_counter()
    sql_cursor.execute("UPDATE Пара SET Предмет=%s WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s",
                       ("Оновлено_SQL", row["Дата"], row["Час_початку"], row["Номер_кабінету"]))
    sql_conn.commit()
    end_sql_update = time.perf_counter()

if random_key:
    start_redis_update = time.perf_counter()
    pair_data = json.loads(redis_client.get(random_key))
    pair_data["Предмет"] = "Оновлено_Redis"
    redis_client.set(random_key, json.dumps(pair_data))
    end_redis_update = time.perf_counter()

print(f"\nЧас SQL ОНОВЛЕННЯ 1 пари: {end_sql_update - start_sql_update:.6f} сек")
print(f"Час Redis ОНОВЛЕННЯ 1 пари: {end_redis_update - start_redis_update:.6f} сек")



# --------------------------- ВИДАЛЕННЯ ---------------------------
start_sql_del = time.time()
for pair_data in pairs_data:
    sql_cursor.execute(
        "DELETE FROM Пара WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s",
        (pair_data["Дата"], pair_data["Час_початку"], pair_data["Номер_кабінету"])
    )
sql_conn.commit()
end_sql_del = time.time()

start_redis_del = time.time()
for pair_data in pairs_data:
    key = f"Пара:{pair_data['Дата']}:{pair_data['Час_початку']}:{pair_data['Номер_кабінету']}"
    redis_client.delete(key)
end_redis_del = time.time()

print(f"\nЧас SQL ВИДАЛЕННЯ 10 пар: {end_sql_del - start_sql_del:.6f} сек")
print(f"Час Redis ВИДАЛЕННЯ 10 пар: {end_redis_del - start_redis_del:.6f} сек")



# --- Закриття ---
sql_cursor.close()
sql_conn.close()
redis_client.close()
