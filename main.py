from repositories.student_repository import StudentRepository, Student
from repositories.staff_repository import StaffRepository, Staff
from repositories.group_repository import GroupRepository, Group
from repositories.cabinet_repository import CabinetRepository, Cabinet
from repositories.event_repository import EventRepository, Event
from repositories.class_repository import ClassRepository, Class
from unit_of_work import UnitOfWork
import mysql.connector

def main():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )
    try:
        # Очистимо тестові дані перед початком
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Студент WHERE Паспорт = %s", ("TST123",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("TST123",))
            cursor.execute("DELETE FROM Член_персоналу WHERE Паспорт = %s", ("TST456",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("TST456",))
            conn.commit()

        # --- Тест UnitOfWork ---
        with UnitOfWork(conn, current_user="test_user") as uow:
            # 1. Додавання студента
            student = Student(
                passport="TST123",
                pib="Тест Студент",
                course=2,
                form="денна",
                group_number=101,
                university_id=1,
                university_name="Київський національний університет"
            )
            uow.students.add_student(student)
            fetched_student = uow.students.get_student_by_passport("TST123")
            assert fetched_student is not None
            print("✅ Додавання студента пройшло успішно")

            # 2. Додавання члена персоналу
            staff_member = Staff(
                passport="TST456",
                pib="Тест Персонал",
                salary=15000,
                cabinet=101,
                university_id=1,
                university_name="Київський національний університет"
            )
            uow.staff.add_staff(staff_member)
            fetched_staff = uow.staff.get_staff_by_passport("TST456")
            assert fetched_staff is not None
            print("✅ Додавання члена персоналу пройшло успішно")

            # 3. Оновлення студента
            student.course = 3
            uow.students.update_student(student)
            updated_student = uow.students.get_student_by_passport("TST123")
            assert updated_student.course == 3
            print("✅ Оновлення студента пройшло успішно")

            # 4. Оновлення персоналу
            staff_member.salary = 16000
            uow.staff.update_staff(staff_member)
            updated_staff = uow.staff.get_staff_by_passport("TST456")
            assert updated_staff.salary == 16000
            print("✅ Оновлення члена персоналу пройшло успішно")

            # 5. Видалення студента
            uow.students.delete_student("TST123")
            deleted_student = uow.students.get_student_by_passport("TST123")
            assert deleted_student is None
            print("✅ Видалення студента пройшло успішно")

            # 6. Видалення персоналу
            uow.staff.delete_staff("TST456")
            deleted_staff = uow.staff.get_staff_by_passport("TST456")
            assert deleted_staff is None
            print("✅ Видалення члена персоналу пройшло успішно")

            # 7. Відновлення студента
            uow.students.restore_student("TST123")
            restored_student = uow.students.get_student_by_passport("TST123")
            assert restored_student is not None
            print("✅ Відновлення студента пройшло успішно")

            # 8. Відновлення персоналу
            uow.staff.restore_staff("TST456")
            restored_staff = uow.staff.get_staff_by_passport("TST456")
            assert restored_staff is not None
            print("✅ Відновлення члена персоналу пройшло успішно")

            # --- Закомітимо всі зміни ---
            uow.commit()
            print("✅ UnitOfWork коміт успішний")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
