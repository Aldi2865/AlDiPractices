-- Active: 1737450681071@@127.0.0.1@5432@ammunitionsupplydb

CREATE DATABASE ammunitionsupplydb;

SET DATABASE = 'ammunitionsupplydb';

CREATE TABLE ammunitionstock (
    ammunitionid INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Type VARCHAR(50),
    Quantity INT,
    StorageLocation VARCHAR(100),
    ExpirationDate DATE
);
INSERT INTO ammunitionstock (Type, quantity, storagelocation,expirationdate) VALUES
('9mm', 1200, 'Warehouse A', '2025-12-31'),
('5.56mm', 600, 'Warehouse B', '2024-11-30'),
('7.62mm', 800, 'Warehouse C', '2026-10-15'),
('9mm', 1100, 'Warehouse A', '2025-12-31'),
('5.56mm', 550, 'Warehouse B', '2024-11-30'),
('7.62mm', 700, 'Warehouse C', '2026-10-15'),
('9mm', 1300, 'Warehouse A', '2025-12-31'),
('5.56mm', 650, 'Warehouse B', '2024-11-30'),
('7.62mm', 850, 'Warehouse C', '2026-10-15'),
('9mm', 1400, 'Warehouse A', '2025-12-31'),
('5.56mm', 700, 'Warehouse B', '2024-11-30'),
('7.62mm', 900, 'Warehouse C', '2026-10-15'),
('9mm', 1500, 'Warehouse A', '2025-12-31'),
('5.56mm', 750, 'Warehouse B', '2024-11-30'),
('7.62mm', 950, 'Warehouse C', '2026-10-15'),
('9mm', 1600, 'Warehouse A', '2025-12-31'),
('5.56mm', 800, 'Warehouse B', '2024-11-30'),
('7.62mm', 1000, 'Warehouse C', '2026-10-15'),
('9mm', 1700, 'Warehouse A', '2025-12-31'),
('5.56mm', 850, 'Warehouse B', '2024-11-30'),
('7.62mm', 1050, 'Warehouse C', '2026-10-15'),
('9mm', 1800, 'Warehouse A', '2025-12-31'),
('5.56mm', 900, 'Warehouse B', '2024-11-30');