import time
import mysql.connector
from datetime import datetime, timedelta

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


#--------------------------------ЧИТАННЯ-------------------------
# --- SQL: 1 випадкова пара ---
sql_cursor.execute("SELECT * FROM Пара ORDER BY RAND() LIMIT 1")
pair = sql_cursor.fetchone()

# --- Замір часу SQL ---
start_sql = time.perf_counter()

sql_cursor.execute("""
    SELECT p.*, c.Поверх AS Кабінет_поверх, c.Кількість_місць,
           GROUP_CONCAT(DISTINCT l.ПІБ) AS Викладачі,
           GROUP_CONCAT(DISTINCT g.Номер) AS Групи,
           GROUP_CONCAT(DISTINCT s.ПІБ) AS Студенти
    FROM Пара p
    LEFT JOIN Кабінет c ON p.Номер_кабінету = c.Номер
    LEFT JOIN Проведення_пар pp ON p.Дата = pp.Дата AND p.Час_початку = pp.Час_початку AND p.Номер_кабінету = pp.Номер_кабінету
    LEFT JOIN Людина l ON pp.Паспорт_викладача = l.Паспорт
    LEFT JOIN Група_Пара gp ON p.Дата = gp.Дата AND p.Час_початку = gp.Час_початку AND p.Номер_кабінету = gp.Номер_кабінету
    LEFT JOIN Група g ON gp.Номер_групи = g.Номер
    LEFT JOIN Відвідування v ON p.Дата = v.Дата AND p.Час_початку = v.Час_початку AND p.Номер_кабінету = v.Номер_кабінету
    LEFT JOIN Студент st ON v.Паспорт = st.Паспорт
    LEFT JOIN Людина s ON st.Паспорт = s.Паспорт
    WHERE p.Дата=%s AND p.Час_початку=%s AND p.Номер_кабінету=%s
    GROUP BY p.Дата, p.Час_початку, p.Номер_кабінету
""", (pair["Дата"], pair["Час_початку"], pair["Номер_кабінету"]))

_ = sql_cursor.fetchone()

end_sql = time.perf_counter()
total_sql_time = end_sql - start_sql

# --- MongoDB: 1 випадковий документ ---
mongo_doc = mongo_pairs.aggregate([{"$sample": {"size": 1}}])
doc = next(mongo_doc)  # беремо перший документ

# --- Замір часу Mongo ---
start_mongo = time.perf_counter()

_ = mongo_pairs.find_one({
    "Дата": doc["Дата"],
    "Час_початку": doc["Час_початку"],
    "Номер_кабінету": doc["Номер_кабінету"]
})

end_mongo = time.perf_counter()
total_mongo_time = end_mongo - start_mongo

# --- Вивід результатів ---
print(f"\nЧас для SQL ЧИТАННЯ повної інформації про 1 пару: {total_sql_time:.6f} сек.")
print(f"Час для MongoDB ЧИТАННЯ повної інформації про 1 пару: {total_mongo_time:.6f} сек.")



#--------------------------------ВСТАВКА-------------------------
# ------------------ Базові дані для пари ------------------
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
pair_duration = timedelta(hours=1, minutes=30)  # тривалість пари

start_sql = time.time()

