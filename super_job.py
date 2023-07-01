import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv
from general_functions import averaging, get_table_for_print


def predict_rub_salary_for_sj(vacancy):
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


def get_salary_pool_sj(token, params, number_pages, salary_pool):
    if number_pages:
        for page in range(1, int(number_pages)):
            params['page'] = page
            response = get_response_sj(params, token)

            for vacancy in response['objects']:
                avg_salary = predict_rub_salary_for_sj(vacancy)
                if avg_salary:
                    salary_pool.append(avg_salary)
    return salary_pool
    

def get_one_language_info_sj(response, salary_pool):
    information_about_one_language = {
        'vacancies_found': response['total'],
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }
    
    if len(salary_pool):
        information_about_one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))
        
    return information_about_one_language


def print_superjob_vacancies(token, languages, town_id):
    all_languages_info= {}
    for lang in languages:
        salary_pool = []
        params = {
                "keyword": f"Программист {lang}",
                "town": town_id,
            }
        response = get_response_sj(params, token)
        for vacancy in response['objects']:
            avg_salary = predict_rub_salary_for_sj(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)

        number_pages = response['total'] / 20

        if number_pages > 25:
            number_pages = 25
        elif number_pages % 10:
            number_pages = int(number_pages) + 1
        elif number_pages == 0:
            continue

        salary_pool = get_salary_pool_sj(token, params, number_pages, salary_pool)
        all_languages_info[lang] = get_one_language_info_sj(response, salary_pool)

    return get_table_for_print(all_languages_info, "SuperJob Moscow")
    


def main():
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN']
    mosсow_id = 4
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    print(print_superjob_vacancies(token, languages, mosсow_id))



