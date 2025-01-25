--б) Перевірка зв'язків за допомогою SQL-запитів:

--1. Вивести всі звіти для підрозділу "Підрозділ Альфа":

SELECT r.*
FROM Reports r
JOIN Units u ON r.unit_id = u.unit_id
WHERE u.name = 'Підрозділ Альфа';

--2. Вивести маршрут, який виконував 'Танк Т-72':
SELECT r.*
FROM Routes r
JOIN Equipment e ON r.equipment_id = e.equipment_id
WHERE e.name = 'Танк Т-72';

--3. Вивести весь особовий склад, що відноситься до підрозділу "Підрозділ Бета":
SELECT p.*
FROM Personnel p
JOIN Units u ON p.unit_id = u.unit_id
WHERE u.name = 'Підрозділ Бета';

--4. Вивести всі операції, що заплановані на грудень:
SELECT *
FROM Operations
WHERE start_date >= '2023-12-01' AND end_date <= '2023-12-31';

--5. Вивести усі маршрути, що задіяні в операції "Щит":
SELECT r.*
FROM Routes r
JOIN Operations o ON o.name = 'Операція "Щит"'
WHERE EXISTS (SELECT 1 FROM Operations op WHERE op.name = 'Операція "Щит"')