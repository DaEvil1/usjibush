CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS deadpool (
    id SERIAL PRIMARY KEY,
    month TEXT NOT NULL,
    year TEXT NOT NULL,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    amount INT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS burger_location (
    id SERIAL PRIMARY KEY,
    location TEXT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS burger_review (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    location BIGINT REFERENCES burger_location(id) NOT NULL,
    date DATE NOT NULL,
    burger_name TEXT NOT NULL,
    bun_rating INT NOT NULL,
    bun_remarks TEXT,
    patty_rating INT NOT NULL,
    patty_remarks TEXT,
    toppings_rating INT NOT NULL,
    toppings_remarks TEXT,
    fries_rating INT,
    fries_remarks TEXT,
    location_rating INT NOT NULL,
    location_remarks TEXT,
    value_rating INT NOT NULL,
    value_remarks TEXT,
    x_factor_rating INT NOT NULL,
    x_factor_remarks TEXT
)
;

CREATE TABLE IF NOT EXISTS approved_user_email (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
)
;