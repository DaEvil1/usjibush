import bcrypt

import sql_templates, db_adapter

class Util:

    def __init__(self, db_adapter: db_adapter.DBAdapter):
        self.db_adapter = db_adapter

    async def login(self, username: str, password: str) -> dict:
        success: bool = False
        user: dict = [{}]
        result: dict = await self.db_adapter.fetchone(sql_templates.LOGIN_SQL, {"username": username})
        if result:
            stored_hash = result[0]["password_hash"]
            success = bcrypt.checkpw(password.encode(), stored_hash.encode())
        if success:
            user = await self.db_adapter.fetchone(sql_templates.GET_USER_SQL, {"username": username})
        return {"success": success, "user": user[0]}
    
    async def generate_session_token(self, username: str) -> str:
        return bcrypt.hashpw(username.encode(), bcrypt.gensalt()).decode()
    
    async def get_burger_locations(self) -> list:
        return await self.db_adapter.fetchall(sql_templates.GET_BURGER_LOCATIONS_SQL)
    
    async def add_burger_review(self, username: str, review: dict) -> None:
        existing_burger_review_data = {
            "location": review["location"],
            "username": username,
        }
        review["username"] = username
        existing_burger_review_id = await self.db_adapter.fetchone(sql_templates.CHECK_EXISTING_BURGER_REVIEW_SQL, {**existing_burger_review_data})
        if existing_burger_review_id:
            review["id"] = existing_burger_review_id[0]["id"]
            await self.db_adapter.execute(sql_templates.UPDATE_BURGER_REVIEW_SQL, {**review})
        else:
            await self.db_adapter.execute(sql_templates.ADD_BURGER_REVIEW_SQL, {**review})
    
    async def get_burger_reviews(self, username: str) -> dict:
        burger_reviews: list = await self.db_adapter.fetchall(sql_templates.GET_BURGER_REVIEWS_SQL, {"username": username})
        burger_reviews_dict = {}
        for review in burger_reviews:
            burger_reviews_dict[review["burger_location_id"]] = review
        return burger_reviews_dict
    
    async def get_all_burger_reviews(self) -> list:
        return await self.db_adapter.fetchall(sql_templates.GET_ALL_BURGER_REVIEWS_SQL)