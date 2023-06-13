import requests
import json


def get_request():  # ф-ция выполняющая запрос к сайту hh.ru полученные данные сохраняются в json формате
    response = requests.get("https://api.hh.ru/vacancies", params={"page": 0, "per_page": 100})
    data = response.json()['items']
    with open('HH.json', "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def json_data_read():  # ф-ция выполняющая чтение данных json файла
    with open('HH.json', "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def get_employers_list(data):  # ф-ция формирует список работодателей
    employs = []

    for item in data:
        if len(employs) >= 20:
            break
        elif item['employer']['name'] not in employs:
            employs.append(item['employer']['name'])

    return employs


def get_salary(salary):  # ф-я для конвертации з/п в рубли в случае если она указана в валюте
    formatted_salary = [None, None]
    if salary and salary["from"] and salary["from"] != 0:
        formatted_salary[0] = salary["from"] if salary["currency"].lower() == "rur" else salary["from"] * 80
    if salary and salary["to"] and salary["to"] != 0:
        formatted_salary[1] = salary["to"] if salary["currency"].lower() == "rur" else salary["to"] * 80

    return formatted_salary
