import sqlite3

# Connect to database
conn = sqlite3.connect('data/hospital.db')
cursor = conn.cursor()

# Backup existing data
cursor.execute("SELECT * FROM billing")
existing_data = cursor.fetchall()

# Get column names
cursor.execute("PRAGMA table_info(billing)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]

print("Current billing table columns:", column_names)

# Drop and recreate table with new schema
cursor.execute("DROP TABLE billing")

# Create new billing table with correct schema
cursor.execute("""
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
)
""")

# Insert existing data with mapping
for row in existing_data:
    bill_id, patient_id, appointment_id, amount, description, created_at = row
    cursor.execute("""
        INSERT INTO billing (bill_id, patient_id, appointment_id, total_amount, paid_amount, payment_status, bill_date, due_date, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, 0, 'pending', ?, NULL, ?, ?, ?)
    """, (bill_id, patient_id, appointment_id, amount, created_at, description, created_at, created_at))

conn.commit()
conn.close()

print("Database migration completed successfully.")
