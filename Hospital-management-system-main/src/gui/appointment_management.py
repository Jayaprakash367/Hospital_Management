"""
Appointment Management Module
Advanced appointment scheduling and management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

class AppointmentManagement:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.create_widgets()
        self.load_appointments()
        
    def create_widgets(self):
        """Create appointment management interface"""
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text="📅 Appointment Management",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Control buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="➕ New Appointment",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.new_appointment
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Reschedule",
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.reschedule_appointment
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.cancel_appointment
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="✅ Complete",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.complete_appointment
        ).pack(side='left', padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(self.parent, bg='white')
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Date filter
        tk.Label(
            filter_frame,
            text="📅 Date:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left')
        
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(
            filter_frame,
            textvariable=self.date_var,
            font=('Arial', 11),
            width=12,
            relief='solid',
            bd=1
        )
        date_entry.pack(side='left', padx=10)
        
        tk.Button(
            filter_frame,
            text="Today",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            cursor='hand2',
            command=self.show_today
        ).pack(side='left', padx=5)
        
        # Status filter
        tk.Label(
            filter_frame,
            text="Status:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left', padx=(20, 5))
        
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "Scheduled", "Completed", "Cancelled", "No Show"],
            width=12,
            state="readonly"
        )
        status_combo.pack(side='left', padx=5)
        status_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Doctor filter
        tk.Label(
            filter_frame,
            text="Doctor:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left', padx=(20, 5))
        
        self.doctor_var = tk.StringVar(value="All")
        self.doctor_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.doctor_var,
            width=20,
            state="readonly"
        )
        self.doctor_combo.pack(side='left', padx=5)
        self.doctor_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Load doctors for filter
        self.load_doctors_filter()
        
        # Appointment list
        self.create_appointment_list()
        
    def create_appointment_list(self):
        """Create appointment list with treeview"""
        list_frame = tk.Frame(self.parent, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Time', 'Patient', 'Doctor', 'Duration', 'Status', 'Notes')
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = {'ID': 50, 'Time': 80, 'Patient': 150, 'Doctor': 150,
                        'Duration': 80, 'Status': 100, 'Notes': 200}
        
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
        
        # Configure row colors based on status
        self.tree.tag_configure('scheduled', background='#e8f5e8')
        self.tree.tag_configure('completed', background='#e8f4f8')
        self.tree.tag_configure('cancelled', background='#f8e8e8')
        self.tree.tag_configure('no_show', background='#fff2e8')
        
    def load_doctors_filter(self):
        """Load doctors for filter dropdown"""
        try:
            doctors = self.db_manager.execute_query(
                "SELECT doctor_id, first_name, last_name FROM doctors ORDER BY first_name"
            )
            
            doctor_list = ["All"]
            for doctor in doctors:
                doctor_list.append(f"{doctor['first_name']} {doctor['last_name']}")
                
            self.doctor_combo['values'] = doctor_list
            
        except Exception as e:
            print(f"Failed to load doctors: {e}")
            
    def load_appointments(self):
        """Load appointments from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get current date filter
            filter_date = self.date_var.get()
            
            # Build query with filters
            query = '''
                SELECT a.appointment_id, a.appointment_time, a.duration_minutes,
                       a.status, a.notes,
                       (p.first_name || ' ' || p.last_name) as patient_name,
                       (d.first_name || ' ' || d.last_name) as doctor_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE DATE(a.appointment_date) = ?
                ORDER BY a.appointment_time
            '''
            
            appointments = self.db_manager.execute_query(query, (filter_date,))
            
            for appointment in appointments:
                # Determine row tag based on status
                status = appointment['status'].lower()
                tag = status if status in ['scheduled', 'completed', 'cancelled'] else 'no_show'
                
                self.tree.insert('', 'end', values=(
                    appointment['appointment_id'],
                    appointment['appointment_time'],
                    appointment['patient_name'],
                    appointment['doctor_name'],
                    f"{appointment['duration_minutes']} min",
                    appointment['status'].title(),
                    appointment['notes'] or ''
                ), tags=(tag,))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")
            
    def on_filter(self, *args):
        """Handle filter changes"""
        self.load_appointments()
        
    def show_today(self):
        """Show today's appointments"""
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.load_appointments()
        
    def on_item_double_click(self, event):
        """Handle double-click on appointment item"""
        self.view_appointment_details()
        
    def new_appointment(self):
        """Open new appointment dialog"""
        NewAppointmentDialog(self.parent, self.db_manager, self.load_appointments)
        
    def reschedule_appointment(self):
        """Reschedule selected appointment"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an appointment to reschedule.")
            return
            
        appointment_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Reschedule appointment {appointment_id} - Implementation in progress")
        
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an appointment to cancel.")
            return
            
        appointment_id = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            try:
                self.db_manager.execute_update(
                    "UPDATE appointments SET status = 'cancelled' WHERE appointment_id = ?",
                    (appointment_id,)
                )
                messagebox.showinfo("Success", "Appointment cancelled successfully.")
                self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
                
    def complete_appointment(self):
        """Mark appointment as completed"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an appointment to complete.")
            return
            
        appointment_id = self.tree.item(selected[0])['values'][0]
        
        try:
            self.db_manager.execute_update(
                "UPDATE appointments SET status = 'completed' WHERE appointment_id = ?",
                (appointment_id,)
            )
            messagebox.showinfo("Success", "Appointment marked as completed.")
            self.load_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete appointment: {str(e)}")
            
    def view_appointment_details(self):
        """View detailed appointment information"""
        selected = self.tree.selection()
        if not selected:
            return
            
        appointment_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Appointment details for {appointment_id} - Implementation in progress")
        
    def refresh(self):
        """Refresh appointment list"""
        self.load_appointments()

