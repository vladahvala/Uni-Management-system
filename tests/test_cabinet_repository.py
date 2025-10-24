import mysql.connector
from repositories.cabinet_repository import Cabinet, CabinetRepository  # імпортуємо твій репо

def test_cabinet_repository(connection):
    repo = CabinetRepository(connection, current_user="test_user")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Кабінет WHERE Номер IN (404)")
        connection.commit()

    print("=== Тест: Додавання кабінету ===")
    cab1 = Cabinet(number=404, floor=2, capacity=30, type="Лекції", university_id=1)
    repo.add_cabinet(cab1)
    
    fetched = repo.get_cabinet_by_number(404)
    assert fetched is not None, "Кабінет не доданий"
    assert fetched.number == 404
    assert fetched.floor == 2
    assert fetched.capacity == 30
    assert fetched.type == "Лекції"
    print("Додавання пройшло успішно")

    print("\n=== Тест: Оновлення кабінету ===")
    cab1.floor = 3
    cab1.capacity = 35
    cab1.type = "Семінари"
    repo.update_cabinet(cab1)

    updated = repo.get_cabinet_by_number(404)
    assert updated.floor == 3
    assert updated.capacity == 35
    assert updated.type == "Семінари"
    print("Оновлення пройшло успішно")

    print("\n=== Тест: Отримання всіх кабінетів ===")
    all_cabs = repo.get_all_cabinets()
    assert any(c.number == 404 for c in all_cabs)
    print(f"Всього кабінетів: {len(all_cabs)}")

    print("\n=== Тест: Soft delete та restore ===")
    repo.delete_cabinet(404)
    deleted = repo.get_cabinet_by_number(404)
    assert deleted is None, "Кабінет не видалено"
    print("Soft delete пройшло успішно")

    repo.restore_cabinet(404)
    restored = repo.get_cabinet_by_number(404)
    assert restored is not None, "Кабінет не відновлено"
    print("Restore пройшло успішно")

    print("\n=== Тест: Отримання активних кабінетів через view ===")
    active_cabs = repo.get_active_cabinets()
    assert any(c.number == 404 for c in active_cabs)
    print(f"Активних кабінетів: {len(active_cabs)}")

    print("\n=== Тест: Деталі кабінету через view ===")
    details = repo.get_cabinet_details(404)
    assert details is not None
    assert details.number == 404
    assert details.university_id == 1
    print("Деталі кабінету отримано успішно")

    print("\n=== Всі тести пройшли! ===")



if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

    try:
        test_cabinet_repository(conn)
    finally:
        conn.close()