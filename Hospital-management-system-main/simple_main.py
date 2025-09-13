#!/usr/bin/env python3
"""
Hospital Management System v2.0 - Simple Console Interface
A simplified, user-friendly console-based hospital management system
"""

import os
import sys
import sqlite3
import hashlib
import shutil
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import DatabaseManager

class SimpleHospitalSystem:
    def __init__(self):
        print("=" * 70)
        print("🏥 HOSPITAL MANAGEMENT SYSTEM v2.0 - SIMPLE INTERFACE")
        print("=" * 70)
        
        # Initialize database
        try:
            self.db = DatabaseManager()
            self.db.create_tables()
            self.db.create_default_admin()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return
            
        self.current_user = None
        self.run_system()
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, title):
        """Print a formatted header"""
        self.clear_screen()
        print("=" * 70)
        print(f"🏥 {title}")
        print("=" * 70)
        
    def login(self):
        """User login"""
        self.print_header("LOGIN")
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            print(f"\nLogin Attempt {attempts + 1}/{max_attempts}")
            print("-" * 30)
            
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            if not username or not password:
                print("❌ Please enter both username and password")
                attempts += 1
                continue
                
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Check credentials
            try:
                query = '''
                    SELECT user_id, username, role, full_name
                    FROM users 
                    WHERE username = ? AND password_hash = ? AND is_active = 1
                '''
                
                result = self.db.execute_query(query, (username, password_hash))
                
                if result:
                    self.current_user = dict(result[0])
                    print(f"✅ Login successful! Welcome, {self.current_user['full_name']}")
                    input("\nPress Enter to continue...")
                    return True
                else:
                    print("❌ Invalid username or password")
                    attempts += 1
                    
            except Exception as e:
                print(f"❌ Login error: {e}")
                attempts += 1
                
        print(f"\n❌ Maximum login attempts exceeded. System locked.")
        return False
        
    def main_menu(self):
        """Main menu"""
        while True:
            self.print_header(f"MAIN MENU - Welcome {self.current_user['full_name'] if self.current_user else 'User'}")
            
            print("📋 Select an option:")
            print()
            print("1. 👥 Patient Management")
            print("2. 👨‍⚕️ Doctor Management") 
            print("3. 📅 Appointment Management")
            print("4. 💰 Billing Management")
            print("5. 📊 Reports & Statistics")
            print("6. ⚙️  System Settings")
            print("7. 🚪 Logout")
            print()
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                self.billing_menu()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                self.settings_menu()
            elif choice == '7':
                print("\n👋 Logging out...")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                input("Press Enter to continue...")
                
    def patient_menu(self):
        """Patient management menu"""
        while True:
            self.print_header("PATIENT MANAGEMENT")
            
            print("📋 Patient Options:")
            print()
            print("1. ➕ Add New Patient")
            print("2. 👁️  View Patient Details")
            print("3. 📝 Edit Patient Information")
            print("4. 🗑️  Delete Patient")
            print("5. 🔍 Search Patients")
            print("6. 📄 List All Patients")
            print("7. ⬅️  Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.view_patient()
            elif choice == '3':
                self.edit_patient()
            elif choice == '4':
                self.delete_patient()
            elif choice == '5':
                self.search_patients()
            elif choice == '6':
                self.list_patients()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                input("Press Enter to continue...")
                
    def add_patient(self):
        """Add new patient"""
        self.print_header("ADD NEW PATIENT")
        
        try:
            print("Enter patient information:")
            print("(* indicates required fields)")
            print()
            
            # Required fields
            national_id = input("* National ID: ").strip()
            if not national_id:
                print("❌ National ID is required")
                input("Press Enter to continue...")
                return
                
            first_name = input("* First Name: ").strip()
            if not first_name:
                print("❌ First name is required")
                input("Press Enter to continue...")
                return
                
            last_name = input("* Last Name: ").strip()
            if not last_name:
                print("❌ Last name is required")
                input("Press Enter to continue...")
                return
                
            date_of_birth = input("* Date of Birth (YYYY-MM-DD): ").strip()
            if not date_of_birth:
                print("❌ Date of birth is required")
                input("Press Enter to continue...")
                return
                
            print("\nGender options: Male, Female, Other")
            gender = input("* Gender: ").strip()
            if not gender:
                print("❌ Gender is required")
                input("Press Enter to continue...")
                return
                
            # Optional fields
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            address = input("Address: ").strip()
            emergency_contact = input("Emergency Contact Name: ").strip()
            emergency_phone = input("Emergency Contact Phone: ").strip()
            blood_group = input("Blood Group: ").strip()
            allergies = input("Allergies: ").strip()
            insurance_info = input("Insurance Information: ").strip()
            
            # Insert into database
            query = '''
                INSERT INTO patients (
                    national_id, first_name, last_name, date_of_birth, gender,
                    phone, email, address, emergency_contact, emergency_phone,
                    blood_group, allergies, insurance_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                national_id, first_name, last_name, date_of_birth, gender,
                phone, email, address, emergency_contact, emergency_phone,
                blood_group, allergies, insurance_info
            )
            
            patient_id = self.db.execute_insert(query, values)
            
            print(f"\n✅ Patient added successfully!")
            print(f"Patient ID: {patient_id}")
            print(f"Name: {first_name} {last_name}")
            
        except Exception as e:
            print(f"❌ Error adding patient: {e}")
            
        input("\nPress Enter to continue...")
        
    def list_patients(self):
        """List all patients"""
        self.print_header("ALL PATIENTS")
        
        try:
            query = '''
                SELECT patient_id, national_id, first_name, last_name, 
                       date_of_birth, gender, phone
                FROM patients 
                ORDER BY last_name, first_name
            '''
            
            patients = self.db.execute_query(query)
            
            if not patients:
                print("📭 No patients found in the system.")
            else:
                print(f"Found {len(patients)} patients:")
                print()
                print("ID  | National ID | Name                    | DOB        | Gender | Phone")
                print("-" * 80)
                
                for patient in patients:
                    name = f"{patient['first_name']} {patient['last_name']}"
                    phone = patient['phone'] or 'N/A'
                    
                    print(f"{patient['patient_id']:<3} | {patient['national_id']:<11} | "
                          f"{name:<23} | {patient['date_of_birth']} | "
                          f"{patient['gender']:<6} | {phone}")
                          
        except Exception as e:
            print(f"❌ Error loading patients: {e}")
            
        input("\nPress Enter to continue...")
        
    def view_patient(self):
        """View patient details"""
        self.print_header("VIEW PATIENT DETAILS")
        
        try:
            patient_id = input("Enter Patient ID: ").strip()
            
            if not patient_id.isdigit():
                print("❌ Please enter a valid patient ID")
                input("Press Enter to continue...")
                return
                
            query = '''
                SELECT * FROM patients WHERE patient_id = ?
            '''
            
            result = self.db.execute_query(query, (int(patient_id),))
            
            if not result:
                print(f"❌ No patient found with ID: {patient_id}")
            else:
                patient = result[0]
                print(f"\n📋 Patient Details:")
                print("=" * 50)
                print(f"Patient ID: {patient['patient_id']}")
                print(f"National ID: {patient['national_id']}")
                print(f"Name: {patient['first_name']} {patient['last_name']}")
                print(f"Date of Birth: {patient['date_of_birth']}")
                print(f"Gender: {patient['gender']}")
                print(f"Phone: {patient['phone'] or 'N/A'}")
                print(f"Email: {patient['email'] or 'N/A'}")
                print(f"Address: {patient['address'] or 'N/A'}")
                print(f"Emergency Contact: {patient['emergency_contact'] or 'N/A'}")
                print(f"Emergency Phone: {patient['emergency_phone'] or 'N/A'}")
                print(f"Blood Group: {patient['blood_group'] or 'N/A'}")
                print(f"Allergies: {patient['allergies'] or 'N/A'}")
                print(f"Insurance: {patient['insurance_info'] or 'N/A'}")
                print(f"Created: {patient['created_at']}")
                
        except Exception as e:
            print(f"❌ Error viewing patient: {e}")
            
        input("\nPress Enter to continue...")
        
    def doctor_menu(self):
        """Doctor management menu"""
        while True:
            self.print_header("DOCTOR MANAGEMENT")
            
            print("📋 Doctor Options:")
            print()
            print("1. ➕ Add New Doctor")
            print("2. 👁️  View Doctor Details")
            print("3. 📝 Edit Doctor Information")
            print("4. 🗑️  Delete Doctor")
            print("5. 📄 List All Doctors")
            print("6. ⬅️  Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_doctor()
            elif choice == '3':
                print("📝 Edit doctor feature - Coming soon!")
                input("Press Enter to continue...")
            elif choice == '4':
                print("🗑️ Delete doctor feature - Coming soon!")
                input("Press Enter to continue...")
            elif choice == '5':
                self.list_doctors()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                input("Press Enter to continue...")
                
    def add_doctor(self):
        """Add new doctor"""
        self.print_header("ADD NEW DOCTOR")
        
        try:
            print("Enter doctor information:")
            print("(* indicates required fields)")
            print()
            
            # Required fields
            employee_id = input("* Employee ID: ").strip()
            if not employee_id:
                print("❌ Employee ID is required")
                input("Press Enter to continue...")
                return
                
            first_name = input("* First Name: ").strip()
            if not first_name:
                print("❌ First name is required")
                input("Press Enter to continue...")
                return
                
            last_name = input("* Last Name: ").strip()
            if not last_name:
                print("❌ Last name is required")
                input("Press Enter to continue...")
                return
                
            print("\nSpecialization options:")
            print("Cardiology, Neurology, Orthopedics, Pediatrics, General Medicine,")
            print("Surgery, Emergency, Radiology, Dermatology, Psychiatry")
            specialization = input("* Specialization: ").strip()
            if not specialization:
                print("❌ Specialization is required")
                input("Press Enter to continue...")
                return
                
            # Optional fields
            qualification = input("Qualification: ").strip()
            experience_years = input("Experience (years): ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            address = input("Address: ").strip()
            consultation_fee = input("Consultation Fee: ").strip()
            
            # Convert numeric fields
            exp_years = int(experience_years) if experience_years.isdigit() else None
            fee = float(consultation_fee) if consultation_fee.replace('.','').isdigit() else None
            
            # Insert into database
            query = '''
                INSERT INTO doctors (
                    employee_id, first_name, last_name, specialization,
                    qualification, experience_years, phone, email, address,
                    consultation_fee, is_available
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                employee_id, first_name, last_name, specialization,
                qualification, exp_years, phone, email, address, fee, 1
            )
            
            doctor_id = self.db.execute_insert(query, values)
            
            print(f"\n✅ Doctor added successfully!")
            print(f"Doctor ID: {doctor_id}")
            print(f"Name: Dr. {first_name} {last_name}")
            print(f"Specialization: {specialization}")
            
        except Exception as e:
            print(f"❌ Error adding doctor: {e}")
            
        input("\nPress Enter to continue...")
        
    def list_doctors(self):
        """List all doctors"""
        self.print_header("ALL DOCTORS")
        
        try:
            query = '''
                SELECT doctor_id, employee_id, first_name, last_name, 
                       specialization, experience_years, consultation_fee, is_available
                FROM doctors 
                ORDER BY last_name, first_name
            '''
            
            doctors = self.db.execute_query(query)
            
            if not doctors:
                print("📭 No doctors found in the system.")
            else:
                print(f"Found {len(doctors)} doctors:")
                print()
                print("ID | Emp ID | Name                    | Specialization    | Exp | Fee    | Status")
                print("-" * 85)
                
                for doctor in doctors:
                    name = f"Dr. {doctor['first_name']} {doctor['last_name']}"
                    exp = f"{doctor['experience_years']}y" if doctor['experience_years'] else 'N/A'
                    fee = f"${doctor['consultation_fee']}" if doctor['consultation_fee'] else 'N/A'
                    status = "Available" if doctor['is_available'] else "Unavailable"
                    
                    print(f"{doctor['doctor_id']:<2} | {doctor['employee_id']:<6} | "
                          f"{name:<23} | {doctor['specialization']:<17} | "
                          f"{exp:<3} | {fee:<6} | {status}")
                          
        except Exception as e:
            print(f"❌ Error loading doctors: {e}")
            
        input("\nPress Enter to continue...")
        
    def view_doctor(self):
        """View doctor details"""
        self.print_header("VIEW DOCTOR DETAILS")
        
        try:
            doctor_id = input("Enter Doctor ID: ").strip()
            
            if not doctor_id.isdigit():
                print("❌ Please enter a valid doctor ID")
                input("Press Enter to continue...")
                return
                
            query = '''
                SELECT * FROM doctors WHERE doctor_id = ?
            '''
            
            result = self.db.execute_query(query, (int(doctor_id),))
            
            if not result:
                print(f"❌ No doctor found with ID: {doctor_id}")
            else:
                doctor = result[0]
                print(f"\n📋 Doctor Details:")
                print("=" * 50)
                print(f"Doctor ID: {doctor['doctor_id']}")
                print(f"Employee ID: {doctor['employee_id']}")
                print(f"Name: Dr. {doctor['first_name']} {doctor['last_name']}")
                print(f"Specialization: {doctor['specialization']}")
                print(f"Qualification: {doctor['qualification'] or 'N/A'}")
                print(f"Experience: {doctor['experience_years']} years" if doctor['experience_years'] else 'Experience: N/A')
                print(f"Phone: {doctor['phone'] or 'N/A'}")
                print(f"Email: {doctor['email'] or 'N/A'}")
                print(f"Address: {doctor['address'] or 'N/A'}")
                print(f"Consultation Fee: ${doctor['consultation_fee']}" if doctor['consultation_fee'] else 'Fee: N/A')
                print(f"Status: {'Available' if doctor['is_available'] else 'Unavailable'}")
                print(f"Created: {doctor['created_at']}")
                
        except Exception as e:
            print(f"❌ Error viewing doctor: {e}")
            
        input("\nPress Enter to continue...")
        
    def appointment_menu(self):
        """Appointment management menu"""
        self.print_header("APPOINTMENT MANAGEMENT")
        
        print("📅 Appointment Options:")
        print()
        print("1. ➕ Schedule New Appointment")
        print("2. 👁️  View Appointment Details")
        print("3. 📄 List Today's Appointments")
        print("4. 📄 List All Appointments")
        print("5. ❌ Cancel Appointment")
        print("6. ⬅️  Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self.schedule_appointment()
        elif choice == '2':
            print("👁️ View appointment details - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '3':
            self.list_today_appointments()
        elif choice == '4':
            self.list_all_appointments()
        elif choice == '5':
            print("❌ Cancel appointment - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice. Please select 1-6.")
            input("Press Enter to continue...")
            
        # Return to appointment menu
        self.appointment_menu()
        
    def schedule_appointment(self):
        """Schedule new appointment"""
        self.print_header("SCHEDULE NEW APPOINTMENT")
        
        try:
            # Show available doctors
            doctors = self.db.execute_query(
                "SELECT doctor_id, first_name, last_name, specialization FROM doctors WHERE is_available = 1"
            )
            
            if not doctors:
                print("❌ No available doctors found")
                input("Press Enter to continue...")
                return
                
            print("Available Doctors:")
            print("ID | Name                    | Specialization")
            print("-" * 50)
            for doctor in doctors:
                name = f"Dr. {doctor['first_name']} {doctor['last_name']}"
                print(f"{doctor['doctor_id']:<2} | {name:<23} | {doctor['specialization']}")
                
            print()
            doctor_id = input("Select Doctor ID: ").strip()
            
            if not doctor_id.isdigit():
                print("❌ Please enter a valid doctor ID")
                input("Press Enter to continue...")
                return
                
            # Show patients
            patients = self.db.execute_query(
                "SELECT patient_id, first_name, last_name FROM patients ORDER BY last_name"
            )
            
            if not patients:
                print("❌ No patients found")
                input("Press Enter to continue...")
                return
                
            print("\nPatients:")
            print("ID | Name")
            print("-" * 30)
            for patient in patients[:10]:  # Show first 10
                name = f"{patient['first_name']} {patient['last_name']}"
                print(f"{patient['patient_id']:<2} | {name}")
                
            if len(patients) > 10:
                print("... (showing first 10 patients)")
                
            print()
            patient_id = input("Enter Patient ID: ").strip()
            
            if not patient_id.isdigit():
                print("❌ Please enter a valid patient ID")
                input("Press Enter to continue...")
                return
                
            # Get appointment details
            appointment_date = input("Appointment Date (YYYY-MM-DD): ").strip()
            appointment_time = input("Appointment Time (HH:MM): ").strip()
            duration = input("Duration in minutes (default 30): ").strip() or "30"
            notes = input("Notes (optional): ").strip()
            
            # Insert appointment
            query = '''
                INSERT INTO appointments (
                    patient_id, doctor_id, appointment_date, appointment_time,
                    duration_minutes, status, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                int(patient_id), int(doctor_id), appointment_date, 
                appointment_time + ":00", int(duration), 'scheduled', notes
            )
            
            appointment_id = self.db.execute_insert(query, values)
            
            print(f"\n✅ Appointment scheduled successfully!")
            print(f"Appointment ID: {appointment_id}")
            print(f"Date: {appointment_date}")
            print(f"Time: {appointment_time}")
            
        except Exception as e:
            print(f"❌ Error scheduling appointment: {e}")
            
        input("\nPress Enter to continue...")
        
    def list_today_appointments(self):
        """List today's appointments"""
        self.print_header("TODAY'S APPOINTMENTS")
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            query = '''
                SELECT a.appointment_id, a.appointment_time, a.status,
                       (p.first_name || ' ' || p.last_name) as patient_name,
                       (d.first_name || ' ' || d.last_name) as doctor_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE DATE(a.appointment_date) = ?
                ORDER BY a.appointment_time
            '''
            
            appointments = self.db.execute_query(query, (today,))
            
            if not appointments:
                print(f"📭 No appointments scheduled for today ({today})")
            else:
                print(f"Appointments for {today}:")
                print()
                print("ID | Time  | Patient               | Doctor                | Status")
                print("-" * 75)
                
                for apt in appointments:
                    time_str = apt['appointment_time'][:5]  # HH:MM
                    print(f"{apt['appointment_id']:<2} | {time_str} | "
                          f"{apt['patient_name']:<21} | {apt['doctor_name']:<21} | "
                          f"{apt['status'].title()}")
                          
        except Exception as e:
            print(f"❌ Error loading appointments: {e}")
            
        input("\nPress Enter to continue...")
        
    def list_all_appointments(self):
        """List all appointments"""
        self.print_header("ALL APPOINTMENTS")
        
        try:
            query = '''
                SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.status,
                       (p.first_name || ' ' || p.last_name) as patient_name,
                       (d.first_name || ' ' || d.last_name) as doctor_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
                LIMIT 20
            '''
            
            appointments = self.db.execute_query(query)
            
            if not appointments:
                print("📭 No appointments found")
            else:
                print("Recent Appointments (last 20):")
                print()
                print("ID | Date       | Time  | Patient           | Doctor            | Status")
                print("-" * 80)
                
                for apt in appointments:
                    time_str = apt['appointment_time'][:5]  # HH:MM
                    print(f"{apt['appointment_id']:<2} | {apt['appointment_date']} | {time_str} | "
                          f"{apt['patient_name']:<17} | {apt['doctor_name']:<17} | "
                          f"{apt['status'].title()}")
                          
        except Exception as e:
            print(f"❌ Error loading appointments: {e}")
            
        input("\nPress Enter to continue...")
        
    def billing_menu(self):
        """Billing management menu"""
        self.print_header("BILLING MANAGEMENT")
        
        print("💰 Billing Options:")
        print()
        print("1. ➕ Create New Bill")
        print("2. 💳 Record Payment")
        print("3. 👁️  View Bill Details")
        print("4. 📄 List Pending Bills")
        print("5. 📊 Financial Summary")
        print("6. ⬅️  Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self.create_bill()
        elif choice == '2':
            print("💳 Record payment - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '3':
            print("👁️ View bill details - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '4':
            self.list_pending_bills()
        elif choice == '5':
            self.financial_summary()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice. Please select 1-6.")
            input("Press Enter to continue...")
            
        # Return to billing menu
        self.billing_menu()
        
    def create_bill(self):
        """Create new bill"""
        self.print_header("CREATE NEW BILL")
        
        try:
            # Show patients
            patients = self.db.execute_query(
                "SELECT patient_id, first_name, last_name FROM patients ORDER BY last_name"
            )
            
            if not patients:
                print("❌ No patients found")
                input("Press Enter to continue...")
                return
                
            print("Patients:")
            print("ID | Name")
            print("-" * 30)
            for patient in patients[:10]:  # Show first 10
                name = f"{patient['first_name']} {patient['last_name']}"
                print(f"{patient['patient_id']:<2} | {name}")
                
            if len(patients) > 10:
                print("... (showing first 10 patients)")
                
            print()
            patient_id = input("Enter Patient ID: ").strip()
            
            if not patient_id.isdigit():
                print("❌ Please enter a valid patient ID")
                input("Press Enter to continue...")
                return
                
            total_amount = input("Total Amount: $").strip()
            
            if not total_amount.replace('.','').isdigit():
                print("❌ Please enter a valid amount")
                input("Press Enter to continue...")
                return
                
            due_date = input("Due Date (YYYY-MM-DD, optional): ").strip()
            notes = input("Notes (optional): ").strip()
            
            # Insert bill
            query = '''
                INSERT INTO billing (
                    patient_id, total_amount, paid_amount, payment_status,
                    bill_date, due_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                int(patient_id), float(total_amount), 0, 'pending',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                due_date if due_date else None, notes
            )
            
            bill_id = self.db.execute_insert(query, values)
            
            print(f"\n✅ Bill created successfully!")
            print(f"Bill ID: {bill_id}")
            print(f"Amount: ${total_amount}")
            print(f"Status: Pending")
            
        except Exception as e:
            print(f"❌ Error creating bill: {e}")
            
        input("\nPress Enter to continue...")
        
    def list_pending_bills(self):
        """List pending bills"""
        self.print_header("PENDING BILLS")
        
        try:
            query = '''
                SELECT b.bill_id, b.total_amount, b.paid_amount, b.bill_date, b.due_date,
                       (p.first_name || ' ' || p.last_name) as patient_name
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.payment_status = 'pending'
                ORDER BY b.due_date, b.bill_date
            '''
            
            bills = self.db.execute_query(query)
            
            if not bills:
                print("📭 No pending bills found")
            else:
                print(f"Found {len(bills)} pending bills:")
                print()
                print("ID | Patient               | Amount    | Due Date   | Days")
                print("-" * 60)
                
                for bill in bills:
                    amount = f"${bill['total_amount']:.2f}"
                    due_date = bill['due_date'] or 'No due date'
                    
                    # Calculate days until due
                    days = ""
                    if bill['due_date']:
                        try:
                            due = datetime.strptime(bill['due_date'], '%Y-%m-%d')
                            diff = (due - datetime.now()).days
                            if diff < 0:
                                days = f"{abs(diff)} overdue"
                            elif diff == 0:
                                days = "Due today"
                            else:
                                days = f"{diff} days"
                        except:
                            days = ""
                    
                    print(f"{bill['bill_id']:<2} | {bill['patient_name']:<21} | "
                          f"{amount:<9} | {due_date:<10} | {days}")
                          
        except Exception as e:
            print(f"❌ Error loading bills: {e}")
            
        input("\nPress Enter to continue...")
        
    def financial_summary(self):
        """Show financial summary"""
        self.print_header("FINANCIAL SUMMARY")
        
        try:
            # Total revenue
            revenue_result = self.db.execute_query(
                "SELECT SUM(paid_amount) as revenue FROM billing"
            )
            total_revenue = revenue_result[0]['revenue'] if revenue_result and revenue_result[0]['revenue'] else 0
            
            # Outstanding amount
            outstanding_result = self.db.execute_query(
                "SELECT SUM(total_amount - paid_amount) as outstanding FROM billing WHERE payment_status != 'paid'"
            )
            outstanding = outstanding_result[0]['outstanding'] if outstanding_result and outstanding_result[0]['outstanding'] else 0
            
            # This month's revenue
            month_result = self.db.execute_query(
                "SELECT SUM(paid_amount) as month_revenue FROM billing WHERE strftime('%Y-%m', bill_date) = strftime('%Y-%m', 'now')"
            )
            month_revenue = month_result[0]['month_revenue'] if month_result and month_result[0]['month_revenue'] else 0
            
            # Pending bills count
            pending_result = self.db.execute_query(
                "SELECT COUNT(*) as pending_count FROM billing WHERE payment_status = 'pending'"
            )
            pending_count = pending_result[0]['pending_count'] if pending_result else 0
            
            print("💰 Financial Overview:")
            print("=" * 40)
            print(f"Total Revenue:        ${total_revenue:,.2f}")
            print(f"Outstanding Amount:   ${outstanding:,.2f}")
            print(f"This Month's Revenue: ${month_revenue:,.2f}")
            print(f"Pending Bills:        {pending_count}")
            print()
            
            if outstanding > 0:
                print("⚠️  Action Required:")
                print(f"   • Follow up on ${outstanding:,.2f} in outstanding payments")
                print(f"   • {pending_count} bills need attention")
                
        except Exception as e:
            print(f"❌ Error loading financial summary: {e}")
            
        input("\nPress Enter to continue...")
        
    def reports_menu(self):
        """Reports and statistics menu"""
        self.print_header("REPORTS & STATISTICS")
        
        print("📊 Available Reports:")
        print()
        print("1. 📈 System Overview")
        print("2. 👥 Patient Statistics")
        print("3. 👨‍⚕️ Doctor Statistics")
        print("4. 📅 Appointment Report")
        print("5. 💰 Financial Report")
        print("6. ⬅️  Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self.system_overview()
        elif choice == '2':
            self.patient_statistics()
        elif choice == '3':
            self.doctor_statistics()
        elif choice == '4':
            self.appointment_report()
        elif choice == '5':
            self.financial_summary()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice. Please select 1-6.")
            input("Press Enter to continue...")
            
        # Return to reports menu
        self.reports_menu()
        
    def system_overview(self):
        """Show system overview"""
        self.print_header("SYSTEM OVERVIEW")
        
        try:
            # Get counts
            patients_count = len(self.db.execute_query("SELECT patient_id FROM patients"))
            doctors_count = len(self.db.execute_query("SELECT doctor_id FROM doctors"))
            appointments_total = len(self.db.execute_query("SELECT appointment_id FROM appointments"))
            appointments_today = len(self.db.execute_query(
                "SELECT appointment_id FROM appointments WHERE DATE(appointment_date) = DATE('now')"
            ))
            
            print("📊 System Statistics:")
            print("=" * 40)
            print(f"Total Patients:       {patients_count}")
            print(f"Total Doctors:        {doctors_count}")
            print(f"Total Appointments:   {appointments_total}")
            print(f"Today's Appointments: {appointments_today}")
            print()
            
            # Recent activity
            print("📈 Recent Activity (Last 7 Days):")
            print("-" * 40)
            
            # New patients
            new_patients = len(self.db.execute_query(
                "SELECT patient_id FROM patients WHERE DATE(created_at) >= DATE('now', '-7 days')"
            ))
            print(f"New Patients:         {new_patients}")
            
            # Recent appointments
            recent_appointments = len(self.db.execute_query(
                "SELECT appointment_id FROM appointments WHERE DATE(appointment_date) >= DATE('now', '-7 days')"
            ))
            print(f"Appointments Booked:  {recent_appointments}")
            
        except Exception as e:
            print(f"❌ Error loading overview: {e}")
            
        input("\nPress Enter to continue...")
        
    def patient_statistics(self):
        """Show patient statistics"""
        self.print_header("PATIENT STATISTICS")
        
        try:
            # Gender distribution
            gender_data = self.db.execute_query(
                "SELECT gender, COUNT(*) as count FROM patients GROUP BY gender"
            )
            
            print("👥 Patient Demographics:")
            print("=" * 30)
            print("Gender Distribution:")
            for row in gender_data:
                print(f"  {row['gender']}: {row['count']} patients")
                
            print()
            
            # Age distribution (simplified)
            print("Age Groups (approximate):")
            age_ranges = [
                ("Children (0-18)", "date_of_birth >= DATE('now', '-18 years')"),
                ("Adults (19-65)", "date_of_birth < DATE('now', '-18 years') AND date_of_birth >= DATE('now', '-65 years')"),
                ("Seniors (65+)", "date_of_birth < DATE('now', '-65 years')")
            ]
            
            for label, condition in age_ranges:
                result = self.db.execute_query(f"SELECT COUNT(*) as count FROM patients WHERE {condition}")
                count = result[0]['count'] if result else 0
                print(f"  {label}: {count} patients")
                
        except Exception as e:
            print(f"❌ Error loading patient statistics: {e}")
            
        input("\nPress Enter to continue...")
        
    def doctor_statistics(self):
        """Show doctor statistics"""
        self.print_header("DOCTOR STATISTICS")
        
        try:
            # Specialization distribution
            spec_data = self.db.execute_query(
                "SELECT specialization, COUNT(*) as count FROM doctors GROUP BY specialization ORDER BY count DESC"
            )
            
            print("👨‍⚕️ Doctor Distribution by Specialization:")
            print("=" * 45)
            for row in spec_data:
                print(f"  {row['specialization']}: {row['count']} doctors")
                
            print()
            
            # Availability
            avail_data = self.db.execute_query(
                "SELECT is_available, COUNT(*) as count FROM doctors GROUP BY is_available"
            )
            
            print("Availability Status:")
            for row in avail_data:
                status = "Available" if row['is_available'] else "Unavailable"
                print(f"  {status}: {row['count']} doctors")
                
        except Exception as e:
            print(f"❌ Error loading doctor statistics: {e}")
            
        input("\nPress Enter to continue...")
        
    def appointment_report(self):
        """Show appointment report"""
        self.print_header("APPOINTMENT REPORT")
        
        try:
            # Status distribution
            status_data = self.db.execute_query(
                "SELECT status, COUNT(*) as count FROM appointments GROUP BY status"
            )
            
            print("📅 Appointment Status Distribution:")
            print("=" * 40)
            for row in status_data:
                print(f"  {row['status'].title()}: {row['count']} appointments")
                
            print()
            
            # This week's appointments
            week_data = self.db.execute_query(
                "SELECT DATE(appointment_date) as date, COUNT(*) as count FROM appointments WHERE DATE(appointment_date) >= DATE('now', '-7 days') GROUP BY DATE(appointment_date) ORDER BY date"
            )
            
            if week_data:
                print("This Week's Appointments:")
                for row in week_data:
                    print(f"  {row['date']}: {row['count']} appointments")
                    
        except Exception as e:
            print(f"❌ Error loading appointment report: {e}")
            
        input("\nPress Enter to continue...")
        
    def settings_menu(self):
        """Settings menu"""
        self.print_header("SYSTEM SETTINGS")
        
        print("⚙️ Settings Options:")
        print()
        print("1. 👤 User Management")
        print("2. 🔐 Change Password")
        print("3. 💾 Database Backup")
        print("4. 📁 List Backups")
        print("5. ℹ️  System Information")
        print("6. ⬅️  Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self.user_management()
        elif choice == '2':
            self.change_password()
        elif choice == '3':
            self.database_backup()
        elif choice == '4':
            self.list_backups()
        elif choice == '5':
            self.system_info()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice. Please select 1-6.")
            input("Press Enter to continue...")
            
        # Return to settings menu
        self.settings_menu()
        
    def user_management(self):
        """User management menu"""
        self.print_header("USER MANAGEMENT")
        
        print("👤 User Management Options:")
        print()
        print("1. 📋 View All Users")
        print("2. ➕ Add New User")
        print("3. ✏️  Edit User")
        print("4. 🗑️  Delete User")
        print("5. ⬅️  Back to Settings")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            self.view_users()
        elif choice == '2':
            self.add_user()
        elif choice == '3':
            self.edit_user()
        elif choice == '4':
            self.delete_user()
        elif choice == '5':
            return
        else:
            print("❌ Invalid choice. Please select 1-5.")
            input("Press Enter to continue...")
            
        # Return to user management menu
        self.user_management()
        
    def view_users(self):
        """View all users"""
        self.print_header("ALL USERS")
        
        try:
            query = '''
                SELECT user_id, username, role, full_name, email, phone, 
                       is_active, created_at
                FROM users 
                ORDER BY created_at DESC
            '''
            users = self.db.execute_query(query)
            
            if not users:
                print("No users found.")
                input("Press Enter to continue...")
                return
                
            print(f"Total Users: {len(users)}")
            print("-" * 80)
            
            for user in users:
                status = "🟢 Active" if user['is_active'] else "🔴 Inactive"
                print(f"ID: {user['user_id']} | Username: {user['username']} | Role: {user['role'].title()}")
                print(f"Name: {user['full_name']} | Status: {status}")
                print(f"Email: {user['email'] or 'N/A'} | Phone: {user['phone'] or 'N/A'}")
                print(f"Created: {user['created_at']}")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ Error retrieving users: {e}")
            
        input("Press Enter to continue...")
        
    def add_user(self):
        """Add new user"""
        self.print_header("ADD NEW USER")
        
        print("Enter user details:")
        print()
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username cannot be empty")
            input("Press Enter to continue...")
            return
            
        # Check if username exists
        check_query = "SELECT user_id FROM users WHERE username = ?"
        existing = self.db.execute_query(check_query, (username,))
        if existing:
            print("❌ Username already exists")
            input("Press Enter to continue...")
            return
            
        password = input("Password: ").strip()
        if not password:
            print("❌ Password cannot be empty")
            input("Press Enter to continue...")
            return
            
        full_name = input("Full Name: ").strip()
        if not full_name:
            print("❌ Full name cannot be empty")
            input("Press Enter to continue...")
            return
            
        print("\nAvailable roles:")
        print("1. Admin    2. Doctor    3. Nurse    4. Staff    5. User")
        role_choice = input("Select role (1-5): ").strip()
        
        roles = {'1': 'admin', '2': 'doctor', '3': 'nurse', '4': 'staff', '5': 'user'}
        role = roles.get(role_choice)
        
        if not role:
            print("❌ Invalid role selection")
            input("Press Enter to continue...")
            return
            
        email = input("Email (optional): ").strip() or None
        phone = input("Phone (optional): ").strip() or None
        
        try:
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            query = '''
                INSERT INTO users (username, password_hash, role, full_name, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            
            user_id = self.db.execute_insert(query, (username, password_hash, role, full_name, email, phone))
            
            print(f"\n✅ User '{username}' created successfully with ID: {user_id}")
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            
        input("Press Enter to continue...")
        
    def edit_user(self):
        """Edit user"""
        self.print_header("EDIT USER")
        
        user_id = input("Enter User ID to edit: ").strip()
        
        if not user_id.isdigit():
            print("❌ Please enter a valid user ID")
            input("Press Enter to continue...")
            return
            
        try:
            # Get current user data
            query = "SELECT * FROM users WHERE user_id = ?"
            result = self.db.execute_query(query, (int(user_id),))
            
            if not result:
                print(f"❌ No user found with ID: {user_id}")
                input("Press Enter to continue...")
                return
                
            user = result[0]
            
            print(f"\nEditing user: {user['username']} ({user['full_name']})")
            print("(Press Enter to keep current value)")
            print()
            
            # Get new values
            full_name = input(f"Full Name [{user['full_name']}]: ").strip() or user['full_name']
            email = input(f"Email [{user['email'] or 'N/A'}]: ").strip() or user['email']
            phone = input(f"Phone [{user['phone'] or 'N/A'}]: ").strip() or user['phone']
            
            print(f"\nCurrent role: {user['role']}")
            print("Available roles:")
            print("1. Admin    2. Doctor    3. Nurse    4. Staff    5. User")
            role_choice = input("Select new role (1-5, or Enter to keep current): ").strip()
            
            if role_choice:
                roles = {'1': 'admin', '2': 'doctor', '3': 'nurse', '4': 'staff', '5': 'user'}
                role = roles.get(role_choice, user['role'])
            else:
                role = user['role']
                
            status_choice = input(f"Active status [{'Yes' if user['is_active'] else 'No'}] (Y/N): ").strip().lower()
            if status_choice in ['y', 'yes']:
                is_active = 1
            elif status_choice in ['n', 'no']:
                is_active = 0
            else:
                is_active = user['is_active']
            
            # Update database
            update_query = '''
                UPDATE users 
                SET full_name = ?, email = ?, phone = ?, role = ?, is_active = ?
                WHERE user_id = ?
            '''
            
            self.db.execute_update(update_query, (full_name, email, phone, role, is_active, int(user_id)))
            
            print(f"\n✅ User updated successfully!")
            
        except Exception as e:
            print(f"❌ Error editing user: {e}")
            
        input("Press Enter to continue...")
        
    def delete_user(self):
        """Delete user"""
        self.print_header("DELETE USER")
        
        user_id = input("Enter User ID to delete: ").strip()
        
        if not user_id.isdigit():
            print("❌ Please enter a valid user ID")
            input("Press Enter to continue...")
            return
            
        try:
            # Get user data first
            query = "SELECT username, full_name FROM users WHERE user_id = ?"
            result = self.db.execute_query(query, (int(user_id),))
            
            if not result:
                print(f"❌ No user found with ID: {user_id}")
                input("Press Enter to continue...")
                return
                
            user = result[0]
            
            # Prevent deleting current user
            if self.current_user and self.current_user.get('user_id') == int(user_id):
                print("❌ Cannot delete currently logged in user")
                input("Press Enter to continue...")
                return
            
            # Confirm deletion
            print(f"\n⚠️  WARNING: You are about to delete user:")
            print(f"   ID: {user_id}")
            print(f"   Username: {user['username']}")
            print(f"   Name: {user['full_name']}")
            print("\nThis action cannot be undone!")
            
            confirm = input("\nType 'DELETE' to confirm: ").strip()
            
            if confirm == 'DELETE':
                # Delete user
                self.db.execute_update("DELETE FROM users WHERE user_id = ?", (int(user_id),))
                print(f"\n✅ User '{user['username']}' deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")
                
        except Exception as e:
            print(f"❌ Error deleting user: {e}")
            
        input("Press Enter to continue...")
        
    def change_password(self):
        """Change current user's password"""
        self.print_header("CHANGE PASSWORD")
        
        if not self.current_user:
            print("❌ No user logged in")
            input("Press Enter to continue...")
            return
            
        print(f"Changing password for: {self.current_user['username']}")
        print()
        
        current_password = input("Enter current password: ").strip()
        if not current_password:
            print("❌ Current password cannot be empty")
            input("Press Enter to continue...")
            return
            
        # Verify current password
        current_hash = hashlib.sha256(current_password.encode()).hexdigest()
        query = "SELECT user_id FROM users WHERE user_id = ? AND password_hash = ?"
        result = self.db.execute_query(query, (self.current_user['user_id'], current_hash))
        
        if not result:
            print("❌ Current password is incorrect")
            input("Press Enter to continue...")
            return
            
        new_password = input("Enter new password: ").strip()
        if not new_password:
            print("❌ New password cannot be empty")
            input("Press Enter to continue...")
            return
            
        confirm_password = input("Confirm new password: ").strip()
        
        if new_password != confirm_password:
            print("❌ New passwords do not match")
            input("Press Enter to continue...")
            return
            
        try:
            # Update password
            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
            update_query = "UPDATE users SET password_hash = ? WHERE user_id = ?"
            self.db.execute_update(update_query, (new_hash, self.current_user['user_id']))
            
            print("\n✅ Password changed successfully!")
            
        except Exception as e:
            print(f"❌ Error changing password: {e}")
            
        input("Press Enter to continue...")
        
    def database_backup(self):
        """Create database backup"""
        self.print_header("DATABASE BACKUP")
        
        try:
            # Get the database file path from the database manager
            db_path = "data/hospital.db"  # Default database path
            
            # Check if database file exists
            if not os.path.exists(db_path):
                print("❌ Database file not found!")
                print(f"Expected location: {os.path.abspath(db_path)}")
                print("The database will be created when you first use the system.")
                input("Press Enter to continue...")
                return
            
            # Create backups directory if it doesn't exist
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = os.path.join(backup_dir, f"hospital_db_backup_{timestamp}.db")
            
            # Copy database file
            shutil.copy2(db_path, backup_filename)
            
            print(f"✅ Database backup created successfully!")
            print(f"📁 Backup file: {os.path.basename(backup_filename)}")
            print(f"📊 Location: {os.path.abspath(backup_filename)}")
            
            # Show backup size
            backup_size = os.path.getsize(backup_filename)
            print(f"💾 Size: {backup_size:,} bytes")
            
            # Show backup time
            print(f"⏰ Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            print(f"Details: {str(e)}")
            
        input("Press Enter to continue...")
        
    def list_backups(self):
        """List existing backup files"""
        self.print_header("EXISTING BACKUPS")
        
        backup_dir = "backups"
        
        try:
            if not os.path.exists(backup_dir):
                print("📁 No backup directory found.")
                print("Create your first backup to see backups listed here.")
                input("Press Enter to continue...")
                return
            
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
            
            if not backup_files:
                print("📁 No backup files found in the backups directory.")
                input("Press Enter to continue...")
                return
            
            print(f"Found {len(backup_files)} backup file(s):")
            print("=" * 60)
            
            for i, backup_file in enumerate(sorted(backup_files, reverse=True), 1):
                backup_path = os.path.join(backup_dir, backup_file)
                file_size = os.path.getsize(backup_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(backup_path))
                
                print(f"{i}. 📄 {backup_file}")
                print(f"   💾 Size: {file_size:,} bytes")
                print(f"   ⏰ Modified: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
        except Exception as e:
            print(f"❌ Error listing backups: {e}")
            
        input("Press Enter to continue...")
    
    def system_info(self):
        """Show system information"""
        self.print_header("SYSTEM INFORMATION")
        
        print("ℹ️ Hospital Management System v2.0")
        print("=" * 40)
        print("Version: 2.0 (Simple Interface)")
        print("Database: SQLite")
        print("Interface: Console-based")
        print("Created: 2025")
        print()
        print("Features:")
        print("• Patient Management")
        print("• Doctor Management")
        print("• Appointment Scheduling")
        print("• Billing System")
        print("• Reports & Analytics")
        print("• User Authentication")
        print()
        print(f"Current User: {self.current_user['full_name'] if self.current_user else 'Unknown'}")
        print(f"Role: {self.current_user['role'].title() if self.current_user else 'Unknown'}")
        print(f"Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        input("\nPress Enter to continue...")
        
    def search_patients(self):
        """Search patients"""
        self.print_header("SEARCH PATIENTS")
        
        search_term = input("Enter search term (name, ID, or national ID): ").strip()
        
        if not search_term:
            print("❌ Please enter a search term")
            input("Press Enter to continue...")
            return
            
        try:
            query = '''
                SELECT patient_id, national_id, first_name, last_name, 
                       date_of_birth, gender, phone
                FROM patients 
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ? 
                   OR LOWER(national_id) LIKE ? OR CAST(patient_id AS TEXT) LIKE ?
                ORDER BY last_name, first_name
            '''
            
            search_pattern = f"%{search_term.lower()}%"
            results = self.db.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            
            if not results:
                print(f"📭 No patients found matching '{search_term}'")
            else:
                print(f"Found {len(results)} patients matching '{search_term}':")
                print()
                print("ID  | National ID | Name                    | DOB        | Gender | Phone")
                print("-" * 80)
                
                for patient in results:
                    name = f"{patient['first_name']} {patient['last_name']}"
                    phone = patient['phone'] or 'N/A'
                    
                    print(f"{patient['patient_id']:<3} | {patient['national_id']:<11} | "
                          f"{name:<23} | {patient['date_of_birth']} | "
                          f"{patient['gender']:<6} | {phone}")
                          
        except Exception as e:
            print(f"❌ Error searching patients: {e}")
            
        input("\nPress Enter to continue...")
        
    def edit_patient(self):
        """Edit patient information"""
        self.print_header("EDIT PATIENT")
        
        patient_id = input("Enter Patient ID to edit: ").strip()
        
        if not patient_id.isdigit():
            print("❌ Please enter a valid patient ID")
            input("Press Enter to continue...")
            return
            
        try:
            # Get current patient data
            query = "SELECT * FROM patients WHERE patient_id = ?"
            result = self.db.execute_query(query, (int(patient_id),))
            
            if not result:
                print(f"❌ No patient found with ID: {patient_id}")
                input("Press Enter to continue...")
                return
                
            patient = result[0]
            
            print(f"\nEditing patient: {patient['first_name']} {patient['last_name']}")
            print("(Press Enter to keep current value)")
            print()
            
            # Get new values
            first_name = input(f"First Name [{patient['first_name']}]: ").strip() or patient['first_name']
            last_name = input(f"Last Name [{patient['last_name']}]: ").strip() or patient['last_name']
            phone = input(f"Phone [{patient['phone'] or 'N/A'}]: ").strip() or patient['phone']
            email = input(f"Email [{patient['email'] or 'N/A'}]: ").strip() or patient['email']
            address = input(f"Address [{patient['address'] or 'N/A'}]: ").strip() or patient['address']
            
            # Update database
            update_query = '''
                UPDATE patients 
                SET first_name = ?, last_name = ?, phone = ?, email = ?, address = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE patient_id = ?
            '''
            
            self.db.execute_update(update_query, (first_name, last_name, phone, email, address, int(patient_id)))
            
            print(f"\n✅ Patient updated successfully!")
            
        except Exception as e:
            print(f"❌ Error editing patient: {e}")
            
        input("Press Enter to continue...")
        
    def delete_patient(self):
        """Delete patient"""
        self.print_header("DELETE PATIENT")
        
        patient_id = input("Enter Patient ID to delete: ").strip()
        
        if not patient_id.isdigit():
            print("❌ Please enter a valid patient ID")
            input("Press Enter to continue...")
            return
            
        try:
            # Get patient data first
            query = "SELECT first_name, last_name FROM patients WHERE patient_id = ?"
            result = self.db.execute_query(query, (int(patient_id),))
            
            if not result:
                print(f"❌ No patient found with ID: {patient_id}")
                input("Press Enter to continue...")
                return
                
            patient = result[0]
            patient_name = f"{patient['first_name']} {patient['last_name']}"
            
            # Confirm deletion
            print(f"\n⚠️  WARNING: You are about to delete patient:")
            print(f"   ID: {patient_id}")
            print(f"   Name: {patient_name}")
            print("\nThis action cannot be undone!")
            
            confirm = input("\nType 'DELETE' to confirm: ").strip()
            
            if confirm == 'DELETE':
                # Delete patient
                self.db.execute_update("DELETE FROM patients WHERE patient_id = ?", (int(patient_id),))
                print(f"\n✅ Patient '{patient_name}' deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")
                
        except Exception as e:
            print(f"❌ Error deleting patient: {e}")
            
        input("Press Enter to continue...")
        
    def run_system(self):
        """Main system loop"""
        if self.login():
            self.main_menu()
        
        print("\n👋 Thank you for using Hospital Management System v2.0!")
        self.db.close()

def main():
    """Main function"""
    try:
        SimpleHospitalSystem()
    except KeyboardInterrupt:
        print("\n\n👋 System interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ System error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
