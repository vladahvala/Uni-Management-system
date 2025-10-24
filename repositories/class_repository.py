from datetime import datetime, timedelta, time

from datetime import datetime, timedelta, time

class Class:
    """Модель пари (заняття)"""
    def __init__(self, date, start_time, cabinet_number, subject, duration, is_active=True):
        self.date = date
        self.start_time = start_time
        self.cabinet_number = cabinet_number
        self.subject = subject
        self.duration = duration
        self.is_active = is_active

    @property
    def end_time(self):
        """Обчислює кінець пари, додаючи тривалість"""
        if self.start_time and self.duration is not None:
            # Якщо start_time прийшов як timedelta, конвертуємо в time
            if isinstance(self.start_time, timedelta):
                total_seconds = int(self.start_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                start_time_obj = time(hours, minutes, seconds)
            else:
                start_time_obj = self.start_time  # вже time

            start_dt = datetime.combine(self.date, start_time_obj)
            end_dt = start_dt + timedelta(minutes=self.duration)
            return end_dt.time()
        return None



class ClassRepository:
    """Repository для роботи з парами"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

    # ===== Додавання пари =====
    def add_class(self, class_session: Class):
        with self.connection.cursor() as cursor:
            cursor.callproc('AddClass', [
                class_session.date,
                class_session.start_time,
                class_session.cabinet_number,
                class_session.subject,
                class_session.duration,
                self.current_user
            ])
            self.connection.commit()

    # ===== Логічне видалення =====
    def delete_class(self, date, start_time, cabinet_number):
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteClass', [date, start_time, cabinet_number, self.current_user])
            self.connection.commit()

    # ===== Відновлення =====
    def restore_class(self, date, start_time, cabinet_number):
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreClass', [date, start_time, cabinet_number, self.current_user])
            self.connection.commit()

    # ===== Отримати всі активні пари =====
    def get_all_classes(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllClasses')
            classes = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    classes.append(Class(
                        row['Дата'],
                        row['Час_початку'],
                        row['Номер_кабінету'],
                        row['Предмет'],
                        row['Тривалість'],
                        True
                    ))
            return classes

    # ===== Отримати пару по ключу =====
    def get_class_by_key(self, date, start_time, cabinet_number):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetClassByKey', [date, start_time, cabinet_number])
            row = None
            for result in cursor.stored_results():
                row = result.fetchone()
                break
            if row:
                return Class(
                    row['Дата'],
                    row['Час_початку'],
                    row['Номер_кабінету'],
                    row['Предмет'],
                    row['Тривалість'],
                    True
                )
            return None

    # ===== Отримати деталі пари =====
    def get_class_details(self, date, start_time, cabinet_number):
        query = """
        SELECT *
        FROM ClassDetails
        WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
        """
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (date, start_time, cabinet_number))
            row = cursor.fetchone()
            if row:
                # Конвертація MySQL TIME (може бути timedelta) в time
                start_time_obj = row['Час_початку']
                if isinstance(start_time_obj, timedelta):
                    total_seconds = int(start_time_obj.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    start_time_obj = time(hours, minutes, seconds)

                return {
                    'date': row['Дата'],
                    'start_time': start_time_obj,
                    'end_time': (datetime.combine(row['Дата'], start_time_obj) + timedelta(minutes=row['Тривалість'])).time(),
                    'cabinet_number': row['Номер_кабінету'],
                    'subject': row['Предмет'],
                    'duration': row['Тривалість'],
                    'cabinet_floor': row['Кабінет_поверх'],
                    'cabinet_capacity': row['Кількість_місць'],
                    'university_id': row['Університет_ID'],
                    'university_name': row['Університет'],
                    'teacher': row['Викладач']
                }
        return None

