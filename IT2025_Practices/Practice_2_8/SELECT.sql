-- Active: 1737450681071@@127.0.0.1@5432@IT_2025_pr_2_8

-- 1. Вибрати всі дані з таблиці Units.
SELECT * FROM Units;

-- 2. Вибрати назви всіх підрозділів.
SELECT unit_name FROM Units;

-- 3. Вибрати назви та розташування підрозділів, розташованих в 'Локація А'.
SELECT unit_name, unit_location FROM Units WHERE unit_location = 'Локація А';

-- 4. Вибрати всі операції зі статусом 'Завершено'.
SELECT * FROM Operations WHERE operation_status = 'Завершено';

-- 5. Вибрати назви операцій, що почалися після 01.01.2023.
SELECT operation_name FROM Operations WHERE start_date > '2023-01-01';

-- 6. Вибрати звіти, створені в червні 2023 року.
SELECT * FROM Reports WHERE report_date BETWEEN '2023-06-01' AND '2023-06-30';

-- 7. Вибрати описи звітів, що відносяться до операції з operation_id 10.
SELECT description FROM Reports WHERE operation_id = 10;

-- 8. Вибрати unit_id підрозділів, назва яких починається з 'Підрозділ 1'.
SELECT unit_id FROM Units WHERE unit_name LIKE 'Підрозділ 1%';

-- 9. Вибрати назви операцій, у яких не вказана дата завершення.
SELECT operation_name FROM Operations WHERE end_date IS NULL;

-- 10. Вибрати report_id звітів, опис яких містить слово 'звіт'.
SELECT report_id FROM Reports WHERE description LIKE '%звіт%';

-- 11. Вибрати всі дані з таблиці Units, відсортовані за назвою підрозділу.
SELECT * FROM Units ORDER BY unit_name;

-- 12. Вибрати всі операції, відсортовані за датою початку у спадному порядку.
SELECT * FROM Operations ORDER BY start_date DESC;

-- 13. Вибрати всі звіти, відсортовані за датою звіту у зростаючому порядку, а потім за operation_id.
SELECT * FROM Reports ORDER BY report_date ASC, operation_id;

-- 14. Вибрати перші 5 записів з таблиці Units.
SELECT * FROM Units LIMIT 5;

-- 15. Вибрати 10 записів з таблиці Operations, починаючи з шостого.
SELECT * FROM Operations OFFSET 5 LIMIT 10;

-- 16. Визначити кількість підрозділів.
SELECT COUNT(*) FROM Units;

-- 17. Визначити кількість операцій, що виконуються.
SELECT COUNT(*) FROM Operations WHERE operation_status = 'Виконується';

-- 18. Визначити середнє значення operation_id у звітах (не дуже змістовний приклад, але демонструє функцію).
SELECT AVG(operation_id) FROM Reports;

-- 19. Визначити дату початку найпізнішої операції.
SELECT MAX(start_date) FROM Operations;

-- 20. Визначити дату найпершого звіту.
SELECT MIN(report_date) FROM Reports;

-- 21. Визначити суму unit_id всіх підрозділів (не дуже змістовний приклад, але демонструє функцію).
SELECT SUM(unit_id) FROM Units;

-- 22. Згрупувати операції за статусом та визначити кількість операцій у кожній групі.
SELECT operation_status, COUNT(*) FROM Operations GROUP BY operation_status;

-- 23. Згрупувати звіти за operation_id та визначити кількість звітів для кожної операції.
SELECT operation_id, COUNT(*) FROM Reports GROUP BY operation_id;

-- 24. Вибрати локації, де розташовано більше 50 підрозділів.
SELECT unit_location, COUNT(*) FROM Units GROUP BY unit_location HAVING COUNT(*) > 50;

-- 25. Вибрати operation_id операцій, за якими створено більше 10 звітів.
SELECT operation_id FROM Reports GROUP BY operation_id HAVING COUNT(*) > 10;

-- 26. Вибрати назви підрозділів та операцій, пов'язаних через таблицю Units_Operations.
SELECT u.unit_name, o.operation_name FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id JOIN Operations o ON uo.operation_id = o.operation_id;

-- 27. Вибрати назви операцій та дати й описи пов'язаних звітів (включаючи операції без звітів).
SELECT o.operation_name, r.report_date, r.description FROM Operations o LEFT JOIN Reports r ON o.operation_id = r.operation_id;

