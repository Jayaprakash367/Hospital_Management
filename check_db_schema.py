import sqlite3

conn = sqlite3.connect('data/hospital.db')
cursor = conn.cursor()

# Get schema for billing table
cursor.execute("PRAGMA table_info(billing)")
billing_columns = cursor.fetchall()

print("Billing table schema:")
for col in billing_columns:
    print(f"  {col[1]}: {col[2]}")

conn.close()
