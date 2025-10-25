from repositories.student_repository import StudentRepository, Student
import mysql.connector

def test_student_repository(connection):
    repo = StudentRepository(connection, current_user="test_user")

    # --- Очистка перед тестом ---
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Студент WHERE Паспорт = %s", ("AA123498",))
        cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("AA123498",))
        connection.commit()

    # --- 1. Додавання нового студента ---
    student = Student(
        passport="AA123498",
        pib="Марія Петрова",
        course=2,
        form="денна",
        group_number=104,       
        university_id=3,       
        university_name="Харківський національний університет"
    )
    repo.add_student(student)


    fetched = repo.get_student_by_passport("AA123498")
    assert fetched is not None
    assert fetched.pib == "Марія Петрова"
    assert fetched.course == 2
    assert fetched.form == "денна"
    assert fetched.group_number == 104
    assert fetched.university_id == 3
    assert fetched.university_name == "Харківський національний університет"
    print("Тест додавання студента пройшов успішно")

    # --- 2. Оновлення даних ---
    student.course = 3
    student.form = "заочна"
    student.group_number = 102
    repo.update_student(student)

    updated = repo.get_student_by_passport("AA123498")
    assert updated.course == 3
    assert updated.form == "заочна"
    assert updated.group_number == 102
    print("Тест оновлення студента пройшов успішно")

    # --- 3. Отримання всіх активних студентів ---
    active_students = repo.get_active_students()
    assert any(s.passport == "AA123498" for s in active_students)
    print("Тест отримання активних студентів пройшов успішно")

    # --- 4. Видалення (soft delete) ---
    repo.delete_student("AA123498")
    deleted = repo.get_student_by_passport("AA123498")
    assert deleted is None
    print("Тест видалення студента пройшов успішно")

    # --- 5. Відновлення студента ---
    repo.restore_student("AA123498")
    restored = repo.get_student_by_passport("AA123498")
    assert restored is not None
    assert restored.pib == "Марія Петрова"
    print("Тест відновлення студента пройшов успішно")

    # --- 6. Очистка після тесту ---
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Студент WHERE Паспорт = %s", ("AA123498",))
        cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("AA123498",))
        connection.commit()
    print("Очистка після тесту пройшла успішно")


if __name__ == "__main__":
    # Підключення до MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )
    test_student_repository(conn)
    conn.close()
