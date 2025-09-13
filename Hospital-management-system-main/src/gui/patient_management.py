"""
Patient Management Module
Advanced patient registration, search, and management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

class PatientManagement:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.create_widgets()
        self.load_patients()
        
    def create_widgets(self):
        """Create patient management interface"""
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text="👥 Patient Management",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Control buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="➕ Add Patient",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.add_patient
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit",
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.edit_patient
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.delete_patient
        ).pack(side='left', padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.parent, bg='white')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', padx=10)
        
        # Filter dropdown
        tk.Label(
            search_frame,
            text="Filter by:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left', padx=(20, 5))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_var,
            values=["All", "Male", "Female", "Emergency"],
            width=15,
            state="readonly"
        )
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Patient list
        self.create_patient_list()
        
    def create_patient_list(self):
        """Create patient list with treeview"""
        list_frame = tk.Frame(self.parent, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'National ID', 'Name', 'Age', 'Gender', 'Phone', 'Department', 'Doctor')
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = {'ID': 50, 'National ID': 100, 'Name': 150, 'Age': 60, 
                        'Gender': 80, 'Phone': 120, 'Department': 120, 'Doctor': 150}
        
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=column_widths.get(col, 100), anchor='w')
            
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
    def load_patients(self):
        """Load patients from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get patients data
            query = '''
                SELECT p.patient_id, p.national_id, 
                       (p.first_name || ' ' || p.last_name) as full_name,
                       (DATE('now') - p.date_of_birth) as age,
                       p.gender, p.phone, 
                       COALESCE(d.specialization, 'Not Assigned') as department,
                       COALESCE((d.first_name || ' ' || d.last_name), 'Not Assigned') as doctor
                FROM patients p
                LEFT JOIN appointments a ON p.patient_id = a.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY p.patient_id DESC
            '''
            
            patients = self.db_manager.execute_query(query)
            
            for patient in patients:
                # Calculate age from date of birth
                age = "N/A"
                try:
                    if patient['age']:
                        age = str(patient['age'])
                except:
                    pass
                    
                self.tree.insert('', 'end', values=(
                    patient['patient_id'],
                    patient['national_id'],
                    patient['full_name'],
                    age,
                    patient['gender'],
                    patient['phone'] or 'N/A',
                    patient['department'],
                    patient['doctor']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
            
    def on_search(self, *args):
        """Handle search input"""
        search_text = self.search_var.get().lower()
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not search_text:
            self.load_patients()
            return
            
        # Search in database
        query = '''
            SELECT p.patient_id, p.national_id, 
                   (p.first_name || ' ' || p.last_name) as full_name,
                   (DATE('now') - p.date_of_birth) as age,
                   p.gender, p.phone,
                   COALESCE(d.specialization, 'Not Assigned') as department,
                   COALESCE((d.first_name || ' ' || d.last_name), 'Not Assigned') as doctor
            FROM patients p
            LEFT JOIN appointments a ON p.patient_id = a.patient_id
            LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE LOWER(p.first_name) LIKE ? OR LOWER(p.last_name) LIKE ? 
               OR LOWER(p.national_id) LIKE ? OR LOWER(p.phone) LIKE ?
            ORDER BY p.patient_id DESC
        '''
        
        search_pattern = f"%{search_text}%"
        patients = self.db_manager.execute_query(
            query, (search_pattern, search_pattern, search_pattern, search_pattern)
        )
        
        for patient in patients:
            age = "N/A"
            try:
                if patient['age']:
                    age = str(patient['age'])
            except:
                pass
                
            self.tree.insert('', 'end', values=(
                patient['patient_id'],
                patient['national_id'],
                patient['full_name'],
                age,
                patient['gender'],
                patient['phone'] or 'N/A',
                patient['department'],
                patient['doctor']
            ))
            
    def on_filter(self, *args):
        """Handle filter selection"""
        # Implementation for filtering
        self.load_patients()
        
    def on_item_double_click(self, event):
        """Handle double-click on patient item"""
        self.view_patient_details()
        
    def add_patient(self):
        """Open add patient dialog"""
        AddPatientDialog(self.parent, self.db_manager, self.load_patients)
        
    def edit_patient(self):
        """Edit selected patient"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a patient to edit.")
            return
            
        patient_id = self.tree.item(selected[0])['values'][0]
        EditPatientDialog(self.parent, self.db_manager, patient_id, self.load_patients)
        
    def delete_patient(self):
        """Delete selected patient"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a patient to delete.")
            return
            
        patient_id = self.tree.item(selected[0])['values'][0]
        patient_name = self.tree.item(selected[0])['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient '{patient_name}'?"):
            try:
                self.db_manager.execute_update("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
                messagebox.showinfo("Success", "Patient deleted successfully.")
                self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
                
    def view_patient_details(self):
        """View detailed patient information"""
        selected = self.tree.selection()
        if not selected:
            return
            
        patient_id = self.tree.item(selected[0])['values'][0]
        PatientDetailsDialog(self.parent, self.db_manager, patient_id)
        
    def refresh(self):
        """Refresh patient list"""
        self.load_patients()

class AddPatientDialog:
    def __init__(self, parent, db_manager, callback):
        self.db_manager = db_manager
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Patient")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='white')
        
        # Center dialog
        self.center_dialog()
        
        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def center_dialog(self):
        """Center the dialog window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
        
    def create_widgets(self):
        """Create form widgets"""
        # Header
        header = tk.Label(
            self.dialog,
            text="➕ Add New Patient",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.dialog, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Form fields
        fields = [
            ("National ID*", "national_id"),
            ("First Name*", "first_name"),
            ("Last Name*", "last_name"),
            ("Date of Birth* (YYYY-MM-DD)", "date_of_birth"),
            ("Gender*", "gender"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
            ("Emergency Contact", "emergency_contact"),
            ("Emergency Phone", "emergency_phone"),
            ("Blood Group", "blood_group"),
            ("Allergies", "allergies"),
            ("Insurance Info", "insurance_info")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            # Label
            tk.Label(
                form_frame,
                text=label,
                font=('Arial', 11),
                bg='white',
                fg='#34495e'
            ).grid(row=i, column=0, sticky='w', pady=5)
            
            # Entry
            if field == "gender":
                self.entries[field] = ttk.Combobox(
                    form_frame,
                    values=["Male", "Female", "Other"],
                    width=30,
                    state="readonly"
                )
            elif field in ["allergies", "insurance_info"]:
                self.entries[field] = tk.Text(
                    form_frame,
                    width=35,
                    height=3,
                    font=('Arial', 10)
                )
            else:
                self.entries[field] = tk.Entry(
                    form_frame,
                    width=35,
                    font=('Arial', 10)
                )
                
            self.entries[field].grid(row=i, column=1, sticky='w', padx=10, pady=5)
            
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Save Patient",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_patient
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#7f8c8d',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.dialog.destroy
        ).pack(side='left', padx=10)
        
    def save_patient(self):
        """Save new patient to database"""
        try:
            # Get form data
            data = {}
            for field, widget in self.entries.items():
                if isinstance(widget, tk.Text):
                    data[field] = widget.get(1.0, 'end-1c').strip()
                else:
                    data[field] = widget.get().strip()
                    
            # Validate required fields
            required = ['national_id', 'first_name', 'last_name', 'date_of_birth', 'gender']
            for field in required:
                if not data[field]:
                    messagebox.showerror("Validation Error", f"{field.replace('_', ' ').title()} is required.")
                    return
                    
            # Validate date format
            try:
                datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid date format. Use YYYY-MM-DD.")
                return
                
            # Validate email if provided
            if data['email'] and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', data['email']):
                messagebox.showerror("Validation Error", "Invalid email format.")
                return
                
            # Insert into database
            query = '''
                INSERT INTO patients (
                    national_id, first_name, last_name, date_of_birth, gender,
                    phone, email, address, emergency_contact, emergency_phone,
                    blood_group, allergies, insurance_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                data['national_id'], data['first_name'], data['last_name'],
                data['date_of_birth'], data['gender'], data['phone'],
                data['email'], data['address'], data['emergency_contact'],
                data['emergency_phone'], data['blood_group'], data['allergies'],
                data['insurance_info']
            )
            
            self.db_manager.execute_insert(query, values)
            
            messagebox.showinfo("Success", "Patient added successfully!")
            self.callback()  # Refresh patient list
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patient: {str(e)}")

class EditPatientDialog:
    def __init__(self, parent, db_manager, patient_id, callback):
        self.db_manager = db_manager
        self.patient_id = patient_id
        self.callback = callback
        
        # Similar to AddPatientDialog but with pre-filled data
        # Implementation would be similar to AddPatientDialog
        messagebox.showinfo("Info", "Edit Patient dialog - Implementation in progress")

class PatientDetailsDialog:
    def __init__(self, parent, db_manager, patient_id):
        self.db_manager = db_manager
        self.patient_id = patient_id
        
        # Create details dialog
        # Implementation would show comprehensive patient information
        messagebox.showinfo("Info", "Patient Details dialog - Implementation in progress")
