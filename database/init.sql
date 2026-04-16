CREATE TABLE IF NOT EXISTS password_checks (
    id SERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    score INT NOT NULL,
    strength TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);