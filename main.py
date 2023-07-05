from hh_parser import start_hh_parser
from super_job import start_sj_parser
import os
from dotenv import load_dotenv


if __name__ == "__main__": 
    load_dotenv()
    token = os.environ['SUPERJOB_TOKEN'] 
    languages = ['Python', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 'Go', 'Swift', 'TypeScript']

    print(start_sj_parser(token, languages))
    print()
    print(start_hh_parser(languages))