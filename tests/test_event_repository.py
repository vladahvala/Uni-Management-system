import mysql.connector
from datetime import datetime, time, timedelta
from repositories.event_repository import EventRepository, Event


def test_event_repository(connection):
    repo = EventRepository(connection, current_user="test_user")

    # === Попереднє очищення тестового запису (щоб не дублювався) ===
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM Захід
            WHERE Дата = '2025-10-25' AND Час_початку = '10:00:00' AND Номер_кабінету = 301
        """)
        connection.commit()

    print("=== Тест 1: Додавання заходу ===")
    test_date = datetime(2025, 10, 25).date()
    test_time = time(10, 0)
    test_event = Event(
        date=test_date,
        start_time=test_time,
        cabinet_number=301,
        event_type="Засідання",
        duration=90
    )

    repo.add_event(test_event)
    fetched = repo.get_event_details(test_date, test_time, 301)
    assert fetched is not None, "Помилка: захід не додано"
    assert fetched.date == test_date

    db_time = fetched.start_time
    if isinstance(db_time, datetime):
        db_time = db_time.time()
    elif isinstance(db_time, str):
        db_time = time.fromisoformat(db_time)
    elif isinstance(db_time, timedelta):
        total_seconds = int(db_time.total_seconds())
        db_time = time(total_seconds // 3600, (total_seconds % 3600) // 60)

    assert db_time == test_time, f"Очікувалось {test_time}, отримано {db_time}"

    assert fetched.cabinet_number == 301
    assert fetched.event_type == "Засідання"
    assert fetched.duration == 90
    print("Додавання успішне")

    print("=== Тест 2: Оновлення заходу ===")
    test_event.event_type = "Семінар"
    test_event.duration = 120
    repo.update_event(test_event)
    updated = repo.get_event_details(test_date, test_time, 301)
    assert updated.event_type == "Семінар"
    assert updated.duration == 120
    print("Оновлення успішне")

    print("=== Тест 3: Отримання всіх активних заходів ===")
    active = repo.get_active_events()
    assert any(a["Номер_кабінету"] == 301 for a in active), "Захід не знайдено серед активних"
    print("Активні заходи отримано")

    print("=== Тест 4: Логічне видалення заходу ===")
    repo.delete_event(test_date, test_time, 301)
    deleted = repo.get_event_details(test_date, test_time, 301)
    assert deleted is None, "Захід не видалено логічно"
    print("Видалення успішне")

    print("=== Тест 5: Відновлення заходу ===")
    repo.restore_event(test_date, test_time, 301)
    restored = repo.get_event_details(test_date, test_time, 301)
    assert restored is not None, "Захід не відновлено"
    print("Відновлення успішне")

    print("=== Тест 6: Перевірка GetAllEvents ===")
    events = repo.get_all_events()
    assert any(e.cabinet_number == 301 for e in events), "Захід не знайдено серед усіх"
    print("GetAllEvents працює")

    print("=== Тест 7: Кінець заходу ===")
    end_time = test_event.end_time
    assert end_time is not None, "end_time не обчислено"
    print(f"Кінець заходу: {end_time}")

    print("\nУсі тести для EventRepository пройшли успішно!\n")


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

    try:
        test_event_repository(conn)
    finally:
        conn.close()