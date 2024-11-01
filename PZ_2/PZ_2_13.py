# Дано двузначное число. Вывести число, полученное при
# перестановке цифр исходного числа.
# Ввод двузначного числа
while True:
    try:
        number = int(input("Введите двузначное число:"))
        if len(number) == 2 and number.isdigit():
            str_number = str(number)
            swapped_number = str_number[1] + str_number[0]
            print(swapped_number)
        break
    except ValueError:
        print("Введите двузначное число!")    
