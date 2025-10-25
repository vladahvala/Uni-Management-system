from repositories.student_repository import Student
from repositories.staff_repository import Staff
from repositories.group_repository import Group
from repositories.cabinet_repository import Cabinet
from repositories.event_repository import Event
from repositories.class_repository import Class
from unit_of_work import UnitOfWork
import mysql.connector

def demo_unit_of_work():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

     # --- Видалення через прямі SQL-запити ---
    with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Студент WHERE Паспорт = %s", ("DEMO123",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("DEMO123",))
            cursor.execute("DELETE FROM Член_персоналу WHERE Паспорт = %s", ("DEMO456",))
            cursor.execute("DELETE FROM Людина WHERE Паспорт = %s", ("DEMO456",))
            cursor.execute("DELETE FROM Група WHERE Номер = %s", (888,))
            cursor.execute("DELETE FROM Кабінет WHERE Номер = %s", (888,))
            cursor.execute("""
                DELETE FROM Захід
                WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
            """, ("2025-10-26", "09:00", 101))
            cursor.execute("""
                DELETE FROM Пара
                WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
            """, ("2025-10-26", "11:00", 101))
            conn.commit()
            print("Усі додані записи видалені успішно")

    try:
        with UnitOfWork(conn, current_user="demo_user") as uow:
            # --- Додавання об'єктів ---
            student = Student("DEMO123", "Демо Студент", 1, "денна", 101, 1, "иївський національний університет")
            uow.students.add_student(student)

            staff_member = Staff("DEMO456", "Демо Персонал", 12000, 101, 1, "Київський національний університет")
            uow.staff.add_staff(staff_member)

            group = Group(888, 20, "Демо Група", 1, "Київський національний університет")
            uow.groups.add_group(group)

            cabinet = Cabinet(888, 1, 40, "Лекції", 1)
            uow.cabinets.add_cabinet(cabinet)

            event = Event("2025-10-26", "09:00", 101, "Засідання", 60)
            uow.events.add_event(event)

            class_ = Class("2025-10-26", "11:00", 101, "Демо Заняття", 90)
            uow.classes.add_class(class_)

            # --- Commit змін ---
            uow.commit()
            print("Усі зміни закомічені успішно")

    finally:
        conn.close()


if __name__ == "__main__":
    demo_unit_of_work()
