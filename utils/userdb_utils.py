from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QMessageBox

USERS_DB_CONNECTION_NAME = "users_db"
USERS_DATABASE_NAME = "users.db"


def initialize_userdb():
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

def register_user(username, password):
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.prepare("INSERT INTO users (username, password) VALUES (:username, :password)")
    query.bindValue(":username", username)
    query.bindValue(":password", password)

    if not query.exec():
        if "UNIQUE constraint failed" in query.lastError().text():
            return {
                "status": "error",
                "message": "Username already exists."
            }
        else:
            return {
                "status": "error",
                "message": "Registration failed."
            }
    else:
        return {
            "status": "success",
            "user_id": query.lastInsertId()
        }

def login_user(username, password):
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.prepare("SELECT * FROM users WHERE username = :username AND password = :password")
    query.bindValue(":username", username)
    query.bindValue(":password", password)

    if query.exec() and query.next():
        user_id = query.value("id")
        return {
            "status": "success",
            "user_id": user_id
        }
    else:
        return {
            "status": "error",
            "message": "Invalid username or password."
        }
