import sqlite3
from tabulate import tabulate

# Создаем соединение с базой данных (файл будет создан автоматически)
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

# Создаем таблицу товаров, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_code INTEGER PRIMARY KEY,
    brand TEXT NOT NULL,
    product_type TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    min_stock INTEGER NOT NULL
)
''')
conn.commit()


def add_sample_data():
    """Добавление 10 тестовых записей в базу данных"""
    sample_data = [
        (1001, 'Samsung', 'Смартфон', 599.99, 50, 10),
        (1002, 'Apple', 'Ноутбук', 1299.99, 30, 5),
        (1003, 'Xiaomi', 'Наушники', 49.99, 120, 20),
        (1004, 'Bosch', 'Холодильник', 899.99, 15, 3),
        (1005, 'LG', 'Телевизор', 799.99, 25, 5),
        (1006, 'Philips', 'Кофеварка', 129.99, 40, 8),
        (1007, 'Sony', 'Игровая консоль', 499.99, 18, 4),
        (1008, 'Canon', 'Фотоаппарат', 699.99, 22, 6),
        (1009, 'Dyson', 'Пылесос', 399.99, 35, 7),
        (1010, 'Braun', 'Блендер', 89.99, 60, 12)
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO products (product_code, brand, product_type, price, quantity, min_stock)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_data)
    conn.commit()
    print("Добавлено 10 тестовых записей.")


def add_product():
    """Добавление нового товара в базу данных"""
    print("\nДобавление нового товара:")
    product_code = int(input("Код товара: "))
    brand = input("Торговая марка: ")
    product_type = input("Тип товара: ")
    price = float(input("Цена: "))
    quantity = int(input("Количество на складе: "))
    min_stock = int(input("Минимальный запас: "))

    cursor.execute('''
    INSERT INTO products (product_code, brand, product_type, price, quantity, min_stock)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_code, brand, product_type, price, quantity, min_stock))
    conn.commit()
    print("Товар успешно добавлен!")


def search_products():
    """Поиск товаров по различным критериям"""
    print("\nВарианты поиска:")
    print("1. По торговой марке")
    print("2. По типу товара")
    print("3. Товары с количеством ниже минимального запаса")
    choice = input("Выберите вариант поиска (1-3): ")

    if choice == '1':
        brand = input("Введите торговую марку для поиска: ")
        cursor.execute('SELECT * FROM products WHERE brand LIKE ?', (f'%{brand}%',))
    elif choice == '2':
        product_type = input("Введите тип товара для поиска: ")
        cursor.execute('SELECT * FROM products WHERE product_type LIKE ?', (f'%{product_type}%',))
    elif choice == '3':
        cursor.execute('SELECT * FROM products WHERE quantity < min_stock')
    else:
        print("Неверный выбор.")
        return

    results = cursor.fetchall()
    if results:
        print("\nРезультаты поиска:")
        print(tabulate(results, headers=["Код", "Марка", "Тип", "Цена", "Кол-во", "Мин.запас"], floatfmt=".2f"))
    else:
        print("Товары не найдены.")


def delete_products():
    """Удаление товаров по различным критериям"""
    print("\nВарианты удаления:")
    print("1. По коду товара")
    print("2. По торговой марке")
    print("3. Товары с нулевым количеством")
    choice = input("Выберите вариант удаления (1-3): ")

    if choice == '1':
        code = int(input("Введите код товара для удаления: "))
        cursor.execute('DELETE FROM products WHERE product_code = ?', (code,))
    elif choice == '2':
        brand = input("Введите торговую марку для удаления: ")
        cursor.execute('DELETE FROM products WHERE brand LIKE ?', (f'%{brand}%',))
    elif choice == '3':
        cursor.execute('DELETE FROM products WHERE quantity = 0')
    else:
        print("Неверный выбор.")
        return

    conn.commit()
    print(f"Удалено {cursor.rowcount} записей.")
def edit_products():
    """Редактирование товаров"""
    print("\nВарианты редактирования:")
    print("1. Изменить цену товара по коду")
    print("2. Обновить количество на складе по коду")
    print("3. Изменить минимальный запас для всех товаров марки")
    choice = input("Выберите вариант редактирования (1-3): ")

    if choice == '1':
        code = int(input("Введите код товара: "))
        new_price = float(input("Введите новую цену: "))
        cursor.execute('UPDATE products SET price = ? WHERE product_code = ?', (new_price, code))
    elif choice == '2':
        code = int(input("Введите код товара: "))
        new_quantity = int(input("Введите новое количество: "))
        cursor.execute('UPDATE products SET quantity = ? WHERE product_code = ?', (new_quantity, code))
    elif choice == '3':
        brand = input("Введите торговую марку: ")
        new_min_stock = int(input("Введите новый минимальный запас: "))
        cursor.execute('UPDATE products SET min_stock = ? WHERE brand LIKE ?', (new_min_stock, f'%{brand}%'))
    else:
        print("Неверный выбор.")
        return

    conn.commit()
    print(f"Обновлено {cursor.rowcount} записей.")


def show_all_products():
    """Отображение всех товаров в базе данных"""
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    if products:
        print("\nВсе товары на складе:")
        print(tabulate(products, headers=["Код", "Марка", "Тип", "Цена", "Кол-во", "Мин.запас"], floatfmt=".2f"))
    else:
        print("В базе данных нет товаров.")


def main_menu():
    """Главное меню программы"""
    while True:
        print("\n=== Управление товарными запасами ===")
        print("1. Добавить товар")
        print("2. Поиск товаров")
        print("3. Удалить товары")
        print("4. Редактировать товары")
        print("5. Показать все товары")
        print("6. Добавить тестовые данные (10 записей)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            search_products()
        elif choice == '3':
            delete_products()
        elif choice == '4':
            edit_products()
        elif choice == '5':
            show_all_products()
        elif choice == '6':
            add_sample_data()
        elif choice == '0':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()
    conn.close()