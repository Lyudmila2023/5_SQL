-- 1) получает список всех компаний и количество вакансий у каждой компании
SELECT employer_name, COUNT(*) FROM headhunter
GROUP BY employer_name

-- 2) получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT vacancy_name, employer_name, salary_to, salary_from, url  FROM headhunter

--3) получает среднюю зарплату по вакансиям.
SELECT vacancy_name, ROUND(AVG(salary_to-salary_from)) FROM headhunter
GROUP BY vacancy_name

--4) получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT vacancy_name, salary_to FROM headhunter
WHERE salary_to>(SELECT AVG(salary_to) FROM headhunter)

--5) получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python"
SELECT vacancy_name FROM headhunter\n"
WHERE vacancy_name LIKE %python%