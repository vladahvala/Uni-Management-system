# tests/test_unit_of_work_full.py

from repositories.student_repository import Student
from repositories.staff_repository import Staff
from repositories.group_repository import Group
from repositories.cabinet_repository import Cabinet
from repositories.event_repository import Event
from repositories.class_repository import Class
from unit_of_work import UnitOfWork
import mysql.connector

def test_unit_of_work_full():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

    try:
        # Очистка тестових даних
        with conn.cursor() as cursor:
            # Студенти
            cursor.execute("DELETE FROM Студент WHERE Паспорт = %s", ("TST123",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("TST123",))
            # Персонал
            cursor.execute("DELETE FROM Член_персоналу WHERE Паспорт = %s", ("TST456",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("TST456",))
            # Групи
            cursor.execute("DELETE FROM Група WHERE Номер = %s", (999,))
            # Кабінети
            cursor.execute("DELETE FROM Кабінет WHERE Номер = %s", (999,))
            # Заходи
            cursor.execute("""
                DELETE FROM Захід 
                WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
            """, ("2025-10-25", "10:00", 101))
            # Заняття (Пара)
            cursor.execute("""
                DELETE FROM Пара 
                WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
            """, ("2025-10-25", "12:00", 101))
            conn.commit()

        with UnitOfWork(conn, current_user="test_user") as uow:
            # --- Тест Student ---
            student = Student("TST123", "Тест Студент", 2, "денна", 101, 1, "КНУ")
            uow.students.add_student(student)
            fetched_student = uow.students.get_student_by_passport("TST123")
            assert fetched_student is not None
            print("Студент доданий")

            # --- Тест Staff ---
            staff_member = Staff("TST456", "Тест Персонал", 15000, 101, 1, "КНУ")
            uow.staff.add_staff(staff_member)
            fetched_staff = uow.staff.get_staff_by_passport("TST456")
            assert fetched_staff is not None
            print("Персонал доданий")

            # --- Тест Group ---
            group = Group(999, 10, "Тест", 1, "КНУ")
            uow.groups.add_group(group)
            fetched_group = uow.groups.get_group_by_number(999)
            assert fetched_group is not None
            print("Група додана")
            # --- Тест Cabinet ---
            cabinet = Cabinet(999, 1, 30, "Лекції", 1)
            uow.cabinets.add_cabinet(cabinet)
            fetched_cabinet = uow.cabinets.get_cabinet_by_number(999)
            assert fetched_cabinet is not None
            print("Кабінет доданий")

            # --- Тест Event ---
            event = Event("2025-10-25", "10:00", 101, "Засідання", 1)
            uow.events.add_event(event)
            fetched_event = uow.events.get_event_by_key("2025-10-25", "10:00", 101)
            assert fetched_event is not None
            print("Захід доданий")

            # --- Тест Class (Пара) ---
            class_ = Class("2025-10-25", "12:00", 101, "Тестове заняття", 1)
            uow.classes.add_class(class_)
            fetched_class = uow.classes.get_class_by_key("2025-10-25", "12:00", 101)
            assert fetched_class is not None
            print("Заняття додане")

            # --- Soft delete / restore Student ---
            uow.students.delete_student("TST123")
            deleted_student = uow.students.get_student_by_passport("TST123")
            assert deleted_student is None
            print("Студент видалений (soft delete)")

            uow.students.restore_student("TST123")
            restored_student = uow.students.get_student_by_passport("TST123")
            assert restored_student is not None
            print("Студент відновлений")

            # --- Commit транзакції ---
            uow.commit()
            print("UnitOfWork коміт успішний")

    finally:
        conn.close()


if __name__ == "__main__":
    test_unit_of_work_full()
