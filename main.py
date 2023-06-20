import psycopg2
from utils import get_request, json_data_read, get_employers_list, get_salary
from dbmanager_class import DBManager


def main():
    get_request()
    data = json_data_read()
    employs = get_employers_list(data)

    conn = psycopg2.connect(  # подключение к БД
        host='localhost',
        database='headhunter',
        user='postgres',
        password='123'
    )
    cur = conn.cursor()  # создание таблицы в БД
    cur.execute("""CREATE TABLE IF NOT EXISTS headhunter(vacancy_id int PRIMARY KEY,
                vacancy_name varchar,
                url varchar,
                salary_to int,
                salary_from int ,
                employer_id int ,
                employer_name varchar,
                requirement text,
                responsibility text);
                """)
    for item in data:  # формирование данных и заполнение таблицы
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
    data = DBManager()
    while True:
        user_input = input("Выберете действие:\n"
                           "1 - получает список всех компаний и количество вакансий у каждой компании\n"
                           "2 -получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
                           "3- получает среднюю зарплату по вакансиям.\n"
                           "4-получает список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                           "5-получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'Диспетчер'\n"
                           "выход - выйти из программы\n")
        if user_input == "1":
            print(data.get_companies_and_vacancies_count())
        elif user_input == "2":
            print(data.get_all_vacancies())
        elif user_input == "3":
            print(data.get_avg_salary())
        elif user_input == "4":
            print(data.get_vacancies_with_higher_salary())
        elif user_input == "5":
            word = input("Введите слово: ")
            print(data.get_vacancies_with_keyword(word))
        elif user_input == "выход":
            break
        else:
            print("Нет такого значения")
            continue

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