class NewAppointmentDialog:
    def __init__(self, parent, db_manager, callback):
        self.db_manager = db_manager
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Appointment")
        self.dialog.geometry("500x600")
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
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
    def create_widgets(self):
        """Create form widgets"""
        # Header
        header = tk.Label(
            self.dialog,
            text="📅 Schedule New Appointment",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.dialog, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Patient selection
        tk.Label(
            form_frame,
            text="Patient*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            form_frame,
            textvariable=self.patient_var,
            width=35,
            state="readonly"
        )
        self.patient_combo.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        
        # Doctor selection
        tk.Label(
            form_frame,
            text="Doctor*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            form_frame,
            textvariable=self.doctor_var,
            width=35,
            state="readonly"
        )
        self.doctor_combo.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        
        # Date
        tk.Label(
            form_frame,
            text="Date*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = tk.Entry(
            form_frame,
            textvariable=self.date_var,
            width=35,
            font=('Arial', 10)
        )
        self.date_entry.grid(row=2, column=1, sticky='w', padx=10, pady=10)
        
        # Time
        tk.Label(
            form_frame,
            text="Time*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=3, column=0, sticky='w', pady=10)
        
        time_frame = tk.Frame(form_frame, bg='white')
        time_frame.grid(row=3, column=1, sticky='w', padx=10, pady=10)
        
        self.hour_var = tk.StringVar(value="09")
        hour_combo = ttk.Combobox(
            time_frame,
            textvariable=self.hour_var,
            values=[f"{i:02d}" for i in range(8, 18)],
            width=5,
            state="readonly"
        )
        hour_combo.pack(side='left')
        
        tk.Label(time_frame, text=":", bg='white', font=('Arial', 12)).pack(side='left', padx=5)
        
        self.minute_var = tk.StringVar(value="00")
        minute_combo = ttk.Combobox(
            time_frame,
            textvariable=self.minute_var,
            values=["00", "15", "30", "45"],
            width=5,
            state="readonly"
        )
        minute_combo.pack(side='left')
        
        # Duration
        tk.Label(
            form_frame,
            text="Duration (minutes)*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=4, column=0, sticky='w', pady=10)
        
        self.duration_var = tk.StringVar(value="30")
        duration_combo = ttk.Combobox(
            form_frame,
            textvariable=self.duration_var,
            values=["15", "30", "45", "60"],
            width=35,
            state="readonly"
        )
        duration_combo.grid(row=4, column=1, sticky='w', padx=10, pady=10)
        
        # Notes
        tk.Label(
            form_frame,
            text="Notes",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=5, column=0, sticky='nw', pady=10)
        
        self.notes_text = tk.Text(
            form_frame,
            width=35,
            height=4,
            font=('Arial', 10),
            wrap='word'
        )
        self.notes_text.grid(row=5, column=1, sticky='w', padx=10, pady=10)
        
        # Load data
        self.load_patients()
        self.load_doctors()
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Schedule Appointment",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_appointment
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
        
    def load_patients(self):
        """Load patients for dropdown"""
        try:
            patients = self.db_manager.execute_query(
                "SELECT patient_id, first_name, last_name FROM patients ORDER BY first_name"
            )
            
            patient_list = []
            self.patient_data = {}
            
            for patient in patients:
                name = f"{patient['first_name']} {patient['last_name']}"
                patient_list.append(name)
                self.patient_data[name] = patient['patient_id']
                
            self.patient_combo['values'] = patient_list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
            
    def load_doctors(self):
        """Load doctors for dropdown"""
        try:
            doctors = self.db_manager.execute_query(
                "SELECT doctor_id, first_name, last_name, specialization FROM doctors WHERE is_available = 1 ORDER BY first_name"
            )
            
            doctor_list = []
            self.doctor_data = {}
            
            for doctor in doctors:
                name = f"Dr. {doctor['first_name']} {doctor['last_name']} ({doctor['specialization']})"
                doctor_list.append(name)
                self.doctor_data[name] = doctor['doctor_id']
                
            self.doctor_combo['values'] = doctor_list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")
            
    def save_appointment(self):
        """Save new appointment to database"""
        try:
            # Validate required fields
            if not self.patient_var.get():
                messagebox.showerror("Validation", "Please select a patient.")
                return
                
            if not self.doctor_var.get():
                messagebox.showerror("Validation", "Please select a doctor.")
                return
                
            # Get data
            patient_id = self.patient_data[self.patient_var.get()]
            doctor_id = self.doctor_data[self.doctor_var.get()]
            appointment_date = self.date_var.get()
            appointment_time = f"{self.hour_var.get()}:{self.minute_var.get()}:00"
            duration = int(self.duration_var.get())
            notes = self.notes_text.get(1.0, 'end-1c').strip()
            
            # Validate date
            try:
                datetime.strptime(appointment_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Validation", "Invalid date format. Use YYYY-MM-DD.")
                return
                
            # Check for conflicts
            conflict_query = '''
                SELECT appointment_id FROM appointments 
                WHERE doctor_id = ? AND appointment_date = ? 
                AND appointment_time = ? AND status != 'cancelled'
            '''
            
            conflicts = self.db_manager.execute_query(
                conflict_query, (doctor_id, appointment_date, appointment_time)
            )
            
            if conflicts:
                messagebox.showerror("Conflict", "This time slot is already booked for the selected doctor.")
                return
                
            # Insert appointment
            insert_query = '''
                INSERT INTO appointments (
                    patient_id, doctor_id, appointment_date, appointment_time,
                    duration_minutes, status, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            self.db_manager.execute_insert(
                insert_query, 
                (patient_id, doctor_id, appointment_date, appointment_time, 
                 duration, 'scheduled', notes)
            )
            
            messagebox.showinfo("Success", "Appointment scheduled successfully!")
            self.callback()  # Refresh appointment list
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save appointment: {str(e)}")
