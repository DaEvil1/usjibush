LOGIN_SQL = """
SELECT password_hash FROM "user" WHERE username = %(username)s
"""

CHANGE_PASSWORD_SQL = """
UPDATE "user" SET password_hash = %(password_hash)s WHERE username = %(username)s
"""

GET_USER_SQL = """
SELECT * FROM "user" WHERE username = %(username)s
"""

GET_BURGER_LOCATIONS_SQL = """
SELECT id, "name" FROM burger_location order by "name"
"""

ADD_BURGER_REVIEW_SQL = """
INSERT INTO burger_review (
    user_id,
    burger_location_id,
    date,
    burger_name,
    bun_rating,
    bun_remarks,
    patty_rating,
    patty_remarks,
    toppings_rating,
    toppings_remarks,
    fries_rating,
    fries_remarks,
    taste_total_rating,
    taste_total_remarks,
    location_rating,
    location_remarks,
    value_rating, 
    value_remarks,
    x_factor_rating,
    x_factor_remarks)
VALUES (
    (SELECT id FROM "user" WHERE username = %(username)s),
    %(location)s,
    %(date)s,
    %(burger_name)s,
    %(bun_rating)s,
    %(bun_remarks)s,
    %(patty_rating)s,
    %(patty_remarks)s,
    %(toppings_rating)s,
    %(toppings_remarks)s,
    %(fries_rating)s,
    %(fries_remarks)s,
    %(taste_total_rating)s,
    %(taste_total_remarks)s,
    %(location_rating)s,
    %(location_remarks)s,
    %(value_rating)s,
    %(value_remarks)s,
    %(x_factor_rating)s,
    %(x_factor_remarks)s
    )
"""

CHECK_EXISTING_BURGER_REVIEW_SQL = """
SELECT id FROM burger_review WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s) AND burger_location_id = %(location)s
"""

UPDATE_BURGER_REVIEW_SQL = """
UPDATE burger_review SET
date = %(date)s,
burger_name = %(burger_name)s,
bun_rating = %(bun_rating)s,
bun_remarks = %(bun_remarks)s,
patty_rating = %(patty_rating)s,
patty_remarks = %(patty_remarks)s,
toppings_rating = %(toppings_rating)s,
toppings_remarks = %(toppings_remarks)s,
fries_rating = %(fries_rating)s,
fries_remarks = %(fries_remarks)s,
taste_total_rating = %(taste_total_rating)s,
taste_total_remarks = %(taste_total_remarks)s,
location_rating = %(location_rating)s,
location_remarks = %(location_remarks)s,
value_rating = %(value_rating)s,
value_remarks = %(value_remarks)s,
x_factor_rating = %(x_factor_rating)s,
x_factor_remarks = %(x_factor_remarks)s,
overall_remarks = %(overall_remarks)s
WHERE id = %(id)s
"""

GET_BURGER_REVIEW_SQL = """
SELECT * FROM burger_review WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s) AND burger_location_id = %(burger_location_id)s
"""

GET_ALL_BURGER_REVIEWS_SQL = """
SELECT 
br.id,
u.username,
bl."name" AS location,
br.date,
br.burger_name,
br.bun_rating,
br.bun_remarks,
br.patty_rating,
br.patty_remarks,
br.toppings_rating,
br.toppings_remarks,
br.fries_rating,
br.fries_remarks,
br.location_rating,
br.location_remarks,
br.value_rating,
br.value_remarks,
br.x_factor_rating,
br.x_factor_remarks,
br.overall_remarks
FROM burger_review br
JOIN "user" u ON br.user_id = u.id
JOIN burger_location bl ON br.burger_location_id = bl.id
ORDER BY br.date DESC, u.username
"""

GET_DEADPOOL_RESULTS_SQL = """
SELECT
u.username,
dr.month,
dr.year,
dr.amount as result_amount,
d.amount as guess_amount,
d.is_winner
FROM deadpool d
JOIN deadpool_result dr ON dr.month = d.month and dr.year = d.year
JOIN "user" u ON d.user_id = u.id
where 
    dr.year = extract(year from now()) and dr.month != 'December'
    or dr.year = extract(year from now()) - 1 and dr.month = 'December'
ORDER BY dr.year, dr.month, u.username
"""

GET_DEADPOOL_ANSWER_PREVIOUS_MONTH_SQL = """
SELECT
dr.amount
FROM deadpool_result dr
WHERE dr.month = (select "month" from get_previous_month_and_year())
and dr.year = (select "year" from get_previous_month_and_year())
"""

ADD_DEDPOOL_ANSWER_PREVIOUS_MONTH_SQL = """
INSERT INTO deadpool_result (month, year, amount)
VALUES ((select "month" from get_previous_month_and_year()), (select "year" from get_previous_month_and_year()), %(amount)s)
"""

UPDATE_DEADPOOL_ANSWER_PREVIOUS_MONTH_SQL = """
UPDATE deadpool_result
SET amount = %(amount)s
WHERE month = (select "month" from get_previous_month_and_year())
AND year = (select "year" from get_previous_month_and_year())
"""

GET_DEADPOOL_GUESS_SQL = """
with next_month as (
select extract(year from now()) as year, extract(month from now()) as month
)
SELECT
d.amount
FROM deadpool d
JOIN "user" u ON d.user_id = u.id
WHERE u.username = %(username)s
AND d.month = (select "month" from get_next_month_and_year())
and d.year = (select "year" from get_next_month_and_year())
"""

ADD_DEADPOOL_GUESS_SQL = """
INSERT INTO deadpool (user_id, month, year, amount)
VALUES ((SELECT id FROM "user" WHERE username = %(username)s),
(select "month" from get_next_month_and_year()),
(select "year" from get_next_month_and_year()),
%(amount)s)
"""

UPDATE_DEADPOOL_GUESS_SQL = """
UPDATE deadpool
SET amount = %(amount)s
WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s)
AND month = (select "month" from get_next_month_and_year())
AND year = (select "year" from get_next_month_and_year())
"""

CHECK_EXISTING_DEADPOOL_GUESS_SQL = """
SELECT id FROM deadpool WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s) 
AND month = (select "month" from get_next_month_and_year())
AND year = (select "year" from get_next_month_and_year())
"""

IS_ADMIN_SQL = """
SELECT
case when r.name = 'admin' then true else false end as is_admin
from "user" u
join "role" r on u.role_id = r.id
where u.username = %(username)s
"""

SET_DEADPOOL_WINNERS_PREVIOUS_MONTH_SQL = """
UPDATE deadpool d
SET is_winner = true
FROM deadpool_result dr
WHERE d.month = dr.month
AND d.year = dr.year
AND d.amount = (select min(amount) from deadpool where month = dr.month and year = dr.year)
AND dr.month = (select "month" from get_previous_month_and_year())
AND dr.year = (select "year" from get_previous_month_and_year())
"""