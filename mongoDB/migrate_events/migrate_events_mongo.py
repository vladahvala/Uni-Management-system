# migrate_events.py
import mysql.connector
from pymongo import MongoClient

# --- Підключення до SQL ---
sql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="14768967H&ab",
    database="university"
)
sql_cursor = sql_conn.cursor(dictionary=True)

# --- Підключення до MongoDB ---
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["university_db"]
mongo_events = mongo_db["Заходи"]

# --- Отримуємо всі заходи ---
sql_cursor.execute("SELECT * FROM Захід")
events = sql_cursor.fetchall()

for event in events:
    event_doc = {
        "Дата": event["Дата"].isoformat(),
        "Час_початку": str(event["Час_початку"]),
        "Номер_кабінету": event["Номер_кабінету"],
        "Тип": event["Тип"],
        "Тривалість": event["Тривалість"],
        "Деталі_типу": {},
        "Кабінет": None,
        "Учасники_персонал": []
    }

    # --- Деталі типу ---
    if event["Тип"] == "Засідання":
        sql_cursor.execute("""
            SELECT Кількість_учасників
            FROM Засідання
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (event["Дата"], event["Час_початку"], event["Номер_кабінету"]))
        meeting = sql_cursor.fetchone()
        if meeting:
            event_doc["Деталі_типу"] = {"Кількість_учасників": meeting["Кількість_учасників"]}
    elif event["Тип"] == "Культурна_подія":
        sql_cursor.execute("""
            SELECT Тематика, Програма
            FROM Культурна_подія
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (event["Дата"], event["Час_початку"], event["Номер_кабінету"]))
        cultural = sql_cursor.fetchone()
        if cultural:
            event_doc["Деталі_типу"] = {"Тематика": cultural["Тематика"], "Програма": cultural["Програма"]}

    # --- Кабінет ---
    sql_cursor.execute("SELECT * FROM Кабінет WHERE Номер=%s", (event["Номер_кабінету"],))
    cabinet = sql_cursor.fetchone()
    if cabinet:
        event_doc["Кабінет"] = {
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
        event_doc["Учасники_персонал"].append({
            "Паспорт": p["Паспорт"],
            "ПІБ": p["ПІБ"],
        })

    # --- Вставка в MongoDB ---
    mongo_events.insert_one(event_doc)

print("Міграція сутності 'Захід' завершена!")

sql_cursor.close()
sql_conn.close()
mongo_client.close()
