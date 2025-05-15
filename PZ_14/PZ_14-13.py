#В строках исходного текстового файла (dates1.txt) все даты представить в виде
#подстроки. Поместить в новый текстовый файл все даты февраля в формате
#ДД/ММ/ГГГГ.
import re
def extract_feb_dates(input_file, output_file):
    #Паттерны для разных форматов дат февраля
    patterns = [
        (r'\b(\d{4})-02-(\d{2})\b', lambda m: f"{m[2]}/02/{m[1]}"),  #ГГГГ-02-ДД
        (r'\b(\d{2})\.02\.(\d{4})\b', lambda m: f"{m[1]}/02/{m[2]}"),  #ДД.02.ГГГГ
        (r'\b(\d{2})/02/(\d{4})\b', lambda m: f"{m[1]}/02/{m[2]}"),  #ДД/02/ГГГГ
        (r'\bFebruary (\d{1,2}), (\d{4})\b', lambda m: f"{m[1].zfill(2)}/02/{m[2]}")  #February Д, ГГГГ
    ]
    feb_dates = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            for pattern, converter in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Преобразование в нужный формат и добавление в список
                    feb_dates.append(converter(match))
    #Запись результатов в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(feb_dates))
#Использование
extract_feb_dates('dates1.txt', 'feb_dates.txt')