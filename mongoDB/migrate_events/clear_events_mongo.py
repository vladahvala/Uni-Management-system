import mysql.connector

# --- Підключення до SQL ---
sql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="14768967H&ab",
    database="university"
)
sql_cursor = sql_conn.cursor()

# --- Видалення всіх заходів ---
sql_cursor.execute("DELETE FROM Захід")

sql_conn.commit()
print(f"Видалено {sql_cursor.rowcount} записів із таблиці Захід.")

sql_cursor.close()
sql_conn.close()
