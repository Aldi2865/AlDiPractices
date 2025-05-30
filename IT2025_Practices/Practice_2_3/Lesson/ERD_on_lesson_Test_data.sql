-- Додавання даних в Units
INSERT INTO Units (name, location) VALUES
('Підрозділ Альфа', 'Київ'),
('Підрозділ Бета', 'Львів'),
('Підрозділ Гамма', 'Одеса');

-- Додавання даних в Equipment
INSERT INTO Equipment (name, type, status, unit_id) VALUES
('Танк Т-72', 'Танк', 'Справний', 1),
('БТР-80', 'БТР', 'В ремонті', 1),
('Вантажівка КрАЗ', 'Вантажівка', 'Справний', 2);

-- Додавання даних в Routes
INSERT INTO Routes (origin, destination, distance_km, equipment_id) VALUES
('Київ', 'Житомир', 140, 1),
('Львів', 'Тернопіль', 130, 3),
('Київ', 'Чернігів', 140, 2);

-- Додавання даних в Personnel
INSERT INTO Personnel (name, rank, role, unit_id) VALUES
('Іванов І.І.', 'Капітан', 'Командир', 1),
('Петров П.П.', 'Сержант', 'Водій', 1),
('Сидоров С.С.', 'Лейтенант', 'Заступник', 2);

-- Додавання даних в Reports
INSERT INTO Reports (report_date, description, unit_id, route_id) VALUES
('2023-11-22', 'Звіт про пересування по маршруту Київ-Житомир', 1, 1),
('2023-11-23', 'Звіт про технічний стан БТР-80', 1, NULL),
('2023-11-23', 'Звіт про пересування по маршруту Львів-Тернопіль', 2, 2);


-- Додавання даних в Operations
INSERT INTO Operations (name, start_date, end_date, status, description) VALUES
('Операція "Щит"', '2023-11-20', '2023-11-30', 'Виконується', 'Забезпечення безпеки на ділянці Київ-Житомир'),
('Операція "Межа"', '2023-12-01', '2023-12-15', 'Заплановано', 'Патрулювання кордону');