for i in range(10):
    pair_data = base_pair_data.copy()

    # Генеруємо унікальний час початку
    start_time = (base_date + i * pair_duration).time()
    pair_data["Час_початку"] = start_time.strftime("%H:%M:%S")

    # Кабінет
    cabin_number = 401 + i
    pair_data["Кабінет"] = {
        "Номер": cabin_number,
        "Поверх": 2,
        "Кількість_місць": 30,
        "ID_університету": 1,
        "Тип": "Лекційний"
    }
    pair_data["Номер_кабінету"] = cabin_number
    pairs_data.append(pair_data)

    # --- SQL вставка кабінету ---
    sql_cursor.execute("SELECT Номер FROM Кабінет WHERE Номер=%s", (cabin_number,))
    if not sql_cursor.fetchone():
        sql_cursor.execute(
            "INSERT INTO Кабінет (Номер, Поверх, Кількість_місць, Тип, ID_університету) VALUES (%s, %s, %s, %s, %s)",
            (cabin_number, 2, 30, "Лекційний", 1)
        )

    # Тривалість у хвилинах
    h, m, s = map(int, pair_data["Тривалість"].split(":"))
    duration_minutes = h*60 + m

    sql_cursor.execute(
        "INSERT INTO Пара (Дата, Час_початку, Номер_кабінету, Предмет, Тривалість) VALUES (%s, %s, %s, %s, %s)",
        (pair_data["Дата"], pair_data["Час_початку"], cabin_number, pair_data["Предмет"], duration_minutes)
    )

    # --- Викладачі ---
    for teacher in pair_data["Викладачі"]:
        # Людина
        sql_cursor.execute("SELECT Паспорт FROM Людина WHERE Паспорт=%s", (teacher["Паспорт"],))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Людина (Паспорт, ПІБ) VALUES (%s, %s)",
                (teacher["Паспорт"], teacher["ПІБ"])
            )
        # Викладач
        sql_cursor.execute("SELECT Паспорт FROM Викладач WHERE Паспорт=%s", (teacher["Паспорт"],))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Викладач (Паспорт, Предмет, Науковий_ступінь, Стаж_викладання) VALUES (%s, %s, %s, %s)",
                (teacher["Паспорт"], teacher["Предмет"], teacher["Науковий_ступінь"], 0)
            )
        # Проведення пар (перевірка часу)
        sql_cursor.execute("""
            SELECT * FROM Проведення_пар
            WHERE Паспорт_викладача=%s AND Дата=%s AND Час_початку=%s
        """, (teacher["Паспорт"], pair_data["Дата"], pair_data["Час_початку"]))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Проведення_пар (Паспорт_викладача, Дата, Час_початку, Номер_кабінету) VALUES (%s, %s, %s, %s)",
                (teacher["Паспорт"], pair_data["Дата"], pair_data["Час_початку"], cabin_number)
            )

    # --- Групи ---
    for group in pair_data["Групи"]:
        sql_cursor.execute("SELECT Номер FROM Група WHERE Номер=%s", (group["Номер"],))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Група (Номер, Кількість_студентів, Спеціальність, ID_університету) VALUES (%s, %s, %s, %s)",
                (group["Номер"], group["Кількість_студентів"], group["Спеціальність"], 1)
            )
        sql_cursor.execute(
            "INSERT INTO Група_Пара (Номер_групи, Дата, Час_початку, Номер_кабінету) VALUES (%s, %s, %s, %s)",
            (group["Номер"], pair_data["Дата"], pair_data["Час_початку"], cabin_number)
        )

    # --- Студенти ---
    for student in pair_data["Студенти"]:
        sql_cursor.execute("SELECT Паспорт FROM Людина WHERE Паспорт=%s", (student["Паспорт"],))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Людина (Паспорт, ПІБ) VALUES (%s, %s)",
                (student["Паспорт"], student["ПІБ"])
            )
        sql_cursor.execute("SELECT Паспорт FROM Студент WHERE Паспорт=%s", (student["Паспорт"],))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Студент (Паспорт, Курс_навчання, Форма_навчання, Номер_групи, ID_університету) VALUES (%s, %s, %s, %s, %s)",
                (student["Паспорт"], student["Курс_навчання"], student["Форма_навчання"], student["Номер_групи"], 1)
            )
        # Відвідування (перевірка)
        sql_cursor.execute("""
            SELECT * FROM Відвідування
            WHERE Паспорт=%s AND Дата=%s AND Час_початку=%s
        """, (student["Паспорт"], pair_data["Дата"], pair_data["Час_початку"]))
        if not sql_cursor.fetchone():
            sql_cursor.execute(
                "INSERT INTO Відвідування (Паспорт, Дата, Час_початку, Номер_кабінету) VALUES (%s, %s, %s, %s)",
                (student["Паспорт"], pair_data["Дата"], pair_data["Час_початку"], cabin_number)
            )