-- 28. Вибрати назви підрозділів та операцій, пов'язаних через таблицю Units_Operations (включаючи операції без підрозділів та підрозділи без операцій).
SELECT u.unit_name, o.operation_name FROM Units u RIGHT JOIN Units_Operations uo ON u.unit_id = uo.unit_id RIGHT JOIN Operations o ON uo.operation_id = o.operation_id;

-- 29. Вибрати назви підрозділів та операцій, пов'язаних через таблицю Units_Operations (включаючи операції без підрозділів, підрозділи без операцій, та непов'язані записи).
SELECT u.unit_name, o.operation_name FROM Units u FULL OUTER JOIN Units_Operations uo ON u.unit_id = uo.unit_id FULL OUTER JOIN Operations o ON uo.operation_id = o.operation_id;

-- 30. Вибрати дату, опис звіту та назву відповідної операції.
SELECT r.report_date, r.description, o.operation_name FROM Reports r INNER JOIN Operations o ON r.operation_id = o.operation_id;

-- 31. Вибрати назву кожного підрозділу та кількість операцій, в яких він бере участь.
SELECT u.unit_name, COUNT(uo.operation_id) FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id GROUP BY u.unit_name;

-- 32. Вибрати назву кожної операції та кількість підрозділів, що беруть участь у ній.
SELECT o.operation_name, COUNT(uo.unit_id) FROM Operations o LEFT JOIN Units_Operations uo ON o.operation_id = uo.operation_id GROUP BY o.operation_name;

-- 33. Вибрати назви підрозділів та назви операцій зі статусом 'Виконується', пов'язаних через таблицю Units_Operations.
SELECT u.unit_name, o.operation_name FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id JOIN Operations o ON uo.operation_id = o.operation_id WHERE o.operation_status = 'Виконується';

-- 34. Вивести дату, опис звіту та назву відповідної операції, які розпочалися після '2023-01-01'.
SELECT r.report_date, r.description, o.operation_name FROM Reports r INNER JOIN Operations o ON r.operation_id = o.operation_id WHERE o.start_date > '2023-01-01';

-- 35. Вивести для кожної локації кількість унікальних операцій, що там проводяться.
SELECT u.unit_location, COUNT(DISTINCT o.operation_id) FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id LEFT JOIN Operations o ON uo.operation_id = o.operation_id GROUP BY u.unit_location;

-- 36. Вибрати назви операцій, за якими є звіти, створені після 01.05.2023.
SELECT operation_name FROM Operations WHERE operation_id IN (SELECT operation_id FROM Reports WHERE report_date > '2023-05-01');

-- 37. Вибрати назви підрозділів, що беруть участь у завершених операціях.
SELECT unit_name FROM Units WHERE unit_id IN (SELECT unit_id FROM Units_Operations WHERE operation_id IN (SELECT operation_id FROM Operations WHERE operation_status = 'Завершено'));

-- 38. Вибрати report_id, дату та опис звітів, що відносяться до операції з назвою 'Операція 5'.
SELECT report_id, report_date, description FROM Reports WHERE operation_id = (SELECT operation_id FROM Operations WHERE operation_name = 'Операція 5');

-- 39. Вибрати назви підрозділів, що не беруть участь у жодній операції.
SELECT unit_name FROM Units WHERE unit_id NOT IN (SELECT unit_id FROM Units_Operations);

-- 40. Вибрати назви операцій, за якими немає жодного звіту.
SELECT operation_name FROM Operations WHERE operation_id NOT IN (SELECT operation_id FROM Reports);

-- 41. Вибрати назви підрозділів, що беруть участь у більш ніж 5 операціях.
SELECT unit_name FROM Units WHERE (SELECT COUNT(*) FROM Units_Operations WHERE Units_Operations.unit_id = Units.unit_id) > 5;

-- 42. Вивести назви операцій, за якими є більше двох звітів.
SELECT operation_name FROM Operations WHERE (SELECT COUNT(*) FROM Reports WHERE Reports.operation_id = Operations.operation_id) > 2;

-- 43. Вибрати звіт(и) з найостаннішою датою.
SELECT * FROM Reports WHERE report_date = (SELECT MAX(report_date) FROM Reports);

-- 44. Вивести середню кількість звітів на одну операцію.
SELECT AVG(report_count) FROM (SELECT operation_id, COUNT(*) as report_count FROM Reports GROUP BY operation_id) as subquery;

