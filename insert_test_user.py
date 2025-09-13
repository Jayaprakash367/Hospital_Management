import sqlite3
import hashlib

DATABASE = 'hospital.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insert_test_user():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    username = 'testuser'
    password_hash = hash_password('test')
    role = 'patient'
    full_name = 'Test User'
    email = 'test@example.com'
    phone = '1234567890'

    cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print("Test user already exists.")
    else:
        cursor.execute("INSERT INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, password_hash, role, full_name, email, phone))
        conn.commit()
        print("Test user inserted.")
    conn.close()

if __name__ == '__main__':
    insert_test_user()
