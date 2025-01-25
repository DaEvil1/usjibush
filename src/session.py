class Session:

    def __init__(self, username: str, session_token: str):
        self.username: str = username
        self.session_token: str = session_token