-- 45. Вивести unit_id та unit_name підрозділу(ів), що задіяні у найбільшій кількості операцій.
SELECT unit_id, unit_name FROM Units WHERE unit_id IN (SELECT unit_id FROM Units_Operations GROUP BY unit_id HAVING COUNT(*) = (SELECT MAX(op_count) FROM (SELECT unit_id, COUNT(*) as op_count FROM Units_Operations GROUP BY unit_id) as counts));

-- 46. Вибрати операції, що почалися після 01.01.2023 і зараз виконуються.
SELECT * FROM Operations WHERE start_date > '2023-01-01' AND operation_status = 'Виконується';

-- 47. Вибрати звіти за березень 2023 року або ті, що відносяться до запланованих операцій.
SELECT * FROM Reports WHERE report_date BETWEEN '2023-03-01' AND '2023-03-31' OR operation_id IN (SELECT operation_id FROM Operations WHERE operation_status = 'Заплановано');

-- 48. Вибрати підрозділи, локація яких починається на 'Л' і які беруть участь в операціях, що почалися до 01.04.2023.
SELECT * FROM Units WHERE unit_location LIKE 'Л%' AND unit_id IN (SELECT unit_id FROM Units_Operations WHERE operation_id IN (SELECT operation_id FROM Operations WHERE start_date < '2023-04-01'));

-- 49. Вибрати назви підрозділів, назви операцій та дати звітів для завершених операцій, що проводилися в 'Локація Б'.
SELECT u.unit_name, o.operation_name, r.report_date FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id JOIN Operations o ON uo.operation_id = o.operation_id LEFT JOIN Reports r ON o.operation_id = r.operation_id WHERE u.unit_location = 'Локація Б' AND o.operation_status = 'Завершено';

-- 50. Вивести назви підрозділів та операцій, що розпочались до 01.06.2023 та закінчились після 30.06.2023.
SELECT u.unit_name, o.operation_name FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id JOIN Operations o ON uo.operation_id = o.operation_id WHERE o.start_date < '2023-06-01' AND o.end_date > '2023-06-30';

-- 51. Вибрати операції, що почалися у 2023 році.
SELECT * FROM Operations WHERE EXTRACT(YEAR FROM start_date) = 2023;

-- 52. Вибрати звіти, створені у грудні.
SELECT * FROM Reports WHERE EXTRACT(MONTH FROM report_date) = 12;

-- 53. Вивести для кожної операції її назву, дату початку, дату закінчення та тривалість у днях.
SELECT operation_name, start_date, end_date, EXTRACT(DAY FROM end_date - start_date) AS duration FROM Operations;

-- 54. Вивести кількість звітів, створених у кожному місяці (з назвою місяця).
SELECT to_char(report_date, 'Month') AS month, COUNT(*) FROM Reports GROUP BY month;

-- 55. Вивести кількість операцій, що розпочинаються у кожен день тижня (з назвою дня тижня).
SELECT to_char(start_date, 'Day') AS weekday, COUNT(*) FROM Operations GROUP BY weekday;

-- 56. Вивести operation_id, operation_name та колонку is_completed, де буде 'Так', якщо операція завершена, і 'Ні' в іншому випадку.
SELECT operation_id, operation_name, CASE WHEN operation_status = 'Завершено' THEN 'Так' ELSE 'Ні' END AS is_completed FROM Operations;

-- 57. Вивести операції, у яких дата закінчення менша, ніж дата початку плюс 7 днів.
SELECT * FROM Operations WHERE start_date + INTERVAL '7 days' > end_date;

-- 58. Вивести назву операції та дату її закінчення, а якщо дата закінчення не вказана (NULL), то поточну дату.
SELECT operation_name, COALESCE(end_date, CURRENT_DATE) FROM Operations;

-- 59. Вивести report_id, description, а також колонку modified_description, де значення буде NULL, якщо опис дорівнює 'Опис звіту 1', і оригінальний опис в іншому випадку.
SELECT report_id, description, NULLIF(description, 'Опис звіту 1') AS modified_description FROM Reports;

-- 60. Вивести назву операції та довжину цієї назви.
SELECT operation_name, LENGTH(operation_name) AS name_length FROM Operations;

-- 61. Вивести звіти, в описі яких є слова, схожі на "звіт" або "рапорт".
SELECT * FROM Reports WHERE description SIMILAR TO '%(звіт|рапорт)%';

-- 62. Вивести повну та скорочену (перші 5 символів) назву підрозділу.
SELECT unit_name, SUBSTRING(unit_name, 1, 5) AS short_name FROM Units;

