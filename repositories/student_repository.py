class Student:
    """Модель студента"""
    def __init__(self, passport, pib, course, form, group_number, university_id, university_name):
        self.passport = passport
        self.pib = pib
        self.course = course
        self.form = form
        self.group_number = group_number
        self.university_id = university_id
        self.university_name = university_name


class StudentRepository:
    """Repository для роботи зі студентами"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

    # ---------------------- Отримання студентів ----------------------
    def get_all_students(self):
        """Отримати всіх студентів через збережену процедуру"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllStudents')
            students = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    students.append(Student(
                        row['Паспорт'],
                        row['ПІБ'],
                        row['Курс_навчання'],
                        row['Форма_навчання'],
                        row['Група'],
                        row['Університет_ID'],
                        row['Університет']
                    ))
            return students

    def get_student_by_passport(self, passport):
        """Отримати студента за паспортом"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetStudentByPassport', [passport])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Student(
                        row['Паспорт'],
                        row['ПІБ'],
                        row['Курс_навчання'],
                        row['Форма_навчання'],
                        row['Група'],
                        row['Університет_ID'],
                        row['Університет']
                    )
            return None

    # ---------------------- Додавання та оновлення ----------------------
    def add_student(self, student):
        """Додати студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddStudent', [
                student.passport,
                student.pib,
                student.group_number,
                student.course,
                student.form,
                student.university_id,   # ✅ передаємо ID, як очікує процедура
                self.current_user
            ])
            self.connection.commit()

    def update_student(self, student):
        """Оновити інформацію про студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateStudent', [
                student.passport,
                student.course,
                student.form,
                student.group_number,
                self.current_user
            ])
            self.connection.commit()

    # ---------------------- Видалення / Відновлення ----------------------
    def delete_student(self, passport):
        """Видалити студента (soft delete)"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteStudent', [passport, self.current_user])
            self.connection.commit()

    def restore_student(self, passport):
        """Відновити студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreStudent', [passport, self.current_user])
            self.connection.commit()

    # ---------------------- Методи на основі VIEW ----------------------
    def get_active_students(self):
        """Отримати всіх активних студентів"""
        query = "SELECT * FROM ActiveStudents"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            students = []
            for row in cursor.fetchall():
                students.append(Student(
                    row['Паспорт'],
                    row['ПІБ'],
                    row['Курс_навчання'],
                    row['Форма_навчання'],
                    row['Номер_групи'],
                    None,                # У цій view немає ID
                    row['Університет']
                ))
            return students

    def get_student_details(self, passport):
        """Отримати детальну інформацію про студента"""
        query = "SELECT * FROM StudentDetails WHERE Паспорт = %s"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (passport,))
            row = cursor.fetchone()
            if row:
                return Student(
                    row['Паспорт'],
                    row['ПІБ'],
                    row['Курс_навчання'],
                    row['Форма_навчання'],
                    row['Група'],
                    row['Університет_ID'],
                    row['Університет']
                )
            return None
