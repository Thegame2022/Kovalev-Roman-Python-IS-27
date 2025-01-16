#Дана строка. Подсчитать количество содержащихся в ней цифр.

counter = 0
while True:
    try:
        s = input("Ввод: ") #Ввод пользователем
        if not s.isdigit(): #Проверка на ввод цифр
            raise ValueError("Введите только цифры!")
        break
    except ValueError as e:
        print(e)
for i in range(10): #Подсчитываем цифры от 0 до 9
    counter += s.count(str(i))
print(f"Количество цифр: {counter}") #Результат