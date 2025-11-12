import redis
import json

# --- Підключення до Redis ---
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# --- Отримання всіх ключів, що починаються з "pair:" ---
pair_keys = r.keys("pair:*")

for key in pair_keys:
    data = r.get(key)
    if data:
        pair = json.loads(data)
        print(f"Дата: {pair['Дата']}")
        print(f"Час початку: {pair['Час_початку']}")
        print(f"Номер кабінету: {pair['Номер_кабінету']}")
        print(f"Предмет: {pair['Предмет']}")
        print(f"Тривалість: {pair['Тривалість']} хвилин")
        print(f"Тип пари: {pair.get('Тип', 'Невідомий')}")

        # Деталі типу
        if pair.get("Деталі_типу"):
            for k, v in pair["Деталі_типу"].items():
                print(f"  {k}: {v}")

        # Кабінет
        if pair.get("Кабінет"):
            cab = pair["Кабінет"]
            print(f"Кабінет деталі: Номер: {cab['Номер']}, Поверх: {cab['Поверх']}, Місць: {cab['Кількість_місць']}")

        # Викладачі
        if pair.get("Викладачі"):
            print("Викладачі:")
            for teacher in pair["Викладачі"]:
                print(f"  {teacher['ПІБ']} ({teacher['Предмет']}, {teacher['Науковий_ступінь']})")

        # Групи
        if pair.get("Групи"):
            print("Групи:")
            for group in pair["Групи"]:
                print(f"  Номер: {group['Номер']}, Студентів: {group['Кількість_студентів']}, Спеціальність {group['Спеціальність']}")

        # Студенти
        if pair.get("Студенти"):
            print("Студенти:")
            for student in pair["Студенти"]:
                print(f"  {student['ПІБ']} (Паспорт: {student['Паспорт']}, Група: {student['Номер_групи']}, "
                      f"Курс: {student['Курс_навчання']}, Форма навчання: {student['Форма_навчання']})")

        print("-" * 50)
