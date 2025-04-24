#В строках исходного текстового файла (dates1.txt) все даты представить в виде
#подстроки. Поместить в новый текстовый файл все даты февраля в формате
#ДД/ММ/ГГГГ.
import re
from datetime import datetime
#Создание тестового файла (с кириллическим месяцем)
with open('dates1.txt', 'w', encoding='utf-8') as f:
    f.write("""События:
2024-02-15 - конференция
15.03.2023 - собрание
February 28, 2024 - дедлайн
25/12/2023 - праздник
14.02.2025 - день святого Валентина
Март 1, 2023 - начало весны  
""")
#Чтение файла и извлечение дат
with open('dates1.txt', encoding='utf-8') as f:
    content = f.read()
#Обновлённое регулярное выражение (учитывает кириллицу)
date_pattern = r'\b\d{2}[./-]\d{2}[./-]\d{4}\b|\b(?:[A-Za-z]+|[\u0400-\u04FF]+) \d{1,2}, \d{4}\b'
dates = re.findall(date_pattern, content)
#Функция обработки дат (только для английских месяцев)
def process_date(date_str):
    formats = (
        ('%Y-%m-%d', r'\d{4}-\d{2}-\d{2}'),
        ('%d.%m.%Y', r'\d{2}\.\d{2}\.\d{4}'),
        ('%B %d, %Y', r'[A-Za-z]+ \d{1,2}, \d{4}')
    )
    for fmt, pattern in formats:
        if re.fullmatch(pattern, date_str):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%d/%m/%Y') if dt.month == 2 else None
            except:
                pass
    return None
#Обработка дат и преобразование в список
feb_dates = list(filter(None, map(process_date, dates)))
#Запись результатов
with open('feb_dates.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(feb_dates))
print(f'Найдено дат в феврале: {len(feb_dates)}')