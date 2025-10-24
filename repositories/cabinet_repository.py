class Cabinet:
    """Модель кабінету"""
    def __init__(self, number, floor, capacity=None, university_id=None, university_name=None, is_active=True):
        self.number = number                 
        self.floor = floor                    
        self.capacity = capacity             
        self.university_id = university_id   
        self.university_name = university_name  
        self.is_active = is_active            


class CabinetRepository:
    """Repository для роботи з кабінетами"""
    def __init__(self, connection, current_user="system_user"):
        self.connection = connection
        self.current_user = current_user

    # ---------------------- Отримання кабінетів ----------------------
    def get_all_cabinets(self):
        """Отримати всі кабінети через збережену процедуру"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetAllCabinets')
            cabinets = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    cabinets.append(Cabinet(
                        number=row['Номер'],
                        floor=row['Поверх'],
                        capacity=row.get('Кількість_місць'),
                        university_id=None,
                        university_name=None,
                        is_active=row['IsDeleted'] == 0
                    ))
            return cabinets

    def get_cabinet_by_number(self, number):
        """Отримати кабінет за номером"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetCabinetByNumber', [number])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Cabinet(
                        number=row['Номер'],
                        floor=row['Поверх'],
                        capacity=row.get('Кількість_місць'),
                        university_id=None,
                        university_name=None,
                        is_active=row['IsDeleted'] == 0
                    )
            return None

    # ---------------------- Додавання / Оновлення ----------------------
    def add_cabinet(self, cabinet):
        """Додати новий кабінет"""
        with self.connection.cursor() as cursor:
            cursor.callproc('AddCabinet', [
                cabinet.number,
                None,                   # немає building
                cabinet.floor,
                cabinet.capacity,
                self.current_user
            ])
            self.connection.commit()

    def update_cabinet(self, cabinet):
        """Оновити дані кабінету"""
        with self.connection.cursor() as cursor:
            cursor.callproc('UpdateCabinet', [
                cabinet.number,
                None,                   # немає building
                cabinet.floor,
                cabinet.capacity,
                self.current_user
            ])
            self.connection.commit()

    # ---------------------- Видалення / Відновлення ----------------------
    def delete_cabinet(self, number):
        """Видалити кабінет (soft delete)"""
        with self.connection.cursor() as cursor:
            cursor.callproc('DeleteCabinet', [number, self.current_user])
            self.connection.commit()

    def restore_cabinet(self, number):
        """Відновити кабінет"""
        with self.connection.cursor() as cursor:
            cursor.callproc('RestoreCabinet', [number, self.current_user])
            self.connection.commit()

    # ---------------------- Методи на основі VIEW ----------------------
    def get_active_cabinets(self):
        """Отримати всі активні кабінети (через view ActiveCabinets)"""
        query = "SELECT * FROM ActiveCabinets"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_cabinet_details(self, number):
        """Отримати детальну інформацію про кабінет (через view CabinetDetails)"""
        query = "SELECT * FROM CabinetDetails WHERE Номер = %s"
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (number,))
            row = cursor.fetchone()
            if row:
                return Cabinet(
                    number=row['Номер'],
                    floor=row['Поверх'],
                    capacity=row.get('Кількість_місць'),
                    university_id=row.get('Університет_ID'),
                    university_name=row.get('Університет'),
                    is_active=True
                )
            return None
