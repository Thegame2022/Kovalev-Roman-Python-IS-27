import sqlite3

# Подключение к базе
conn = sqlite3.connect('sklad.db')
c = conn.cursor()

# Создаем таблицу если её нет
c.execute('''CREATE TABLE IF NOT EXISTS tovari (
             kod INTEGER PRIMARY KEY, 
             marka TEXT, 
             tip TEXT, 
             cena REAL, 
             kolvo INTEGER, 
             min_zapas INTEGER)''')
conn.commit()


def dobavit():
    print("\n[Добавить товар]")
    kod = int(input("Код: "))
    marka = input("Марка: ")
    tip = input("Тип: ")
    cena = float(input("Цена: "))
    kolvo = int(input("Кол-во: "))
    min_zapas = int(input("Мин.запас: "))

    c.execute("INSERT INTO tovari VALUES (?,?,?,?,?,?)",
              (kod, marka, tip, cena, kolvo, min_zapas))
    conn.commit()
    print("✅ Товар добавлен")


def poisk():
    print("\n[Поиск]")
    m = input("Марка (Enter - пропустить): ")
    t = input("Тип (Enter - пропустить): ")

    query = "SELECT * FROM tovari WHERE 1=1"
    params = []

    if m:
        query += " AND marka LIKE ?"
        params.append(f'%{m}%')
    if t:
        query += " AND tip LIKE ?"
        params.append(f'%{t}%')

    c.execute(query, params)
    result = c.fetchall()

    if not result:
        print("😢 Ничего не найдено")
    else:
        print("\nСписок товаров:")
        for row in result:
            print(f"{row[0]}. {row[1]} ({row[2]}), {row[4]} шт. по {row[3]} руб.")


def udalit():
    print("\n[Удалить товар]")
    kod = int(input("Код товара: "))

    c.execute("DELETE FROM tovari WHERE kod=?", (kod,))
    conn.commit()

    if c.rowcount > 0:
        print("✅ Товар удален")
    else:
        print("❌ Товар не найден")


def redakt():
    print("\n[Изменить товар]")
    kod = int(input("Код товара: "))

    c.execute("SELECT * FROM tovari WHERE kod=?", (kod,))
    tovar = c.fetchone()

    if not tovar:
        print("❌ Товар не найден")
        return

    print(f"\nТекущие данные:")
    print(f"1. Марка: {tovar[1]}")
    print(f"2. Тип: {tovar[2]}")
    print(f"3. Цена: {tovar[3]}")
    print(f"4. Кол-во: {tovar[4]}")
    print(f"5. Мин.запас: {tovar[5]}")

    pole = int(input("\nЧто меняем? (1-5): "))
    novoe = input("Новое значение: ")

    if pole == 1:
        c.execute("UPDATE tovari SET marka=? WHERE kod=?", (novoe, kod))
    elif pole == 2:
        c.execute("UPDATE tovari SET tip=? WHERE kod=?", (novoe, kod))
    elif pole == 3:
        c.execute("UPDATE tovari SET cena=? WHERE kod=?", (float(novoe), kod))
    elif pole == 4:
        c.execute("UPDATE tovari SET kolvo=? WHERE kod=?", (int(novoe), kod))
    elif pole == 5:
        c.execute("UPDATE tovari SET min_zapas=? WHERE kod=?", (int(novoe), kod))
    else:
        print("❌ Ошибка выбора")
        return

    conn.commit()
    print("✅ Изменения сохранены")


def spisok():
    print("\n[Весь склад]")
    c.execute("SELECT * FROM tovari")
    all_tov = c.fetchall()

    if not all_tov:
        print("😢 Склад пуст")
        return

    for t in all_tov:
        status = "⚠️ МАЛО!" if t[4] < t[5] else "✅"
        print(f"{t[0]}. {t[1]} ({t[2]}): {t[4]} шт. по {t[3]} руб. {status}")


def test_dannie():
    test = [
        (1, 'Samsung', 'Телефон', 500.0, 10, 5),
        (2, 'Apple', 'Планшет', 700.0, 3, 4),
        (3, 'Xiaomi', 'Наушники', 50.0, 20, 15),
        (4, 'Bosch', 'Холодильник', 899.99, 15, 3),
        (5, 'LG', 'Телевизор', 799.99, 25, 5),
        (6, 'Philips', 'Кофеварка', 129.99, 40, 8),
        (7, 'Sony', 'Игровая консоль', 499.99, 18, 4),
        (8, 'Canon', 'Фотоаппарат', 699.99, 22, 6),
        (9, 'Dyson', 'Пылесос', 399.99, 35, 7),
        (10, 'Braun', 'Блендер', 89.99, 60, 12)
    ]

    c.executemany("INSERT OR IGNORE INTO tovari VALUES (?,?,?,?,?,?)", test)
    conn.commit()
    print("✅ Тестовые данные добавлены")


# Главное меню
while True:
    print("\n" + "=" * 30)
    print("  УЧЕТ ТОВАРОВ НА СКЛАДЕ")
    print("=" * 30)
    print("1. Добавить товар")
    print("2. Найти товар")
    print("3. Удалить товар")
    print("4. Изменить товар")
    print("5. Весь склад")
    print("6. Тестовые данные")
    print("0. Выход")
    print("-" * 30)

    v = input("Выберите действие: ")

    if v == '1':
        dobavit()
    elif v == '2':
        poisk()
    elif v == '3':
        udalit()
    elif v == '4':
        redakt()
    elif v == '5':
        spisok()
    elif v == '6':
        test_dannie()
    elif v == '0':
        print("Выход...")
        break
    else:
        print("❌ Неверный выбор")

conn.close()