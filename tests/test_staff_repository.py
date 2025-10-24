from repositories.staff_repository import StaffRepository, Staff
import mysql.connector

def test_staff_repository(connection):
    repo = StaffRepository(connection, current_user="test_user")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Член_персоналу WHERE Паспорт = %s", ("AA123497",))
        cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("AA123497",))
        connection.commit()

    # --- 1. Додавання нового члена персоналу ---
    staff_member = Staff(
        passport="AA123497",
        pib="Іван Іваненко",
        salary=12000,
        cabinet=101,
        university_id=1,
        university_name='Київський національний університет'
    )
    repo.add_staff(staff_member)
    print("Член персоналу доданий")

    # Перевірка, що член персоналу доданий
    fetched = repo.get_staff_by_passport("AA123497")
    assert fetched is not None
    assert fetched.pib == "Іван Іваненко"
    assert fetched.salary == 12000
    assert fetched.cabinet == 101
    assert fetched.university_id == 1
    assert fetched.university_name == "Київський національний університет"
    print("Перевірка доданого члена персоналу пройдена")

    # --- 2. Оновлення даних ---
    staff_member.salary = 13000
    staff_member.cabinet = 102
    repo.update_staff(staff_member)
    updated = repo.get_staff_by_passport("AA123497")
    assert updated.salary == 13000
    assert updated.cabinet == 102
    print("Оновлення даних пройшло успішно")

    # --- 3. Отримання всіх активних ---
    active_staff = repo.get_active_staff()
    assert any(s.passport == "AA123497" for s in active_staff)
    print("Отримання всіх активних членів персоналу пройшло успішно")

    # --- 4. Видалення (soft delete) ---
    repo.delete_staff("AA123497")
    deleted = repo.get_staff_by_passport("AA123497")
    assert deleted is None
    print("Soft delete члена персоналу пройшов успішно")

    # --- 5. Відновлення ---
    repo.restore_staff("AA123497")
    restored = repo.get_staff_by_passport("AA123497")
    assert restored is not None
    assert restored.pib == "Іван Іваненко"
    print("Відновлення члена персоналу пройшло успішно")

    print("Всі тести StaffRepository пройшли успішно!")


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )
    test_staff_repository(conn)
    conn.close()
    