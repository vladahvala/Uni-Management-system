# migrate_events_redis_fixed.py
import mysql.connector
import redis
import json
from datetime import datetime

# --- Підключення до SQL ---
sql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="14768967H&ab",
    database="university"
)
sql_cursor = sql_conn.cursor(dictionary=True)

# --- Підключення до Redis ---
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# --- Функція для форматування часу ---
def format_time(td):
    if hasattr(td, "strftime"):  # datetime.time або datetime
        return td.strftime("%H:%M:%S")
    return str(td)

# --- Отримуємо всі заходи ---
sql_cursor.execute("SELECT * FROM Захід")
events = sql_cursor.fetchall()

for event in events:
    # Формуємо структуру даних
    event_data = {
        "Дата": event["Дата"].isoformat(),
        "Час_початку": format_time(event["Час_початку"]),
        "Номер_кабінету": event["Номер_кабінету"],
        "Тип": event["Тип"].strip() if event["Тип"] else "Невідомий",
        "Тривалість": event["Тривалість"],
        "Деталі_типу": {},
        "Кабінет": None,
        "Учасники_персонал": []
    }

    # --- Деталі типу ---
    if event_data["Тип"] == "Засідання":
        sql_cursor.execute("""
            SELECT Кількість_учасників
            FROM Засідання
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (event["Дата"], event["Час_початку"], event["Номер_кабінету"]))
        meeting = sql_cursor.fetchone()
        if meeting:
            event_data["Деталі_типу"] = {"Кількість_учасників": meeting["Кількість_учасників"]}

    elif event_data["Тип"] == "Культурна_подія":
        sql_cursor.execute("""
            SELECT Тематика, Програма
            FROM Культурна_подія
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (event["Дата"], event["Час_початку"], event["Номер_кабінету"]))
        cultural = sql_cursor.fetchone()
        if cultural:
            event_data["Деталі_типу"] = {
                "Тематика": cultural["Тематика"],
                "Програма": cultural["Програма"]
            }

    # --- Кабінет ---
    sql_cursor.execute("SELECT * FROM Кабінет WHERE Номер=%s", (event["Номер_кабінету"],))
    cabinet = sql_cursor.fetchone()
    if cabinet:
        event_data["Кабінет"] = {
            "Номер": cabinet["Номер"],
            "Поверх": cabinet["Поверх"],
            "Кількість_місць": cabinet["Кількість_місць"],
            "Тип": cabinet["Тип"],
            "ID_університету": cabinet["ID_університету"]
        }

    # --- Учасники персонал ---
    sql_cursor.execute("""
        SELECT Член_персоналу.Паспорт, Людина.ПІБ
        FROM Відвідування_заходів
        JOIN Член_персоналу USING (Паспорт)
        JOIN Людина USING (Паспорт)
        WHERE Відвідування_заходів.Дата=%s AND Відвідування_заходів.Час_початку=%s AND Відвідування_заходів.Номер_кабінету=%s
    """, (event["Дата"], event["Час_початку"], event["Номер_кабінету"]))
    staff = sql_cursor.fetchall()
    for p in staff:
        event_data["Учасники_персонал"].append({
            "Паспорт": p["Паспорт"],
            "ПІБ": p["ПІБ"],
        })

    # --- Створюємо ключ для Redis ---
    key = f"event:{event_data['Дата']}:{event_data['Час_початку']}:{event_data['Номер_кабінету']}"
    
    # --- Вивід для перевірки ---
    print(f"Формується ключ: {key}")

    # --- Зберігаємо у Redis ---
    r.set(key, json.dumps(event_data, ensure_ascii=False))
    print(f"Ключ збережено: {key}, існує в Redis? {r.exists(key)}")

print("Міграція сутності 'Захід' в Redis завершена!")

sql_cursor.close()
sql_conn.close()
r.close()
