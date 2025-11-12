# print_events_redis.py
import redis
import json

# Підключаємося до Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Отримуємо всі ключі, що починаються з event:
keys = list(r.scan_iter("event:*"))

if not keys:
    print("Ключів не знайдено у Redis.")
else:
    print(f"Знайдено {len(keys)} ключів:\n")
    for key in keys:
        key_str = key.decode("utf-8")  # перетворюємо байти у рядок
        event_json = r.get(key)
        if event_json:
            event = json.loads(event_json)
            print(f"Ключ: {key_str}")
            print(f"Дата: {event.get('Дата')}")
            print(f"Час початку: {event.get('Час_початку')}")
            print(f"Номер кабінету: {event.get('Номер_кабінету')}")
            print(f"Тип заходу: {event.get('Тип', 'Невідомий')}")
            print(f"Тривалість: {event.get('Тривалість')} хвилин")
            if event.get("Деталі_типу"):
                print("Деталі типу:")
                for k, v in event["Деталі_типу"].items():
                    print(f"  {k}: {v}")
            if event.get("Кабінет"):
                cab = event["Кабінет"]
                print(f"Кабінет: Номер {cab['Номер']}, Поверх {cab['Поверх']}, Місць {cab['Кількість_місць']}, Тип {cab['Тип']}")
            if event.get("Учасники_персонал"):
                print("Учасники персонал:")
                for staff in event["Учасники_персонал"]:
                    print(f"  {staff['ПІБ']}")
            print("-" * 50)

r.close()
