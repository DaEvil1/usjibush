import session

class Sessions:

    def __init__(self):
        self.sessions = {}

    async def login(self, username: str, session_token: str):
        self.sessions[session_token] = session.Session(username, session_token)

    async def logout(self, session_token: str):
        self.sessions.pop(session_token, None)