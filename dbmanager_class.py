import psycopg2


class DBManager:

    def __init__(self):
        conn = psycopg2.connect(
            host='localhost',
            database='headhunter',
            user='postgres',
            password='123'
        )
        cur = conn.cursor()
        self.keyword = None
        self.cur = cur

    def get_companies_and_vacancies_count(self):
        # получает список всех компаний и количество вакансий у каждой компании
        self.cur.execute("SELECT employer_name, COUNT(*) FROM headhunter\n"
                         "GROUP BY employer_name")
        data = self.cur.fetchall()
        return data

    def get_all_vacancies(self):
        # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        self.cur.execute("SELECT vacancy_name, employer_name, salary_to, salary_from, url  FROM headhunter")

        data = self.cur.fetchall()
        return data

    def get_avg_salary(self):
        # получает среднюю зарплату по вакансиям.
        self.cur.execute("SELECT vacancy_name, ROUND(AVG(salary_to-salary_from)) FROM headhunter\n"
                         "Group by vacancy_name")

        data = self.cur.fetchall()
        return data

    def get_vacancies_with_higher_salary(self):
        # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        self.cur.execute(f"Select vacancy_name, salary_to FROM headhunter\n"
                         f"WHERE salary_to>(SELECT AVG(salary_to) FROM headhunter)")
        data = self.cur.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword):
        # получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python"
        self.keyword = keyword
        self.cur.execute(f"SELECT vacancy_name FROM headhunter\n"
                         f"WHERE vacancy_name LIKE '%{self.keyword}%'")
        data = self.cur.fetchall()
        return data
        

