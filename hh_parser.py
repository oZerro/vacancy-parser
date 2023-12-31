import requests
from general_functions import (
        get_table_for_print,
        get_averaging, 
        get_language_synopsis
    )



def predict_rub_salary_hh(vacancy):
    currency = vacancy['currency']

    if currency != "RUR":
        return
    
    from_salary = vacancy['from']
    to_salary = vacancy['to']

    if currency == "RUR":
        return get_averaging(from_salary, to_salary)


def get_response_hh(params):
    url = 'https://api.hh.ru/vacancies'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def add_salary_to_calculate(vacancies):
    sal_pool = []
    for vacancy in vacancies:
        if not vacancy['salary']:
            continue
        avg_salary = predict_rub_salary_hh(vacancy['salary'])
        if avg_salary:
            sal_pool.append(avg_salary)
    return sal_pool


def start_hh_parser(languages):
    mosсow_id = 1
    number_jobs_on_page = 100
    all_languages_synopsis = {}
    
    for lang in languages:
        salary_pool = []
        params = {
                'text': f'Программист {lang}',
                'area': mosсow_id,
                'per_page': number_jobs_on_page,
            }
        response = get_response_hh(params)
        vacancies = response['items']
        salary_pool.extend(add_salary_to_calculate(vacancies))
        number_pages = response['pages']

        for page in range(1, number_pages):
            params['page'] = page
            response = get_response_hh(params)
            vacancies = response['items']
            salary_pool.extend(add_salary_to_calculate(vacancies))

        vacancy_rate = response['found']
        all_languages_synopsis[lang] = get_language_synopsis(vacancy_rate, salary_pool)

    return all_languages_synopsis



