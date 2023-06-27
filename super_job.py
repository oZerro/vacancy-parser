import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv


load_dotenv()
token = os.environ['SUPERJOB_TOKEN']

def predict_rub_salary_for_superJob(vacancy):
    from_salary = vacancy['payment_from']
    to_salary = vacancy['payment_to']
  
    if from_salary and to_salary:
        return int((from_salary + to_salary) // 2)
            
    if from_salary and not(to_salary):
        return int(from_salary * 1.2)
            
    if not(from_salary) and to_salary:
        return int(to_salary * 0.8) 
    return None


def get_response_superjob(params, token):
    url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Api-App-Id": token
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_salary_pool(params, number_pages):
    salary_pool = []
    for page in range(int(number_pages)):
        params['page'] = page
        response = get_response_superjob(params, token)

        for vacancy in response['objects']:
            avg_salary = predict_rub_salary_for_superJob(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)
    return salary_pool


def get_table_for_print(languages_info):
    header_table = [
            ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
        ]
    for lang in languages_info:
        one_language_info = []
        one_language_info.append(lang)
        for info in languages_info[lang]:
            one_language_info.append(languages_info[lang][info])
        header_table.append(one_language_info)
    
    return header_table


def print_terminal_table(table, title):
    table_instance = AsciiTable(table, title)
    print(table_instance.table)


def get_language_info_superjob(response, salary_pool):
    one_lenguage_info = {}
    one_lenguage_info['vacancies_found'] = response['total']
            
    one_lenguage_info['vacancies_processed'] = len(salary_pool)
    if len(salary_pool):
        one_lenguage_info['average_salary'] = int(sum(salary_pool) / len(salary_pool))
    else:
        one_lenguage_info['average_salary'] = 0
    return one_lenguage_info


def main_superjob():
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN']
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    languages_info = {}
    for lang in languages:
        params = {
                "keyword": f"Программист {lang}",
                "town": 4,
            }
        response = get_response_superjob(params, token)
        number_pages = response['total'] / 20

        if number_pages > 25:
            number_pages = 25
        elif number_pages % 10:
            number_pages = int(number_pages) + 1
        elif number_pages == 0:
            continue

        salary_pool = get_salary_pool(params, number_pages)
        languages_info[lang] = get_language_info_superjob(response, salary_pool)

    table = get_table_for_print(languages_info)
    print_terminal_table(table, "SuperJob Moscow")


if __name__ == "__main__":
    main_superjob()

