import requests
from itertools import count
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to, salary_currency):
    if salary_currency != "RUR" and salary_currency != "rub":
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def get_hh_salary_statistic(language):
    salaries = []
    url = 'https://api.hh.ru/vacancies'
    for page in count(0):
        payload = {
            "User-Agent": User-Agent 
            "professional_role": "96",
            "area":"1",
            "period":"30",
            "text": f"Программист{language}",
            "text": "Програмист Python",
            "only_with_salary": True,
            "page":page
    }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        vacancy_response = response.json()
        for vacancy in vacancy_response["items"]:
            vacancy_salary = vacancy["salary"]
            salary_from = vacancy_salary["from"]
            salary_to = vacancy_salary["to"]
            salary_currency = vacancy_salary["currency"]
            salary = predict_salary(salary_from, salary_to, salary_currency)
            if salary:
                salaries.append(salary)
        if page == vacancy_response["pages"]-1:
            break
    vacancies_found = vacancy_response["found"]
    vacancies_processed = len(salaries)
    if vacancies_processed:
        average_salary = sum(salaries) // vacancies_processed
    return { 
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }



def get_sj_salary_statistic(language):
    sj_salaries =[]
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id" : sj_key
    }
    for page in count(0):
        sj_payload = {
        "town_id" : 4,
        "keyword": "программист",
        "page" : page
    }
    sj_response = requests.get(url, params=sj_payload, headers=headers)
    sj_response.raise_for_status()
    sj_vacancies = sj_response.json()
    vacancies_found = sj_vacancies["total"]
    for vacancy in sj_vacancies["objects"]:
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
        salary_currency = vacancy["currency"]
        sj_salary = predict_salary(salary_from, salary_to, salary_currency)
        if sj_salary:
            sj_salaries.append(sj_salary)
        if not sj_vacancies["more"]:
            break
    vacancies_processed = len(sj_salaries)
    if vacancies_processed:
        average_salary = sum(sj_salaries) // vacancies_processed
    else:
        average_salary = 0
    return { 
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


def make_table(salaries_statistic, title):
    table_content = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for language, vacancy in salaries_statistic.items():
        raw = [language, vacancy["vacancies_found"], vacancy["vacancies_processed"], vacancy["average_salary"]]
        table_content.append(raw)
    table = AsciiTable(table_content, title)
    return table.table

def main():
    load_dotenv()
    sj_key = os.getenv("SUPERJOB_KEY")
    languages = [
        "Python",
        "Java",
        "Go",
        "Javascript",
        "C#",
        "C",
        "PHP",
        "Ruby"
    ]
    full_salaries_statistic_hh = {}
    full_salaries_statistic_sj = {}
    title_hh = "HeadHunter Moscow"
    title_sj = "SuperJob Moscow"
    for language in languages:
        full_salary_statistic_sj = get_sj_salary_statistic(language)
        full_salaries_statistic_sj[language] = full_salary_statistic_sj
        full_salary_statistic_hh = get_hh_salary_statistic(language)
        full_salaries_statistic_hh[language] = full_salary_statistic_hh
    table_sj = make_table(full_salaries_statistic_sj, title_sj)
    table_hh = make_table(full_salaries_statistic_hh, title_hh)
    print(table_sj)
    print(table_hh)


if __name__ == "__main__":
     main()