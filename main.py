from repositories.student_repository import StudentRepository, Student
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
    repo = StudentRepository(connection)

    # --- 1. Тест get_all_students ---
    print("== Усі студенти ==")
    students = repo.get_all_students()
    for s in students:
        print(s.pib, s.university)

    # --- 2. Тест get_student_by_passport ---
    print("\n== Пошук студента ==")
    passport = "AA123456"
    student = repo.get_student_by_passport(passport)
    if student:
        print(f"Знайдено: {student.pib}")
        # --- 3. Тест get_student_details ---
        print("\n== Деталі студента ==")
        details = repo.get_student_details(passport)
        if details:
            print("Паспорт:", details["Паспорт"])
            print("ПІБ:", details["ПІБ"])
            print("Курс:", details["Курс_навчання"])
            print("Форма навчання:", details["Форма_навчання"])
            print("Група:", details["Група"])
            print("Університет:", details["Університет"])
        else:
            print("Деталі студента не знайдено.")
    else:
        print("Студента не знайдено.")

    # --- 6. Тест перегляду активних студентів ---
    print("\n== Активні студенти ==")
    active_students = repo.get_active_students()
    for s in active_students:
        print(s["ПІБ"], s["Університет"])

    connection.close()


if __name__ == "__main__":
    main()