sql_conn.commit()
end_sql = time.time()


# --- MongoDB вставка ---
# ------------------ Вимір часу MongoDB вставки ------------------
start_mongo = time.time()
mongo_pairs.insert_many(pairs_data)
end_mongo = time.time()

#--------------------------------ВИДАЛЕННЯ-------------------------
cabin_numbers = [401 + i for i in range(10)]

# --- Видалення SQL ---
start_sql_del = time.time()
for cabin_number in cabin_numbers:
    sql_cursor.execute("DELETE FROM Відвідування WHERE Номер_кабінету=%s", (cabin_number,))
    sql_cursor.execute("DELETE FROM Проведення_пар WHERE Номер_кабінету=%s", (cabin_number,))
    sql_cursor.execute("DELETE FROM Група_Пара WHERE Номер_кабінету=%s", (cabin_number,))
    sql_cursor.execute("DELETE FROM Пара WHERE Номер_кабінету=%s", (cabin_number,))
    sql_cursor.execute("DELETE FROM Кабінет WHERE Номер=%s", (cabin_number,))
sql_conn.commit()
end_sql_del = time.time()

# --- Видалення MongoDB ---
start_mongo_del = time.time()
mongo_pairs.delete_many({"Номер_кабінету": {"$in": cabin_numbers}})
end_mongo_del = time.time()

print(f"\nЧас для SQL ВСТАВКИ повної інформації про 10 пар: {end_sql - start_sql:.4f} сек")
print(f"Час для MongoDB ВСТАВКИ повної інформації про 10 пар: {end_mongo - start_mongo:.4f} сек")

# --- Вивід часу виконання ---
print(f"\nЧас для SQL ВИДАЛЕННЯ повної інформації про 10 пар: {end_sql_del - start_sql_del:.4f} сек")
print(f"Час для MongoDB ВИДАЛЕННЯ повної інформації про 10 пар: {end_mongo_del - start_mongo_del:.4f} сек")



#--------------------------------ОНОВЛЕННЯ-------------------------
# Вибираємо випадкову пару
sql_cursor.execute("SELECT * FROM Пара ORDER BY RAND() LIMIT 1")
row = sql_cursor.fetchone()

if row:
    start_sql_update = time.perf_counter()

    sql_cursor.execute("""
        UPDATE Пара
        SET Предмет=%s
        WHERE Дата=%s AND Час_початку=%s AND Номер_кабінету=%s
    """, ("Оновлено_SQL", row["Дата"], row["Час_початку"], row["Номер_кабінету"]))

    sql_conn.commit()
    end_sql_update = time.perf_counter()

    print(f"\nЧас для SQL ОНОВЛЕННЯ повної інформації про 1 пару:   {end_sql_update - start_sql_update:.6f} сек")
else:
    print("Немає записів у таблиці Пара")


# ---------- MONGO UPDATE ----------
# Беремо випадковий документ
sample = mongo_pairs.aggregate([{"$sample": {"size": 1}}])
doc = next(sample, None)

if doc:
    start_mongo_update = time.perf_counter()

    mongo_pairs.update_one(
        {
            "Дата": doc["Дата"],
            "Час_початку": doc["Час_початку"],
            "Номер_кабінету": doc["Номер_кабінету"]
        },
        {"$set": {"Предмет": "Оновлено_Mongo"}}
    )

    end_mongo_update = time.perf_counter()
    print(f"Час для MongoDB ОНОВЛЕННЯ повної інформації про 1 пару:: {end_mongo_update - start_mongo_update:.6f} сек")
else:
    print("Колекція Пуста")




# --- Закриття підключень ---
sql_cursor.close()
sql_conn.close()
mongo_client.close()