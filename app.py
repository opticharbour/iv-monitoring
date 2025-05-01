from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_PATH = 'iv_monitoring.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            condition TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/staff_login', methods=['POST'])
def staff_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin123':
        session['user'] = 'staff'
        return redirect('/staff_home')
    else:
        return render_template('index.html', error='Invalid Staff Credentials')

@app.route('/patient_login', methods=['POST'])
def patient_login():
    patient_id = request.form['patient_id']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    cursor.execute('SELECT date, notes FROM history WHERE patient_id = ? ORDER BY date DESC', (patient_id,))
    history = cursor.fetchall()
    conn.close()
    if patient:
        return render_template('iv_interface.html', patient=patient, history=history)
    else:
        return render_template('index.html', error='Patient ID not found')

@app.route('/staff_home')
def staff_home():
    if 'user' in session and session['user'] == 'staff':
        return render_template('staff_home.html')
    return redirect('/')

@app.route('/new_patient')
def new_patient():
    return render_template('new_patient.html')

@app.route('/register_patient', methods=['POST'])
def register_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    condition = request.form['condition']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO patients (name, age, gender, condition) VALUES (?, ?, ?, ?)',
                   (name, age, gender, condition))
    conn.commit()
    patient_id = cursor.lastrowid
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return render_template('iv_interface.html', patient=patient, history=[])

@app.route('/existing_patient')
def existing_patient():
    return render_template('existing_patient.html')

@app.route('/load_existing_patient', methods=['POST'])
def load_existing_patient():
    patient_id = request.form['patient_id']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    cursor.execute('SELECT date, notes FROM history WHERE patient_id = ? ORDER BY date DESC', (patient_id,))
    history = cursor.fetchall()
    conn.close()
    if patient:
        return render_template('iv_interface.html', patient=patient, history=history)
    else:
        return render_template('existing_patient.html', error='Patient not found')

@app.route('/view_history')
def view_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_history.html', patients=patients)

@app.route('/add_history', methods=['POST'])
def add_history():
    patient_id = request.form['patient_id']
    notes = request.form['notes']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (patient_id, date, notes) VALUES (?, ?, ?)',
                   (patient_id, date, notes))
    conn.commit()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    cursor.execute('SELECT date, notes FROM history WHERE patient_id = ? ORDER BY date DESC', (patient_id,))
    history = cursor.fetchall()
    conn.close()
    return render_template('iv_interface.html', patient=patient, history=history)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
