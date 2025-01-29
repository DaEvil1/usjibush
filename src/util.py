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
    
    async def is_admin(self, username: str) -> bool:
        user = await self.db_adapter.fetchone(sql_templates.IS_ADMIN_SQL, {"username": username})
        return user[0]["is_admin"]
    
    async def change_password(self, username: str, password: str) -> None:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        await self.db_adapter.execute(sql_templates.CHANGE_PASSWORD_SQL, {"username": username, "password_hash": password_hash})
    
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
    
    async def get_burger_reviews(self, username: str, burger_location_id: int) -> dict:
        burger_review: list = await self.db_adapter.fetchall(sql_templates.GET_BURGER_REVIEW_SQL, {"username": username, "burger_location_id": burger_location_id})
        burger_review_dict = {
            id: None,
            "burger_location_id": burger_location_id,
            "bun_rating": 0,
            "bun_remarks": "",
            "patty_rating": 0,
            "patty_remarks": "",
            "toppings_rating": 0,
            "toppings_remarks": "",
            "fries_rating": 0,
            "fries_remarks": "",
            "location_rating": 0,
            "location_remarks": "",
            "value_rating": 0,
            "value_remarks": "",
            "x_factor_rating": 0,
            "x_factor_remarks": "",
        }
        if len(burger_review) == 1:
            burger_review_dict = burger_review[0]
        return burger_review_dict
    
    async def get_all_burger_reviews(self) -> list:
        burger_reviews: list = await self.db_adapter.fetchall(sql_templates.GET_ALL_BURGER_REVIEWS_SQL)
        for review in burger_reviews:
            for key, value in review.items():
                if 'remarks' in key and value is None:
                    review[key] = ""
        return burger_reviews

    async def get_deadpool_results(self) -> list:
        results_dict: dict = {}
        results = await self.db_adapter.fetchall(sql_templates.GET_DEADPOOL_RESULTS_SQL)
        for result in results:
            if result["month"] not in results_dict:
                results_dict[result["month"]] = []
            results_dict[result["month"]].append(result)
        return results_dict

    async def get_deadpool_guess(self, username: str) -> dict:
        guessed: list = await self.db_adapter.fetchone(sql_templates.GET_DEADPOOL_GUESS_SQL, {"username": username})
        return int(guessed[0]['amount']) if guessed else {}
    
    async def add_deadpool_guess(self, username: str, amount: int) -> None:
        existing_deadpool_guess_data = {
            "username": username,
        }
        guess = {
            "username": username,
            "amount": amount,
        }
        existing_deadpool_guess_id = await self.db_adapter.fetchone(sql_templates.CHECK_EXISTING_DEADPOOL_GUESS_SQL, {**existing_deadpool_guess_data})
        if existing_deadpool_guess_id:
            await self.db_adapter.execute(sql_templates.UPDATE_DEADPOOL_GUESS_SQL, {**guess})
        else:
            await self.db_adapter.execute(sql_templates.ADD_DEADPOOL_GUESS_SQL, {**guess})

    async def get_deadpool_answer_previous_month(self) -> dict:
        answer_previous_month: int = None
        db_result = await self.db_adapter.fetchone(sql_templates.GET_DEADPOOL_ANSWER_PREVIOUS_MONTH_SQL)
        if db_result:
            answer_previous_month = db_result[0]["amount"]
        return answer_previous_month
    
    async def set_deadpool_answer_previous_month(self, amount: int) -> None:
        existing_deadpool_answer_data = self.get_deadpool_answer_previous_month()
        if existing_deadpool_answer_data != None:
            await self.db_adapter.execute(sql_templates.UPDATE_DEADPOOL_ANSWER_PREVIOUS_MONTH_SQL, {"amount": amount})
        else:
            await self.db_adapter.execute(sql_templates.ADD_DEDPOOL_ANSWER_PREVIOUS_MONTH_SQL, {"amount": amount})
    
    async def set_deadpool_winners_previous_month(self) -> None:
        await self.db_adapter.execute(sql_templates.SET_DEADPOOL_WINNERS_PREVIOUS_MONTH_SQL)