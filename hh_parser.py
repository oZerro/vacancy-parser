import requests
from terminaltables import AsciiTable
from super_job import get_table_for_print, averaging



def predict_rub_salary(vacancy):
    if vacancy['salary']:
        currency = vacancy['salary']['currency']
        from_salary = vacancy['salary']['from']
        to_salary = vacancy['salary']['to']

        if currency == "RUR":
            return averaging(from_salary, to_salary)


def get_response_hh(params):
    url = "https://api.hh.ru/vacancies"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_salary_pool_hh(params, number_pages):
    salary_pool = []
    for page in range(number_pages):
        params['page'] = page
        response = get_response_hh(params)
        vacancies = response['items']
        
        for vacancy in vacancies:
            avg_salary = predict_rub_salary(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)
    return salary_pool


def get_one_language_info_hh(response, salary_pool):
    information_about_one_language = {
        'vacancies_found': response['found'],
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }

    if len(salary_pool):
        information_about_one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))

    return information_about_one_language
    

def launching_hh_collection():
    mosсow_id = 1
    number_jobs_on_page = 100
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages_info = {}
    for lang in languages:
        params = {
                "text": f"Программист {lang}",
                "area": mosсow_id,
                "per_page": number_jobs_on_page,
            }
        response = get_response_hh(params)

        number_pages = response['pages']

        salary_pool = get_salary_pool_hh(params, number_pages)
        all_languages_info[lang] = get_one_language_info_hh(response, salary_pool)

    table = get_table_for_print(all_languages_info)
    table_instance = AsciiTable(table, title="HeadHunter Moscow")
    print(table_instance.table)


