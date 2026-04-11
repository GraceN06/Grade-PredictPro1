from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
import sqlite3
import joblib
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from sklearn.linear_model import LinearRegression
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "students.db"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

model = joblib.load('model.pkl')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        admission_number TEXT UNIQUE,

        f1_math_t1 REAL, f1_math_t2 REAL, f1_math_t3 REAL,
        f1_english_t1 REAL, f1_english_t2 REAL, f1_english_t3 REAL,
        f1_biology_t1 REAL, f1_biology_t2 REAL, f1_biology_t3 REAL,
        f1_chemistry_t1 REAL, f1_chemistry_t2 REAL, f1_chemistry_t3 REAL,
        f1_physics_t1 REAL, f1_physics_t2 REAL, f1_physics_t3 REAL,
        f1_history_t1 REAL, f1_history_t2 REAL, f1_history_t3 REAL,
        f1_geography_t1 REAL, f1_geography_t2 REAL, f1_geography_t3 REAL,
        f1_business_t1 REAL, f1_business_t2 REAL, f1_business_t3 REAL,

        f2_math_t1 REAL, f2_math_t2 REAL, f2_math_t3 REAL,
        f2_english_t1 REAL, f2_english_t2 REAL, f2_english_t3 REAL,
        f2_biology_t1 REAL, f2_biology_t2 REAL, f2_biology_t3 REAL,
        f2_chemistry_t1 REAL, f2_chemistry_t2 REAL, f2_chemistry_t3 REAL,
        f2_physics_t1 REAL, f2_physics_t2 REAL, f2_physics_t3 REAL,
        f2_history_t1 REAL, f2_history_t2 REAL, f2_history_t3 REAL,
        f2_geography_t1 REAL, f2_geography_t2 REAL, f2_geography_t3 REAL,
        f2_business_t1 REAL, f2_business_t2 REAL, f2_business_t3 REAL,

        f3_math_t1 REAL, f3_math_t2 REAL, f3_math_t3 REAL,
        f3_english_t1 REAL, f3_english_t2 REAL, f3_english_t3 REAL,
        f3_biology_t1 REAL, f3_biology_t2 REAL, f3_biology_t3 REAL,
        f3_chemistry_t1 REAL, f3_chemistry_t2 REAL, f3_chemistry_t3 REAL,
        f3_physics_t1 REAL, f3_physics_t2 REAL, f3_physics_t3 REAL,
        f3_history_t1 REAL, f3_history_t2 REAL, f3_history_t3 REAL,
        f3_geography_t1 REAL, f3_geography_t2 REAL, f3_geography_t3 REAL,
        f3_business_t1 REAL, f3_business_t2 REAL, f3_business_t3 REAL,

        f4_math_t1 REAL, f4_math_t2 REAL, f4_math_t3 REAL,
        f4_english_t1 REAL, f4_english_t2 REAL, f4_english_t3 REAL,
        f4_biology_t1 REAL, f4_biology_t2 REAL, f4_biology_t3 REAL,
        f4_chemistry_t1 REAL, f4_chemistry_t2 REAL, f4_chemistry_t3 REAL,
        f4_physics_t1 REAL, f4_physics_t2 REAL, f4_physics_t3 REAL,
        f4_history_t1 REAL, f4_history_t2 REAL, f4_history_t3 REAL,
        f4_geography_t1 REAL, f4_geography_t2 REAL, f4_geography_t3 REAL,
        f4_business_t1 REAL, f4_business_t2 REAL, f4_business_t3 REAL,

        f1_math_avg REAL, f1_english_avg REAL, f1_biology_avg REAL, f1_chemistry_avg REAL,
        f1_physics_avg REAL, f1_history_avg REAL, f1_geography_avg REAL, f1_business_avg REAL,

        f2_math_avg REAL, f2_english_avg REAL, f2_biology_avg REAL, f2_chemistry_avg REAL,
        f2_physics_avg REAL, f2_history_avg REAL, f2_geography_avg REAL, f2_business_avg REAL,

        f3_math_avg REAL, f3_english_avg REAL, f3_biology_avg REAL, f3_chemistry_avg REAL,
        f3_physics_avg REAL, f3_history_avg REAL, f3_geography_avg REAL, f3_business_avg REAL,

        f4_math_avg REAL, f4_english_avg REAL, f4_biology_avg REAL, f4_chemistry_avg REAL,
        f4_physics_avg REAL, f4_history_avg REAL, f4_geography_avg REAL, f4_business_avg REAL,

        predicted_score REAL,
        predicted_grade TEXT,
        risk_status TEXT,
        lecturer_username TEXT
    )
""")

    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ("admin", "admin@gmail.com", "1234", "admin"))

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

    init_db()

def calc_avg(a, b, c):
    return round((float(a) + float(b) + float(c)) / 3, 2)

# Test login route
@app.route('/test-login')
def test_login():
   conn = get_db_connection()
   cursor = conn.cursor()

   cursor.execute(...)
   rows = cursor.fetchall()

   conn.close()
   return str(users)

# Run app
@app.route('/login', methods=['POST'])
def login():
    init_db()
    
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    expected_role = request.form['role'].strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()

    conn.close()

    if not user:
        return "Invalid username or password"

    actual_role = user['role'].strip().lower()

    if actual_role != expected_role:
        return f"This account is not registered as {expected_role}"

    session['username'] = user['username']
    session['role'] = user['role']

    if actual_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif actual_role == 'lecturer':
        return redirect(url_for('lecturer_dashboard'))
    elif actual_role == 'student':
        return redirect(url_for('student_dashboard'))

    return "Invalid role"


@app.route('/student-page')
def student_page():
    if 'user' not in session or session['role'] != 'student':
        return redirect(url_for('home'))

    user = request.args.get('user')
    return render_template('student.html', user=user)

@app.route('/lecturer-page')
def lecturer_page():
    if 'user' not in session or session['role'] != 'lecturer':
        return redirect(url_for('home'))

    return render_template('lecturer.html')

@app.route('/admin-page')
def admin_page():
    if 'user' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/student-dashboard')
def student_dashboard():
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('student_login'))

    admission_number = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE admission_number = ?
    """, (admission_number,))

    student = cursor.fetchone()
    conn.close()

    if not student:
        return f"No student record found for {admission_number}"

    # ===== FORM 1 TOTALS =====
    f1_t1_total = (
        student["f1_math_t1"] + student["f1_english_t1"] + student["f1_biology_t1"] + student["f1_chemistry_t1"] +
        student["f1_physics_t1"] + student["f1_history_t1"] + student["f1_geography_t1"] + student["f1_business_t1"]
    )
    f1_t2_total = (
        student["f1_math_t2"] + student["f1_english_t2"] + student["f1_biology_t2"] + student["f1_chemistry_t2"] +
        student["f1_physics_t2"] + student["f1_history_t2"] + student["f1_geography_t2"] + student["f1_business_t2"]
    )
    f1_t3_total = (
        student["f1_math_t3"] + student["f1_english_t3"] + student["f1_biology_t3"] + student["f1_chemistry_t3"] +
        student["f1_physics_t3"] + student["f1_history_t3"] + student["f1_geography_t3"] + student["f1_business_t3"]
    )
    f1_avg = round((f1_t1_total + f1_t2_total + f1_t3_total) / 24, 2)

    # ===== FORM 2 =====
    f2_t1_total = (
        student["f2_math_t1"] + student["f2_english_t1"] + student["f2_biology_t1"] + student["f2_chemistry_t1"] +
        student["f2_physics_t1"] + student["f2_history_t1"] + student["f2_geography_t1"] + student["f2_business_t1"]
    )
    f2_t2_total = (
        student["f2_math_t2"] + student["f2_english_t2"] + student["f2_biology_t2"] + student["f2_chemistry_t2"] +
        student["f2_physics_t2"] + student["f2_history_t2"] + student["f2_geography_t2"] + student["f2_business_t2"]
    )
    f2_t3_total = (
        student["f2_math_t3"] + student["f2_english_t3"] + student["f2_biology_t3"] + student["f2_chemistry_t3"] +
        student["f2_physics_t3"] + student["f2_history_t3"] + student["f2_geography_t3"] + student["f2_business_t3"]
    )
    f2_avg = round((f2_t1_total + f2_t2_total + f2_t3_total) / 24, 2)

    # ===== FORM 3 =====
    f3_t1_total = (
        student["f3_math_t1"] + student["f3_english_t1"] + student["f3_biology_t1"] + student["f3_chemistry_t1"] +
        student["f3_physics_t1"] + student["f3_history_t1"] + student["f3_geography_t1"] + student["f3_business_t1"]
    )
    f3_t2_total = (
        student["f3_math_t2"] + student["f3_english_t2"] + student["f3_biology_t2"] + student["f3_chemistry_t2"] +
        student["f3_physics_t2"] + student["f3_history_t2"] + student["f3_geography_t2"] + student["f3_business_t2"]
    )
    f3_t3_total = (
        student["f3_math_t3"] + student["f3_english_t3"] + student["f3_biology_t3"] + student["f3_chemistry_t3"] +
        student["f3_physics_t3"] + student["f3_history_t3"] + student["f3_geography_t3"] + student["f3_business_t3"]
    )
    f3_avg = round((f3_t1_total + f3_t2_total + f3_t3_total) / 24, 2)

    # ===== FORM 4 =====
    f4_t1_total = (
        student["f4_math_t1"] + student["f4_english_t1"] + student["f4_biology_t1"] + student["f4_chemistry_t1"] +
        student["f4_physics_t1"] + student["f4_history_t1"] + student["f4_geography_t1"] + student["f4_business_t1"]
    )
    f4_t2_total = (
        student["f4_math_t2"] + student["f4_english_t2"] + student["f4_biology_t2"] + student["f4_chemistry_t2"] +
        student["f4_physics_t2"] + student["f4_history_t2"] + student["f4_geography_t2"] + student["f4_business_t2"]
    )
    f4_t3_total = (
        student["f4_math_t3"] + student["f4_english_t3"] + student["f4_biology_t3"] + student["f4_chemistry_t3"] +
        student["f4_physics_t3"] + student["f4_history_t3"] + student["f4_geography_t3"] + student["f4_business_t3"]
    )
    f4_avg = round((f4_t1_total + f4_t2_total + f4_t3_total) / 24, 2)

    # ===== RISK =====
    if student['predicted_score'] >= 80:
        status = "Safe"
    elif student['predicted_score'] >= 50:
        status = "Warning"
    else:
        status = "At Risk"

    return render_template(
        'student.html',
        student=student,
        f1_t1_total=f1_t1_total, f1_t2_total=f1_t2_total, f1_t3_total=f1_t3_total, f1_avg=f1_avg,
        f2_t1_total=f2_t1_total, f2_t2_total=f2_t2_total, f2_t3_total=f2_t3_total, f2_avg=f2_avg,
        f3_t1_total=f3_t1_total, f3_t2_total=f3_t2_total, f3_t3_total=f3_t3_total, f3_avg=f3_avg,
        f4_t1_total=f4_t1_total, f4_t2_total=f4_t2_total, f4_t3_total=f4_t3_total, f4_avg=f4_avg,
        status=status
    )

