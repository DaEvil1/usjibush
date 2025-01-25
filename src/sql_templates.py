LOGIN_SQL = """
SELECT password_hash FROM "user" WHERE username = %(username)s
"""

GET_USER_SQL = """
SELECT * FROM "user" WHERE username = %(username)s
"""