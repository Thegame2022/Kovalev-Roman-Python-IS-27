# Дан номер года (положительное целое число). Определить количество дней в этом
# году, учитывая, что обычный год насчитывает 365 дней, а високосный — 366 дней.
# Високосным считается год, делящийся на 4, за исключением тех годов, которые
# делятся на 100 и не делятся на 400 (например, годы 300, 1300 и 1900 не являются
# високосными, а 1200 и 2000 — являются).
n = int(input())
if n % 4 != 0:
    print('365')
elif n % 100 != 0:
    print('366')
elif n % 400 != 0:
    print('365')
else:
    print('366')
