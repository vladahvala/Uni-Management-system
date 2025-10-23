class Group:
    """Модель групи"""
    def __init__(self, number, student_count, specialty, university_id, university_name, curator_passport=None, curator_pib=None):
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

    # ---------------------- Отримання груп ----------------------
    def get_all_groups(self):
        """Отримати всі групи через збережену процедуру"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllGroups')  # якщо буде така процедура
            groups = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    groups.append(Group(
                        row['Номер'],
                        row['Кількість_студентів'],
                        row['Спеціальність'],
                        row['Університет_ID'],
                        row.get('Університет')
                    ))
            return groups

    def get_group_by_number(self, number):
        """Отримати групу за номером"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetGroupByNumber', [number])  # якщо буде така процедура
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Group(
                        row['Номер'],
                        row['Кількість_студентів'],
                        row['Спеціальність'],
                        row['Університет_ID'],
                        row.get('Університет')
                    )
            return None

    # ---------------------- Додавання та оновлення ----------------------
    def add_group(self, group):
        """Додати групу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddGroup', [
                group.number,
                group.student_count,
                group.specialty,
                group.university_id,
                self.current_user
            ])
            self.connection.commit()

    def update_group(self, group):
        """Оновити інформацію про групу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateGroup', [
                group.number,
                group.student_count,
                group.specialty,
                group.university_id,
                self.current_user
            ])
            self.connection.commit()

    # ---------------------- Видалення / Відновлення ----------------------
    def delete_group(self, number):
        """Видалити групу (soft delete)"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteGroup', [number, self.current_user])
            self.connection.commit()

    def restore_group(self, number):
        """Відновити групу"""
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreGroup', [number, self.current_user])
            self.connection.commit()

    # ---------------------- Методи на основі VIEW ----------------------
    def get_active_groups(self):
        """Отримати всі активні групи"""
        query = "SELECT * FROM ActiveGroups"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_group_details(self, number):
        """Отримати детальну інформацію про групу"""
        query = "SELECT * FROM GroupDetails WHERE Номер = %s"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (number,))
            return cursor.fetchone()
