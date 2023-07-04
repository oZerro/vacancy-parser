import requests
from general_functions import get_table_for_print, get_averaging



def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        currency = vacancy['salary']['currency']
        from_salary = vacancy['salary']['from']
        to_salary = vacancy['salary']['to']

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


def get_language_synopsis_hh(response, salary_pool):
    one_language = {
        'vacancies_found': response['found'],
        'vacancies_processed': len(salary_pool),
        'average_salary': 0
    }

    if len(salary_pool):
        one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))

    return one_language
    

def main():
    mosсow_id = 1
    number_jobs_on_page = 100
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages = {}
    for lang in languages:
        salary_pool = []
        params = {
                'text': f'Программист {lang}',
                'area': mosсow_id,
                'per_page': number_jobs_on_page,
            }
        response = get_response_hh(params)
        vacancies = response['items']

        for vacancy in vacancies:
            avg_salary = predict_rub_salary_hh(vacancy)
            if avg_salary:
                salary_pool.append(avg_salary)

        number_pages = response['pages']

        for page in range(1, number_pages):
            params['page'] = page
            response = get_response_hh(params)
            vacancies = response['items']

            for vacancy in vacancies:
                avg_salary = predict_rub_salary_hh(vacancy)
                if avg_salary:
                    salary_pool.append(avg_salary)

        all_languages[lang] = get_language_synopsis_hh(response, salary_pool)
        table_for_print = get_table_for_print(all_languages, 'HeadHunter Moscow')

    print(table_for_print)



