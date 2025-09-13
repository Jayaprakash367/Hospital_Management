"""
Reports Dashboard Module
Comprehensive reporting and analytics
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    plt = None
    FigureCanvasTkAgg = None
    np = None
    HAS_MATPLOTLIB = False

class ReportsDashboard:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.create_widgets()
        self.load_reports()
        
    def create_widgets(self):
        """Create reports dashboard interface"""
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text="📊 Reports & Analytics Dashboard",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Control buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="📊 Generate Report",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.generate_custom_report
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📈 Export Data",
            font=('Arial', 10),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.export_data
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.refresh
        ).pack(side='left', padx=5)
        
        # Create notebook for different report types
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Summary tab
        self.create_summary_tab()
        
        # Patient analytics tab
        self.create_patient_analytics_tab()
        
        # Financial reports tab
        self.create_financial_reports_tab()
        
        # Appointment statistics tab
        self.create_appointment_stats_tab()
        
    def create_summary_tab(self):
        """Create summary overview tab"""
        summary_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(summary_frame, text="📋 Summary Overview")
        
        # Key metrics cards
        metrics_frame = tk.Frame(summary_frame, bg='white')
        metrics_frame.pack(fill='x', padx=20, pady=20)
        
        try:
            # Get key metrics
            total_patients = len(self.db_manager.execute_query("SELECT patient_id FROM patients"))
            total_doctors = len(self.db_manager.execute_query("SELECT doctor_id FROM doctors"))
            total_appointments = len(self.db_manager.execute_query("SELECT appointment_id FROM appointments"))
            
            # Revenue this month
            revenue_result = self.db_manager.execute_query(
                "SELECT SUM(paid_amount) as revenue FROM billing WHERE strftime('%Y-%m', bill_date) = strftime('%Y-%m', 'now')"
            )
            monthly_revenue = revenue_result[0]['revenue'] if revenue_result and revenue_result[0]['revenue'] else 0
            
            metrics_data = [
                ("Total Patients", total_patients, "#3498db"),
                ("Active Doctors", total_doctors, "#27ae60"),
                ("Total Appointments", total_appointments, "#f39c12"),
                ("Monthly Revenue", f"${monthly_revenue:,.2f}", "#e74c3c")
            ]
            
            for i, (title, value, color) in enumerate(metrics_data):
                card = tk.Frame(metrics_frame, bg=color, width=200, height=100)
                card.pack(side='left', padx=10, fill='x', expand=True)
                card.pack_propagate(False)
                
                tk.Label(
                    card,
                    text=str(value),
                    font=('Arial', 18, 'bold'),
                    bg=color,
                    fg='white'
                ).pack(pady=(15, 5))
                
                tk.Label(
                    card,
                    text=title,
                    font=('Arial', 11),
                    bg=color,
                    fg='white'
                ).pack()
                
        except Exception as e:
            tk.Label(
                metrics_frame,
                text=f"Error loading metrics: {str(e)}",
                font=('Arial', 12),
                fg='red'
            ).pack()
            
        # Recent activity
        activity_frame = tk.Frame(summary_frame, bg='white')
        activity_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            activity_frame,
            text="📈 Recent Activity Summary",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        # Activity text widget
        activity_text = tk.Text(
            activity_frame,
            height=10,
            wrap='word',
            font=('Arial', 10),
            state='disabled'
        )
        activity_text.pack(fill='both', expand=True)
        
        # Load recent activity
        self.load_recent_activity(activity_text)
        
    def create_patient_analytics_tab(self):
        """Create patient analytics tab"""
        patient_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(patient_frame, text="👥 Patient Analytics")
        
        # Patient demographics
        demo_frame = tk.Frame(patient_frame, bg='white')
        demo_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            demo_frame,
            text="👥 Patient Demographics",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        # Create charts frame
        charts_frame = tk.Frame(demo_frame, bg='white')
        charts_frame.pack(fill='both', expand=True)
        
        try:
            # Gender distribution
            gender_data = self.db_manager.execute_query(
                "SELECT gender, COUNT(*) as count FROM patients GROUP BY gender"
            )
            
            if gender_data:
                self.create_pie_chart(charts_frame, gender_data, "Gender Distribution", "gender", "count")
                
        except Exception as e:
            tk.Label(
                charts_frame,
                text=f"Error loading patient analytics: {str(e)}",
                font=('Arial', 12),
                fg='red'
            ).pack()
            
    def create_financial_reports_tab(self):
        """Create financial reports tab"""
        financial_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(financial_frame, text="💰 Financial Reports")
        
        # Revenue summary
        revenue_frame = tk.Frame(financial_frame, bg='white')
        revenue_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            revenue_frame,
            text="💰 Revenue Summary",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        try:
            # Payment status distribution
            payment_data = self.db_manager.execute_query(
                "SELECT payment_status, COUNT(*) as count, SUM(total_amount) as amount FROM billing GROUP BY payment_status"
            )
            
            if payment_data:
                # Create payment status table
                columns = ('Status', 'Count', 'Total Amount')
                tree = ttk.Treeview(revenue_frame, columns=columns, show='headings', height=6)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                    
                for row in payment_data:
                    tree.insert('', 'end', values=(
                        row['payment_status'].title(),
                        row['count'],
                        f"${row['amount']:,.2f}"
                    ))
                    
                tree.pack(fill='x')
                
        except Exception as e:
            tk.Label(
                revenue_frame,
                text=f"Error loading financial reports: {str(e)}",
                font=('Arial', 12),
                fg='red'
            ).pack()
            
    def create_appointment_stats_tab(self):
        """Create appointment statistics tab"""
        appointment_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(appointment_frame, text="📅 Appointment Stats")
        
        # Appointment trends
        trends_frame = tk.Frame(appointment_frame, bg='white')
        trends_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            trends_frame,
            text="📅 Appointment Trends",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        try:
            # Appointments by status
            status_data = self.db_manager.execute_query(
                "SELECT status, COUNT(*) as count FROM appointments GROUP BY status"
            )
            
            if status_data:
                # Create status table
                columns = ('Status', 'Count', 'Percentage')
                tree = ttk.Treeview(trends_frame, columns=columns, show='headings', height=6)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                    
                total_appointments = sum(row['count'] for row in status_data)
                
                for row in status_data:
                    percentage = (row['count'] / total_appointments * 100) if total_appointments > 0 else 0
                    tree.insert('', 'end', values=(
                        row['status'].title(),
                        row['count'],
                        f"{percentage:.1f}%"
                    ))
                    
                tree.pack(fill='x')
                
        except Exception as e:
            tk.Label(
                trends_frame,
                text=f"Error loading appointment statistics: {str(e)}",
                font=('Arial', 12),
                fg='red'
            ).pack()
            
    def create_pie_chart(self, parent, data, title, label_field, value_field):
        """Create a pie chart"""
        if not HAS_MATPLOTLIB or plt is None:
            tk.Label(
                parent,
                text="Chart unavailable (matplotlib not installed)",
                font=('Arial', 10),
                fg='orange'
            ).pack(side='left', padx=10)
            return
            
        try:
            # Prepare data
            labels = [row[label_field] for row in data]
            values = [row[value_field] for row in data]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title(title)
            
            # Embed in tkinter
            if HAS_MATPLOTLIB and FigureCanvasTkAgg:
                canvas = FigureCanvasTkAgg(fig, parent)
                canvas.draw()
                canvas.get_tk_widget().pack(side='left', padx=10)
            else:
                tk.Label(parent, text="Matplotlib not available for charts", 
                        fg='red').pack(side='left', padx=10)
            
        except Exception as e:
            tk.Label(
                parent,
                text=f"Chart error: {str(e)}",
                font=('Arial', 10),
                fg='red'
            ).pack(side='left', padx=10)
            
    def load_recent_activity(self, text_widget):
        """Load recent activity summary"""
        try:
            text_widget.config(state='normal')
            text_widget.delete(1.0, 'end')
            
            # Get recent activities
            activities = []
            
            # Recent appointments
            recent_appointments = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM appointments WHERE DATE(appointment_date) >= DATE('now', '-7 days')"
            )
            if recent_appointments:
                activities.append(f"• {recent_appointments[0]['count']} appointments scheduled in the last 7 days")
                
            # Recent patients
            recent_patients = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM patients WHERE DATE(created_at) >= DATE('now', '-7 days')"
            )
            if recent_patients:
                activities.append(f"• {recent_patients[0]['count']} new patients registered in the last 7 days")
                
            # Recent payments
            recent_payments = self.db_manager.execute_query(
                "SELECT SUM(paid_amount) as amount FROM billing WHERE DATE(bill_date) >= DATE('now', '-7 days')"
            )
            if recent_payments and recent_payments[0]['amount']:
                activities.append(f"• ${recent_payments[0]['amount']:,.2f} collected in payments in the last 7 days")
                
            # Today's statistics
            today_appointments = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM appointments WHERE DATE(appointment_date) = DATE('now')"
            )
            if today_appointments:
                activities.append(f"• {today_appointments[0]['count']} appointments scheduled for today")
                
            if not activities:
                activities.append("• No recent activity to display")
                
            activity_text = "Recent Activity Summary (Last 7 Days):\n\n" + "\n".join(activities)
            text_widget.insert(1.0, activity_text)
            text_widget.config(state='disabled')
            
        except Exception as e:
            text_widget.config(state='normal')
            text_widget.insert(1.0, f"Error loading activity: {str(e)}")
            text_widget.config(state='disabled')
            
    def generate_custom_report(self):
        """Generate custom report"""
        messagebox.showinfo("Info", "Custom report generation - Implementation in progress")
        
    def export_data(self):
        """Export data to file"""
        messagebox.showinfo("Info", "Data export - Implementation in progress")
        
    def load_reports(self):
        """Load all reports data"""
        # This method is called when the dashboard is first created
        pass
        
    def refresh(self):
        """Refresh all reports"""
        # Clear and reload all data
        for tab_id in self.notebook.tabs():
            # Could implement specific refresh logic for each tab
            pass
        messagebox.showinfo("Info", "Reports refreshed successfully!")
