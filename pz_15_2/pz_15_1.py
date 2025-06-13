import sqlite3

# Подключение к базе
conn = sqlite3.connect('sklad.db')
c = conn.cursor()

# Создаем таблицу, если её нет
c.execute('''CREATE TABLE IF NOT EXISTS tovari ( kod INTEGER PRIMARY KEY, marka TEXT, tip TEXT, cena REAL, kolvo INTEGER, min_zapas INTEGER)''')
conn.commit()

def dobavit():
    print("\n[Добавить товар]")
    kod = int(input("Код: "))
    marka = input("Марка: ")
    tip = input("Тип: ")
    cena = float(input("Цена: "))
    kolvo = int(input("Количество: "))
    min_zapas = int(input("Минимальный запас: "))

    c.execute("INSERT INTO tovari VALUES (?,?,?,?,?,?)",
              (kod, marka, tip, cena, kolvo, min_zapas))
    conn.commit()
    print("Товар успешно добавлен.")

def poisk():
    print("\n[Поиск товара]")
    m = input("Марка (или Enter для пропуска): ")
    t = input("Тип (или Enter для пропуска): ")

    query = "SELECT * FROM tovari WHERE 1=1"
    params = []

    if m:
        query += " AND marka LIKE ?"
        params.append(f"%{m}%")
    if t:
        query += " AND tip LIKE ?"
        params.append(f"%{t}%")

    c.execute(query, params)
    result = c.fetchall()

    if not result:
        print("Товаров не найдено.")
    else:
        print("Результат поиска:")
        for row in result:
            print(f"{row[0]}: {row[1]} ({row[2]}), кол-во: {row[4]}, цена: {row[3]}₽")

def udalit():
    print("\n[Удалить товар]")
    kod = int(input("Введите код товара: "))

    c.execute("DELETE FROM tovari WHERE kod=?", (kod,))
    conn.commit()

    if c.rowcount > 0:
        print("Товар успешно удалён.")
    else:
        print("Такой товар не найден.")

def redakt():
    print("\n[Редактировать товар]")
    kod = int(input("Введите код товара: "))

    c.execute("SELECT * FROM tovari WHERE kod=?", (kod,))
    tovar = c.fetchone()

    if not tovar:
        print("Товар не найден.")
        return

    print(f"Текущие данные:\n"
          f"1. Марка: {tovar[1]}\n"
          f"2. Тип: {tovar[2]}\n"
          f"3. Цена: {tovar[3]}\n"
          f"4. Количество: {tovar[4]}\n"
          f"5. Минимальный запас: {tovar[5]}"
         )

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
        print("Ошибка выбора.")
        return

    conn.commit()
    print("Изменения сохранены.")

def spisok():
    print("\n[Весь склад]")
    c.execute("SELECT * FROM tovari")
    all_tov = c.fetchall()

    if not all_tov:
        print("Склад пуст.")
        return

    for t in all_tov:
        status = "Мало!" if t[4] < t[5] else ""
        print(f"{t[0]}. {t[1]} ({t[2]}): {t[4]} шт., цена: {t[3]}₽ {status}")

# Меню программы
while True:
    print("\n" + "="*30)
    print(" Управление складом")
    print("="*30)
    print("1. Добавить товар")
    print("2. Найти товар")
    print("3. Удалить товар")
    print("4. Редактировать товар")
    print("5. Показать весь склад")
    print("0. Завершить работу")
    print("-"*30)

    v = input("Ваш выбор: ").strip()

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
    elif v == '0':
        print("Завершение работы...")
        break
    else:
        print("Ошибка: неправильный выбор. Попробуйте ещё раз.")

conn.close()