-- 63. Вивести назву підрозділу та його локацію, замінивши слово 'Локація' на 'Місце'.
SELECT unit_name, REPLACE(unit_location, 'Локація', 'Місце') FROM Units;

-- 64. Вивести підрозділи, назва яких починається з 'підрозділ' (незалежно від регістру).
SELECT * FROM Units WHERE LOWER(unit_name) LIKE 'підрозділ%';

-- 65. Вивести назву операції та цю ж назву без пробілів на початку і в кінці.
SELECT operation_name, TRIM(operation_name) FROM Operations;

-- 66. Вивести для кожної операції її назву, дати початку та закінчення, а також середню тривалість всіх операцій.
SELECT operation_name, start_date, end_date, AVG(EXTRACT(DAY FROM end_date - start_date)) OVER () FROM Operations;

-- 67. Вивести report_id, дату, operation_id та ранг звіту в межах кожної операції, відсортований за датою.
SELECT report_id, report_date, operation_id, RANK() OVER (PARTITION BY operation_id ORDER BY report_date) AS report_rank FROM Reports;

-- 68. Вивести назву підрозділу, локацію та порядковий номер підрозділу в межах кожної локації, відсортований за назвою.
SELECT unit_name, unit_location, ROW_NUMBER() OVER (PARTITION BY unit_location ORDER BY unit_name) as row_num FROM Units;

-- 69. Вивести назву операції, дату початку та дату початку попередньої операції (або ту саму дату, якщо попередньої немає).
SELECT operation_name, start_date, LAG(start_date, 1, start_date) OVER (ORDER BY start_date) AS prev_start_date FROM Operations;

-- 70. Вивести report_id, дату звіту та дату наступного звіту (або ту саму дату, якщо наступного немає).
SELECT report_id, report_date, LEAD(report_date, 1, report_date) OVER (ORDER BY report_date) AS next_report_date FROM Reports;

-- 71. Для кожного підрозділу вивести його назву, unit_id та кількість підрозділів з такою ж назвою.
SELECT unit_name, unit_id, COUNT(*) OVER (PARTITION BY unit_name) AS total_units_with_same_name FROM Units;

-- 72. Вивести назву, operation_id кожної операції, а також накопичувальну суму operation_id в порядку зростання operation_id.
SELECT operation_name, operation_id, SUM(operation_id) OVER (ORDER BY operation_id) as running_total FROM Operations;

-- 73. Визначити середню тривалість операцій, використовуючи CTE для розрахунку тривалості кожної операції.
WITH OperationDurations AS (SELECT operation_name, EXTRACT(DAY FROM end_date - start_date) AS duration FROM Operations) SELECT AVG(duration) FROM OperationDurations;

-- 74. Вибрати звіти, що відносяться до операцій, які почалися після 01.01.2023, використовуючи CTE для фільтрації операцій.
WITH RelevantOperations AS (SELECT operation_id FROM Operations WHERE start_date > '2023-01-01') SELECT * FROM Reports WHERE operation_id IN (SELECT operation_id FROM RelevantOperations);

-- 75. Вивести назви підрозділів та кількість операцій, в яких вони беруть участь, для тих підрозділів, що беруть участь у більш ніж 10 операціях, використовуючи CTE.
WITH UnitOperationCounts AS (SELECT u.unit_name, COUNT(uo.operation_id) AS operation_count FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id GROUP BY u.unit_name) SELECT * FROM UnitOperationCounts WHERE operation_count > 10;

-- 76. Вивести всі звіти, що стосуються 5 найновіших операцій (за датою початку). Використовується CTE для визначення найновіших операцій.
WITH TopOperations AS (SELECT operation_id, operation_name FROM Operations ORDER BY start_date DESC LIMIT 5) SELECT r.* FROM Reports r JOIN TopOperations t ON r.operation_id = t.operation_id;

-- 77. Вивести всі операції, за якими немає жодного звіту. Використовується CTE для виявлення операцій, пов'язаних зі звітами.
WITH OperationsWithReports AS (SELECT DISTINCT operation_id FROM Reports) SELECT o.* FROM Operations o LEFT JOIN OperationsWithReports owr ON o.operation_id = owr.operation_id WHERE owr.operation_id IS NULL;

