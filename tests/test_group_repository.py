# tests/test_group_repository.py
import mysql.connector
from repositories.group_repository import GroupRepository, Group

def test_group_repository(connection):
    repo = GroupRepository(connection, current_user="test_user")

    test_number = 999
    test_student_count = 25
    test_specialty = "Тестова спеціальність"
    test_university_id = 1
    test_curator_passport = None

    # === Попереднє очищення тестового запису ===
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Група WHERE Номер = %s", (test_number,))
        connection.commit()

    print("=== Тест 1: Додавання групи ===")
    group = Group(
        number=test_number,
        student_count=test_student_count,
        specialty=test_specialty,
        university_id=test_university_id,
        university_name=None,
        curator_passport=test_curator_passport
    )
    repo.add_group(group)

    fetched = repo.get_group_by_number(test_number)
    assert fetched is not None, "Помилка: групу не додано"
    assert fetched.number == test_number
    assert fetched.student_count == test_student_count
    assert fetched.specialty == test_specialty
    assert fetched.university_id == test_university_id
    assert fetched.curator_passport == test_curator_passport
    print("Додавання групи успішне")

    print("=== Тест 2: Оновлення групи ===")
    group.student_count = 30
    group.specialty = "Оновлена спеціальність"
    repo.update_group(group)

    fetched = repo.get_group_by_number(test_number)
    assert fetched.student_count == 30
    assert fetched.specialty == "Оновлена спеціальність"
    print("Оновлення групи успішне")

    print("=== Тест 3: Логічне видалення групи ===")
    repo.delete_group(test_number)
    fetched_active = repo.get_active_groups()
    numbers = [g['Номер'] for g in fetched_active]
    assert test_number not in numbers, "Помилка: група не видалена логічно"
    print("Логічне видалення успішне")

    print("=== Тест 4: Відновлення групи ===")
    repo.restore_group(test_number)
    fetched_active = repo.get_active_groups()
    numbers = [g['Номер'] for g in fetched_active]
    assert test_number in numbers, "Помилка: групу не відновлено"
    print("Відновлення групи успішне")

    print("=== Тест 5: Деталі групи ===")
    details = repo.get_group_details(test_number)
    assert details is not None, "Помилка: деталі групи не отримано"
    assert details['Номер'] == test_number
    print("Отримання деталей групи успішне")

    # === Прибирання після тесту ===
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Група WHERE Номер = %s", (test_number,))
        connection.commit()
    print("Тестовий запис видалено після тестів")


if __name__ == "__main__":
    # Приклад підключення до MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )
    test_group_repository(conn)
    conn.close()
