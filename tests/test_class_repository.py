import mysql.connector
from datetime import datetime, time
from repositories.class_repository import Class, ClassRepository

def test_class_repository(connection):
    repo = ClassRepository(connection, current_user="test_user")

    # === Дані для тесту ===
    test_date = datetime(2025, 10, 25).date()
    test_time = time(10, 0)
    cabinet_number = 301
    subject = "Тестова пара"
    duration = 90

    # === Попереднє очищення конкретного запису ===
    print("\n=== Очищення таблиці Пара від запису з номером 301 ===")
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM Пара
            WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
        """, (test_date, test_time, cabinet_number))
        connection.commit()
    print("Старий запис (якщо був) видалено")

    # === Тест 1: Додавання нової пари ===
    print("\n=== Тест 1: Додавання нової пари ===")
    cls = Class(test_date, test_time, cabinet_number, subject, duration)
    repo.add_class(cls)
    fetched = repo.get_class_by_key(test_date, test_time, cabinet_number)

    assert fetched is not None, "Пару не додано"
    assert fetched.subject == subject
    assert fetched.duration == duration
    assert fetched.cabinet_number == cabinet_number
    print("Пару успішно додано")

    # === Тест 2: Отримання всіх активних пар ===
    print("\n=== Тест 2: Отримання всіх активних пар ===")
    all_classes = repo.get_all_classes()
    assert any(c.subject == subject and c.cabinet_number == cabinet_number for c in all_classes), \
        "Додана пара не знайдена серед активних"
    print(f"Отримано {len(all_classes)} активних пар")

    # === Тест 3: Перевірка end_time ===
    print("\n=== Тест 3: Перевірка end_time ===")
    end_time = fetched.end_time
    assert end_time is not None, "end_time не обчислено"
    print(f"Час завершення обчислено: {end_time}")

    # === Тест 4: Логічне видалення ===
    print("\n=== Тест 4: Логічне видалення пари ===")
    repo.delete_class(test_date, test_time, cabinet_number)
    deleted = repo.get_class_by_key(test_date, test_time, cabinet_number)
    assert deleted is None, "Пару не позначено як видалену"
    print("Пару логічно видалено")

    # === Тест 5: Відновлення ===
    print("\n=== Тест 5: Відновлення пари ===")
    repo.restore_class(test_date, test_time, cabinet_number)
    restored = repo.get_class_by_key(test_date, test_time, cabinet_number)
    assert restored is not None, "Пару не відновлено"
    print("Пару успішно відновлено")

    print("\n=== Усі тести ClassRepository пройшли успішно ===")


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

    try:
        test_class_repository(conn)
    finally:
        conn.close()