-- 78. Вибрати назви операцій, що почалися після 01.01.2023, в яких беруть участь більше двох різних підрозділів.
SELECT o.operation_name, COUNT(DISTINCT u.unit_id) FROM Operations o LEFT JOIN Units_Operations uo ON o.operation_id = uo.operation_id LEFT JOIN Units u ON uo.unit_id = u.unit_id WHERE o.start_date > '2023-01-01' GROUP BY o.operation_name HAVING COUNT(DISTINCT u.unit_id) > 2;

-- 79. Вибрати назви підрозділів, які не беруть участь у жодній скасованій операції.
SELECT u.unit_name FROM Units u WHERE NOT EXISTS (SELECT 1 FROM Units_Operations uo WHERE uo.unit_id = u.unit_id AND uo.operation_id IN (SELECT operation_id FROM Operations WHERE operation_status = 'Скасовано'));

-- 80. Вивести пари назв різних підрозділів, що розташовані в одній локації.
SELECT u1.unit_name, u2.unit_name FROM Units u1 CROSS JOIN Units u2 WHERE u1.unit_id < u2.unit_id AND u1.unit_location = u2.unit_location;

-- 81. Вивести пари назв операцій, що перетинаються в часі (перша операція починається раніше другої, але перша закінчується пізніше, ніж починається друга).
SELECT o1.operation_name, o2.operation_name FROM Operations o1 JOIN Operations o2 ON o1.start_date < o2.start_date AND o1.end_date > o2.start_date WHERE o1.operation_id <> o2.operation_id;

-- 82. Вивести для кожного підрозділу його назву, кількість операцій, в яких він бере участь, та кількість підрозділів в тій самій локації.
SELECT u.unit_name, (SELECT COUNT(*) FROM Units_Operations uo WHERE uo.unit_id = u.unit_id) as op_count, (SELECT COUNT(*) FROM Units WHERE unit_location = u.unit_location) as units_in_location FROM Units u ORDER BY op_count DESC;

-- 83. Вивести назву підрозділу, report_id та дату найстарішого звіту, пов'язаного з цим підрозділом.
SELECT u.unit_name, r.report_id, r.report_date FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id LEFT JOIN Operations o ON uo.operation_id = o.operation_id LEFT JOIN Reports r ON o.operation_id = r.operation_id WHERE r.report_date = (SELECT MIN(report_date) FROM Reports);

-- 84. Вибрати підрозділи, які беруть участь у всіх існуючих операціях.
SELECT * FROM Units WHERE unit_id IN (SELECT unit_id FROM Units_Operations GROUP BY unit_id HAVING COUNT(DISTINCT operation_id) = (SELECT COUNT(DISTINCT operation_id) FROM Operations));

-- 85. Об'єднати operation_id з operation_name та unit_id з unit_name в одну таблицю, привівши числові ідентифікатори до текстового типу.
SELECT CAST(operation_id AS TEXT), operation_name FROM Operations UNION SELECT CAST(unit_id AS TEXT), unit_name FROM Units;

-- 86. Вивести операції, які мають статус 'Виконується' і поточна дата знаходиться між датою початку та датою закінчення операції.
SELECT * FROM Operations WHERE operation_status = 'Виконується' AND CURRENT_DATE BETWEEN start_date AND end_date;

-- 87. Вивести перші два звіти по кожній операції (відсортовані за датою).
SELECT r.* FROM Reports r WHERE (SELECT COUNT(*) FROM Reports WHERE operation_id = r.operation_id AND report_date < r.report_date) < 2;

-- 88. Вивести підрозділ(и), що задіяні у найбільшій кількості унікальних операцій.
SELECT u.* FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id GROUP BY u.unit_id HAVING COUNT(DISTINCT uo.operation_id) = (SELECT MAX(op_count) FROM (SELECT unit_id, COUNT(DISTINCT operation_id) as op_count FROM Units_Operations GROUP BY unit_id) as counts);

-- 89. Вивести операції, в яких задіяно більше підрозділів, ніж в середньому по всіх операціях.
SELECT o.*, (SELECT COUNT(*) FROM Units_Operations uo WHERE uo.operation_id = o.operation_id) as num_units FROM Operations o WHERE (SELECT COUNT(*) FROM Units_Operations uo WHERE uo.operation_id = o.operation_id) > (SELECT AVG(unit_count) FROM (SELECT operation_id, COUNT(*) as unit_count FROM Units_Operations GROUP BY operation_id) as counts);

-- 90. Вивести звіти, пов'язані з найпершою операцією (за датою початку).
SELECT r.* FROM Reports r WHERE operation_id IN (SELECT operation_id FROM Operations WHERE start_date = (SELECT MIN(start_date) FROM Operations));

