class StaffMember:
    """Модель члена_персоналу"""
    def __init__(self, passport, pib):
        self.passport = passport
        self.pib = pib


class StaffMemberRepository:
    """Repository для роботи із членами персоналу"""
    def __init__(self, connection):
        self.connection = connection

    def get_all_staffmembers(self):
        """Отримати всіх членів персоналу через збережену процедуру"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllStaff')
            staffmems = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    staffmems.append(StaffMember(row['Паспорт'], row['ПІБ']))
            return staffmems

    def get_staffmember_by_passport(self, passport):
        """Отримати члена персоналу за паспортом"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetStudentByPassport', [passport])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Student(row['Паспорт'], row['ПІБ'], row['ID_групи'])
            return None

    def add_student(self, student):
        """Додати студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddStudent', [student.passport, student.pib, student.group_id])
            self.connection.commit()

    def update_student(self, student):
        """Оновити інформацію про студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateStudent', [student.passport, student.pib, student.group_id])
            self.connection.commit()

    def delete_student(self, passport):
        """Видалити студента"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteStudent', [passport])
            self.connection.commit()

    # --- Нові методи на основі VIEW ---
    def get_active_students(self):
        """Отримати всіх активних студентів"""
        query = "SELECT * FROM ActiveStudents"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_student_details(self, passport):
        """Отримати детальну інформацію про студента"""
        query = "SELECT * FROM StudentDetails WHERE Паспорт = %s"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (passport,))
            return cursor.fetchone()
