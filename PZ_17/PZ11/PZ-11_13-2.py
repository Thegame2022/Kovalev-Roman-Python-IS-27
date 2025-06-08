#2. Из предложенного текстового файла (text18-13.txt) вывести на экран его содержимое,
#количество символов в тексте. Сформировать новый файл, в который поместить текст в
#стихотворной форме предварительно вставив после строки N (N – задается пользователем)
#произвольную фразу
#Чтение содержимого файла и вывод
with open('text18-13.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    lines = content.split('\n')
print("Содержимое файла:")
print(content)
print("\nКоличество символов в тексте:", len(content))
#Ввод данных пользователем
try:
    n = int(input("\nВведите номер строки N (начиная с 1): ")) - 1
    if n < 0:
        n = 0
except ValueError:
    print("Ошибка: введено не число.")
    exit()
fraza = input("Введите фразу для вставки: ")
#Вставка фразы после указанной строки
if n >= len(lines):
    lines.append(fraza)
else:
    lines.insert(n + 1, fraza)
#Создание нового файла с измененным текстом
new_file = '\n'.join(lines)
with open('new_file.txt', 'w', encoding='utf-8') as file:
    file.write(new_file)
print("\nФраза успешно добавлена. Результат сохранен в файл 'new_file.txt'.")