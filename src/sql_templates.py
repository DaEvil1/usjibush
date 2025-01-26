LOGIN_SQL = """
SELECT password_hash FROM "user" WHERE username = %(username)s
"""

GET_USER_SQL = """
SELECT * FROM "user" WHERE username = %(username)s
"""

GET_BURGER_LOCATIONS_SQL = """
SELECT id, "name" FROM burger_location order by "name"
"""

ADD_BURGER_REVIEW_SQL = """
INSERT INTO burger_review (user_id, burger_location_id, date, burger_name, bun_rating, bun_remarks, patty_rating, patty_remarks, toppings_rating, toppings_remarks, fries_rating, fries_remarks, location_rating, location_remarks, value_rating, value_remarks, x_factor_rating, x_factor_remarks)
VALUES ((SELECT id FROM "user" WHERE username = %(username)s), %(location)s, %(date)s, %(burger_name)s, %(bun_rating)s, %(bun_remarks)s, %(patty_rating)s, %(patty_remarks)s, %(toppings_rating)s, %(toppings_remarks)s, %(fries_rating)s, %(fries_remarks)s, %(location_rating)s, %(location_remarks)s, %(value_rating)s, %(value_remarks)s, %(x_factor_rating)s, %(x_factor_remarks)s)
"""

CHECK_EXISTING_BURGER_REVIEW_SQL = """
SELECT id FROM burger_review WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s) AND burger_location_id = %(location)s
"""

UPDATE_BURGER_REVIEW_SQL = """
UPDATE burger_review SET date = %(date)s, burger_name = %(burger_name)s, bun_rating = %(bun_rating)s, bun_remarks = %(bun_remarks)s, patty_rating = %(patty_rating)s, patty_remarks = %(patty_remarks)s, toppings_rating = %(toppings_rating)s, toppings_remarks = %(toppings_remarks)s, fries_rating = %(fries_rating)s, fries_remarks = %(fries_remarks)s, location_rating = %(location_rating)s, location_remarks = %(location_remarks)s, value_rating = %(value_rating)s, value_remarks = %(value_remarks)s, x_factor_rating = %(x_factor_rating)s, x_factor_remarks = %(x_factor_remarks)s
WHERE id = %(id)s
"""

GET_BURGER_REVIEWS_SQL = """
SELECT * FROM burger_review WHERE user_id = (SELECT id FROM "user" WHERE username = %(username)s)
"""

GET_ALL_BURGER_REVIEWS_SQL = """
SELECT * FROM burger_review
"""