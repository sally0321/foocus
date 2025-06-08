import uuid
import bcrypt

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QMessageBox

USERS_DB_CONNECTION_NAME = "foocus_users_db"
USERS_DATABASE_NAME = "foocus_users.db"


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
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

def register_user(username, password):
    query = QSqlQuery(QSqlDatabase.database(USERS_DB_CONNECTION_NAME))
    query.prepare("INSERT INTO users (id, username, password) VALUES (:id, :username, :password)")
    query.bindValue(":id", str(uuid.uuid4()))
    query.bindValue(":username", username)
    query.bindValue(":password", bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

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
    query.prepare("SELECT * FROM users WHERE username = :username")
    query.bindValue(":username", username)

    if query.exec() and query.next():
        user_id = query.value("id")
        hashed_pw = query.value("password")

        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))
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
        return {
            "status": "error",
            "message": "Invalid username."
        }
