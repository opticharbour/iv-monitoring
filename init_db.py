import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('iv_monitoring.db')
cursor = conn.cursor()

# Create a table for patients
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    case_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Database initialized successfully.")
