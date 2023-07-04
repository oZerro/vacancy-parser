from terminaltables import AsciiTable


def get_averaging(from_salary, to_salary):
    if from_salary and to_salary:
        return int((from_salary + to_salary) // 2)
            
    if from_salary and not to_salary:
        return int(from_salary * 1.2)
            
    if not from_salary and to_salary:
        return int(to_salary * 0.8) 
    
    return None


def get_table_for_print(all_languages_synopsis, title):
    table_header = [
            ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
        ]
    for lang in all_languages_synopsis:
        one_language_synopsis = []
        one_language_synopsis.append(lang)
        for info in all_languages_synopsis[lang]:
            one_language_synopsis.append(all_languages_synopsis[lang][info])
        table_header.append(one_language_synopsis)
    
    table_instance = AsciiTable(table_header, title)
    return table_instance.table
