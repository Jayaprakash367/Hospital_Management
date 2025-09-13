"""
Main Window for Hospital Management System
Modern dashboard with navigation and modules
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.gui.patient_management import PatientManagement
from src.gui.doctor_management import DoctorManagement
from src.gui.appointment_management import AppointmentManagement
from src.gui.billing_management import BillingManagement
from src.gui.reports_dashboard import ReportsDashboard

class MainWindow:
    def __init__(self, root, db_manager, current_user):
        self.root = root
        self.db_manager = db_manager
        self.current_user = current_user
        
        # Configure main window
        self.setup_main_window()
        
        # Create main interface
        self.create_widgets()
        
        # Initialize modules
        self.init_modules()
        
    def setup_main_window(self):
        """Configure the main window"""
        self.root.title(f"HMS v2.0 - Welcome {self.current_user['full_name']}")
        self.root.geometry("1400x900")
        self.root.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def center_window(self):
        """Center the main window"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange main widgets"""
        # Header frame
        self.create_header()
        
        # Main content frame
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self):
        """Create header with navigation and user info"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_frame, bg='#34495e')
        left_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(
            left_frame,
            text="🏥 HMS",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='#3498db'
        ).pack(side='left')
        
        tk.Label(
            left_frame,
            text="Hospital Management System v2.0",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(side='left', padx=(10, 0))
        
        # Right side - User info and controls
        right_frame = tk.Frame(header_frame, bg='#34495e')
        right_frame.pack(side='right', padx=20, pady=10)
        
        # User info
        user_frame = tk.Frame(right_frame, bg='#34495e')
        user_frame.pack(side='right')
        
        tk.Label(
            user_frame,
            text=f"Welcome, {self.current_user['full_name']}",
            font=('Arial', 11, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(anchor='e')
        
        tk.Label(
            user_frame,
            text=f"Role: {self.current_user['role'].title()} | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7'
        ).pack(anchor='e')
        
        # Logout button
        logout_btn = tk.Button(
            right_frame,
            text="Logout",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.logout
        )
        logout_btn.pack(side='right', padx=(0, 20))
        
    def create_main_content(self):
        """Create main content area with navigation and modules"""
        # Main container
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Navigation panel
        self.create_navigation(main_container)
        
        # Content area
        self.create_content_area(main_container)
        
    def create_navigation(self, parent):
        """Create navigation sidebar"""
        nav_frame = tk.Frame(parent, bg='#2c3e50', width=250)
        nav_frame.pack(side='left', fill='y', padx=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Navigation title
        tk.Label(
            nav_frame,
            text="Navigation",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "🏠", self.show_dashboard),
            ("Patients", "👥", self.show_patients),
            ("Doctors", "👨‍⚕️", self.show_doctors),
            ("Appointments", "📅", self.show_appointments),
            ("Medical Records", "📋", self.show_medical_records),
            ("Billing", "💰", self.show_billing),
            ("Staff", "👨‍💼", self.show_staff),
            ("Rooms", "🏠", self.show_rooms),
            ("Reports", "📊", self.show_reports),
            ("Settings", "⚙️", self.show_settings)
        ]
        
        for text, icon, command in nav_items:
            btn = tk.Button(
                nav_frame,
                text=f"{icon} {text}",
                font=('Arial', 11),
                bg='#34495e',
                fg='white',
                relief='flat',
                width=20,
                height=2,
                anchor='w',
                padx=15,
                cursor='hand2',
                command=command
            )
            btn.pack(fill='x', padx=10, pady=2)
            self.nav_buttons[text] = btn
            
        # Quick stats
        self.create_quick_stats(nav_frame)
        
    def create_quick_stats(self, parent):
        """Create quick statistics panel"""
        stats_frame = tk.Frame(parent, bg='#2c3e50')
        stats_frame.pack(side='bottom', fill='x', padx=10, pady=20)
        
        tk.Label(
            stats_frame,
            text="Quick Stats",
            font=('Arial', 12, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=(0, 10))
        
        # Get statistics from database
        try:
            patients_count = len(self.db_manager.execute_query("SELECT patient_id FROM patients"))
            doctors_count = len(self.db_manager.execute_query("SELECT doctor_id FROM doctors"))
            appointments_today = len(self.db_manager.execute_query(
                "SELECT appointment_id FROM appointments WHERE DATE(appointment_date) = DATE('now')"
            ))
            
            stats_data = [
                ("Patients", patients_count, "#3498db"),
                ("Doctors", doctors_count, "#2ecc71"),
                ("Today's Appointments", appointments_today, "#f39c12")
            ]
            
            for label, value, color in stats_data:
                stat_frame = tk.Frame(stats_frame, bg=color, height=60)
                stat_frame.pack(fill='x', pady=2)
                stat_frame.pack_propagate(False)
                
                tk.Label(
                    stat_frame,
                    text=str(value),
                    font=('Arial', 16, 'bold'),
                    bg=color,
                    fg='white'
                ).pack(pady=(5, 0))
                
                tk.Label(
                    stat_frame,
                    text=label,
                    font=('Arial', 8),
                    bg=color,
                    fg='white'
                ).pack()
                
        except Exception as e:
            tk.Label(
                stats_frame,
                text="Stats unavailable",
                font=('Arial', 10),
                bg='#2c3e50',
                fg='#7f8c8d'
            ).pack()
        
    def create_content_area(self, parent):
        """Create main content display area"""
        self.content_frame = tk.Frame(parent, bg='white', relief='flat', bd=1)
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Default dashboard view
        self.show_dashboard()
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg='#95a5a6', height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white'
        )
        self.status_label.pack(side='left', padx=10, pady=2)
        
        # System info
        system_info = tk.Label(
            status_frame,
            text="HMS v2.0 | Database Connected",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white'
        )
        system_info.pack(side='right', padx=10, pady=2)
        
    def init_modules(self):
        """Initialize all management modules"""
        # These will be created when needed to improve startup time
        self.modules = {}
        
    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def set_active_nav(self, active_name):
        """Set active navigation button"""
        for name, btn in self.nav_buttons.items():
            if name == active_name:
                btn.config(bg='#3498db', fg='white')
            else:
                btn.config(bg='#34495e', fg='white')
                
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.set_active_nav("Dashboard")
        
        # Dashboard header
        header = tk.Label(
            self.content_frame,
            text="🏠 Dashboard Overview",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header.pack(pady=20)
        
        # Dashboard content
        dashboard_frame = tk.Frame(self.content_frame, bg='white')
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Recent activities, charts, etc. can be added here
        welcome_text = f"""
        Welcome to the Hospital Management System v2.0!
        
        Current User: {self.current_user['full_name']}
        Role: {self.current_user['role'].title()}
        Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This advanced system provides comprehensive healthcare management
        with modern features and intuitive interface.
        
        Use the navigation panel to access different modules.
        """
        
        tk.Label(
            dashboard_frame,
            text=welcome_text,
            font=('Arial', 12),
            bg='white',
            fg='#34495e',
            justify='left'
        ).pack(pady=50)
        
    def show_patients(self):
        """Show patient management"""
        self.clear_content()
        self.set_active_nav("Patients")
        
        if 'patients' not in self.modules:
            self.modules['patients'] = PatientManagement(self.content_frame, self.db_manager)
        else:
            self.modules['patients'].refresh()
            
    def show_doctors(self):
        """Show doctor management"""
        self.clear_content()
        self.set_active_nav("Doctors")
        
        if 'doctors' not in self.modules:
            self.modules['doctors'] = DoctorManagement(self.content_frame, self.db_manager)
        else:
            self.modules['doctors'].refresh()
            
    def show_appointments(self):
        """Show appointment management"""
        self.clear_content()
        self.set_active_nav("Appointments")
        
        if 'appointments' not in self.modules:
            self.modules['appointments'] = AppointmentManagement(self.content_frame, self.db_manager)
        else:
            self.modules['appointments'].refresh()
            
    def show_medical_records(self):
        """Show medical records"""
        self.clear_content()
        self.set_active_nav("Medical Records")
        
        tk.Label(
            self.content_frame,
            text="📋 Medical Records Module",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=50)
        
    def show_billing(self):
        """Show billing management"""
        self.clear_content()
        self.set_active_nav("Billing")
        
        if 'billing' not in self.modules:
            self.modules['billing'] = BillingManagement(self.content_frame, self.db_manager)
        else:
            self.modules['billing'].refresh()
            
    def show_staff(self):
        """Show staff management"""
        self.clear_content()
        self.set_active_nav("Staff")
        
        tk.Label(
            self.content_frame,
            text="👨‍💼 Staff Management Module",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=50)
        
    def show_rooms(self):
        """Show room management"""
        self.clear_content()
        self.set_active_nav("Rooms")
        
        tk.Label(
            self.content_frame,
            text="🏠 Room Management Module",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=50)
        
    def show_reports(self):
        """Show reports dashboard"""
        self.clear_content()
        self.set_active_nav("Reports")
        
        if 'reports' not in self.modules:
            self.modules['reports'] = ReportsDashboard(self.content_frame, self.db_manager)
        else:
            self.modules['reports'].refresh()
            
    def show_settings(self):
        """Show settings"""
        self.clear_content()
        self.set_active_nav("Settings")
        
        tk.Label(
            self.content_frame,
            text="⚙️ System Settings",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=50)
        
    def logout(self):
        """Handle user logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()
            
    def on_close(self):
        """Handle window close"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.db_manager.close()
            self.root.quit()
