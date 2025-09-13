"""
Doctor Management Module
Comprehensive doctor registration and management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class DoctorManagement:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.create_widgets()
        self.load_doctors()
        
    def create_widgets(self):
        """Create doctor management interface"""
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text="👨‍⚕️ Doctor Management",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Control buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="➕ Add Doctor",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.add_doctor
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
            command=self.edit_doctor
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📅 Schedule",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.manage_schedule
        ).pack(side='left', padx=5)
        
        # Search and filter
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
        
        # Specialization filter
        tk.Label(
            search_frame,
            text="Specialization:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left', padx=(20, 5))
        
        self.spec_var = tk.StringVar(value="All")
        spec_combo = ttk.Combobox(
            search_frame,
            textvariable=self.spec_var,
            values=["All", "Cardiology", "Neurology", "Orthopedics", "Pediatrics", 
                   "General Medicine", "Surgery", "Emergency", "Radiology"],
            width=15,
            state="readonly"
        )
        spec_combo.pack(side='left', padx=5)
        spec_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Doctor list
        self.create_doctor_list()
        
    def create_doctor_list(self):
        """Create doctor list with treeview"""
        list_frame = tk.Frame(self.parent, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Employee ID', 'Name', 'Specialization', 'Experience', 
                  'Phone', 'Fee', 'Status', 'Patients Today')
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = {'ID': 50, 'Employee ID': 100, 'Name': 150, 'Specialization': 120,
                        'Experience': 80, 'Phone': 120, 'Fee': 80, 'Status': 80, 'Patients Today': 100}
        
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
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
    def load_doctors(self):
        """Load doctors from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get doctors data with appointment count for today
            query = '''
                SELECT d.doctor_id, d.employee_id,
                       (d.first_name || ' ' || d.last_name) as full_name,
                       d.specialization, d.experience_years, d.phone,
                       d.consultation_fee, 
                       CASE WHEN d.is_available = 1 THEN 'Available' ELSE 'Unavailable' END as status,
                       COUNT(a.appointment_id) as appointments_today
                FROM doctors d
                LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
                    AND DATE(a.appointment_date) = DATE('now')
                GROUP BY d.doctor_id
                ORDER BY d.doctor_id DESC
            '''
            
            doctors = self.db_manager.execute_query(query)
            
            for doctor in doctors:
                self.tree.insert('', 'end', values=(
                    doctor['doctor_id'],
                    doctor['employee_id'],
                    doctor['full_name'],
                    doctor['specialization'],
                    f"{doctor['experience_years']} years" if doctor['experience_years'] else 'N/A',
                    doctor['phone'] or 'N/A',
                    f"${doctor['consultation_fee']}" if doctor['consultation_fee'] else 'N/A',
                    doctor['status'],
                    doctor['appointments_today']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")
            
    def on_search(self, *args):
        """Handle search input"""
        search_text = self.search_var.get().lower()
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not search_text:
            self.load_doctors()
            return
            
        # Search in database
        query = '''
            SELECT d.doctor_id, d.employee_id,
                   (d.first_name || ' ' || d.last_name) as full_name,
                   d.specialization, d.experience_years, d.phone,
                   d.consultation_fee,
                   CASE WHEN d.is_available = 1 THEN 'Available' ELSE 'Unavailable' END as status,
                   COUNT(a.appointment_id) as appointments_today
            FROM doctors d
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
                AND DATE(a.appointment_date) = DATE('now')
            WHERE LOWER(d.first_name) LIKE ? OR LOWER(d.last_name) LIKE ? 
               OR LOWER(d.employee_id) LIKE ? OR LOWER(d.specialization) LIKE ?
            GROUP BY d.doctor_id
            ORDER BY d.doctor_id DESC
        '''
        
        search_pattern = f"%{search_text}%"
        doctors = self.db_manager.execute_query(
            query, (search_pattern, search_pattern, search_pattern, search_pattern)
        )
        
        for doctor in doctors:
            self.tree.insert('', 'end', values=(
                doctor['doctor_id'],
                doctor['employee_id'],
                doctor['full_name'],
                doctor['specialization'],
                f"{doctor['experience_years']} years" if doctor['experience_years'] else 'N/A',
                doctor['phone'] or 'N/A',
                f"${doctor['consultation_fee']}" if doctor['consultation_fee'] else 'N/A',
                doctor['status'],
                doctor['appointments_today']
            ))
            
    def on_filter(self, *args):
        """Handle specialization filter"""
        self.load_doctors()  # Simplified - could implement actual filtering
        
    def on_item_double_click(self, event):
        """Handle double-click on doctor item"""
        self.view_doctor_details()
        
    def add_doctor(self):
        """Open add doctor dialog"""
        AddDoctorDialog(self.parent, self.db_manager, self.load_doctors)
        
    def edit_doctor(self):
        """Edit selected doctor"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a doctor to edit.")
            return
            
        doctor_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Edit doctor {doctor_id} - Implementation in progress")
        
    def manage_schedule(self):
        """Manage doctor schedule"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a doctor to manage schedule.")
            return
            
        doctor_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Schedule management for doctor {doctor_id} - Implementation in progress")
        
    def view_doctor_details(self):
        """View detailed doctor information"""
        selected = self.tree.selection()
        if not selected:
            return
            
        doctor_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Doctor details for {doctor_id} - Implementation in progress")
        
    def refresh(self):
        """Refresh doctor list"""
        self.load_doctors()

class AddDoctorDialog:
    def __init__(self, parent, db_manager, callback):
        self.db_manager = db_manager
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Doctor")
        self.dialog.geometry("600x600")
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
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"600x600+{x}+{y}")
        
    def create_widgets(self):
        """Create form widgets"""
        # Header
        header = tk.Label(
            self.dialog,
            text="👨‍⚕️ Add New Doctor",
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
            ("Employee ID*", "employee_id"),
            ("First Name*", "first_name"),
            ("Last Name*", "last_name"),
            ("Specialization*", "specialization"),
            ("Qualification", "qualification"),
            ("Experience (Years)", "experience_years"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
            ("Consultation Fee", "consultation_fee"),
            ("Available", "is_available")
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
            ).grid(row=i, column=0, sticky='w', pady=8)
            
            # Entry
            if field == "specialization":
                self.entries[field] = ttk.Combobox(
                    form_frame,
                    values=["Cardiology", "Neurology", "Orthopedics", "Pediatrics", 
                           "General Medicine", "Surgery", "Emergency", "Radiology",
                           "Dermatology", "Psychiatry", "Gynecology", "Urology"],
                    width=30
                )
            elif field == "is_available":
                self.entries[field] = ttk.Combobox(
                    form_frame,
                    values=["Yes", "No"],
                    width=30,
                    state="readonly"
                )
                self.entries[field].set("Yes")
            else:
                self.entries[field] = tk.Entry(
                    form_frame,
                    width=35,
                    font=('Arial', 10)
                )
                
            self.entries[field].grid(row=i, column=1, sticky='w', padx=10, pady=8)
            
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Save Doctor",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_doctor
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
        
    def save_doctor(self):
        """Save new doctor to database"""
        try:
            # Get form data
            data = {}
            for field, widget in self.entries.items():
                data[field] = widget.get().strip()
                    
            # Validate required fields
            required = ['employee_id', 'first_name', 'last_name', 'specialization']
            for field in required:
                if not data[field]:
                    messagebox.showerror("Validation Error", f"{field.replace('_', ' ').title()} is required.")
                    return
                    
            # Validate numeric fields
            if data['experience_years'] and not data['experience_years'].isdigit():
                messagebox.showerror("Validation Error", "Experience must be a number.")
                return
                
            if data['consultation_fee']:
                try:
                    float(data['consultation_fee'])
                except ValueError:
                    messagebox.showerror("Validation Error", "Consultation fee must be a valid number.")
                    return
                    
            # Convert boolean
            is_available = 1 if data['is_available'] == 'Yes' else 0
            
            # Insert into database
            query = '''
                INSERT INTO doctors (
                    employee_id, first_name, last_name, specialization,
                    qualification, experience_years, phone, email, address,
                    consultation_fee, is_available
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                data['employee_id'], data['first_name'], data['last_name'],
                data['specialization'], data['qualification'], 
                int(data['experience_years']) if data['experience_years'] else None,
                data['phone'], data['email'], data['address'],
                float(data['consultation_fee']) if data['consultation_fee'] else None,
                is_available
            )
            
            self.db_manager.execute_insert(query, values)
            
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.callback()  # Refresh doctor list
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save doctor: {str(e)}")
