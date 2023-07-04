from terminaltables import AsciiTable


def get_averaging(from_salary, to_salary):
    if from_salary and to_salary:
        return int((from_salary + to_salary) // 2)
            
    if from_salary and not to_salary:
        return int(from_salary * 1.2)
            
    if not from_salary and to_salary:
        return int(to_salary * 0.8) 
    
    return None


def get_language_synopsis(vacancy_rate, salary_pool):
    one_language_synopsis = {
        'vacancies_found': vacancy_rate,
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }
    
    if len(salary_pool):
        one_language_synopsis['average_salary'] = int(sum(salary_pool) / len(salary_pool))
        
    return one_language_synopsis


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
