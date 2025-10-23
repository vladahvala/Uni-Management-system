from repositories.student_repository import StudentRepository, Student
from repositories.staff_repository import StaffRepository, Staff
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="14768967H&ab",
        database="university"
    )

def main():
    connection = create_connection()
    student = StudentRepository(connection)
    staff = StaffRepository(connection)

    # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student.get_student_details(passport)
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
    # active_students = student.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])


    # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student.get_student_details(passport)
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
    # active_students = student.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])

     # # --- 1. Тест get_all_students ---
    # print("== Усі студенти ==")
    # students = student.get_all_students()
    # for s in students:
    #     print(s.pib, s.university)

    # # --- 2. Тест get_student_by_passport ---
    # print("\n== Пошук студента ==")
    # passport = "AA123456"
    # student = student.get_student_by_passport(passport)
    # if student:
    #     print(f"Знайдено: {student.pib}")
    #     # --- 3. Тест get_student_details ---
    #     print("\n== Деталі студента ==")
    #     details = student.get_student_details(passport)
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
    # active_students = student.get_active_students()
    # for s in active_students:
    #     print(s["ПІБ"], s["Університет"])


    # --- 1. Тест get_all_staff ---
    print("== Усі члени персоналу ==")
    staffmems = staff.get_all_staff()
    for s in staffmems:
        print(s.pib, s.university)

    # --- 2. Тест get_staff_by_passport ---
    print("\n== Пошук члена персоналу ==")
    passport = "JJ456456"
    staffs = staff.get_staff_by_passport(passport)
    if staffs:
        print(f"Знайдено: {staffs.pib}")
        # --- 3. Тест get_staff_details ---
        print("\n== Деталі члена персоналу ==")
        details = staff.get_staff_details(passport)
        if details:
            print("Паспорт:", details["Паспорт"])
            print("ПІБ:", details["ПІБ"])
            print("Зарплата:", details["Зарплата"])
            print("Кабінет:", details["Кабінет"])
            print("Університет:", details["Університет"])
        else:
            print("Деталі члена персоналу не знайдено.")
    else:
        print("Члена персоналу не знайдено.")

    # --- 6. Тест перегляду активних членів персоналу ---
    print("\n== Активні члени персоналу ==")
    active_staffs = staff.get_active_staff()
    for s in active_staffs:
        print(s["ПІБ"], s["Університет"])

    connection.close()


if __name__ == "__main__":
    main()
