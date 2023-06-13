import psycopg2
from utils import get_request, json_data_read, get_employers_list, get_salary


def main():
    get_request()
    data = json_data_read()
    employs = get_employers_list(data)
    # print(employs)

    conn = psycopg2.connect( # подключение к БД
        host='localhost',
        database='headhunter',
        user='postgres',
        password='123'
    )
    cur = conn.cursor()

    for item in data: # формирование данных и заполнение таблицы
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
