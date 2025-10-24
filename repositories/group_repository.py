class Group:
    """Модель групи"""
    def __init__(self, number, student_count, specialty, university_id, university_name,
                 curator_passport=None, curator_pib=None):
        self.number = number
        self.student_count = student_count
        self.specialty = specialty
        self.university_id = university_id
        self.university_name = university_name
        self.curator_passport = curator_passport
        self.curator_pib = curator_pib


class GroupRepository:
    """Repository для роботи з групами"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

    # ---------------------- Отримання всіх груп ----------------------
    def get_all_groups(self):
        """Отримати всі групи (через збережену процедуру GetAllGroups)"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllGroups')
            groups = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    groups.append(Group(
                        number=row['Номер'],
                        student_count=row['Кількість_студентів'],
                        specialty=row['Спеціальність'],
                        university_id=row['ID_університету'],
                        university_name=row['Університет'],
                        curator_passport=row.get('Паспорт_викладача'),
                        curator_pib=row.get('Викладач')
                    ))
            return groups

    # ---------------------- Отримання групи за номером ----------------------
    def get_group_by_number(self, number):
        """Отримати групу за номером (через збережену процедуру GetGroupByNumber)"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetGroupByNumber', [number])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Group(
                        number=row['Номер'],
                        student_count=row['Кількість_студентів'],
                        specialty=row['Спеціальність'],
                        university_id=row['ID_університету'],
                        university_name=row['Університет'],
                        curator_passport=row.get('Паспорт_викладача'),
                        curator_pib=row.get('Викладач')
                    )
        return None

    # ---------------------- Додавання групи ----------------------
    def add_group(self, group):
        """Додати нову групу через процедуру AddGroup"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddGroup', [
                group.number,
                group.student_count,
                group.specialty,
                group.university_id,
                group.curator_passport,  # тепер передаємо паспорт куратора
                self.current_user
            ])
            self.connection.commit()

    # ---------------------- Оновлення групи ----------------------
    def update_group(self, group):
        """Оновити групу через процедуру UpdateGroup"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateGroup', [
                group.number,
                group.student_count,
                group.specialty,
                group.university_id,
                group.curator_passport,  # паспорт куратора
                self.current_user
            ])
            self.connection.commit()

    # ---------------------- Логічне видалення ----------------------
    def delete_group(self, number):
        """Позначити групу як видалену через процедуру DeleteGroup"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteGroup', [number, self.current_user])
            self.connection.commit()

    # ---------------------- Відновлення групи ----------------------
    def restore_group(self, number):
        """Відновити логічно видалену групу через процедуру RestoreGroup"""
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreGroup', [number, self.current_user])
            self.connection.commit()

    # ---------------------- Дані з VIEW ----------------------
    def get_active_groups(self):
        """Отримати всі активні групи з в'ю ActiveGroups"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM ActiveGroups")
            return cursor.fetchall()

    def get_group_details(self, number):
        """Отримати детальну інформацію про групу з в'ю GroupDetails"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM GroupDetails WHERE Номер = %s", (number,))
            return cursor.fetchone()
