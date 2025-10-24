from datetime import datetime, timedelta, time

class Event:
    """Модель заходу"""
    def __init__(self, date, start_time, cabinet_number, event_type, duration, is_active=True):
        self.date = date
        self.start_time = start_time
        self.cabinet_number = cabinet_number
        self.event_type = event_type
        self.duration = duration
        self.is_active = is_active

    @property
    def end_time(self):
        """Обчислює кінець заходу"""
        if self.start_time and self.duration is not None:
            if isinstance(self.start_time, timedelta):
                total_seconds = self.start_time.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                start_time_obj = time(hours, minutes, seconds)
            elif isinstance(self.start_time, time):
                start_time_obj = self.start_time
            else:
                return None

            start_dt = datetime.combine(self.date, start_time_obj)
            end_dt = start_dt + timedelta(minutes=self.duration)
            return end_dt.time()
        return None


class EventRepository:
    """Repository для роботи з заходами"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

    # ===== Отримати всі активні заходи =====
    def get_all_events(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllEvents')
            events = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    events.append(Event(
                        row['Дата'],
                        row['Час_початку'],
                        row['Номер_кабінету'],
                        row['Тип'],
                        row['Тривалість'],
                        row['IsDeleted'] == 0
                    ))
            return events

    # ===== Додати захід =====
    def add_event(self, event):
        with self.connection.cursor() as cursor:
            cursor.callproc('AddEvent', [
                event.date,
                event.start_time,
                event.cabinet_number,
                event.event_type,
                event.duration,
                self.current_user
            ])
            self.connection.commit()

    # ===== Оновити захід =====
    def update_event(self, event):
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateEvent', [
                event.date,
                event.start_time,
                event.cabinet_number,
                event.event_type,
                event.duration,
                self.current_user
            ])
            self.connection.commit()

     # ===== Отримати захід за ключем (дата, час, кабінет) =====
    def get_event_by_key(self, date, start_time, cabinet_number):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetEventByKey', [date, start_time, cabinet_number])
            # Зберемо результати з курсора
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Event(
                        row['Дата'],
                        row['Час_початку'],
                        row['Номер_кабінету'],
                        row['Тип'],
                        row['Тривалість'],
                        True
                    )
            return None

    # ===== Логічно видалити =====
    def delete_event(self, date, start_time, cabinet_number):
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteEvent', [date, start_time, cabinet_number, self.current_user])
            self.connection.commit()

    # ===== Відновити =====
    def restore_event(self, date, start_time, cabinet_number):
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreEvent', [date, start_time, cabinet_number, self.current_user])
            self.connection.commit()

    # ===== Отримати всі активні заходи через VIEW =====
    def get_active_events(self):
        query = "SELECT * FROM ActiveEvents"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    # ===== Деталі заходу =====
    def get_event_details(self, date, start_time, cabinet_number):
        query = """
        SELECT *
        FROM EventDetails
        WHERE Дата = %s AND Час_початку = %s AND Номер_кабінету = %s
        """
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (date, start_time, cabinet_number))
            row = cursor.fetchone()
            if row:
                return Event(
                    row['Дата'],
                    row['Час_початку'],
                    row['Номер_кабінету'],
                    row['Тип'],
                    row['Тривалість'],
                    True
                )
            return None
