import sqlite3
from sqlite3 import connect, Error

schema = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS patients (
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

CREATE TABLE IF NOT EXISTS doctors (
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

CREATE TABLE IF NOT EXISTS appointments (
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

CREATE TABLE IF NOT EXISTS billing (
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

CREATE TABLE IF NOT EXISTS billing_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    session_date TEXT,
    status TEXT DEFAULT 'active',
    created_by INTEGER,
    created_at TEXT,
    FOREIGN KEY(bill_id) REFERENCES billing(bill_id),
    FOREIGN KEY(created_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS billing_details (
    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    session_id INTEGER,
    item_description TEXT,
    quantity INTEGER DEFAULT 1,
    unit_price REAL,
    total_price REAL,
    item_type TEXT, -- 'service', 'medication', 'procedure', etc.
    created_at TEXT,
    FOREIGN KEY(bill_id) REFERENCES billing(bill_id),
    FOREIGN KEY(session_id) REFERENCES billing_sessions(session_id)
);

CREATE TABLE IF NOT EXISTS medical_records (
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

conn = sqlite3.connect("data/hospital.db")
conn.executescript(schema)

# Insert sample data
cursor = conn.cursor()

# Sample users
cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
               ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', 'Admin User', 'admin@example.com', '1234567890'))
cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
               ('patient1', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'patient', 'John Doe', 'john@example.com', '0987654321'))
cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
               ('doctor1', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'doctor', 'Dr. Jane Smith', 'jane@example.com', '1122334455'))

# Sample patients
cursor.execute("INSERT OR IGNORE INTO patients (user_id, national_id, first_name, last_name, date_of_birth, gender, address, emergency_contact, emergency_phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (2, '123456789', 'John', 'Doe', '1990-01-01', 'Male', '123 Main St', 'Jane Doe', '0987654321'))

# Sample doctors
cursor.execute("INSERT OR IGNORE INTO doctors (user_id, full_name, specialization, phone, email, available_from, available_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (3, 'Dr. Jane Smith', 'Cardiology', '1122334455', 'jane@example.com', '09:00', '17:00'))

# Sample appointments
cursor.execute("INSERT OR IGNORE INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, duration_minutes) VALUES (?, ?, ?, ?, ?, ?)",
               (1, 1, '2023-12-01', '10:00', 'scheduled', 30))

# Sample billing
cursor.execute("INSERT OR IGNORE INTO billing (patient_id, appointment_id, total_amount, paid_amount, payment_status, bill_date, due_date, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (1, 1, 100.0, 0.0, 'pending', '2023-12-01', '2023-12-15', 'Consultation fee', '2023-12-01 10:00:00', '2023-12-01 10:00:00'))

conn.commit()
conn.close()
print("Database initialized successfully with sample data.")
