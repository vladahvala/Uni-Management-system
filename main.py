from repositories.student_repository import StudentRepository, Student
from repositories.staff_repository import StaffRepository, Staff
from repositories.group_repository import GroupRepository, Group
from repositories.cabinet_repository import CabinetRepository, Cabinet
from repositories.event_repository import EventRepository, Event
from repositories.class_repository import ClassRepository, Class
import mysql.connector
from datetime import datetime, timedelta, date, time


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

def main():
    connection = create_connection()
    student_repo = StudentRepository(connection)
    staff_repo = StaffRepository(connection)
    group_repo = GroupRepository(connection)
    cabinet_repo = CabinetRepository(connection)
    event_repo = EventRepository(connection)
    class_repo = ClassRepository(connection)

    #---------------------------------Student------------------------------
    # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student_repo.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student_repo.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student_repo.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student_repo.get_student_details(passport)
    #     if details:
    #         print("Паспорт:", details["Паспорт"])
    #         print("ПІБ:", details["ПІБ"])
    #         print("Курс:", details["Курс_навчання"])
    #         print("Форма навчання:", details["Форма_навчання"])
    #         print("Група:", details["Група"])
    #         print("Університет:", details["Університет"])
    #     else:
    #         print("Деталі студента не знайдено.")
    # else:
    #     print("Студента не знайдено.")

    # # --- 6. Тест перегляду активних студентів ---
    # print("\n== Активні студенти ==")
    # active_students = student_repo.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])


    # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student_repo.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student_repo.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student_repo.get_student_details(passport)
    #     if details:
    #         print("Паспорт:", details["Паспорт"])
    #         print("ПІБ:", details["ПІБ"])
    #         print("Курс:", details["Курс_навчання"])
    #         print("Форма навчання:", details["Форма_навчання"])
    #         print("Група:", details["Група"])
    #         print("Університет:", details["Університет"])
    #     else:
    #         print("Деталі студента не знайдено.")
    # else:
    #     print("Студента не знайдено.")

    # # --- 6. Тест перегляду активних студентів ---
    # print("\n== Активні студенти ==")
    # active_students = student_repo.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])

     # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student_repo.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student_repo.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student_repo.get_student_details(passport)
    #     if details:
    #         print("Паспорт:", details["Паспорт"])
    #         print("ПІБ:", details["ПІБ"])
    #         print("Курс:", details["Курс_навчання"])
    #         print("Форма навчання:", details["Форма_навчання"])
    #         print("Група:", details["Група"])
    #         print("Університет:", details["Університет"])
    #     else:
    #         print("Деталі студента не знайдено.")
    # else:
    #     print("Студента не знайдено.")

    # # --- 6. Тест перегляду активних студентів ---
    # print("\n== Активні студенти ==")
    # active_students = student_repo.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])


    #---------------------------------Staff Member------------------------------
    # # --- 1. Тест get_all_staff ---
    # print("== Усі члени персоналу ==")
    # staffmems = staff_repo.get_all_staff()
    # for s in staffmems:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_staff_by_passport ---
    # print("\n== Пошук члена персоналу ==")
    # passport = "JJ456456"
    # staffs = staff_repo.get_staff_by_passport(passport)
    # if staffs:
    #     print(f"Знайдено: {staffs.pib}")
    #     # --- 3. Тест get_staff_details ---
    #     print("\n== Деталі члена персоналу ==")
    #     details = staff_repo.get_staff_details(passport)
    #     if details:
    #         print("Паспорт:", details["Паспорт"])
    #         print("ПІБ:", details["ПІБ"])
    #         print("Зарплата:", details["Зарплата"])
    #         print("Кабінет:", details["Кабінет"])
    #         print("Університет:", details["Університет"])
    #     else:
    #         print("Деталі члена персоналу не знайдено.")
    # else:
    #     print("Члена персоналу не знайдено.")

    # # --- 6. Тест перегляду активних членів персоналу ---
    # print("\n== Активні члени персоналу ==")
    # active_staffs = staff_repo.get_active_staff()
    # for s in active_staffs:
    #     print(s["ПІБ"], s["Університет"])


    #---------------------------------Group------------------------------
    # # --- 1. Тест get_all_groups ---
    # print("== Усі групи ==")
    # groups = group_repo.get_all_groups()
    # for g in groups:
    #     print(f"Група {g.number}: {g.specialty}, Студентів: {g.student_count}, Університет: {g.university_name}")

    # # --- 2. Тест get_group_by_number ---
    # print("\n== Пошук групи ==")
    # group_number = 101
    # group = group_repo.get_group_by_number(group_number)
    # if group:
    #     print(f"Знайдено групу {group.number}: {group.specialty}, Університет: {group.university_name}")
    #     # --- 3. Тест get_group_details ---
    #     print("\n== Деталі групи ==")
    #     details = group_repo.get_group_details(group_number)
    #     if details:
    #         print("Номер:", details["Номер"])
    #         print("Спеціальність:", details["Спеціальність"])
    #         print("Кількість студентів:", details["Кількість_студентів"])
    #         print("Університет:", details["Університет"])
    #         if "Паспорт_викладача" in details:
    #             print("Куратор (паспорт):", details.get("Паспорт_викладача"))
    #             print("Куратор (ПІБ):", details.get("ПІБ"))
    #     else:
    #         print("Деталі групи не знайдено.")
    # else:
    #     print("Групу не знайдено.")

    # # --- 4. Тест перегляду активних груп ---
    # print("\n== Активні групи ==")
    # active_groups = group_repo.get_active_groups()
    # for g in active_groups:
    #     print(f"Група {g['Номер']}: {g['Спеціальність']}, Студентів: {g['Кількість_студентів']}, Університет: {g.get('Університет')}")


    #---------------------------------Cabinet------------------------------
    # # --- 1. Тест get_all_cabinets ---
    # print("== Усі кабінети ==")
    # cabinets = cabinet_repo.get_all_cabinets()
    # for c in cabinets:
    #     print(f"Номер: {c.number}, Поверх: {c.floor}, Кількість місць: {c.capacity}")

    # # --- 2. Тест get_cabinet_by_number ---
    # print("\n== Пошук кабінету ==")
    # cabinet_number = 101  # заміни на існуючий номер
    # cab = cabinet_repo.get_cabinet_by_number(cabinet_number)
    # if cab:
    #     print(f"Знайдено: Кабінет {cab.number}, поверх {cab.floor}")

    #     # --- 3. Тест get_cabinet_details ---
    #     print("\n== Деталі кабінету ==")
    #     details = cabinet_repo.get_cabinet_details(cabinet_number)
    #     if details:
    #         print("Номер:", details.number)
    #         print("Поверх:", details.floor)
    #         print("Кількість місць:", details.capacity)
    #         if details.university_name:
    #             print("Університет:", details.university_name)
    #         if hasattr(details, 'responsible_person') and details.responsible_person:
    #             print("Відповідальний співробітник:", details.responsible_person)
    #     else:
    #         print("Деталі кабінету не знайдено.")
    # else:
    #     print("Кабінет не знайдено.")

    # # --- 4. Тест get_active_cabinets ---
    # print("\n== Активні кабінети ==")
    # active_cabinets = cabinet_repo.get_active_cabinets()
    # for c in active_cabinets:
    #     print(f"Номер: {c['Номер']}, Поверх: {c['Поверх']}, Кількість місць: {c.get('Кількість_місць')}")


    #---------------------------------Events------------------------------
    # --- 1. Тест get_all_events ---
    # print("== Усі заходи ==")
    # events = event_repo.get_all_events()
    # for e in events:
    #     print(f"{e.date} {e.start_time} | Кабінет: {e.cabinet_number} | Назва: {e.name} | Тип: {e.event_type} | Кінець: {e.end_time}")

    # # --- 2. Тест get_event_details ---
    # print("\n== Деталі заходу ==")
    # test_date = date(2025, 10, 23)          # постав свою дату
    # test_start_time = time(10, 0)            # час початку
    # test_cabinet = 101                       # номер кабінету
    # details = event_repo.get_event_details(test_date, test_start_time, test_cabinet)
    # if details:
    #     print(f"Дата: {details.date}")
    #     print(f"Час початку: {details.start_time}")
    #     print(f"Кінець: {details.end_time}")
    #     print(f"Кабінет: {details.cabinet_number}")
    #     print(f"Тип: {details.event_type}")
    #     print(f"Тривалість: {details.duration} хв")
    # else:
    #     print("Деталі заходу не знайдено.")

    # # --- 6. Тест перегляду активних заходів ---
    # print("\n== Активні заходи ==")
    # active_events = event_repo.get_active_events()
    # for e in active_events:
    #     print(f"{e['Дата']} {e['Час_початку']} | Кабінет: {e['Номер_кабінету']} | Назва: {e.get('Назва')} | Тип: {e.get('Тип')}")


    #---------------------------------Classes------------------------------
    # ====== 1. Тест get_all_classes ======
    # print("== Усі активні пари ==")
    # classes = class_repo.get_all_classes()
    # for c in classes:
    #     print(f"{c.date} {c.start_time} | Кабінет: {c.cabinet_number} | Предмет: {c.subject} | Кінець: {c.end_time}")

    # # ====== 2. Тест get_class_details ======
    # print("\n== Деталі пари ==")
    # test_date = datetime(2025, 10, 23).date()
    # test_start_time = time(9, 0)
    # test_cabinet = 101
    # details = class_repo.get_class_details(test_date, test_start_time, test_cabinet)
    # if details:
    #     print(f"Дата: {details['date']}")
    #     print(f"Час початку: {details['start_time']}")
    #     print(f"Кінець: {details['end_time']}")
    #     print(f"Кабінет: {details['cabinet_number']}")
    #     print(f"Предмет: {details['subject']}")
    #     print(f"Тривалість: {details['duration']} хв")
    #     print(f"Поверх кабінету: {details['cabinet_floor']}")
    #     print(f"Кількість місць: {details['cabinet_capacity']}")
    #     print(f"Університет: {details['university_name']} (ID: {details['university_id']})")
    #     print(f"Викладач: {details['teacher']}")
    # else:
    #     print("Деталі пари не знайдено.")

    # # ====== 6. Перевірка активних пар після відновлення ======
    # classes = class_repo.get_all_classes()
    # print("\n== Всі активні пари після відновлення ==")
    # for c in classes:
    #     print(f"{c.date} {c.start_time} | Кабінет: {c.cabinet_number} | Предмет: {c.subject} | Кінець: {c.end_time}")


    connection.close()


if __name__ == "__main__":
    main()
