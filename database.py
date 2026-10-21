
from pathlib import Path
import sqlite3

# Find the project directory
BASE_DIR = Path(__file__).resolve().parent

# Database and schema file locations
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "books.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_db():
    conn = sqlite3.connect(DB_PATH)

    # Return rows that can be accessed by column name
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    # Create the instance folder if needed
    INSTANCE_DIR.mkdir(exist_ok=True)

    conn = get_db()

    try:
        # Execute table creation and seed SQL
        conn.executescript(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
