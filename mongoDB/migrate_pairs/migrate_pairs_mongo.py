# migrate_pairs.py
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
mongo_pairs = mongo_db["Пари"]

def format_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"

# --- Отримуємо всі пари ---
sql_cursor.execute("SELECT * FROM Пара")
pairs = sql_cursor.fetchall()

for pair in pairs:
    pair_doc = {
        "Дата": pair["Дата"].isoformat(),
        "Час_початку": format_time(pair["Час_початку"]),
        "Номер_кабінету": pair["Номер_кабінету"],
        "Предмет": pair["Предмет"],
        "Тривалість": pair["Тривалість"],
        "Тип": None,
        "Деталі_типу": {},
        "Кабінет": None,
        "Викладачі": [],
        "Групи": [],
    }

    # --- Визначаємо тип пари та додаємо специфічні поля ---
    type_found = False

    # Лекція
    sql_cursor.execute("""
        SELECT Розглянутий_матеріал
        FROM Лекція
        WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
    """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
    lecture = sql_cursor.fetchone()
    if lecture:
        pair_doc["Тип"] = "Лекція"
        pair_doc["Деталі_типу"] = {"Розглянутий_матеріал": lecture["Розглянутий_матеріал"]}
        type_found = True

    # Практика
    if not type_found:
        sql_cursor.execute("""
            SELECT Кількість_учасників
            FROM Практика
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
        practice = sql_cursor.fetchone()
        if practice:
            pair_doc["Тип"] = "Практика"
            pair_doc["Деталі_типу"] = {"Кількість_учасників": practice["Кількість_учасників"]}
            type_found = True

    # Екзамен
    if not type_found:
        sql_cursor.execute("""
            SELECT Кількість_перевіряючих
            FROM Екзамен
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
        exam = sql_cursor.fetchone()
        if exam:
            pair_doc["Тип"] = "Екзамен"
            pair_doc["Деталі_типу"] = {"Кількість_перевіряючих": exam["Кількість_перевіряючих"]}
            type_found = True

    # Консультація
    if not type_found:
        sql_cursor.execute("""
            SELECT Питання
            FROM Консультація
            WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
        """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
        consultation = sql_cursor.fetchone()
        if consultation:
            pair_doc["Тип"] = "Консультація"
            pair_doc["Деталі_типу"] = {"Питання": consultation["Питання"]}
            type_found = True

    if not type_found:
        pair_doc["Тип"] = "Невідомий"

    # --- Кабінет ---
    sql_cursor.execute("SELECT * FROM Кабінет WHERE Номер = %s", (pair["Номер_кабінету"],))
    cabinet = sql_cursor.fetchone()
    if cabinet:
        pair_doc["Кабінет"] = {
            "Номер": cabinet["Номер"],
            "Поверх": cabinet["Поверх"],
            "Кількість_місць": cabinet["Кількість_місць"],
            "Тип": cabinet["Тип"],
            "ID_університету": cabinet["ID_університету"]
        }

    # --- Викладачі ---
    sql_cursor.execute("""
        SELECT Паспорт_викладача
        FROM Проведення_пар
        WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
    """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
    teachers = sql_cursor.fetchall()
    for t in teachers:
        sql_cursor.execute("""
            SELECT ПІБ, Предмет, Науковий_ступінь
            FROM Викладач
            JOIN Член_персоналу USING (Паспорт)
            JOIN Людина USING (Паспорт)
            WHERE Паспорт=%s
        """, (t["Паспорт_викладача"],))
        teacher_info = sql_cursor.fetchone()
        if teacher_info:
            pair_doc["Викладачі"].append(teacher_info)

    # --- Групи ---
    sql_cursor.execute("""
        SELECT Номер_групи
        FROM Група_Пара
        WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
    """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))
    groups = sql_cursor.fetchall()
    for g in groups:
        sql_cursor.execute("SELECT Номер, Кількість_студентів, Спеціальність FROM Група WHERE Номер=%s", (g["Номер_групи"],))
        group_info = sql_cursor.fetchone()
        if group_info:
            pair_doc["Групи"].append(group_info)

    # --- Студенти ---
    pair_doc["Студенти"] = []

    sql_cursor.execute("""
        SELECT Відвідування.Паспорт, Студент.Номер_групи, Студент.Курс_навчання, Студент.Форма_навчання, Людина.ПІБ
        FROM Відвідування
        JOIN Студент USING (Паспорт)
        JOIN Людина USING (Паспорт)
        WHERE Відвідування.Дата=%s AND Відвідування.Час_початку=%s AND Відвідування.Номер_кабінету=%s
    """, (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))

    students = sql_cursor.fetchall()
    for s in students:
        pair_doc["Студенти"].append({
            "Паспорт": s["Паспорт"],
            "ПІБ": s["ПІБ"],
            "Номер_групи": s["Номер_групи"],
            "Курс_навчання": s["Курс_навчання"],
            "Форма_навчання": s["Форма_навчання"]
        })


    # --- Вставка в MongoDB ---
    mongo_pairs.insert_one(pair_doc)

print("Міграція сутності 'Пара' завершена!")

sql_cursor.close()
sql_conn.close()
mongo_client.close()
