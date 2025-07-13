class LoginSession:
    """Singleton class to manage user login session."""

    _instance = None  # to hold singleton instance
    
    def __new__(cls):
        """Create a new instance of LoginSession if it doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize user session attributes here instead of in __init__ to avoid re-initialization
            cls._instance.user_id = None
            cls._instance.username = None
        return cls._instance

    def set_user(self, user_id, username):
        """Set the user ID and username for the session."""
        if self.user_id is not None:
            raise RuntimeError("User already set! Only set once after login.")
        self.user_id = user_id
        self.username = username

    def get_user_id(self):
        return self.user_id

    def get_username(self):
       return self.username

    def clear_user(self):
        """Clear the user session."""
        self.user_id = None
        self.username = None