# Lecturer dasboard
@app.route('/lecturer-dashboard')
def lecturer_dashboard():
    if 'username' not in session or session.get('role') != 'lecturer':
        return redirect(url_for('lecturer_login'))

    lecturer_username = session['username']
    search_admission = request.args.get('admission_number', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    if search_admission:
        cursor.execute("""
            SELECT *
            FROM students
            WHERE lecturer_username = ? AND admission_number LIKE ?
        """, (lecturer_username, f"%{search_admission}%"))
    else:
        cursor.execute("""
            SELECT *
            FROM students
            WHERE lecturer_username = ?
        """, (lecturer_username,))

    rows = cursor.fetchall()
    conn.close()

    students = []

    for row in rows:
        # Form 1 totals
        f1_t1_total = (
            row["f1_math_t1"] + row["f1_english_t1"] + row["f1_biology_t1"] + row["f1_chemistry_t1"] +
            row["f1_physics_t1"] + row["f1_history_t1"] + row["f1_geography_t1"] + row["f1_business_t1"]
        )
        f1_t2_total = (
            row["f1_math_t2"] + row["f1_english_t2"] + row["f1_biology_t2"] + row["f1_chemistry_t2"] +
            row["f1_physics_t2"] + row["f1_history_t2"] + row["f1_geography_t2"] + row["f1_business_t2"]
        )
        f1_t3_total = (
            row["f1_math_t3"] + row["f1_english_t3"] + row["f1_biology_t3"] + row["f1_chemistry_t3"] +
            row["f1_physics_t3"] + row["f1_history_t3"] + row["f1_geography_t3"] + row["f1_business_t3"]
        )
        f1_form_average = round((f1_t1_total + f1_t2_total + f1_t3_total) / 24, 2)

        # Form 2 totals
        f2_t1_total = (
            row["f2_math_t1"] + row["f2_english_t1"] + row["f2_biology_t1"] + row["f2_chemistry_t1"] +
            row["f2_physics_t1"] + row["f2_history_t1"] + row["f2_geography_t1"] + row["f2_business_t1"]
        )
        f2_t2_total = (
            row["f2_math_t2"] + row["f2_english_t2"] + row["f2_biology_t2"] + row["f2_chemistry_t2"] +
            row["f2_physics_t2"] + row["f2_history_t2"] + row["f2_geography_t2"] + row["f2_business_t2"]
        )
        f2_t3_total = (
            row["f2_math_t3"] + row["f2_english_t3"] + row["f2_biology_t3"] + row["f2_chemistry_t3"] +
            row["f2_physics_t3"] + row["f2_history_t3"] + row["f2_geography_t3"] + row["f2_business_t3"]
        )
        f2_form_average = round((f2_t1_total + f2_t2_total + f2_t3_total) / 24, 2)

        # Form 3 totals
        f3_t1_total = (
            row["f3_math_t1"] + row["f3_english_t1"] + row["f3_biology_t1"] + row["f3_chemistry_t1"] +
            row["f3_physics_t1"] + row["f3_history_t1"] + row["f3_geography_t1"] + row["f3_business_t1"]
        )
        f3_t2_total = (
            row["f3_math_t2"] + row["f3_english_t2"] + row["f3_biology_t2"] + row["f3_chemistry_t2"] +
            row["f3_physics_t2"] + row["f3_history_t2"] + row["f3_geography_t2"] + row["f3_business_t2"]
        )
        f3_t3_total = (
            row["f3_math_t3"] + row["f3_english_t3"] + row["f3_biology_t3"] + row["f3_chemistry_t3"] +
            row["f3_physics_t3"] + row["f3_history_t3"] + row["f3_geography_t3"] + row["f3_business_t3"]
        )
        f3_form_average = round((f3_t1_total + f3_t2_total + f3_t3_total) / 24, 2)

        # Form 4 totals
        f4_t1_total = (
            row["f4_math_t1"] + row["f4_english_t1"] + row["f4_biology_t1"] + row["f4_chemistry_t1"] +
            row["f4_physics_t1"] + row["f4_history_t1"] + row["f4_geography_t1"] + row["f4_business_t1"]
        )
        f4_t2_total = (
            row["f4_math_t2"] + row["f4_english_t2"] + row["f4_biology_t2"] + row["f4_chemistry_t2"] +
            row["f4_physics_t2"] + row["f4_history_t2"] + row["f4_geography_t2"] + row["f4_business_t2"]
        )
        f4_t3_total = (
            row["f4_math_t3"] + row["f4_english_t3"] + row["f4_biology_t3"] + row["f4_chemistry_t3"] +
            row["f4_physics_t3"] + row["f4_history_t3"] + row["f4_geography_t3"] + row["f4_business_t3"]
        )
        f4_form_average = round((f4_t1_total + f4_t2_total + f4_t3_total) / 24, 2)

        students.append({
            "id": row["id"],
            "name": row["name"],
            "admission_number": row["admission_number"],

            "f1_math_t1": row["f1_math_t1"], "f1_math_t2": row["f1_math_t2"], "f1_math_t3": row["f1_math_t3"],
            "f1_english_t1": row["f1_english_t1"], "f1_english_t2": row["f1_english_t2"], "f1_english_t3": row["f1_english_t3"],
            "f1_biology_t1": row["f1_biology_t1"], "f1_biology_t2": row["f1_biology_t2"], "f1_biology_t3": row["f1_biology_t3"],
            "f1_chemistry_t1": row["f1_chemistry_t1"], "f1_chemistry_t2": row["f1_chemistry_t2"], "f1_chemistry_t3": row["f1_chemistry_t3"],
            "f1_physics_t1": row["f1_physics_t1"], "f1_physics_t2": row["f1_physics_t2"], "f1_physics_t3": row["f1_physics_t3"],
            "f1_history_t1": row["f1_history_t1"], "f1_history_t2": row["f1_history_t2"], "f1_history_t3": row["f1_history_t3"],
            "f1_geography_t1": row["f1_geography_t1"], "f1_geography_t2": row["f1_geography_t2"], "f1_geography_t3": row["f1_geography_t3"],
            "f1_business_t1": row["f1_business_t1"], "f1_business_t2": row["f1_business_t2"], "f1_business_t3": row["f1_business_t3"],

            "f2_math_t1": row["f2_math_t1"], "f2_math_t2": row["f2_math_t2"], "f2_math_t3": row["f2_math_t3"],
            "f2_english_t1": row["f2_english_t1"], "f2_english_t2": row["f2_english_t2"], "f2_english_t3": row["f2_english_t3"],
            "f2_biology_t1": row["f2_biology_t1"], "f2_biology_t2": row["f2_biology_t2"], "f2_biology_t3": row["f2_biology_t3"],
            "f2_chemistry_t1": row["f2_chemistry_t1"], "f2_chemistry_t2": row["f2_chemistry_t2"], "f2_chemistry_t3": row["f2_chemistry_t3"],
            "f2_physics_t1": row["f2_physics_t1"], "f2_physics_t2": row["f2_physics_t2"], "f2_physics_t3": row["f2_physics_t3"],
            "f2_history_t1": row["f2_history_t1"], "f2_history_t2": row["f2_history_t2"], "f2_history_t3": row["f2_history_t3"],
            "f2_geography_t1": row["f2_geography_t1"], "f2_geography_t2": row["f2_geography_t2"], "f2_geography_t3": row["f2_geography_t3"],
            "f2_business_t1": row["f2_business_t1"], "f2_business_t2": row["f2_business_t2"], "f2_business_t3": row["f2_business_t3"],

            "f3_math_t1": row["f3_math_t1"], "f3_math_t2": row["f3_math_t2"], "f3_math_t3": row["f3_math_t3"],
            "f3_english_t1": row["f3_english_t1"], "f3_english_t2": row["f3_english_t2"], "f3_english_t3": row["f3_english_t3"],
            "f3_biology_t1": row["f3_biology_t1"], "f3_biology_t2": row["f3_biology_t2"], "f3_biology_t3": row["f3_biology_t3"],
            "f3_chemistry_t1": row["f3_chemistry_t1"], "f3_chemistry_t2": row["f3_chemistry_t2"], "f3_chemistry_t3": row["f3_chemistry_t3"],
            "f3_physics_t1": row["f3_physics_t1"], "f3_physics_t2": row["f3_physics_t2"], "f3_physics_t3": row["f3_physics_t3"],
            "f3_history_t1": row["f3_history_t1"], "f3_history_t2": row["f3_history_t2"], "f3_history_t3": row["f3_history_t3"],
            "f3_geography_t1": row["f3_geography_t1"], "f3_geography_t2": row["f3_geography_t2"], "f3_geography_t3": row["f3_geography_t3"],
            "f3_business_t1": row["f3_business_t1"], "f3_business_t2": row["f3_business_t2"], "f3_business_t3": row["f3_business_t3"],

            "f4_math_t1": row["f4_math_t1"], "f4_math_t2": row["f4_math_t2"], "f4_math_t3": row["f4_math_t3"],
            "f4_english_t1": row["f4_english_t1"], "f4_english_t2": row["f4_english_t2"], "f4_english_t3": row["f4_english_t3"],
            "f4_biology_t1": row["f4_biology_t1"], "f4_biology_t2": row["f4_biology_t2"], "f4_biology_t3": row["f4_biology_t3"],
            "f4_chemistry_t1": row["f4_chemistry_t1"], "f4_chemistry_t2": row["f4_chemistry_t2"], "f4_chemistry_t3": row["f4_chemistry_t3"],
            "f4_physics_t1": row["f4_physics_t1"], "f4_physics_t2": row["f4_physics_t2"], "f4_physics_t3": row["f4_physics_t3"],
            "f4_history_t1": row["f4_history_t1"], "f4_history_t2": row["f4_history_t2"], "f4_history_t3": row["f4_history_t3"],
            "f4_geography_t1": row["f4_geography_t1"], "f4_geography_t2": row["f4_geography_t2"], "f4_geography_t3": row["f4_geography_t3"],
            "f4_business_t1": row["f4_business_t1"], "f4_business_t2": row["f4_business_t2"], "f4_business_t3": row["f4_business_t3"],

            "f1_math_avg": row["f1_math_avg"], "f1_english_avg": row["f1_english_avg"], "f1_biology_avg": row["f1_biology_avg"], "f1_chemistry_avg": row["f1_chemistry_avg"],
            "f1_physics_avg": row["f1_physics_avg"], "f1_history_avg": row["f1_history_avg"], "f1_geography_avg": row["f1_geography_avg"], "f1_business_avg": row["f1_business_avg"],

            "f2_math_avg": row["f2_math_avg"], "f2_english_avg": row["f2_english_avg"], "f2_biology_avg": row["f2_biology_avg"], "f2_chemistry_avg": row["f2_chemistry_avg"],
            "f2_physics_avg": row["f2_physics_avg"], "f2_history_avg": row["f2_history_avg"], "f2_geography_avg": row["f2_geography_avg"], "f2_business_avg": row["f2_business_avg"],

            "f3_math_avg": row["f3_math_avg"], "f3_english_avg": row["f3_english_avg"], "f3_biology_avg": row["f3_biology_avg"], "f3_chemistry_avg": row["f3_chemistry_avg"],
            "f3_physics_avg": row["f3_physics_avg"], "f3_history_avg": row["f3_history_avg"], "f3_geography_avg": row["f3_geography_avg"], "f3_business_avg": row["f3_business_avg"],

            "f4_math_avg": row["f4_math_avg"], "f4_english_avg": row["f4_english_avg"], "f4_biology_avg": row["f4_biology_avg"], "f4_chemistry_avg": row["f4_chemistry_avg"],
            "f4_physics_avg": row["f4_physics_avg"], "f4_history_avg": row["f4_history_avg"], "f4_geography_avg": row["f4_geography_avg"], "f4_business_avg": row["f4_business_avg"],

            "f1_t1_total": f1_t1_total,
            "f1_t2_total": f1_t2_total,
            "f1_t3_total": f1_t3_total,
            "f1_form_average": f1_form_average,

            "f2_t1_total": f2_t1_total,
            "f2_t2_total": f2_t2_total,
            "f2_t3_total": f2_t3_total,
            "f2_form_average": f2_form_average,

            "f3_t1_total": f3_t1_total,
            "f3_t2_total": f3_t2_total,
            "f3_t3_total": f3_t3_total,
            "f3_form_average": f3_form_average,

            "f4_t1_total": f4_t1_total,
            "f4_t2_total": f4_t2_total,
            "f4_t3_total": f4_t3_total,
            "f4_form_average": f4_form_average,

            "predicted_score": row["predicted_score"],
            "predicted_grade": row["predicted_grade"],
            "risk_status": row["risk_status"]
        })

    students.sort(key=lambda s: s["predicted_score"], reverse=True)

    for index, student in enumerate(students, start=1):
        student["rank"] = index

    return render_template(
        'lecturer.html',
        students=students,
        search_admission=search_admission
    )

@app.route('/add-student', methods=['POST'])
def add_student():
    if 'username' not in session or session.get('role') != 'lecturer':
        return jsonify({"message": "Unauthorized"}), 403

    lecturer_username = session['username']
    data = request.get_json()

    try:
        name = data['name'].strip()
        admission_number = data['admission_number'].strip()

        # ---------- FORM 1 ----------
        f1_math_t1 = float(data['f1_math_t1'])
        f1_math_t2 = float(data['f1_math_t2'])
        f1_math_t3 = float(data['f1_math_t3'])

        f1_english_t1 = float(data['f1_english_t1'])
        f1_english_t2 = float(data['f1_english_t2'])
        f1_english_t3 = float(data['f1_english_t3'])

        f1_biology_t1 = float(data['f1_biology_t1'])
        f1_biology_t2 = float(data['f1_biology_t2'])
        f1_biology_t3 = float(data['f1_biology_t3'])

        f1_chemistry_t1 = float(data['f1_chemistry_t1'])
        f1_chemistry_t2 = float(data['f1_chemistry_t2'])
        f1_chemistry_t3 = float(data['f1_chemistry_t3'])

        f1_physics_t1 = float(data['f1_physics_t1'])
        f1_physics_t2 = float(data['f1_physics_t2'])
        f1_physics_t3 = float(data['f1_physics_t3'])

        f1_history_t1 = float(data['f1_history_t1'])
        f1_history_t2 = float(data['f1_history_t2'])
        f1_history_t3 = float(data['f1_history_t3'])

        f1_geography_t1 = float(data['f1_geography_t1'])
        f1_geography_t2 = float(data['f1_geography_t2'])
        f1_geography_t3 = float(data['f1_geography_t3'])

        f1_business_t1 = float(data['f1_business_t1'])
        f1_business_t2 = float(data['f1_business_t2'])
        f1_business_t3 = float(data['f1_business_t3'])

        # ---------- FORM 2 ----------
        f2_math_t1 = float(data['f2_math_t1'])
        f2_math_t2 = float(data['f2_math_t2'])
        f2_math_t3 = float(data['f2_math_t3'])

        f2_english_t1 = float(data['f2_english_t1'])
        f2_english_t2 = float(data['f2_english_t2'])
        f2_english_t3 = float(data['f2_english_t3'])

        f2_biology_t1 = float(data['f2_biology_t1'])
        f2_biology_t2 = float(data['f2_biology_t2'])
        f2_biology_t3 = float(data['f2_biology_t3'])

        f2_chemistry_t1 = float(data['f2_chemistry_t1'])
        f2_chemistry_t2 = float(data['f2_chemistry_t2'])
        f2_chemistry_t3 = float(data['f2_chemistry_t3'])

        f2_physics_t1 = float(data['f2_physics_t1'])
        f2_physics_t2 = float(data['f2_physics_t2'])
        f2_physics_t3 = float(data['f2_physics_t3'])

        f2_history_t1 = float(data['f2_history_t1'])
        f2_history_t2 = float(data['f2_history_t2'])
        f2_history_t3 = float(data['f2_history_t3'])

        f2_geography_t1 = float(data['f2_geography_t1'])
        f2_geography_t2 = float(data['f2_geography_t2'])
        f2_geography_t3 = float(data['f2_geography_t3'])

        f2_business_t1 = float(data['f2_business_t1'])
        f2_business_t2 = float(data['f2_business_t2'])
        f2_business_t3 = float(data['f2_business_t3'])

        # ---------- FORM 3 ----------
        f3_math_t1 = float(data['f3_math_t1'])
        f3_math_t2 = float(data['f3_math_t2'])
        f3_math_t3 = float(data['f3_math_t3'])

        f3_english_t1 = float(data['f3_english_t1'])
        f3_english_t2 = float(data['f3_english_t2'])
        f3_english_t3 = float(data['f3_english_t3'])

        f3_biology_t1 = float(data['f3_biology_t1'])
        f3_biology_t2 = float(data['f3_biology_t2'])
        f3_biology_t3 = float(data['f3_biology_t3'])

        f3_chemistry_t1 = float(data['f3_chemistry_t1'])
        f3_chemistry_t2 = float(data['f3_chemistry_t2'])
        f3_chemistry_t3 = float(data['f3_chemistry_t3'])

        f3_physics_t1 = float(data['f3_physics_t1'])
        f3_physics_t2 = float(data['f3_physics_t2'])
        f3_physics_t3 = float(data['f3_physics_t3'])

        f3_history_t1 = float(data['f3_history_t1'])
        f3_history_t2 = float(data['f3_history_t2'])
        f3_history_t3 = float(data['f3_history_t3'])

        f3_geography_t1 = float(data['f3_geography_t1'])
        f3_geography_t2 = float(data['f3_geography_t2'])
        f3_geography_t3 = float(data['f3_geography_t3'])

        f3_business_t1 = float(data['f3_business_t1'])
        f3_business_t2 = float(data['f3_business_t2'])
        f3_business_t3 = float(data['f3_business_t3'])

        # ---------- FORM 4 ----------
        f4_math_t1 = float(data['f4_math_t1'])
        f4_math_t2 = float(data['f4_math_t2'])
        f4_math_t3 = float(data['f4_math_t3'])

        f4_english_t1 = float(data['f4_english_t1'])
        f4_english_t2 = float(data['f4_english_t2'])
        f4_english_t3 = float(data['f4_english_t3'])

        f4_biology_t1 = float(data['f4_biology_t1'])
        f4_biology_t2 = float(data['f4_biology_t2'])
        f4_biology_t3 = float(data['f4_biology_t3'])

        f4_chemistry_t1 = float(data['f4_chemistry_t1'])
        f4_chemistry_t2 = float(data['f4_chemistry_t2'])
        f4_chemistry_t3 = float(data['f4_chemistry_t3'])

        f4_physics_t1 = float(data['f4_physics_t1'])
        f4_physics_t2 = float(data['f4_physics_t2'])
        f4_physics_t3 = float(data['f4_physics_t3'])

        f4_history_t1 = float(data['f4_history_t1'])
        f4_history_t2 = float(data['f4_history_t2'])
        f4_history_t3 = float(data['f4_history_t3'])

        f4_geography_t1 = float(data['f4_geography_t1'])
        f4_geography_t2 = float(data['f4_geography_t2'])
        f4_geography_t3 = float(data['f4_geography_t3'])

        f4_business_t1 = float(data['f4_business_t1'])
        f4_business_t2 = float(data['f4_business_t2'])
        f4_business_t3 = float(data['f4_business_t3'])

        # ---------- AVERAGES ----------
        f1_math_avg = calc_avg(f1_math_t1, f1_math_t2, f1_math_t3)
        f1_english_avg = calc_avg(f1_english_t1, f1_english_t2, f1_english_t3)
        f1_biology_avg = calc_avg(f1_biology_t1, f1_biology_t2, f1_biology_t3)
        f1_chemistry_avg = calc_avg(f1_chemistry_t1, f1_chemistry_t2, f1_chemistry_t3)
        f1_physics_avg = calc_avg(f1_physics_t1, f1_physics_t2, f1_physics_t3)
        f1_history_avg = calc_avg(f1_history_t1, f1_history_t2, f1_history_t3)
        f1_geography_avg = calc_avg(f1_geography_t1, f1_geography_t2, f1_geography_t3)
        f1_business_avg = calc_avg(f1_business_t1, f1_business_t2, f1_business_t3)

        f2_math_avg = calc_avg(f2_math_t1, f2_math_t2, f2_math_t3)
        f2_english_avg = calc_avg(f2_english_t1, f2_english_t2, f2_english_t3)
        f2_biology_avg = calc_avg(f2_biology_t1, f2_biology_t2, f2_biology_t3)
        f2_chemistry_avg = calc_avg(f2_chemistry_t1, f2_chemistry_t2, f2_chemistry_t3)
        f2_physics_avg = calc_avg(f2_physics_t1, f2_physics_t2, f2_physics_t3)
        f2_history_avg = calc_avg(f2_history_t1, f2_history_t2, f2_history_t3)
        f2_geography_avg = calc_avg(f2_geography_t1, f2_geography_t2, f2_geography_t3)
        f2_business_avg = calc_avg(f2_business_t1, f2_business_t2, f2_business_t3)

        f3_math_avg = calc_avg(f3_math_t1, f3_math_t2, f3_math_t3)
        f3_english_avg = calc_avg(f3_english_t1, f3_english_t2, f3_english_t3)
        f3_biology_avg = calc_avg(f3_biology_t1, f3_biology_t2, f3_biology_t3)
        f3_chemistry_avg = calc_avg(f3_chemistry_t1, f3_chemistry_t2, f3_chemistry_t3)
        f3_physics_avg = calc_avg(f3_physics_t1, f3_physics_t2, f3_physics_t3)
        f3_history_avg = calc_avg(f3_history_t1, f3_history_t2, f3_history_t3)
        f3_geography_avg = calc_avg(f3_geography_t1, f3_geography_t2, f3_geography_t3)
        f3_business_avg = calc_avg(f3_business_t1, f3_business_t2, f3_business_t3)

        f4_math_avg = calc_avg(f4_math_t1, f4_math_t2, f4_math_t3)
        f4_english_avg = calc_avg(f4_english_t1, f4_english_t2, f4_english_t3)
        f4_biology_avg = calc_avg(f4_biology_t1, f4_biology_t2, f4_biology_t3)
        f4_chemistry_avg = calc_avg(f4_chemistry_t1, f4_chemistry_t2, f4_chemistry_t3)
        f4_physics_avg = calc_avg(f4_physics_t1, f4_physics_t2, f4_physics_t3)
        f4_history_avg = calc_avg(f4_history_t1, f4_history_t2, f4_history_t3)
        f4_geography_avg = calc_avg(f4_geography_t1, f4_geography_t2, f4_geography_t3)
        f4_business_avg = calc_avg(f4_business_t1, f4_business_t2, f4_business_t3)

        input_data = pd.DataFrame(
            [[
                f1_math_avg, f1_english_avg, f1_biology_avg, f1_chemistry_avg,
                f1_physics_avg, f1_history_avg, f1_geography_avg, f1_business_avg,

                f2_math_avg, f2_english_avg, f2_biology_avg, f2_chemistry_avg,
                f2_physics_avg, f2_history_avg, f2_geography_avg, f2_business_avg,

                f3_math_avg, f3_english_avg, f3_biology_avg, f3_chemistry_avg,
                f3_physics_avg, f3_history_avg, f3_geography_avg, f3_business_avg,

                f4_math_avg, f4_english_avg, f4_biology_avg, f4_chemistry_avg,
                f4_physics_avg, f4_history_avg, f4_geography_avg, f4_business_avg
            ]],
            columns=[
                'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
                'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',

                'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
                'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',

                'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
                'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',

                'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
                'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg'
            ]
        )

        predicted_score = model.predict(input_data)
        final_score = min(round(float(predicted_score[0]), 1), 100)

        if final_score >= 80:
            grade = "A"
            risk_status = "Safe"
        elif final_score >= 50:
            grade = "B"
            risk_status = "Warning"
        else:
            grade = "C"
            risk_status = "At Risk"

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE admission_number = ?", (admission_number,))
        existing_student = cursor.fetchone()

        if existing_student:
            conn.close()
            return jsonify({"message": "Admission number already exists"}), 400

        columns = [
            "name", "admission_number",

            "f1_math_t1", "f1_math_t2", "f1_math_t3",
            "f1_english_t1", "f1_english_t2", "f1_english_t3",
            "f1_biology_t1", "f1_biology_t2", "f1_biology_t3",
            "f1_chemistry_t1", "f1_chemistry_t2", "f1_chemistry_t3",
            "f1_physics_t1", "f1_physics_t2", "f1_physics_t3",
            "f1_history_t1", "f1_history_t2", "f1_history_t3",
            "f1_geography_t1", "f1_geography_t2", "f1_geography_t3",
            "f1_business_t1", "f1_business_t2", "f1_business_t3",

            "f2_math_t1", "f2_math_t2", "f2_math_t3",
            "f2_english_t1", "f2_english_t2", "f2_english_t3",
            "f2_biology_t1", "f2_biology_t2", "f2_biology_t3",
            "f2_chemistry_t1", "f2_chemistry_t2", "f2_chemistry_t3",
            "f2_physics_t1", "f2_physics_t2", "f2_physics_t3",
            "f2_history_t1", "f2_history_t2", "f2_history_t3",
            "f2_geography_t1", "f2_geography_t2", "f2_geography_t3",
            "f2_business_t1", "f2_business_t2", "f2_business_t3",

            "f3_math_t1", "f3_math_t2", "f3_math_t3",
            "f3_english_t1", "f3_english_t2", "f3_english_t3",
            "f3_biology_t1", "f3_biology_t2", "f3_biology_t3",
            "f3_chemistry_t1", "f3_chemistry_t2", "f3_chemistry_t3",
            "f3_physics_t1", "f3_physics_t2", "f3_physics_t3",
            "f3_history_t1", "f3_history_t2", "f3_history_t3",
            "f3_geography_t1", "f3_geography_t2", "f3_geography_t3",
            "f3_business_t1", "f3_business_t2", "f3_business_t3",

            "f4_math_t1", "f4_math_t2", "f4_math_t3",
            "f4_english_t1", "f4_english_t2", "f4_english_t3",
            "f4_biology_t1", "f4_biology_t2", "f4_biology_t3",
            "f4_chemistry_t1", "f4_chemistry_t2", "f4_chemistry_t3",
            "f4_physics_t1", "f4_physics_t2", "f4_physics_t3",
            "f4_history_t1", "f4_history_t2", "f4_history_t3",
            "f4_geography_t1", "f4_geography_t2", "f4_geography_t3",
            "f4_business_t1", "f4_business_t2", "f4_business_t3",

            "f1_math_avg", "f1_english_avg", "f1_biology_avg", "f1_chemistry_avg",
            "f1_physics_avg", "f1_history_avg", "f1_geography_avg", "f1_business_avg",

            "f2_math_avg", "f2_english_avg", "f2_biology_avg", "f2_chemistry_avg",
            "f2_physics_avg", "f2_history_avg", "f2_geography_avg", "f2_business_avg",

            "f3_math_avg", "f3_english_avg", "f3_biology_avg", "f3_chemistry_avg",
            "f3_physics_avg", "f3_history_avg", "f3_geography_avg", "f3_business_avg",

            "f4_math_avg", "f4_english_avg", "f4_biology_avg", "f4_chemistry_avg",
            "f4_physics_avg", "f4_history_avg", "f4_geography_avg", "f4_business_avg",

            "predicted_score", "predicted_grade", "risk_status", "lecturer_username"
        ]

        values = [
            name, admission_number,

            f1_math_t1, f1_math_t2, f1_math_t3,
            f1_english_t1, f1_english_t2, f1_english_t3,
            f1_biology_t1, f1_biology_t2, f1_biology_t3,
            f1_chemistry_t1, f1_chemistry_t2, f1_chemistry_t3,
            f1_physics_t1, f1_physics_t2, f1_physics_t3,
            f1_history_t1, f1_history_t2, f1_history_t3,
            f1_geography_t1, f1_geography_t2, f1_geography_t3,
            f1_business_t1, f1_business_t2, f1_business_t3,

            f2_math_t1, f2_math_t2, f2_math_t3,
            f2_english_t1, f2_english_t2, f2_english_t3,
            f2_biology_t1, f2_biology_t2, f2_biology_t3,
            f2_chemistry_t1, f2_chemistry_t2, f2_chemistry_t3,
            f2_physics_t1, f2_physics_t2, f2_physics_t3,
            f2_history_t1, f2_history_t2, f2_history_t3,
            f2_geography_t1, f2_geography_t2, f2_geography_t3,
            f2_business_t1, f2_business_t2, f2_business_t3,

            f3_math_t1, f3_math_t2, f3_math_t3,
            f3_english_t1, f3_english_t2, f3_english_t3,
            f3_biology_t1, f3_biology_t2, f3_biology_t3,
            f3_chemistry_t1, f3_chemistry_t2, f3_chemistry_t3,
            f3_physics_t1, f3_physics_t2, f3_physics_t3,
            f3_history_t1, f3_history_t2, f3_history_t3,
            f3_geography_t1, f3_geography_t2, f3_geography_t3,
            f3_business_t1, f3_business_t2, f3_business_t3,

            f4_math_t1, f4_math_t2, f4_math_t3,
            f4_english_t1, f4_english_t2, f4_english_t3,
            f4_biology_t1, f4_biology_t2, f4_biology_t3,
            f4_chemistry_t1, f4_chemistry_t2, f4_chemistry_t3,
            f4_physics_t1, f4_physics_t2, f4_physics_t3,
            f4_history_t1, f4_history_t2, f4_history_t3,
            f4_geography_t1, f4_geography_t2, f4_geography_t3,
            f4_business_t1, f4_business_t2, f4_business_t3,

            f1_math_avg, f1_english_avg, f1_biology_avg, f1_chemistry_avg,
            f1_physics_avg, f1_history_avg, f1_geography_avg, f1_business_avg,

            f2_math_avg, f2_english_avg, f2_biology_avg, f2_chemistry_avg,
            f2_physics_avg, f2_history_avg, f2_geography_avg, f2_business_avg,

            f3_math_avg, f3_english_avg, f3_biology_avg, f3_chemistry_avg,
            f3_physics_avg, f3_history_avg, f3_geography_avg, f3_business_avg,

            f4_math_avg, f4_english_avg, f4_biology_avg, f4_chemistry_avg,
            f4_physics_avg, f4_history_avg, f4_geography_avg, f4_business_avg,

            final_score, grade, risk_status, lecturer_username
        ]

        placeholders = ", ".join(["?"] * len(values))
        sql = f"INSERT INTO students ({', '.join(columns)}) VALUES ({placeholders})"

        cursor.execute(sql, values)

        cursor.execute("SELECT * FROM users WHERE username = ?", (admission_number,))
        existing_user = cursor.fetchone()

        if not existing_user:
            email = f"{admission_number.lower()}@school.com"
            cursor.execute("""
                INSERT INTO users (username, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (admission_number, email, "1234", "student"))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "login_username": admission_number,
            "login_password": "1234",
            "predicted_score": final_score,
            "predicted_grade": grade,
            "risk_status": risk_status
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/update-student', methods=['POST'])
def update_student():
    if 'username' not in session or session.get('role') != 'lecturer':
        return jsonify({"message": "Unauthorized"}), 403

    lecturer_username = session['username']
    data = request.get_json()

    try:
        student_id = int(data['id'])
        name = data['name'].strip()
        admission_number = data['admission_number'].strip()

        # ---------- FORM 1 ----------
        f1_math_t1 = float(data['f1_math_t1']); f1_math_t2 = float(data['f1_math_t2']); f1_math_t3 = float(data['f1_math_t3'])
        f1_english_t1 = float(data['f1_english_t1']); f1_english_t2 = float(data['f1_english_t2']); f1_english_t3 = float(data['f1_english_t3'])
        f1_biology_t1 = float(data['f1_biology_t1']); f1_biology_t2 = float(data['f1_biology_t2']); f1_biology_t3 = float(data['f1_biology_t3'])
        f1_chemistry_t1 = float(data['f1_chemistry_t1']); f1_chemistry_t2 = float(data['f1_chemistry_t2']); f1_chemistry_t3 = float(data['f1_chemistry_t3'])
        f1_physics_t1 = float(data['f1_physics_t1']); f1_physics_t2 = float(data['f1_physics_t2']); f1_physics_t3 = float(data['f1_physics_t3'])
        f1_history_t1 = float(data['f1_history_t1']); f1_history_t2 = float(data['f1_history_t2']); f1_history_t3 = float(data['f1_history_t3'])
        f1_geography_t1 = float(data['f1_geography_t1']); f1_geography_t2 = float(data['f1_geography_t2']); f1_geography_t3 = float(data['f1_geography_t3'])
        f1_business_t1 = float(data['f1_business_t1']); f1_business_t2 = float(data['f1_business_t2']); f1_business_t3 = float(data['f1_business_t3'])

        # ---------- FORM 2 ----------
        f2_math_t1 = float(data['f2_math_t1']); f2_math_t2 = float(data['f2_math_t2']); f2_math_t3 = float(data['f2_math_t3'])
        f2_english_t1 = float(data['f2_english_t1']); f2_english_t2 = float(data['f2_english_t2']); f2_english_t3 = float(data['f2_english_t3'])
        f2_biology_t1 = float(data['f2_biology_t1']); f2_biology_t2 = float(data['f2_biology_t2']); f2_biology_t3 = float(data['f2_biology_t3'])
        f2_chemistry_t1 = float(data['f2_chemistry_t1']); f2_chemistry_t2 = float(data['f2_chemistry_t2']); f2_chemistry_t3 = float(data['f2_chemistry_t3'])
        f2_physics_t1 = float(data['f2_physics_t1']); f2_physics_t2 = float(data['f2_physics_t2']); f2_physics_t3 = float(data['f2_physics_t3'])
        f2_history_t1 = float(data['f2_history_t1']); f2_history_t2 = float(data['f2_history_t2']); f2_history_t3 = float(data['f2_history_t3'])
        f2_geography_t1 = float(data['f2_geography_t1']); f2_geography_t2 = float(data['f2_geography_t2']); f2_geography_t3 = float(data['f2_geography_t3'])
        f2_business_t1 = float(data['f2_business_t1']); f2_business_t2 = float(data['f2_business_t2']); f2_business_t3 = float(data['f2_business_t3'])

        # ---------- FORM 3 ----------
        f3_math_t1 = float(data['f3_math_t1']); f3_math_t2 = float(data['f3_math_t2']); f3_math_t3 = float(data['f3_math_t3'])
        f3_english_t1 = float(data['f3_english_t1']); f3_english_t2 = float(data['f3_english_t2']); f3_english_t3 = float(data['f3_english_t3'])
        f3_biology_t1 = float(data['f3_biology_t1']); f3_biology_t2 = float(data['f3_biology_t2']); f3_biology_t3 = float(data['f3_biology_t3'])
        f3_chemistry_t1 = float(data['f3_chemistry_t1']); f3_chemistry_t2 = float(data['f3_chemistry_t2']); f3_chemistry_t3 = float(data['f3_chemistry_t3'])
        f3_physics_t1 = float(data['f3_physics_t1']); f3_physics_t2 = float(data['f3_physics_t2']); f3_physics_t3 = float(data['f3_physics_t3'])
        f3_history_t1 = float(data['f3_history_t1']); f3_history_t2 = float(data['f3_history_t2']); f3_history_t3 = float(data['f3_history_t3'])
        f3_geography_t1 = float(data['f3_geography_t1']); f3_geography_t2 = float(data['f3_geography_t2']); f3_geography_t3 = float(data['f3_geography_t3'])
        f3_business_t1 = float(data['f3_business_t1']); f3_business_t2 = float(data['f3_business_t2']); f3_business_t3 = float(data['f3_business_t3'])

        # ---------- FORM 4 ----------
        f4_math_t1 = float(data['f4_math_t1']); f4_math_t2 = float(data['f4_math_t2']); f4_math_t3 = float(data['f4_math_t3'])
        f4_english_t1 = float(data['f4_english_t1']); f4_english_t2 = float(data['f4_english_t2']); f4_english_t3 = float(data['f4_english_t3'])
        f4_biology_t1 = float(data['f4_biology_t1']); f4_biology_t2 = float(data['f4_biology_t2']); f4_biology_t3 = float(data['f4_biology_t3'])
        f4_chemistry_t1 = float(data['f4_chemistry_t1']); f4_chemistry_t2 = float(data['f4_chemistry_t2']); f4_chemistry_t3 = float(data['f4_chemistry_t3'])
        f4_physics_t1 = float(data['f4_physics_t1']); f4_physics_t2 = float(data['f4_physics_t2']); f4_physics_t3 = float(data['f4_physics_t3'])
        f4_history_t1 = float(data['f4_history_t1']); f4_history_t2 = float(data['f4_history_t2']); f4_history_t3 = float(data['f4_history_t3'])
        f4_geography_t1 = float(data['f4_geography_t1']); f4_geography_t2 = float(data['f4_geography_t2']); f4_geography_t3 = float(data['f4_geography_t3'])
        f4_business_t1 = float(data['f4_business_t1']); f4_business_t2 = float(data['f4_business_t2']); f4_business_t3 = float(data['f4_business_t3'])

        # ---------- AVERAGES ----------
        f1_math_avg = calc_avg(f1_math_t1, f1_math_t2, f1_math_t3)
        f1_english_avg = calc_avg(f1_english_t1, f1_english_t2, f1_english_t3)
        f1_biology_avg = calc_avg(f1_biology_t1, f1_biology_t2, f1_biology_t3)
        f1_chemistry_avg = calc_avg(f1_chemistry_t1, f1_chemistry_t2, f1_chemistry_t3)
        f1_physics_avg = calc_avg(f1_physics_t1, f1_physics_t2, f1_physics_t3)
        f1_history_avg = calc_avg(f1_history_t1, f1_history_t2, f1_history_t3)
        f1_geography_avg = calc_avg(f1_geography_t1, f1_geography_t2, f1_geography_t3)
        f1_business_avg = calc_avg(f1_business_t1, f1_business_t2, f1_business_t3)

        f2_math_avg = calc_avg(f2_math_t1, f2_math_t2, f2_math_t3)
        f2_english_avg = calc_avg(f2_english_t1, f2_english_t2, f2_english_t3)
        f2_biology_avg = calc_avg(f2_biology_t1, f2_biology_t2, f2_biology_t3)
        f2_chemistry_avg = calc_avg(f2_chemistry_t1, f2_chemistry_t2, f2_chemistry_t3)
        f2_physics_avg = calc_avg(f2_physics_t1, f2_physics_t2, f2_physics_t3)
        f2_history_avg = calc_avg(f2_history_t1, f2_history_t2, f2_history_t3)
        f2_geography_avg = calc_avg(f2_geography_t1, f2_geography_t2, f2_geography_t3)
        f2_business_avg = calc_avg(f2_business_t1, f2_business_t2, f2_business_t3)

        f3_math_avg = calc_avg(f3_math_t1, f3_math_t2, f3_math_t3)
        f3_english_avg = calc_avg(f3_english_t1, f3_english_t2, f3_english_t3)
        f3_biology_avg = calc_avg(f3_biology_t1, f3_biology_t2, f3_biology_t3)
        f3_chemistry_avg = calc_avg(f3_chemistry_t1, f3_chemistry_t2, f3_chemistry_t3)
        f3_physics_avg = calc_avg(f3_physics_t1, f3_physics_t2, f3_physics_t3)
        f3_history_avg = calc_avg(f3_history_t1, f3_history_t2, f3_history_t3)
        f3_geography_avg = calc_avg(f3_geography_t1, f3_geography_t2, f3_geography_t3)
        f3_business_avg = calc_avg(f3_business_t1, f3_business_t2, f3_business_t3)

        f4_math_avg = calc_avg(f4_math_t1, f4_math_t2, f4_math_t3)
        f4_english_avg = calc_avg(f4_english_t1, f4_english_t2, f4_english_t3)
        f4_biology_avg = calc_avg(f4_biology_t1, f4_biology_t2, f4_biology_t3)
        f4_chemistry_avg = calc_avg(f4_chemistry_t1, f4_chemistry_t2, f4_chemistry_t3)
        f4_physics_avg = calc_avg(f4_physics_t1, f4_physics_t2, f4_physics_t3)
        f4_history_avg = calc_avg(f4_history_t1, f4_history_t2, f4_history_t3)
        f4_geography_avg = calc_avg(f4_geography_t1, f4_geography_t2, f4_geography_t3)
        f4_business_avg = calc_avg(f4_business_t1, f4_business_t2, f4_business_t3)

        input_data = pd.DataFrame(
            [[
                f1_math_avg, f1_english_avg, f1_biology_avg, f1_chemistry_avg,
                f1_physics_avg, f1_history_avg, f1_geography_avg, f1_business_avg,
                f2_math_avg, f2_english_avg, f2_biology_avg, f2_chemistry_avg,
                f2_physics_avg, f2_history_avg, f2_geography_avg, f2_business_avg,
                f3_math_avg, f3_english_avg, f3_biology_avg, f3_chemistry_avg,
                f3_physics_avg, f3_history_avg, f3_geography_avg, f3_business_avg,
                f4_math_avg, f4_english_avg, f4_biology_avg, f4_chemistry_avg,
                f4_physics_avg, f4_history_avg, f4_geography_avg, f4_business_avg
            ]],
            columns=[
                'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
                'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',
                'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
                'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',
                'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
                'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',
                'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
                'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg'
            ]
        )

        predicted_score = model.predict(input_data)
        final_score = min(round(float(predicted_score[0]), 1), 100)

        if final_score >= 80:
            grade = "A"
            risk_status = "Safe"
        elif final_score >= 50:
            grade = "B"
            risk_status = "Warning"
        else:
            grade = "C"
            risk_status = "At Risk"

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET
                name = ?, admission_number = ?,

                f1_math_t1 = ?, f1_math_t2 = ?, f1_math_t3 = ?,
                f1_english_t1 = ?, f1_english_t2 = ?, f1_english_t3 = ?,
                f1_biology_t1 = ?, f1_biology_t2 = ?, f1_biology_t3 = ?,
                f1_chemistry_t1 = ?, f1_chemistry_t2 = ?, f1_chemistry_t3 = ?,
                f1_physics_t1 = ?, f1_physics_t2 = ?, f1_physics_t3 = ?,
                f1_history_t1 = ?, f1_history_t2 = ?, f1_history_t3 = ?,
                f1_geography_t1 = ?, f1_geography_t2 = ?, f1_geography_t3 = ?,
                f1_business_t1 = ?, f1_business_t2 = ?, f1_business_t3 = ?,

                f2_math_t1 = ?, f2_math_t2 = ?, f2_math_t3 = ?,
                f2_english_t1 = ?, f2_english_t2 = ?, f2_english_t3 = ?,
                f2_biology_t1 = ?, f2_biology_t2 = ?, f2_biology_t3 = ?,
                f2_chemistry_t1 = ?, f2_chemistry_t2 = ?, f2_chemistry_t3 = ?,
                f2_physics_t1 = ?, f2_physics_t2 = ?, f2_physics_t3 = ?,
                f2_history_t1 = ?, f2_history_t2 = ?, f2_history_t3 = ?,
                f2_geography_t1 = ?, f2_geography_t2 = ?, f2_geography_t3 = ?,
                f2_business_t1 = ?, f2_business_t2 = ?, f2_business_t3 = ?,

                f3_math_t1 = ?, f3_math_t2 = ?, f3_math_t3 = ?,
                f3_english_t1 = ?, f3_english_t2 = ?, f3_english_t3 = ?,
                f3_biology_t1 = ?, f3_biology_t2 = ?, f3_biology_t3 = ?,
                f3_chemistry_t1 = ?, f3_chemistry_t2 = ?, f3_chemistry_t3 = ?,
                f3_physics_t1 = ?, f3_physics_t2 = ?, f3_physics_t3 = ?,
                f3_history_t1 = ?, f3_history_t2 = ?, f3_history_t3 = ?,
                f3_geography_t1 = ?, f3_geography_t2 = ?, f3_geography_t3 = ?,
                f3_business_t1 = ?, f3_business_t2 = ?, f3_business_t3 = ?,

                f4_math_t1 = ?, f4_math_t2 = ?, f4_math_t3 = ?,
                f4_english_t1 = ?, f4_english_t2 = ?, f4_english_t3 = ?,
                f4_biology_t1 = ?, f4_biology_t2 = ?, f4_biology_t3 = ?,
                f4_chemistry_t1 = ?, f4_chemistry_t2 = ?, f4_chemistry_t3 = ?,
                f4_physics_t1 = ?, f4_physics_t2 = ?, f4_physics_t3 = ?,
                f4_history_t1 = ?, f4_history_t2 = ?, f4_history_t3 = ?,
                f4_geography_t1 = ?, f4_geography_t2 = ?, f4_geography_t3 = ?,
                f4_business_t1 = ?, f4_business_t2 = ?, f4_business_t3 = ?,

                f1_math_avg = ?, f1_english_avg = ?, f1_biology_avg = ?, f1_chemistry_avg = ?,
                f1_physics_avg = ?, f1_history_avg = ?, f1_geography_avg = ?, f1_business_avg = ?,

                f2_math_avg = ?, f2_english_avg = ?, f2_biology_avg = ?, f2_chemistry_avg = ?,
                f2_physics_avg = ?, f2_history_avg = ?, f2_geography_avg = ?, f2_business_avg = ?,

                f3_math_avg = ?, f3_english_avg = ?, f3_biology_avg = ?, f3_chemistry_avg = ?,
                f3_physics_avg = ?, f3_history_avg = ?, f3_geography_avg = ?, f3_business_avg = ?,

                f4_math_avg = ?, f4_english_avg = ?, f4_biology_avg = ?, f4_chemistry_avg = ?,
                f4_physics_avg = ?, f4_history_avg = ?, f4_geography_avg = ?, f4_business_avg = ?,

                predicted_score = ?, predicted_grade = ?, risk_status = ?
            WHERE id = ? AND lecturer_username = ?
        """, (
            name, admission_number,

            f1_math_t1, f1_math_t2, f1_math_t3,
            f1_english_t1, f1_english_t2, f1_english_t3,
            f1_biology_t1, f1_biology_t2, f1_biology_t3,
            f1_chemistry_t1, f1_chemistry_t2, f1_chemistry_t3,
            f1_physics_t1, f1_physics_t2, f1_physics_t3,
            f1_history_t1, f1_history_t2, f1_history_t3,
            f1_geography_t1, f1_geography_t2, f1_geography_t3,
            f1_business_t1, f1_business_t2, f1_business_t3,

            f2_math_t1, f2_math_t2, f2_math_t3,
            f2_english_t1, f2_english_t2, f2_english_t3,
            f2_biology_t1, f2_biology_t2, f2_biology_t3,
            f2_chemistry_t1, f2_chemistry_t2, f2_chemistry_t3,
            f2_physics_t1, f2_physics_t2, f2_physics_t3,
            f2_history_t1, f2_history_t2, f2_history_t3,
            f2_geography_t1, f2_geography_t2, f2_geography_t3,
            f2_business_t1, f2_business_t2, f2_business_t3,

            f3_math_t1, f3_math_t2, f3_math_t3,
            f3_english_t1, f3_english_t2, f3_english_t3,
            f3_biology_t1, f3_biology_t2, f3_biology_t3,
            f3_chemistry_t1, f3_chemistry_t2, f3_chemistry_t3,
            f3_physics_t1, f3_physics_t2, f3_physics_t3,
            f3_history_t1, f3_history_t2, f3_history_t3,
            f3_geography_t1, f3_geography_t2, f3_geography_t3,
            f3_business_t1, f3_business_t2, f3_business_t3,

            f4_math_t1, f4_math_t2, f4_math_t3,
            f4_english_t1, f4_english_t2, f4_english_t3,
            f4_biology_t1, f4_biology_t2, f4_biology_t3,
            f4_chemistry_t1, f4_chemistry_t2, f4_chemistry_t3,
            f4_physics_t1, f4_physics_t2, f4_physics_t3,
            f4_history_t1, f4_history_t2, f4_history_t3,
            f4_geography_t1, f4_geography_t2, f4_geography_t3,
            f4_business_t1, f4_business_t2, f4_business_t3,

            f1_math_avg, f1_english_avg, f1_biology_avg, f1_chemistry_avg,
            f1_physics_avg, f1_history_avg, f1_geography_avg, f1_business_avg,

            f2_math_avg, f2_english_avg, f2_biology_avg, f2_chemistry_avg,
            f2_physics_avg, f2_history_avg, f2_geography_avg, f2_business_avg,

            f3_math_avg, f3_english_avg, f3_biology_avg, f3_chemistry_avg,
            f3_physics_avg, f3_history_avg, f3_geography_avg, f3_business_avg,

            f4_math_avg, f4_english_avg, f4_biology_avg, f4_chemistry_avg,
            f4_physics_avg, f4_history_avg, f4_geography_avg, f4_business_avg,

            final_score, grade, risk_status,
            student_id, lecturer_username
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student record updated successfully",
            "predicted_score": final_score,
            "predicted_grade": grade,
            "risk_status": risk_status
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/delete-student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if 'username' not in session or session.get('role') != 'lecturer':
        return jsonify({"message": "Unauthorized"}), 403

    lecturer_username = session['username']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = ? AND lecturer_username = ?",
            (student_id, lecturer_username)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Student deleted successfully"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

    # Admin dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, email, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('admin.html', users=users)

@app.route('/add-user', methods=['POST'])
def add_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('home'))

    username = request.form['username'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    role = request.form['role'].strip().lower()

    if role not in ['admin', 'lecturer']:
        return "Only admin and lecturer can be created here"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return "User already exists"

    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (username, email, password, role))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/check-key')
def check_key():
    return str(app.config.get('SECRET_KEY'))


@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    global model

    if 'username' not in session or session.get('role') != 'lecturer':
        return jsonify({"message": "Unauthorized"}), 403

    file = request.files.get('file')

    if not file or file.filename == '':
        return jsonify({"message": "No file uploaded"}), 400

    filepath = UPLOAD_DIR / file.filename
    file.save(filepath)

    try:
        df = pd.read_csv(filepath)

        required_columns = [
            'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
            'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',

            'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
            'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',

            'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
            'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',

            'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
            'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg',

            'final_exam_score'
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return jsonify({
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400

        X = df[
            [
                'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
                'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',

                'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
                'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',

                'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
                'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',

                'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
                'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg'
            ]
        ]

        y = df['final_exam_score']

        model = LinearRegression()
        model.fit(X, y)

        joblib.dump(model, 'model.pkl')

        return jsonify({"message": "Dataset uploaded and model retrained successfully"})

    except Exception as e:
        return jsonify({"message": f"Error retraining model: {str(e)}"}), 500

@app.route('/download-report/<admission_number>')
def download_report(admission_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE admission_number = ?", (admission_number,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        return "Student not found"

    filename = f"{admission_number}_report.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    # Totals
    f1_t1_total = student["f1_math_t1"] + student["f1_english_t1"] + student["f1_biology_t1"] + student["f1_chemistry_t1"] + student["f1_physics_t1"] + student["f1_history_t1"] + student["f1_geography_t1"] + student["f1_business_t1"]
    f1_t2_total = student["f1_math_t2"] + student["f1_english_t2"] + student["f1_biology_t2"] + student["f1_chemistry_t2"] + student["f1_physics_t2"] + student["f1_history_t2"] + student["f1_geography_t2"] + student["f1_business_t2"]
    f1_t3_total = student["f1_math_t3"] + student["f1_english_t3"] + student["f1_biology_t3"] + student["f1_chemistry_t3"] + student["f1_physics_t3"] + student["f1_history_t3"] + student["f1_geography_t3"] + student["f1_business_t3"]
    f1_avg = round((f1_t1_total + f1_t2_total + f1_t3_total) / 24, 2)

    f2_t1_total = student["f2_math_t1"] + student["f2_english_t1"] + student["f2_biology_t1"] + student["f2_chemistry_t1"] + student["f2_physics_t1"] + student["f2_history_t1"] + student["f2_geography_t1"] + student["f2_business_t1"]
    f2_t2_total = student["f2_math_t2"] + student["f2_english_t2"] + student["f2_biology_t2"] + student["f2_chemistry_t2"] + student["f2_physics_t2"] + student["f2_history_t2"] + student["f2_geography_t2"] + student["f2_business_t2"]
    f2_t3_total = student["f2_math_t3"] + student["f2_english_t3"] + student["f2_biology_t3"] + student["f2_chemistry_t3"] + student["f2_physics_t3"] + student["f2_history_t3"] + student["f2_geography_t3"] + student["f2_business_t3"]
    f2_avg = round((f2_t1_total + f2_t2_total + f2_t3_total) / 24, 2)

    f3_t1_total = student["f3_math_t1"] + student["f3_english_t1"] + student["f3_biology_t1"] + student["f3_chemistry_t1"] + student["f3_physics_t1"] + student["f3_history_t1"] + student["f3_geography_t1"] + student["f3_business_t1"]
    f3_t2_total = student["f3_math_t2"] + student["f3_english_t2"] + student["f3_biology_t2"] + student["f3_chemistry_t2"] + student["f3_physics_t2"] + student["f3_history_t2"] + student["f3_geography_t2"] + student["f3_business_t2"]
    f3_t3_total = student["f3_math_t3"] + student["f3_english_t3"] + student["f3_biology_t3"] + student["f3_chemistry_t3"] + student["f3_physics_t3"] + student["f3_history_t3"] + student["f3_geography_t3"] + student["f3_business_t3"]
    f3_avg = round((f3_t1_total + f3_t2_total + f3_t3_total) / 24, 2)

    f4_t1_total = student["f4_math_t1"] + student["f4_english_t1"] + student["f4_biology_t1"] + student["f4_chemistry_t1"] + student["f4_physics_t1"] + student["f4_history_t1"] + student["f4_geography_t1"] + student["f4_business_t1"]
    f4_t2_total = student["f4_math_t2"] + student["f4_english_t2"] + student["f4_biology_t2"] + student["f4_chemistry_t2"] + student["f4_physics_t2"] + student["f4_history_t2"] + student["f4_geography_t2"] + student["f4_business_t2"]
    f4_t3_total = student["f4_math_t3"] + student["f4_english_t3"] + student["f4_biology_t3"] + student["f4_chemistry_t3"] + student["f4_physics_t3"] + student["f4_history_t3"] + student["f4_geography_t3"] + student["f4_business_t3"]
    f4_avg = round((f4_t1_total + f4_t2_total + f4_t3_total) / 24, 2)

    # Title
    content.append(Paragraph("Student Academic Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Name: {student['name']}", styles['Normal']))
    content.append(Paragraph(f"Admission Number: {student['admission_number']}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Prediction summary
    content.append(Paragraph("Prediction Summary", styles['Heading2']))
    prediction_table = Table([
        ["Predicted Final Score", "Predicted Grade", "Risk Status"],
        [student["predicted_score"], student["predicted_grade"], student["risk_status"]]
    ], colWidths=[150, 150, 150])

    prediction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a6cf7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(prediction_table)
    content.append(Spacer(1, 14))

    def add_form_section(form_name, prefix, term1_total, term2_total, term3_total, form_avg):
        content.append(Paragraph(form_name, styles['Heading2']))

        raw_table = Table([
            ["Subject", "Term 1", "Term 2", "Term 3", "Average"],
            ["Math", student[f"{prefix}_math_t1"], student[f"{prefix}_math_t2"], student[f"{prefix}_math_t3"], student[f"{prefix}_math_avg"]],
            ["English", student[f"{prefix}_english_t1"], student[f"{prefix}_english_t2"], student[f"{prefix}_english_t3"], student[f"{prefix}_english_avg"]],
            ["Biology", student[f"{prefix}_biology_t1"], student[f"{prefix}_biology_t2"], student[f"{prefix}_biology_t3"], student[f"{prefix}_biology_avg"]],
            ["Chemistry", student[f"{prefix}_chemistry_t1"], student[f"{prefix}_chemistry_t2"], student[f"{prefix}_chemistry_t3"], student[f"{prefix}_chemistry_avg"]],
            ["Physics", student[f"{prefix}_physics_t1"], student[f"{prefix}_physics_t2"], student[f"{prefix}_physics_t3"], student[f"{prefix}_physics_avg"]],
            ["History", student[f"{prefix}_history_t1"], student[f"{prefix}_history_t2"], student[f"{prefix}_history_t3"], student[f"{prefix}_history_avg"]],
            ["Geography", student[f"{prefix}_geography_t1"], student[f"{prefix}_geography_t2"], student[f"{prefix}_geography_t3"], student[f"{prefix}_geography_avg"]],
            ["Business", student[f"{prefix}_business_t1"], student[f"{prefix}_business_t2"], student[f"{prefix}_business_t3"], student[f"{prefix}_business_avg"]],
        ], colWidths=[100, 80, 80, 80, 80])

        raw_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a6cf7")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))

        content.append(raw_table)
        content.append(Spacer(1, 8))

        totals_table = Table([
            ["Term 1 Total", "Term 2 Total", "Term 3 Total", "Form Average"],
            [f"{term1_total}/800", f"{term2_total}/800", f"{term3_total}/800", f"{form_avg}%"]
        ], colWidths=[120, 120, 120, 120])

        totals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dddddd")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))

        content.append(totals_table)
        content.append(Spacer(1, 14))

    add_form_section("Form 1", "f1", f1_t1_total, f1_t2_total, f1_t3_total, f1_avg)
    add_form_section("Form 2", "f2", f2_t1_total, f2_t2_total, f2_t3_total, f2_avg)
    add_form_section("Form 3", "f3", f3_t1_total, f3_t2_total, f3_t3_total, f3_avg)
    add_form_section("Form 4", "f4", f4_t1_total, f4_t2_total, f4_t3_total, f4_avg)

    doc.build(content)

    return send_file(filename, as_attachment=True)

@app.route('/predict-from-record')
def predict_from_record_page():
    if 'username' not in session:
        return redirect(url_for('home'))

    return render_template('predict_from_record.html')

@app.route('/predict-from-record-data', methods=['POST'])
def predict_from_record_data():
    if 'username' not in session:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    admission_number = data.get('admission_number', '').strip()

    if not admission_number:
        return jsonify({"message": "Admission number is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE admission_number = ?",
            (admission_number,)
        )
        student = cursor.fetchone()
        conn.close()

        if not student:
            return jsonify({"message": "Student record not found"}), 404

        input_data = pd.DataFrame(
            [[
                student['f1_math_avg'], student['f1_english_avg'], student['f1_biology_avg'], student['f1_chemistry_avg'],
                student['f1_physics_avg'], student['f1_history_avg'], student['f1_geography_avg'], student['f1_business_avg'],

                student['f2_math_avg'], student['f2_english_avg'], student['f2_biology_avg'], student['f2_chemistry_avg'],
                student['f2_physics_avg'], student['f2_history_avg'], student['f2_geography_avg'], student['f2_business_avg'],

                student['f3_math_avg'], student['f3_english_avg'], student['f3_biology_avg'], student['f3_chemistry_avg'],
                student['f3_physics_avg'], student['f3_history_avg'], student['f3_geography_avg'], student['f3_business_avg'],

                student['f4_math_avg'], student['f4_english_avg'], student['f4_biology_avg'], student['f4_chemistry_avg'],
                student['f4_physics_avg'], student['f4_history_avg'], student['f4_geography_avg'], student['f4_business_avg']
            ]],
            columns=[
                'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
                'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',

                'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
                'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',

                'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
                'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',

                'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
                'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg'
            ]
        )

        predicted_score = model.predict(input_data)
        final_score = min(round(float(predicted_score[0]), 1), 100)

        if final_score >= 80:
            predicted_grade = "A"
            risk_status = "Safe"
        elif final_score >= 50:
            predicted_grade = "B"
            risk_status = "Warning"
        else:
            predicted_grade = "C"
            risk_status = "At Risk"

        return jsonify({
            "message": "Prediction generated successfully",
            "student": {
                "name": student["name"],
                "admission_number": student["admission_number"],

                "f1_math_avg": student["f1_math_avg"],
                "f1_english_avg": student["f1_english_avg"],
                "f1_biology_avg": student["f1_biology_avg"],
                "f1_chemistry_avg": student["f1_chemistry_avg"],
                "f1_physics_avg": student["f1_physics_avg"],
                "f1_history_avg": student["f1_history_avg"],
                "f1_geography_avg": student["f1_geography_avg"],
                "f1_business_avg": student["f1_business_avg"],

                "f2_math_avg": student["f2_math_avg"],
                "f2_english_avg": student["f2_english_avg"],
                "f2_biology_avg": student["f2_biology_avg"],
                "f2_chemistry_avg": student["f2_chemistry_avg"],
                "f2_physics_avg": student["f2_physics_avg"],
                "f2_history_avg": student["f2_history_avg"],
                "f2_geography_avg": student["f2_geography_avg"],
                "f2_business_avg": student["f2_business_avg"],

                "f3_math_avg": student["f3_math_avg"],
                "f3_english_avg": student["f3_english_avg"],
                "f3_biology_avg": student["f3_biology_avg"],
                "f3_chemistry_avg": student["f3_chemistry_avg"],
                "f3_physics_avg": student["f3_physics_avg"],
                "f3_history_avg": student["f3_history_avg"],
                "f3_geography_avg": student["f3_geography_avg"],
                "f3_business_avg": student["f3_business_avg"],

                "f4_math_avg": student["f4_math_avg"],
                "f4_english_avg": student["f4_english_avg"],
                "f4_biology_avg": student["f4_biology_avg"],
                "f4_chemistry_avg": student["f4_chemistry_avg"],
                "f4_physics_avg": student["f4_physics_avg"],
                "f4_history_avg": student["f4_history_avg"],
                "f4_geography_avg": student["f4_geography_avg"],
                "f4_business_avg": student["f4_business_avg"],

                "predicted_score": final_score,
                "predicted_grade": predicted_grade,
                "risk_status": risk_status
            }
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/create-user/<username>/<email>/<password>/<role>')
def create_user(username, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return f"User {username} already exists"

    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (username, email, password, role))

    conn.commit()
    conn.close()

    return f"User {username} created successfully"

@app.route('/show-users')
def show_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, email, password, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return str([dict(user) for user in users])

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, role FROM users WHERE username = ?",
        (session['username'],)
    )
    user = cursor.fetchone()
    conn.close()

    return render_template('settings.html', user=user)

@app.route('/update-password', methods=['POST'])
def update_password():
    if 'username' not in session:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    current_password = data.get('current_password', '').strip()
    new_password = data.get('new_password', '').strip()
    confirm_password = data.get('confirm_password', '').strip()

    if not current_password or not new_password or not confirm_password:
        return jsonify({"message": "All fields are required"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "New passwords do not match"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (session['username'], current_password)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "Current password is incorrect"}), 400

    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (new_password, session['username'])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Password updated successfully"})

@app.route('/')
def home():
    return render_template('student_login.html')


@app.route('/student-login')
def student_login():
    return render_template('student_login.html')


@app.route('/lecturer-login')
def lecturer_login():
    return render_template('lecturer_login.html')


@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

    return f"Added {added} missing student user(s)"

    init_db()

if __name__ == '__main__':
    init_db()

    app.run(debug=True)