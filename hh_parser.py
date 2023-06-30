import requests
from terminaltables import AsciiTable
from super_job import get_table_for_print, print_terminal_table


def predict_rub_salary(vacancy):
    if vacancy['salary']:
        currency = vacancy['salary']['currency']
        from_salary = vacancy['salary']['from']
        to_salary = vacancy['salary']['to']

        if currency == "RUR":
            if from_salary and to_salary:
                return int((from_salary + to_salary) // 2)
            
            if from_salary and not(to_salary):
                return int(from_salary * 1.2)
            
            if not(from_salary) and to_salary:
                return int(to_salary * 0.8) 
    return None


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
        
        for item in response['items']:
            avg_salary = predict_rub_salary(item)
            if avg_salary:
                salary_pool.append(avg_salary)
    return salary_pool


def get_language_info_hh(response, salary_pool):
    information_about_one_language = {}
    information_about_one_language['vacancies_found'] = response['found']
    
    information_about_one_language['vacancies_processed'] = len(salary_pool)
    if len(salary_pool):
        information_about_one_language['average_salary'] = int(sum(salary_pool) / len(salary_pool))
    else:
        information_about_one_language['average_salary'] = 0
    return information_about_one_language
    

def launching_hh_collection():
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages_info = {}
    for lang in languages:
        params = {
                "text": f"Программист {lang}",
                "area": 1,
                "per_page": 100,
            }
        response = get_response_hh(params)

        number_pages = response['found'] / 100
        if number_pages > 20:
            number_pages = 20
        if number_pages % 10:
            number_pages = int(number_pages) + 1
        if number_pages == 0:
            continue

        salary_pool = get_salary_pool_hh(params, number_pages)
        all_languages_info[lang] = get_language_info_hh(response, salary_pool)

    table = get_table_for_print(all_languages_info)
    print_terminal_table(table, "HeadHunter Moscow")

