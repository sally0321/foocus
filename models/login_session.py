class LoginSession:
    _instance = None  # class-level attribute to hold singleton instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize attributes here to avoid repeated __init__ calls
            cls._instance.user_id = None
            cls._instance.username = None
        return cls._instance

    def set_user(self, user_id, username):
        if self.user_id is not None:
            raise RuntimeError("User already set! Only set once after login.")
        self.user_id = user_id
        self.username = username

    def get_user_id(self):
        return self.user_id

    def get_username(self):
       return self.username

    def clear_user(self):
        self.user_id = None
        self.username = None