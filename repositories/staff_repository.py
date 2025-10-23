class Staff:
    """Модель члена персоналу"""
    def __init__(self, passport, pib, salary, cabinet, university):
        self.passport = passport
        self.pib = pib
        self.salary = salary
        self.cabinet = cabinet
        self.university = university


class StaffRepository:
    """Repository для роботи із членами персоналу"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user 

    # ---------------------- Отримання членів персоналу ----------------------
    def get_all_staff(self):
        """Отримати всіх членів персоналу через збережену процедуру"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllStaff')
            staff = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    staff.append(Staff(
                        row['Паспорт'],
                        row['ПІБ'],
                        row['Зарплата'],
                        row['Кабінет'],
                        row['Університет']
                    ))
            return staff

    def get_staff_by_passport(self, passport):
        """Отримати члена персоналу за паспортом"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetStaffByPassport', [passport])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Staff(
                         row['Паспорт'],
                        row['ПІБ'],
                        row['Зарплата'],
                        row['Кабінет'],
                        row['Університет']
                    )
            return None

    # ---------------------- Додавання та оновлення ----------------------
    def add_staff(self, staff):
        """Додати члена персоналу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddStaff', [
                staff.passport,
                staff.pib,
                staff.salary,
                staff.cabinet,
                staff.university,      # тут передаємо ID університету
                self.current_user        # хто додає
            ])
            self.connection.commit()

    def update_staff(self, staff):
        """Оновити інформацію про члена персоналу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateStaff', [
                staff.passport,
                staff.salary,
                staff.cabinet,
                self.current_user        # хто оновлює
            ])
            self.connection.commit()

    # ---------------------- Видалення / Відновлення ----------------------
    def delete_staff(self, passport):
        """Видалити члена персоналу (soft delete)"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteStaff', [passport, self.current_user])
            self.connection.commit()

    def restore_staff(self, passport):
        """Відновити члена персоналу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreStaff', [passport, self.current_user])
            self.connection.commit()

    # ---------------------- Методи на основі VIEW ----------------------
    def get_active_staff(self):
        """Отримати всіх активних членів персоналу"""
        query = "SELECT * FROM ActiveStaff"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
        
    def get_staff_details(self, passport):
        """Отримати детальну інформацію про члена персоанлу"""
        query = "SELECT * FROM StaffDetails WHERE Паспорт = %s"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (passport,))
            return cursor.fetchone()

