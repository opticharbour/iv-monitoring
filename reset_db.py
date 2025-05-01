import sqlite3

# Connect to the database (will create it if it doesn't exist)
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Delete the old table if it exists
cursor.execute("DROP TABLE IF EXISTS patients")

# Create a new table with the correct columns
cursor.execute("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    condition TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ patients table has been reset with correct schema.")
