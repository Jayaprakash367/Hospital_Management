"""
-- SQLite schema (run once to create tables) --
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    national_id TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    gender TEXT,
    address TEXT,
    emergency_contact TEXT,
    emergency_phone TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    specialization TEXT,
    phone TEXT,
    email TEXT,
    available_from TEXT,
    available_to TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date TEXT,
    appointment_time TEXT,
    status TEXT,
    duration_minutes INTEGER,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE billing (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    appointment_id INTEGER,
    total_amount REAL NOT NULL,
    paid_amount REAL DEFAULT 0,
    payment_status TEXT DEFAULT 'pending',
    bill_date TEXT,
    due_date TEXT,
    description TEXT,
    notes TEXT,
    payment_method TEXT,
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id)
);

CREATE TABLE medical_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_id INTEGER,
    diagnosis TEXT,
    prescription TEXT,
    created_at TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id)
);
"""

from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3
import hashlib
from datetime import datetime
import smtplib  # For email (implement as needed)
from src.utils.config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

config = Config()
DATABASE = config.DATABASE_PATH

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def send_sms(phone, message):
    print(f"SMS to {phone}: {message}")
    # Integrate with SMS API here

def send_email(email, subject, message):
    print(f"Email to {email}: {subject}\n{message}")
    # Integrate with email API here

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password_hash)).fetchone()
        if user:
            session['user'] = dict(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        national_id = request.form['national_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        emergency_contact = request.form['emergency_contact']
        emergency_phone = request.form['emergency_phone']

        db = get_db()
        if db.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
            return render_template('register.html', error="Username exists")
        if db.execute("SELECT 1 FROM patients WHERE national_id=?", (national_id,)).fetchone():
            return render_template('register.html', error="National ID exists")

        password_hash = hash_password(password)
        cur = db.cursor()
        cur.execute("INSERT INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, 'patient', ?, ?, ?)",
                    (username, password_hash, f"{first_name} {last_name}", email, phone))
        user_id = cur.lastrowid
        cur.execute('''INSERT INTO patients (user_id, national_id, first_name, last_name, date_of_birth, gender, address, emergency_contact, emergency_phone)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (user_id, national_id, first_name, last_name, date_of_birth, gender, address, emergency_contact, emergency_phone))
        db.commit()

        message = f"Your registration is successful. Username: {username}, Password: {password}."
        send_sms(phone, message)
        send_email(email, "Registration Successful", message)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/patient/dashboard')
def patient_dashboard():
    if 'user' not in session or session['user']['role'] != 'patient':
        return redirect(url_for('login'))
    db = get_db()
    patient = db.execute("SELECT * FROM patients WHERE user_id=?", (session['user']['user_id'],)).fetchone()
    appointments = db.execute("SELECT * FROM appointments WHERE patient_id=?", (patient['patient_id'],)).fetchall()
    billing = db.execute("SELECT * FROM billing WHERE patient_id=?", (patient['patient_id'],)).fetchall()
    medical_records = db.execute("SELECT * FROM medical_records WHERE patient_id=?", (patient['patient_id'],)).fetchall()
    return render_template('patient_dashboard.html', patient=patient, appointments=appointments, billing=billing, medical_records=medical_records, user=session['user'])

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'user' not in session or session['user']['role'] != 'doctor':
        return redirect(url_for('login'))
    db = get_db()
    doctor = db.execute("SELECT * FROM doctors WHERE user_id=?", (session['user']['user_id'],)).fetchone()
    appointments = db.execute("SELECT * FROM appointments WHERE doctor_id=?", (doctor['doctor_id'],)).fetchall()
    return render_template('doctor_dashboard.html', doctor=doctor, appointments=appointments)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user' not in session or session['user']['role'] != 'patient':
        return redirect(url_for('login'))
    db = get_db()
    doctors = db.execute("SELECT * FROM doctors").fetchall()
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        duration = int(request.form.get('duration', 30))
        patient = db.execute("SELECT * FROM patients WHERE user_id=?", (session['user']['user_id'],)).fetchone()
        # Check doctor availability
        conflicts = db.execute('''
            SELECT * FROM appointments
            WHERE doctor_id=? AND appointment_date=? AND status='scheduled'
            AND (
                (appointment_time <= ? AND time(appointment_time, '+' || duration_minutes || ' minutes') > ?)
                OR
                (appointment_time < time(?, '+' || ? || ' minutes') AND time(appointment_time, '+' || duration_minutes || ' minutes') >= time(?, '+' || ? || ' minutes'))
            )
        ''', (doctor_id, appointment_date, appointment_time, appointment_time, appointment_time, duration, appointment_time, duration)).fetchall()
        if conflicts:
            return render_template('book_appointment.html', doctors=doctors, error="Doctor is busy at this time. Please choose another slot.")
        db.execute('''INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, duration_minutes)
                      VALUES (?, ?, ?, ?, 'scheduled', ?)''',
                   (patient['patient_id'], doctor_id, appointment_date, appointment_time, duration))
        db.commit()
        return redirect(url_for('patient_dashboard'))
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/doctor/check_availability/<int:doctor_id>', methods=['GET'])
def doctor_check_availability(doctor_id):
    appointment_date = request.args.get('date')
    appointment_time = request.args.get('time')
    duration = int(request.args.get('duration', 30))
    db = get_db()
    conflicts = db.execute('''
        SELECT * FROM appointments
        WHERE doctor_id=? AND appointment_date=? AND status='scheduled'
        AND (
            (appointment_time <= ? AND time(appointment_time, '+' || duration_minutes || ' minutes') > ?)
            OR
            (appointment_time < time(?, '+' || ? || ' minutes') AND time(appointment_time, '+' || duration_minutes || ' minutes') >= time(?, '+' || ? || ' minutes'))
        )
    ''', (doctor_id, appointment_date, appointment_time, appointment_time, appointment_time, duration, appointment_time, duration)).fetchall()
    available = len(conflicts) == 0
    return jsonify({'available': available})

@app.route('/doctor/receipt/<int:appointment_id>', methods=['GET', 'POST'])
def doctor_receipt(appointment_id):
    if 'user' not in session or session['user']['role'] != 'doctor':
        return redirect(url_for('login'))
    db = get_db()
    appointment = db.execute("SELECT * FROM appointments WHERE appointment_id=?", (appointment_id,)).fetchone()
    patient = db.execute("SELECT * FROM patients WHERE patient_id=?", (appointment['patient_id'],)).fetchone()
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']
        amount = float(request.form['amount'])
        description = request.form['description']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('''INSERT INTO medical_records (patient_id, doctor_id, appointment_id, diagnosis, prescription, created_at)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (patient['patient_id'], appointment['doctor_id'], appointment_id, diagnosis, prescription, now))
        db.execute('''INSERT INTO billing (patient_id, appointment_id, total_amount, paid_amount, payment_status, bill_date, due_date, description, created_at, updated_at)
                      VALUES (?, ?, ?, 0, 'pending', ?, NULL, ?, ?, ?)''',
                   (patient['patient_id'], appointment_id, amount, now[:10], description, now, now))
        db.commit()
        return redirect(url_for('doctor_dashboard'))
    return render_template('doctor_receipt.html', appointment=appointment, patient=patient)

from flask import request, jsonify

@app.route('/billing')
def billing():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('billing.html', user=session['user'])

@app.route('/billing/create', methods=['GET', 'POST'])
def billing_create():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        patient_id = data.get('patient_id')
        appointment_id = data.get('appointment_id')
        total_amount = data.get('total_amount')
        due_date = data.get('due_date')
        description = data.get('description')
        notes = data.get('notes')
        if not patient_id or not total_amount:
            return jsonify({'error': 'Patient and total amount are required.'}), 400
        try:
            total_amount = float(total_amount)
            if total_amount <= 0:
                return jsonify({'error': 'Total amount must be greater than zero.'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid total amount.'}), 400
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            db.execute('''
                INSERT INTO billing (patient_id, appointment_id, total_amount, paid_amount, payment_status, bill_date, due_date, description, notes, created_at, updated_at)
                VALUES (?, ?, ?, 0, 'pending', ?, ?, ?, ?, ?, ?)
            ''', (patient_id, appointment_id, total_amount, now, due_date, description, notes, now, now))
            db.commit()
            return jsonify({'message': 'Bill created successfully.'}), 201
        except Exception as e:
            return jsonify({'error': 'Failed to create bill.'}), 500
    else:
        # GET request - render form
        patients = db.execute("SELECT patient_id, first_name, last_name FROM patients ORDER BY first_name").fetchall()
        appointments = db.execute("SELECT appointment_id, appointment_date FROM appointments ORDER BY appointment_date DESC").fetchall()
        return render_template('billing_create.html', user=session['user'], patients=patients, appointments=appointments)

@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('reports.html', user=session['user'])

@app.route('/generate_report', methods=['POST'])
def generate_report():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    report_type = request.form.get('report_type')
    db = get_db()
    report_data = {}
    report_title = "Report"

    if report_type == 'patient_summary':
        report_title = "Patient Summary Report"
        patients = db.execute("SELECT gender, COUNT(*) as count FROM patients GROUP BY gender").fetchall()
        report_data['patient_by_gender'] = [dict(p) for p in patients]
        
        total_patients_result = db.execute("SELECT COUNT(*) as count FROM patients").fetchone()
        report_data['total_patients'] = total_patients_result['count'] if total_patients_result else 0

    elif report_type == 'financial_summary':
        report_title = "Financial Summary Report"
        # Using total_amount from billing table as per init_db.py
        billing_summary = db.execute("SELECT payment_status, COUNT(*) as count, SUM(total_amount) as total FROM billing GROUP BY payment_status").fetchall()
        report_data['billing_summary'] = [dict(b) for b in billing_summary]
        
        total_revenue_result = db.execute("SELECT SUM(paid_amount) as total FROM billing").fetchone()
        report_data['total_revenue'] = total_revenue_result['total'] if total_revenue_result and total_revenue_result['total'] else 0.0

    else:
        # Redirect back to reports page if report_type is unknown
        return redirect(url_for('reports'))

    return render_template('report_view.html', user=session['user'], report_title=report_title, report_data=report_data, report_type=report_type)

@app.route('/api/patients')
def api_patients():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    patients = db.execute("SELECT * FROM patients").fetchall()
    patients_list = [dict(p) for p in patients]
    return jsonify(patients_list)

@app.route('/api/doctors')
def api_doctors():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    doctors = db.execute("SELECT * FROM doctors").fetchall()
    doctors_list = []
    for d in doctors:
        full_name = d['full_name'] or ''
        parts = full_name.split(' ', 1)
        first_name = parts[0] if len(parts) > 0 else ''
        last_name = parts[1] if len(parts) > 1 else ''
        # Determine availability based on available_from and available_to (simplified)
        is_available = True
        doctors_list.append({
            'doctor_id': d['doctor_id'],
            'first_name': first_name,
            'last_name': last_name,
            'specialization': d['specialization'],
            'phone': d['phone'],
            'email': d['email'],
            'is_available': is_available
        })
    return jsonify(doctors_list)

@app.route('/api/appointments')
def api_appointments():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    appointments = db.execute("SELECT * FROM appointments").fetchall()
    appointments_list = [dict(a) for a in appointments]
    return jsonify(appointments_list)

@app.route('/patients')
def patients():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Add any backend logic for patients page if needed
    return render_template('patients.html', user=session['user'])

@app.route('/api/billing')
def api_billing():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized access. Please log in to view billing records.'}), 401
    try:
        db = get_db()
        billing_records = db.execute("SELECT * FROM billing").fetchall()
        billing_list = []
        for b in billing_records:
            billing_list.append({
                'bill_id': b['bill_id'],
                'patient_id': b['patient_id'],
                'appointment_id': b['appointment_id'],
                'total_amount': b['total_amount'],
                'paid_amount': b['paid_amount'],
                'payment_status': b['payment_status'],
                'description': b['description'],
                'created_at': b['created_at']
            })
        return jsonify(billing_list)
    except Exception as e:
        print("Billing API error:", e)
        return jsonify({'error': 'Unable to retrieve billing records. Please try again later.'}), 500

@app.route('/doctors')
def doctors():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Add any backend logic for doctors page if needed
    return render_template('doctors.html', user=session['user'])

@app.route('/appointments')
def appointments():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Add any backend logic for appointments page if needed
    return render_template('appointments.html', user=session['user'])

if __name__ == '__main__':
    from waitress import serve
    print("Starting server at http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
