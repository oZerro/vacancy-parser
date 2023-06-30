import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv



def averaging(from_salary, to_salary):
    if from_salary and to_salary:
        return int((from_salary + to_salary) // 2)
            
    if from_salary and not(to_salary):
        return int(from_salary * 1.2)
            
    if not(from_salary) and to_salary:
        return int(to_salary * 0.8) 
    
    return None


def predict_rub_salary_for_superJob(vacancy):
    from_salary = vacancy['payment_from']
    to_salary = vacancy['payment_to']
    return averaging(from_salary, to_salary)
    


def get_response_sj(params, token):
    url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Api-App-Id": token
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_salary_pool(token, params, number_pages):
    salary_pool = []
    for page in range(int(number_pages)):
        params['page'] = page
        response = get_response_sj(params, token)

        for vacancy in response['objects']:
            avg_salary = predict_rub_salary_for_superJob(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)
    return salary_pool


def get_table_for_print(all_languages_info):
    header_table = [
            ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
        ]
    for lang in all_languages_info:
        information_about_one_language = []
        information_about_one_language.append(lang)
        for info in all_languages_info[lang]:
            information_about_one_language.append(all_languages_info[lang][info])
        header_table.append(information_about_one_language)
    
    return header_table


def print_terminal_table(table, title):
    table_instance = AsciiTable(table, title)
    print(table_instance.table)


def get_one_language_info_sj(response, salary_pool):
    information_about_one_language = {
        'vacancies_found': response['total'],
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }
    
    if len(salary_pool):
        information_about_one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))
        
    return information_about_one_language


def print_superjob_vacancies(token):
    mosсow_id = 4
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages_info= {}
    for lang in languages:
        params = {
                "keyword": f"Программист {lang}",
                "town": mosсow_id,
            }
        response = get_response_sj(params, token)
        number_pages = response['total'] / 20

        if number_pages > 25:
            number_pages = 25
        elif number_pages % 10:
            number_pages = int(number_pages) + 1
        elif number_pages == 0:
            continue

        salary_pool = get_salary_pool(token, params, number_pages)
        all_languages_info[lang] = get_one_language_info_sj(response, salary_pool)

    table = get_table_for_print(all_languages_info)
    print_terminal_table(table, "SuperJob Moscow")


def launching_sj_collection():
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN']
    print_superjob_vacancies(token)



