import bcrypt

import sql_templates, db_adapter

class Util:

    def __init__(self, db_adapter: db_adapter.DBAdapter):
        self.db_adapter = db_adapter

    async def login(self, username: str, password: str) -> dict:
        success: bool = False
        user: dict = {}
        result: dict = await self.db_adapter.fetchone(sql_templates.LOGIN_SQL, {"username": username})
        if result:
            stored_hash = result[0]["password_hash"]
            success = bcrypt.checkpw(password.encode(), stored_hash.encode())
        if success:
            user = await self.db_adapter.fetchone(sql_templates.GET_USER_SQL, {"username": username})
        return {"success": success, "user": user[0]}
    
    async def generate_session_token(self, username: str) -> str:
        return bcrypt.hashpw(username.encode(), bcrypt.gensalt()).decode()