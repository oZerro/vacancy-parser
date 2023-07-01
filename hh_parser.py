import requests
from terminaltables import AsciiTable
from general_functions import get_table_for_print, averaging



def predict_rub_salary_hh(vacancy):
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


def get_salary_pool_hh(params, number_pages, salary_pool):
    if number_pages:
        for page in range(1, number_pages):
            params['page'] = page
            response = get_response_hh(params)
            vacancies = response['items']

            for vacancy in vacancies:
                avg_salary = predict_rub_salary_hh(vacancy)
                if avg_salary:
                    salary_pool.append(avg_salary)
    return salary_pool


def get_one_language_info_hh(response, salary_pool):
    one_language = {
        'vacancies_found': response['found'],
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }

    if len(salary_pool):
        one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))

    return one_language
    

def launching_hh_collection(languages, area_id, number_jobs_on_page):
    all_languages = {}
    for lang in languages:
        salary_pool = []
        params = {
                "text": f"Программист {lang}",
                "area": area_id,
                "per_page": number_jobs_on_page,
            }
        response = get_response_hh(params)
        vacancies = response['items']

        for vacancy in vacancies:
            avg_salary = predict_rub_salary_hh(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)

        number_pages = response['pages']

        salary_pool = get_salary_pool_hh(params, number_pages, salary_pool)
        all_languages[lang] = get_one_language_info_hh(response, salary_pool)

    return get_table_for_print(all_languages, "HeadHunter Moscow")


def main():
    mosсow_id = 1
    number_jobs_on_page = 100
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    print(launching_hh_collection(languages, mosсow_id, number_jobs_on_page))


