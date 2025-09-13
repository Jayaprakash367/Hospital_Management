"""
Database Manager for Hospital Management System
Handles all database operations with SQLite
"""

import sqlite3
import os
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self, db_path="data/hospital.db"):
        self.db_path = db_path
        self.ensure_data_directory()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def create_tables(self):
        """Create all required database tables"""
        cursor = self.conn.cursor()
        
        # Users table (for authentication)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                national_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,
                blood_group TEXT,
                allergies TEXT,
                medical_history TEXT,
                insurance_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                qualification TEXT,
                experience_years INTEGER,
                phone TEXT,
                email TEXT,
                address TEXT,
                consultation_fee DECIMAL(10,2),
                schedule TEXT,
                is_available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                duration_minutes INTEGER DEFAULT 30,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
            )
        ''')
        
        # Medical records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                symptoms TEXT,
                diagnosis TEXT,
                prescription TEXT,
                lab_tests TEXT,
                follow_up_date DATE,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
            )
        ''')
        
        # Billing table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS billing (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                appointment_id INTEGER,
                total_amount DECIMAL(10,2) NOT NULL,
                paid_amount DECIMAL(10,2) DEFAULT 0,
                payment_status TEXT DEFAULT 'pending',
                payment_method TEXT,
                bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date DATE,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
            )
        ''')
        
        # Staff table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                salary DECIMAL(10,2),
                hire_date DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                room_type TEXT NOT NULL,
                floor INTEGER,
                capacity INTEGER DEFAULT 1,
                current_occupancy INTEGER DEFAULT 0,
                status TEXT DEFAULT 'available',
                daily_rate DECIMAL(10,2),
                facilities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def create_default_admin(self):
        """Create default admin user if not exists"""
        cursor = self.conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT user_id FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone():
            return
            
        # Create default admin
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, full_name, email)
            VALUES (?, ?, ?, ?, ?)
        ''', ("admin", password_hash, "admin", "System Administrator", "admin@hospital.com"))
        
        self.conn.commit()
        
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
        
    def execute_insert(self, query, params):
        """Execute insert query and return last row id"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid
        
    def execute_update(self, query, params):
        """Execute update/delete query"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.rowcount
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
