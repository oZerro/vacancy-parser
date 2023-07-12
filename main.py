from hh_parser import start_hh_parser
from super_job import start_sj_parser
import os
from dotenv import load_dotenv
from general_functions import get_table_for_print


if __name__ == "__main__": 
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN'] 
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']
    all_languages_synopsis_sj = start_sj_parser(token, languages)
    table_for_print_sj = get_table_for_print(all_languages_synopsis_sj, 'SuperJob Moscow')

    all_languages_synopsis_hh = start_hh_parser(languages)
    table_for_print_hh = get_table_for_print(all_languages_synopsis_hh, 'HeadHunter Moscow')

    print(table_for_print_sj)
    print()
    print(table_for_print_hh)