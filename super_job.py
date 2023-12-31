import requests
from general_functions import (
        get_averaging,
        get_table_for_print, 
        get_language_synopsis
    )


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


def add_salary_to_calculate(vacancies):
    salary_pool = []
    for vacancy in vacancies:
        avg_salary = predict_rub_salary_for_sj(vacancy)
        if avg_salary:
            salary_pool.append(avg_salary)
    return salary_pool


def start_sj_parser(token, languages):
    mosсow_id = 4
    jobs_per_page = 20
    all_languages_synopsis = {}

    for lang in languages:
        salary_pool = []
        params = {
                'keyword': f'Программист {lang}',
                'town': mosсow_id,
            }
        response = get_response_sj(params, token)
        vacancies = response['objects']
        salary_pool.extend(add_salary_to_calculate(vacancies))

        number_pages = response['total'] / jobs_per_page

        for page in range(1, int(number_pages)):
            params['page'] = page
            response = get_response_sj(params, token)
            vacancies = response['objects']
            salary_pool.extend(add_salary_to_calculate(vacancies))

        vacancy_rate = response['total']
        all_languages_synopsis[lang] = get_language_synopsis(vacancy_rate, salary_pool)

    return all_languages_synopsis
    



