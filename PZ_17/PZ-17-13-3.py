import os
import shutil


def main():
    # 1. Перейти в каталог PZ11 и вывести список файлов (без подкаталогов)
    print("\n1. Список файлов в каталоге PZ11:")
    try:
        os.chdir("PZ11")
        for item in os.listdir():
            if os.path.isfile(item):
                print(item)
    except FileNotFoundError:
        print("Каталог PZ11 не найден")
        return

    # 2. Создание структуры папок и файлов
    print("\n2. Создание структуры папок и файлов:")
    # Возвращаемся в корень проекта
    os.chdir("..")

    # Создаем папки
    os.makedirs("test/test1", exist_ok=True)

    # Копируем файлы из PZ6 (берем первые 2 файла, если они есть)
    pz6_files = []
    if os.path.exists("PZ6"):
        pz6_files = [f for f in os.listdir("PZ6") if os.path.isfile(os.path.join("PZ6", f))]

    if len(pz6_files) >= 2:
        for file in pz6_files[:2]:
            src = os.path.join("PZ6", file)
            dst = os.path.join("test", file)
            shutil.copy2(src, dst)
            print(f"Скопирован файл {file} в папку test")
    else:
        print("В папке PZ6 недостаточно файлов (нужно минимум 2)")
        # Создаем тестовые файлы, если их нет
        with open(os.path.join("test", "file1.txt"), 'w') as f:
            f.write("Тестовый файл 1")
        with open(os.path.join("test", "file2.txt"), 'w') as f:
            f.write("Тестовый файл 2")

    # Копируем файл из PZ7 (если есть)
    pz7_file = None
    if os.path.exists("PZ7"):
        pz7_files = [f for f in os.listdir("PZ7") if os.path.isfile(os.path.join("PZ7", f))]
        if pz7_files:
            pz7_file = pz7_files[0]
            src = os.path.join("PZ7", pz7_file)
            dst = os.path.join("test", "test1", "test.txt")
            shutil.copy2(src, dst)
            print(f"Скопирован и переименован файл {pz7_file} в test/test1/test.txt")
        else:
            print("В папке PZ7 нет файлов")
            # Создаем тестовый файл, если его нет
            with open(os.path.join("test", "test1", "test.txt"), 'w') as f:
                f.write("Тестовый файл")
    else:
        print("Папка PZ7 не найдена")
        # Создаем тестовый файл, если папки нет
        with open(os.path.join("test", "test1", "test.txt"), 'w') as f:
            f.write("Тестовый файл")

    # Выводим информацию о размере файлов в папке test
    print("\nИнформация о размере файлов в папке test:")
    total_size = 0
    for root, dirs, files in os.walk("test"):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            total_size += size
            print(f"{file_path}: {size} байт")
    print(f"Общий размер: {total_size} байт")

    # 3. Найти файл с самым коротким именем в PZ11
    print("\n3. Поиск файла с самым коротким именем в PZ11:")
    try:
        os.chdir("PZ11")
        files = [f for f in os.listdir() if os.path.isfile(f)]
        if files:
            shortest_file = min(files, key=lambda x: len(os.path.splitext(os.path.basename(x))[0]))
            print(f"Файл с самым коротким именем: {os.path.basename(shortest_file)}")
        else:
            print("В каталоге нет файлов")
    except FileNotFoundError:
        print("Каталог PZ11 не найден")

    # 4. Запуск PDF файла
    print("\n4. Попытка запуска PDF файла:")
    pdf_files = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    if pdf_files:
        pdf_path = pdf_files[0]
        print(f"Запускаем файл: {pdf_path}")
        try:
            os.startfile(pdf_path)
        except Exception as e:
            print(f"Ошибка при запуске файла: {e}")
    else:
        print("PDF файлы не найдены")

    # 5. Удаление файла test.txt
    print("\n5. Удаление файла test.txt:")
    test_txt_path = os.path.join("..", "test", "test1", "test.txt")
    if os.path.exists(test_txt_path):
        try:
            os.remove(test_txt_path)
            print("Файл test.txt успешно удален")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
    else:
        print("Файл test.txt не найден")


if __name__ == "__main__":
    main()