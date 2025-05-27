#Приложение ТОВАРНЫЙ ЗАПАС для автоматизированного учета товарных
#запасов на складе. БД должна содержать таблицу Товары со следующей структурой
#записи: Код товара, Торговая марка, Тип, Цена, Количество на складе, Минимальный
#запас.

import sqlite3
conn = sqlite3.connect('sklad.db')
c = conn.cursor()
#Создание таблицы если нет
c.execute('''CREATE TABLE IF NOT EXISTS tovari
             (kod INTEGER PRIMARY KEY, 
              marka TEXT, 
              tip TEXT, 
              cena REAL, 
              kolvo INTEGER, 
              min_zapas INTEGER)''')
conn.commit()
def dobavit():
    print("\nДобавить товар:")
    kod = int(input("Код: "))
    marka = input("Марка: ")
    tip = input("Тип: ")
    cena = float(input("Цена: "))
    kolvo = int(input("Количество: "))
    min_zapas = int(input("Мин. запас: "))

    c.execute("INSERT INTO tovari VALUES (?,?,?,?,?,?)",
              (kod, marka, tip, cena, kolvo, min_zapas))
    conn.commit()
    print("Добавлено!\n")
def poisk():
    print("\nПоиск:")
    print("1-По марке 2-По типу 3-Мало на складе")
    vibor = input("Выбор: ")

    if vibor == '1':
        m = input("Марка: ")
        c.execute("SELECT * FROM tovari WHERE marka LIKE ?", ('%' + m + '%',))
    elif vibor == '2':
        t = input("Тип: ")
        c.execute("SELECT * FROM tovari WHERE tip LIKE ?", ('%' + t + '%',))
    elif vibor == '3':
        c.execute("SELECT * FROM tovari WHERE kolvo < min_zapas")
    else:
        print("Неправильно!")
        return
    result = c.fetchall()
    if not result:
        print("Ничего не найдено")
    else:
        print("\nКод | Марка | Тип | Цена | Кол-во | Мин")
        for row in result:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
def udalit():
    print("\nУдалить:")
    print("1-По коду 2-По марке 3-Нет в наличии")
    vibor = input("Выбор: ")

    if vibor == '1':
        kod = int(input("Код: "))
        c.execute("DELETE FROM tovari WHERE kod=?", (kod,))
    elif vibor == '2':
        m = input("Марка: ")
        c.execute("DELETE FROM tovari WHERE marka=?", (m,))
    elif vibor == '3':
        c.execute("DELETE FROM tovari WHERE kolvo=0")
    else:
        print("Неправильно!")
        return
    conn.commit()
    print(f"Удалено: {c.rowcount}")
def redakt():
    print("\nРедактировать:")
    print("1-Цену 2-Количество 3-Мин.запас")
    vibor = input("Выбор: ")
    if vibor == '1':
        kod = int(input("Код товара: "))
        nova_cena = float(input("Новая цена: "))
        c.execute("UPDATE tovari SET cena=? WHERE kod=?", (nova_cena, kod))
    elif vibor == '2':
        kod = int(input("Код товара: "))
        novo_kol = int(input("Новое кол-во: "))
        c.execute("UPDATE tovari SET kolvo=? WHERE kod=?", (novo_kol, kod))
    elif vibor == '3':
        m = input("Марка: ")
        nov_min = int(input("Новый мин.запас: "))
        c.execute("UPDATE tovari SET min_zapas=? WHERE marka=?", (nov_min, m))
    else:
        print("Ошибка!")
        return
    conn.commit()
    print("Изменено!")
def spisok():
    c.execute("SELECT * FROM tovari")
    all_tov = c.fetchall()
    if not all_tov:
        print("Склад пуст!")
    else:
        print("\nВсе товары:")
        print("Код | Марка | Тип | Цена | Кол-во | Мин")
        for t in all_tov:
            print(f"{t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]}")
def test_dannie():
    test = [
        (111, 'Samsung', 'Телефон', 500.0, 10, 5),
        (222, 'Apple', 'Планшет', 700.0, 3, 4),
        (333, 'Xiaomi', 'Наушники', 50.0, 20, 15),
        (1004, 'Bosch', 'Холодильник', 899.99, 15, 3),
        (1005, 'LG', 'Телевизор', 799.99, 25, 5),
        (1006, 'Philips', 'Кофеварка', 129.99, 40, 8),
        (1007, 'Sony', 'Игровая консоль', 499.99, 18, 4),
        (1008, 'Canon', 'Фотоаппарат', 699.99, 22, 6),
        (1009, 'Dyson', 'Пылесос', 399.99, 35, 7),
        (1010, 'Braun', 'Блендер', 89.99, 60, 12)
    ]
    c.executemany("INSERT OR IGNORE INTO tovari VALUES (?,?,?,?,?,?)", test)
    conn.commit()
    print("Тестовые данные добавлены!")
while True:
    print("\nСКЛАД")
    print("1-Добавить")
    print("2-Поиск")
    print("3-Удалить")
    print("4-Изменить")
    print("5-Список")
    print("6-Тест данные")
    print("0-Выход")
    v = input("Ваш выбор: ")
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
        print("Не понял!")
conn.close()