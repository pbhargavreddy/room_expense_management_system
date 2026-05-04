import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://bhargav:bhargav123!@localhost:5432/p2",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_schema():
    if not DATABASE_URL.startswith("postgresql"):
        return

    statements = [
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role VARCHAR NOT NULL DEFAULT 'user'
        """,
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            message TEXT NOT NULL,
            category VARCHAR NOT NULL,
            amount FLOAT,
            due_date DATE,
            sent_by INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notification_recipients (
            id SERIAL PRIMARY KEY,
            notification_id INTEGER NOT NULL REFERENCES notifications(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            is_read BOOLEAN NOT NULL DEFAULT FALSE,
            read_at TIMESTAMP WITHOUT TIME ZONE
        )
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
