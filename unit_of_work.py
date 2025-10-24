from repositories.student_repository import StudentRepository, Student
from repositories.staff_repository import StaffRepository, Staff
from repositories.group_repository import GroupRepository, Group
from repositories.cabinet_repository import CabinetRepository, Cabinet
from repositories.event_repository import EventRepository, Event
from repositories.class_repository import ClassRepository, Class

class UnitOfWork:
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

        # Підключаємо існуючі репозиторії
        self.students = StudentRepository(connection, current_user)
        self.staff = StaffRepository(connection, current_user)  # Член персоналу
        self.groups = GroupRepository(connection, current_user)
        self.cabinets = CabinetRepository(connection, current_user)
        self.events = EventRepository(connection, current_user)
        self.classes = ClassRepository(connection, current_user)

        self._active = False

    def __enter__(self):
        self._active = True
        self.connection.start_transaction()  # замість begin()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.connection.rollback()  # відкат, якщо була помилка
        else:
            self.connection.commit()  # коміт, якщо все пройшло успішно
        self._active = False

    def commit(self):
        if self._active:
            self.connection.commit()

    def rollback(self):
        if self._active:
            self.connection.rollback()
