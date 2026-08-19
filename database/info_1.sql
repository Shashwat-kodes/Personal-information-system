CREATE DATABASE IF NOT EXISTS pis_db;
USE pis_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE personal_details (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    gender VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------
-- DEMO ACCOUNT (for project presentation)
-- Username: demo   Password: demo123
-- Password below is already hashed with werkzeug's generate_password_hash,
-- matching what app.py expects — no extra setup needed.
-- ---------------------------------------------------------------

INSERT INTO users (username, password, email)
VALUES (
    'demo',
    'scrypt:32768:8:1$8Z7HyLsb5taNIF8O$348b565047783aa5492c24be63037f0e1993c2f06adbbcb5a1dd2d3e660714cf62e4446d7483246f5a28102f8b1b15d8488580418adb9b7f4b77dcaf2f73f881',
    'demo@example.com'
);

INSERT INTO personal_details (user_id, full_name, dob, gender, phone, email, address)
VALUES (
    LAST_INSERT_ID(),
    'Demo User',
    '2003-05-14',
    'Other',
    '+91 90000 00000',
    'demo@example.com',
    'BBD University, Lucknow'
);