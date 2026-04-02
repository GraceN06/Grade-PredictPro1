from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
import sqlite3
import joblib
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.linear_model import LinearRegression
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "data"))
UPLOAD_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "students.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

model = joblib.load('model.pkl')

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        cat_score REAL,
        assignment_score REAL,
        attendance REAL,
        predicted_grade TEXT,
        lecturer_username TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin@gmail.com', '1234', 'admin'))

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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
        return redirect(url_for('home'))

    admission_number = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE admission_number = ?",
        (admission_number,)
    )
    student = cursor.fetchone()

    conn.close()

    if not student:
        return f"No student record found for {admission_number}"

    predicted_score = model.predict([[
        student['cat_score'],
        student['assignment_score'],
        student['attendance']
    ]])

    final_score = int(round(predicted_score[0]))

    if final_score >= 70:
        grade = "A"
        status = "Safe"
    elif final_score >= 50:
        grade = "B"
        status = "Warning"
    else:
        grade = "C"
        status = "At Risk"

    return render_template(
        'student.html',
        student=student,
        final_score=final_score,
        grade=grade,
        status=status
    )

# Lecturer dasboard
@app.route('/lecturer-dashboard')
def lecturer_dashboard():
    if 'username' not in session or session.get('role') != 'lecturer':
        return redirect(url_for('home'))

    lecturer_username = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, admission_number, cat_score, assignment_score, attendance
        FROM students
        WHERE lecturer_username = ?
    """, (lecturer_username,))
    rows = cursor.fetchall()

    conn.close()

    students = []

    for row in rows:
        cat = row['cat_score']
        assignment = row['assignment_score']
        attendance = row['attendance']

        predicted_score = model.predict([[cat, assignment, attendance]])
        final_score = int(round(predicted_score[0]))

        if final_score >= 70:
            grade = "A"
            status = "Safe"
        elif final_score >= 50:
            grade = "B"
            status = "Warning"
        else:
            grade = "C"
            status = "At Risk"

        students.append({
        "id": row["id"],
        "name": row["name"],
        "admission_number": row["admission_number"],
        "cat_score": cat,
        "assignment_score": assignment,
        "attendance": attendance,
        "final_score": final_score,
        "grade": grade,
        "status": status
        })

    return render_template('lecturer.html', students=students)

@app.route('/add-student', methods=['POST'])
def add_student():
    if 'username' not in session or session.get('role') != 'lecturer':
        return jsonify({"message": "Unauthorized"})

    lecturer_username = session['username']
    data = request.get_json()

    name = data['name'].strip()
    admission_number = data['admission_number'].strip()
    cat = float(data['cat'])
    assignment = float(data['assignment'])
    attendance = float(data['attendance'])

    predicted_score = model.predict([[cat, assignment, attendance]])
    final_score = round(predicted_score[0], 1)

    if final_score >= 70:
        grade = "A"
        status = "Safe"
    elif final_score >= 50:
        grade = "B"
        status = "Warning"
    else:
        grade = "C"
        status = "At Risk"

    conn = get_db_connection()
    cursor = conn.cursor()

    # check if admission number already exists in students
    cursor.execute("SELECT * FROM students WHERE admission_number = ?", (admission_number,))
    existing_student = cursor.fetchone()

    if existing_student:
        conn.close()
        return jsonify({"message": "Admission number already exists"})

    cursor.execute("""
        INSERT INTO students (name, admission_number, cat_score, assignment_score, attendance, predicted_grade, lecturer_username)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, admission_number, cat, assignment, attendance, grade, lecturer_username))

    # create student user automatically using admission number as username
    cursor.execute("SELECT * FROM users WHERE username = ?", (admission_number,))
    existing_user = cursor.fetchone()

    if not existing_user:
        safe_name = name.lower().replace(" ", "")
        safe_adm = admission_number.replace("/", "").replace(" ", "")
        email = f"{safe_name}{safe_adm}@school.com"

    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (admission_number, email, "1234", "student"))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student added successfully",
        "name": name,
        "admission_number": admission_number,
        "predicted_score": final_score,
        "grade": grade,
        "status": status,
        "login_username": admission_number,
        "login_password": "1234"
    })

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
        return jsonify({"message": "Unauthorized"})

    file = request.files.get('file')

    if not file or file.filename == '':
        return jsonify({"message": "No file uploaded"})

    filepath = UPLOAD_DIR / file.filename
    file.save(filepath)

    df = pd.read_csv(filepath)
    

    X = df[['cat', 'assignment', 'attendance']]
    y = df['final_score']

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, 'model.pkl')

    return jsonify({"message": "Dataset uploaded and model trained successfully"})

@app.route('/download-report/<username>')
def download_report(username):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM students WHERE name = ?"
    cursor.execute(query, (username,))
    student = cursor.fetchone()

    conn.close()

    if not student:
        return "Student not found"

    filename = f"{username}_report.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Student Report: {student['name']}", styles['Title']))
    content.append(Paragraph(f"CAT: {student['cat_score']}", styles['Normal']))
    content.append(Paragraph(f"Assignment: {student['assignment_score']}", styles['Normal']))
    content.append(Paragraph(f"Attendance: {student['attendance']}", styles['Normal']))
    content.append(Paragraph(f"Grade: {student['predicted_grade']}", styles['Normal']))

    doc.build(content)

    from flask import send_file
    return send_file(filename, as_attachment=True)

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
if __name__ == '__main__':
    init_db()
    app.run(debug=True)