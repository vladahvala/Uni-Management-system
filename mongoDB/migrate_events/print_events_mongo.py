# show_events.py
from pymongo import MongoClient

# --- Підключення до MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["university_db"]
events = db["Заходи"]

# --- Вивід ---
for event in events.find():
    print(f"Дата: {event['Дата']}")
    print(f"Час початку: {event['Час_початку']}")
    print(f"Номер кабінету: {event['Номер_кабінету']}")
    print(f"Тип заходу: {event.get('Тип', 'Невідомий')}")
    print(f"Тривалість: {event['Тривалість']} хвилин")

    # Деталі типу
    if event.get("Деталі_типу"):
        print("Деталі типу:")
        for key, value in event["Деталі_типу"].items():
            print(f"  {key}: {value}")

    # Кабінет
    if event.get("Кабінет"):
        cab = event["Кабінет"]
        print(f"Кабінет деталі: Номер: {cab['Номер']}, Поверх: {cab['Поверх']}, Місць: {cab['Кількість_місць']}, Тип: {cab['Тип']}")

    # Учасники персонал
    if event.get("Учасники_персонал"):
        print("Учасники (персонал):")
        for staff in event["Учасники_персонал"]:
            print(f"  {staff['ПІБ']}")

    print("-" * 50)