-- 91. Для кожного підрозділу вивести його дані, кількість унікальних операцій, в яких він бере участь, і загальну кількість операцій, в яких він бере участь.
SELECT u.*, (SELECT COUNT(DISTINCT operation_id) FROM Units_Operations WHERE unit_id = u.unit_id) as num_operations, (SELECT COUNT(*) FROM Units_Operations WHERE unit_id = u.unit_id) as total_operations FROM Units u;

-- 92. Вивести операції, в яких бере участь лише один підрозділ.
SELECT o.* FROM Operations o WHERE (SELECT COUNT(DISTINCT unit_id) FROM Units_Operations WHERE operation_id = o.operation_id) = 1;

-- 93. Вивести назви завершених операцій (end_date < поточної дати), за якими немає жодного звіту.
SELECT o.operation_name FROM Operations o LEFT JOIN Reports r ON o.operation_id = r.operation_id WHERE o.end_date < CURRENT_DATE AND r.report_id IS NULL;

-- 94. Вивести для кожного підрозділу кількість унікальних операцій, в яких він бере участь, не враховуючи скасовані операції.
SELECT u.unit_name, COUNT(DISTINCT o.operation_id) FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id LEFT JOIN Operations o ON uo.operation_id = o.operation_id WHERE o.operation_status <> 'Скасовано' GROUP BY u.unit_name;

-- 95. Вивести назву операції (або операцій), що розпочалася у 2023 році і має найбільшу кількість звітів за цей же період.
SELECT o.operation_name, COUNT(r.report_id) FROM Operations o LEFT JOIN Reports r ON o.operation_id = r.operation_id WHERE o.start_date BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY o.operation_name HAVING COUNT(r.report_id) = (SELECT MAX(report_count) FROM (SELECT operation_id, COUNT(report_id) as report_count FROM Reports WHERE report_date BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY operation_id) as counts);

-- 96. Вивести назву підрозділу, назву операції, дату та опис звіту для всіх виконуваних операцій, в яких беруть участь підрозділи, чия локація починається на "Л".
SELECT u.unit_name, o.operation_name, r.report_date, r.description FROM Units u JOIN Units_Operations uo ON u.unit_id = uo.unit_id JOIN Operations o ON uo.operation_id = o.operation_id LEFT JOIN Reports r ON o.operation_id = r.operation_id WHERE u.unit_id IN (SELECT unit_id FROM Units WHERE unit_location LIKE 'Л%') AND o.operation_id IN (SELECT operation_id FROM Operations WHERE operation_status = 'Виконується');

-- 97. Для кожного підрозділу вивести його назву, кількість унікальних завершених операцій та кількість унікальних виконуваних операцій.
SELECT u.unit_name, COUNT(DISTINCT CASE WHEN o.operation_status = 'Завершено' THEN o.operation_id END) as completed_operations, COUNT(DISTINCT CASE WHEN o.operation_status = 'Виконується' THEN o.operation_id END) as ongoing_operations FROM Units u LEFT JOIN Units_Operations uo ON u.unit_id = uo.unit_id LEFT JOIN Operations o ON uo.operation_id = o.operation_id GROUP BY u.unit_name;

-- 98. Для кожної операції вивести її назву та середнє значення report_id серед усіх звітів, пов'язаних з цією операцією.
SELECT o.operation_name, AVG(r.report_id) OVER (PARTITION BY o.operation_id) as avg_report_id FROM Operations o LEFT JOIN Reports r ON o.operation_id = r.operation_id;

-- 99. Вивести пари "підрозділ - операція", для яких даний підрозділ не бере участь у даній операції.
SELECT u.unit_name, o.operation_name FROM Units u CROSS JOIN Operations o WHERE NOT EXISTS (SELECT 1 FROM Units_Operations uo WHERE uo.unit_id = u.unit_id AND uo.operation_id = o.operation_id);

-- 100. Вивести пари "підрозділ - операція" для запланованих операцій в 'Локація А', де даний підрозділ не бере участь у даній операції.
SELECT u.unit_name, o.operation_name FROM Units u, Operations o WHERE NOT EXISTS (SELECT 1 FROM Units_Operations uo WHERE uo.unit_id = u.unit_id AND uo.operation_id = o.operation_id) AND o.operation_status = 'Заплановано' AND u.unit_location = 'Локація А';