import sqlite3

def init_db():
    conn = sqlite3.connect('iv_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            case_details TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_patient(name, mobile, blood_group, case_details):
    conn = sqlite3.connect('iv_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, mobile, blood_group, case_details)
        VALUES (?, ?, ?, ?)
    ''', (name, mobile, blood_group, case_details))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = sqlite3.connect('iv_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients ORDER BY date_created DESC')
    patients = cursor.fetchall()
    conn.close()
    return patients
