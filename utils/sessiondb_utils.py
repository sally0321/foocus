from tinydb import TinyDB
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
import uuid

from models.data import *

SESSION_LOG_DATABASE_NAME = "session_log.json"

SESSION_METRICS_DB_CONNECTION_NAME = "session_metrics_db"
SESSION_METRICS_DATABASE_NAME = "session_metrics.db"
SESSION_METRICS_TABLE_NAME = "session_metrics"

def initialize_session_log_db():
    return TinyDB(SESSION_LOG_DATABASE_NAME)

def initialize_session_metrics_db():
    db = QSqlDatabase.addDatabase("QSQLITE", SESSION_METRICS_DB_CONNECTION_NAME)
    db.setDatabaseName(SESSION_METRICS_DATABASE_NAME)
    if not db.open():
        raise RuntimeError("Could not open SQLite database")
    
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.exec(f"""
        CREATE TABLE IF NOT EXISTS {SESSION_METRICS_TABLE_NAME} (
            session_id TEXT PRIMARY KEY,
            saved_at TEXT NOT NULL,
            user_id TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            active_duration FLOAT NOT NULL,
            pause_duration FLOAT NOT NULL,
            attention_span FLOAT NOT NULL,
            frequency_unfocus INTEGER NOT NULL,
            focus_duration FLOAT NOT NULL,
            unfocus_duration FLOAT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

def insert_session_to_local_db(session_log: SessionLog, session_metrics: SessionMetrics):
    # Store raw data in TinyDB
    db = initialize_session_log_db()
    db.insert({
        "session_id": session_log.session_id,
        "svc_predictions": [int(x) for x in session_log.svc_predictions],
        "ear_values": [float(x) for x in session_log.ear_values]
    })

    # Store metrics in SQLite
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare("""
        INSERT INTO session_metrics (
            session_id,
            saved_at,
            user_id,
            start_time,
            end_time,
            active_duration,
            pause_duration,
            attention_span,
            frequency_unfocus,
            focus_duration,
            unfocus_duration
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)
    query.addBindValue(session_metrics.session_id)
    query.addBindValue(datetime.now().isoformat())
    query.addBindValue(session_metrics.user_id)
    query.addBindValue(session_metrics.start_time)
    query.addBindValue(session_metrics.end_time)
    query.addBindValue(session_metrics.active_duration)
    query.addBindValue(session_metrics.pause_duration)
    query.addBindValue(session_metrics.attention_span)
    query.addBindValue(session_metrics.frequency_unfocus)
    query.addBindValue(session_metrics.focus_duration)
    query.addBindValue(session_metrics.unfocus_duration)
    if not query.exec():
        print("Insert failed:", query.lastError().text())

def get_avg_attention_span(user_id):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"SELECT AVG(attention_span) FROM {SESSION_METRICS_TABLE_NAME} WHERE user_id = ?")
    query.addBindValue(user_id)
    query.exec()
    if query.next():
        avg_attention_span = query.value(0) or 0
        return avg_attention_span
    return None

def get_longest_attention_span(user_id):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"SELECT MAX(attention_span) FROM {SESSION_METRICS_TABLE_NAME} WHERE user_id = ?")
    query.addBindValue(user_id)
    query.exec()
    if query.next():
        longest_attention_span = query.value(0) or 0
        return longest_attention_span
    return None

def get_highest_unfocus_frequency(user_id):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"SELECT MAX(frequency_unfocus) FROM {SESSION_METRICS_TABLE_NAME} WHERE user_id = ?")
    query.addBindValue(user_id)
    query.exec()
    if query.next():
        highest_unfocus_frequency = query.value(0) or 0
        return highest_unfocus_frequency
    return None

def get_lowest_unfocus_frequency(user_id):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"SELECT MIN(frequency_unfocus) FROM {SESSION_METRICS_TABLE_NAME} WHERE user_id = ?")
    query.addBindValue(user_id)
    query.exec()
    if query.next():
        lowest_unfocus_frequency = query.value(0) or 0
        return lowest_unfocus_frequency
    return None

def get_recent_attention_spans(user_id, limit):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"""
        SELECT attention_span, saved_at
        FROM {SESSION_METRICS_TABLE_NAME}
        WHERE user_id = ?
        ORDER BY datetime(saved_at) DESC
        LIMIT {limit}
    """)
    query.addBindValue(user_id)

    # Execute and fetch results
    if query.exec():
        attention_spans = []
        while query.next():
            attention_span = query.value(0)
            saved_at = query.value(1)
            attention_spans.append((saved_at, attention_span))
        return attention_spans
    return None

def get_total_attention_span(user_id):
    query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
    query.prepare(f"SELECT SUM(attention_span) FROM {SESSION_METRICS_TABLE_NAME} WHERE user_id = ?")
    query.addBindValue(user_id)
    query.exec()
    if query.next():
        total_attention_span = query.value(0) or 0
        return total_attention_span
    return None

# def get_metrics(session_id):
#     query = QSqlQuery(QSqlDatabase.database(SESSION_METRICS_DB_CONNECTION_NAME))
#     query.prepare("SELECT * FROM session_metrics WHERE session_id = ?")
#     query.addBindValue(session_id)
#     if query.exec() and query.next():
#         return {
#             "session_id": query.value(0),
#             "avg_ear": query.value(1),
#             "focused_percent": query.value(2),
#             "timestamp": query.value(3)
#         }
#     return None

