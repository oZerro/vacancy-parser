import requests
import os
from dotenv import load_dotenv
from general_functions import get_averaging, get_table_for_print


def predict_rub_salary_for_sj(vacancy):
    from_salary = vacancy['payment_from']
    to_salary = vacancy['payment_to']
    return get_averaging(from_salary, to_salary)
    


def get_response_sj(params, token):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Api-App-Id': token
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
    

def get_language_synopsis_sj(vacancy_rate, salary_pool):
    one_language_synopsis = {
        'vacancies_found': vacancy_rate,
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }
    
    if len(salary_pool):
        one_language_synopsis['average_salary'] = int(sum(salary_pool) / len(salary_pool))
        
    return one_language_synopsis


def add_salary_to_calculate(salary_pool, vacancies):
    for vacancy in vacancies:
        avg_salary = predict_rub_salary_for_sj(vacancy)
        if avg_salary:
            salary_pool.append(avg_salary)
    return salary_pool


def main():
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN']
    mosсow_id = 4
    jobs_per_page = 20
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages_synopsis = {}
    
    for lang in languages:
        salary_pool = []
        params = {
                'keyword': f'Программист {lang}',
                'town': mosсow_id,
            }
        response = get_response_sj(params, token)
        vacancies = response['objects']
        salary_pool += add_salary_to_calculate(salary_pool, vacancies)

        number_pages = response['total'] / jobs_per_page

        for page in range(1, int(number_pages)):
            params['page'] = page
            response = get_response_sj(params, token)
            vacancies = response['objects']
            salary_pool += add_salary_to_calculate(salary_pool, vacancies)

        vacancy_rate = response['total']
        all_languages_synopsis[lang] = get_language_synopsis_sj(vacancy_rate, salary_pool)
        table_for_print = get_table_for_print(all_languages_synopsis, 'SuperJob Moscow')

    print(table_for_print)
    



