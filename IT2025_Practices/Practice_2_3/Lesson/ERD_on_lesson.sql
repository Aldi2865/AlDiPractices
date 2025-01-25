-- Таблиця Units
CREATE TABLE Units (
    unit_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- Таблиця Equipment
CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    status VARCHAR(50),
    unit_id INT REFERENCES Units(unit_id)
);

-- Таблиця Routes
CREATE TABLE Routes (
    route_id SERIAL PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    distance_km INT,
    equipment_id INT REFERENCES Equipment(equipment_id)
);

-- Таблиця Personnel
CREATE TABLE Personnel (
    personnel_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rank VARCHAR(50),
    role VARCHAR(50),
    unit_id INT REFERENCES Units(unit_id)
);

-- Таблиця Reports
CREATE TABLE Reports (
    report_id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    description TEXT,
    unit_id INT REFERENCES Units(unit_id),
    route_id INT REFERENCES Routes(route_id)
);

-- Таблиця Operations
CREATE TABLE Operations (
    operation_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    description TEXT
);