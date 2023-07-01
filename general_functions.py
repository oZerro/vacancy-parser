from terminaltables import AsciiTable


def averaging(from_salary, to_salary):
    if from_salary and to_salary:
        return int((from_salary + to_salary) // 2)
            
    if from_salary and not(to_salary):
        return int(from_salary * 1.2)
            
    if not(from_salary) and to_salary:
        return int(to_salary * 0.8) 
    
    return None


def get_table_for_print(all_languages_info, title):
    table_header = [
            ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
        ]
    for lang in all_languages_info:
        information_about_one_language = []
        information_about_one_language.append(lang)
        for info in all_languages_info[lang]:
            information_about_one_language.append(all_languages_info[lang][info])
        table_header.append(information_about_one_language)
    
    table_instance = AsciiTable(table_header, title)
    return table_instance