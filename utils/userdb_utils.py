import uuid
import bcrypt

from PySide6.QtSql import QSqlDatabase, QSqlQuery

USERS_DB_CONNECTION_NAME = "foocus_users_db"
USERS_DATABASE_NAME = "foocus_users.db"


def initialize_userdb():
    """Initialize the SQLite database for user management."""

    # Connect to SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE", USERS_DB_CONNECTION_NAME)
    db.setDatabaseName(USERS_DATABASE_NAME)
    
    if not db.open():
        raise Exception("Database connection failed!")

    # Create users table if not exists
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.exec(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

def register_user(username, password):
    """Register a new user with a username and password during user sign up."""

    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Prepare the SQL query to insert a new user
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.prepare("INSERT INTO users (user_id, username, password) VALUES (:user_id, :username, :password)")
    query.bindValue(":user_id", user_id)
    query.bindValue(":username", username)
    query.bindValue(":password", bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')) # Hash the password for better security

    if not query.exec():
        # Check if the error is due to a unique constraint violation which indicates that the username already exists
        if "UNIQUE constraint failed" in query.lastError().text():
            return {
                "status": "error",
                "message": "Username already exists."
            }
        else:
            # Handle other database errors
            return {
                "status": "error",
                "message": "Registration failed."
            }
    else:
        return {
            "status": "success",
            "user_id": user_id
        }

def login_user(username, password):
    """Authenticate a user with a username and password during user login."""

    # Prepare the SQL query to find the user by username
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.prepare("SELECT * FROM users WHERE username = :username")
    query.bindValue(":username", username)

    # Execute the query and check if the user exists
    if query.exec() and query.next():
        user_id = query.value("user_id")
        hashed_password = query.value("password")

        # Verify the provided password against the stored hashed password
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')) # Change the input password and hashed password to bytes for comparison
        if is_valid:
            return {
                "status": "success",
                "user_id": user_id
            }
        else:
            return {
                "status": "error",
                "message": "Invalid password."
            }
    else:
        # If the query did not return any results, the username is invalid
        return {
            "status": "error",
            "message": "Invalid username."
        }
