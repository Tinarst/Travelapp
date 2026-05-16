-- Active: 1757052698297@@127.0.0.1@5432@passenger
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    name VARCHAR(50),
    wallet FLOAT DEFAULT 0
);
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR
);
CREATE TABLE trip (
    id SERIAL PRIMARY KEY,
    origin VARCHAR NOT NULL,
    destination VARCHAR NOT NULL,
    departure_date TIMESTAMP NOT NULL,
    price BIGINT NOT NULL,
    capacity INT,
    expired BOOLEAN DEFAULT false
);
CREATE TABLE ticket (
    datetime_issue TIMESTAMP DEFAULT NOW() PRIMARY KEY,
    user_id INT,
    trip_id INT,
    chair_number INT NOT NULL,
    status VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (trip_id) REFERENCES trip (id) ON DELETE SET NULL
);
CREATE TABLE chair (
    number INT NOT NULL,
    trip_id INT NOT NULL REFERENCES trip(id),
    status VARCHAR DEFAULT 'free'
);
CREATE TABLE transaction (
    datetime_issue TIMESTAMP DEFAULT NOW() PRIMARY KEY,
    amount INT NOT NULL,
    -- whithdraw or deposit
    status VARCHAR(10) NOT NULL,
    -- for buy/ cancel or increase
    reason VARCHAR,
    user_id INT REFERENCES users (id)
);

CREATE TABLE entered (
    username VARCHAR PRIMARY KEY,
    password VARCHAR NOT NULL
);

CREATE TABLE auditlog (
    stamp TIMESTAMP DEFAULT now() PRIMARY KEY,
    actor VARCHAR(10) NOT NULL,
    action VARCHAR(50) NOT NULL,
    detail VARCHAR(100)
);
CREATE TABLE log (
    stamp TIMESTAMP DEFAULT NOW() PRIMARY KEY,
    level VARCHAR(20),
    msg VARCHAR(100)
);
CREATE INDEX available_ticket ON trip (id, expired);
CREATE INDEX username ON users (username);

ALTER TABLE chair
ADD UNIQUE (number, trip_id);

-- ✈️ TICKETS
INSERT INTO trip (origin, destination, departure_date, price, capacity)
VALUES
('Tehran', 'Mashhad', '2025-10-20 08:30:00', 650000, 5),
('Isfahan', 'Shiraz', '2025-10-21 10:00:00', 520000, 3),
('Tabriz', 'Tehran', '2025-10-19 07:00:00', 470000, 4),
('Rasht', 'Kish', '2025-10-25 15:45:00', 780000, 2),
('Mashhad', 'Tabriz', '2025-10-18 09:15:00', 560000, 6);
UPDATE trip SET departure_date = '2025-10-13 08:30:00' WHERE id = 14;
-- 💺 CHAIRS
INSERT INTO chair (number, trip_id)
VALUES
(1, 11),
(2, 11),
(3, 11),
(4, 11),
(5, 11),

(1, 12),
(2, 12),
(3, 12),

(1, 13),
(2, 13),
(3, 13),
(4, 13),

(1, 14),
(2, 14),

(1, 15),
(2, 15),
(3, 15),
(4, 15),
(5, 15),
(6, 15);

INSERT INTO admin (username, password) VALUES ('tina', '1234');




CREATE TABLE user_test (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    name VARCHAR(50),
    wallet FLOAT DEFAULT 0
);

INSERT INTO trip (origin, destination, departure_date, price, capacity)
VALUES ('test', 'test', '2100-01-01 00:00:00', 0, 1000)

INSERT INTO chair (number, trip_id)
VALUES 
(1, 21),
(2, 21);