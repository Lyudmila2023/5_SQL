import psycopg2


class DBManager:
    conn = psycopg2.connect(
        host='localhost',
        database='headhunter',
        user='postgres',
        password='123'
    )
    cur = conn.cursor()

    def __init__(self, cur):
        self.keyword = None
        self.cur = cur

    def get_companies_and_vacancies_count(self):
        # получает список всех компаний и количество вакансий у каждой компании
        self.cur.execute("SELECT employer_name, COUNT(*) FROM headhunter\n"
                         "GROUP BY employer_name")

        results = self.cur.fetchall()
        return results

    def get_all_vacancies(self):
        # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        self.cur.execute("SELECT vacancy_name, employer_name, salary_to, salary_from, url  FROM headhunter")

        results = self.cur.fetchall()
        return results

    def get_avg_salary(self):
        # получает среднюю зарплату по вакансиям.
        self.cur.execute("SELECT vacancy_name, ROUND(AVG(salary_to-salary_from)) FROM headhunter\n"
                         "Group by vacancy_name")

        results = self.cur.fetchall()
        return results
        pass

    def get_vacancies_with_higher_salary(self):
        # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        pass

    def get_vacancies_with_keyword(self, keyword):
        # получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python"
        self.keyword = keyword
        self.cur.execute(f"SELECT vacancy_name FROM headhunter\n"
                         f"WHERE vacancy_name LIKE '%{self.keyword}%'")
        results = self.cur.fetchall()
        return results
        

