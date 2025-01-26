CREATE TABLE IF NOT EXISTS "role" (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE
)
;

INSERT INTO "role" ("name") VALUES ('admin') ON CONFLICT DO NOTHING;
INSERT INTO "role" ("name") VALUES ('user') ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT FALSE,
    role_id BIGINT REFERENCES "role"(id) NOT NULL
)
;

CREATE TABLE IF NOT EXISTS deadpool (
    id SERIAL PRIMARY KEY,
    month TEXT NOT NULL,
    year INT NOT NULL,
    user_id BIGINT REFERENCES "user"(id) NOT NULL,
    amount INT NOT NULL,
    is_winner BOOLEAN NOT NULL DEFAULT FALSE
)
;

CREATE TABLE IF NOT EXISTS deadpool_result (
    id SERIAL PRIMARY KEY,
    month TEXT NOT NULL,
    year INT NOT NULL,
    amount INT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS burger_location (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE
)
;

INSERT INTO burger_location ("name") VALUES ('Bien Snackbar') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Royal Burger') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Holy Cow') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Burgern') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Hekkan') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Inside') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Dirty Vegan') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Fly Chicken') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Fridays') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Flame Burger') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Burger Boyz') ON CONFLICT DO NOTHING;
INSERT INTO burger_location ("name") VALUES ('Smash Burgers & Shakes') ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS burger_review (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES "user"(id) NOT NULL,
    burger_location_id BIGINT REFERENCES burger_location(id) NOT NULL,
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

-- functions
CREATE OR REPLACE FUNCTION get_next_month_and_year()
  RETURNS TABLE (
    "month" text,
    "year"   int
  )
  LANGUAGE sql
AS $function$
  SELECT 
    to_char(current_date + INTERVAL '1 month', 'FMMonth') AS "month",
    EXTRACT(YEAR FROM (current_date + INTERVAL '1 month'))::int AS "year"
;
$function$;