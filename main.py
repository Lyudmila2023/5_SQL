import psycopg2
import requests
import json
from dbmanager_class import DBManager

conn = psycopg2.connect(
    host='localhost',
    database='headhunter',
    user='postgres',
    password='123'
)
cur = conn.cursor()


def get_request():
    response = requests.get("https://api.hh.ru/vacancies", params={"page": 0, "per_page": 100})
    data = response.json()['items']
    with open('HH.json', "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_salary(salary):  # ф-я для конвертации з/п в рубли в случае если она указана в валюте
    formatted_salary = [None, None]
    if salary and salary["from"] and salary["from"] != 0:
        formatted_salary[0] = salary["from"] if salary["currency"].lower() == "rur" else salary["from"] * 80
    if salary and salary["to"] and salary["to"] != 0:
        formatted_salary[1] = salary["to"] if salary["currency"].lower() == "rur" else salary["to"] * 80

    return formatted_salary


def main():
    get_request()
    employs = []
    with open('HH.json', "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        if len(employs) >= 20:
            break
        elif item['employer']['name'] not in employs:
            employs.append(item['employer']['name'])

    for item in data:
        if item["employer"]["name"] in employs:
            vacancy_id = item["id"],
            vacancy_name = item["name"],
            url = item["url"]
            salary_from = get_salary(item["salary"])[0]
            salary_to = get_salary(item["salary"])[1]
            employer_id = item["employer"]["id"],
            employer_name = item["employer"]["name"],
            requirement = item["snippet"]["requirement"],
            responsibility = item["snippet"]["responsibility"]
            cur.execute("INSERT INTO headhunter VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vacancy_id,
                                                                                       vacancy_name,
                                                                                       url,
                                                                                       salary_to,
                                                                                       salary_from,
                                                                                       employer_id,
                                                                                       employer_name,
                                                                                       requirement,
                                                                                       responsibility))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
