"""
Billing Management Module
Comprehensive billing and payment tracking
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class BillingManagement:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.create_widgets()
        self.load_bills()
        
    def create_widgets(self):
        """Create billing management interface"""
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text="💰 Billing & Payment Management",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Control buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="➕ New Bill",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.create_bill
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="💳 Record Payment",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.record_payment
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🖨️ Print Bill",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.print_bill
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📊 Reports",
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.show_reports
        ).pack(side='left', padx=5)
        
        # Summary cards
        self.create_summary_cards()
        
        # Filter frame
        filter_frame = tk.Frame(self.parent, bg='white')
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Status filter
        tk.Label(
            filter_frame,
            text="💳 Payment Status:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left')
        
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "Pending", "Partial", "Paid", "Overdue"],
            width=12,
            state="readonly"
        )
        status_combo.pack(side='left', padx=10)
        status_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Date range
        tk.Label(
            filter_frame,
            text="Date Range:",
            font=('Arial', 11),
            bg='white',
            fg='#34495e'
        ).pack(side='left', padx=(20, 5))
        
        self.date_from_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        from_entry = tk.Entry(
            filter_frame,
            textvariable=self.date_from_var,
            font=('Arial', 10),
            width=12,
            relief='solid',
            bd=1
        )
        from_entry.pack(side='left', padx=5)
        
        tk.Label(filter_frame, text="to", bg='white', fg='#34495e').pack(side='left', padx=5)
        
        self.date_to_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        to_entry = tk.Entry(
            filter_frame,
            textvariable=self.date_to_var,
            font=('Arial', 10),
            width=12,
            relief='solid',
            bd=1
        )
        to_entry.pack(side='left', padx=5)
        
        tk.Button(
            filter_frame,
            text="Apply Filter",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            cursor='hand2',
            command=self.apply_date_filter
        ).pack(side='left', padx=10)
        
        # Bills list
        self.create_bills_list()
        
    def create_summary_cards(self):
        """Create summary cards showing financial overview"""
        summary_frame = tk.Frame(self.parent, bg='white')
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        # Get summary data
        try:
            # Total outstanding
            outstanding_result = self.db_manager.execute_query(
                "SELECT SUM(total_amount - paid_amount) as outstanding FROM billing WHERE payment_status != 'paid'"
            )
            outstanding = outstanding_result[0]['outstanding'] if outstanding_result and outstanding_result[0]['outstanding'] else 0
            
            # Today's revenue
            today_result = self.db_manager.execute_query(
                "SELECT SUM(paid_amount) as today_revenue FROM billing WHERE DATE(bill_date) = DATE('now')"
            )
            today_revenue = today_result[0]['today_revenue'] if today_result and today_result[0]['today_revenue'] else 0
            
            # This month's revenue
            month_result = self.db_manager.execute_query(
                "SELECT SUM(paid_amount) as month_revenue FROM billing WHERE strftime('%Y-%m', bill_date) = strftime('%Y-%m', 'now')"
            )
            month_revenue = month_result[0]['month_revenue'] if month_result and month_result[0]['month_revenue'] else 0
            
            # Pending bills count
            pending_result = self.db_manager.execute_query(
                "SELECT COUNT(*) as pending_count FROM billing WHERE payment_status = 'pending'"
            )
            pending_count = pending_result[0]['pending_count'] if pending_result else 0
            
        except Exception as e:
            outstanding = today_revenue = month_revenue = pending_count = 0
            
        # Create cards
        cards_data = [
            ("Outstanding Amount", f"${outstanding:,.2f}", "#e74c3c"),
            ("Today's Revenue", f"${today_revenue:,.2f}", "#27ae60"),
            ("This Month", f"${month_revenue:,.2f}", "#3498db"),
            ("Pending Bills", str(pending_count), "#f39c12")
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card_frame = tk.Frame(summary_frame, bg=color, width=200, height=80)
            card_frame.pack(side='left', padx=10, pady=5, fill='x', expand=True)
            card_frame.pack_propagate(False)
            
            tk.Label(
                card_frame,
                text=value,
                font=('Arial', 16, 'bold'),
                bg=color,
                fg='white'
            ).pack(pady=(10, 0))
            
            tk.Label(
                card_frame,
                text=title,
                font=('Arial', 10),
                bg=color,
                fg='white'
            ).pack()
            
    def create_bills_list(self):
        """Create bills list with treeview"""
        list_frame = tk.Frame(self.parent, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('Bill ID', 'Date', 'Patient', 'Total', 'Paid', 'Balance', 'Status', 'Due Date')
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        column_widths = {'Bill ID': 80, 'Date': 100, 'Patient': 150, 'Total': 100,
                        'Paid': 100, 'Balance': 100, 'Status': 100, 'Due Date': 100}
        
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
        self.tree.tag_configure('paid', background='#e8f5e8')
        self.tree.tag_configure('pending', background='#fff2e8')
        self.tree.tag_configure('overdue', background='#f8e8e8')
        self.tree.tag_configure('partial', background='#e8f4f8')
        
    def load_bills(self):
        """Load bills from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get bills data
            query = '''
                SELECT b.bill_id, b.bill_date, b.total_amount, b.paid_amount,
                       b.payment_status, b.due_date,
                       (p.first_name || ' ' || p.last_name) as patient_name
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                ORDER BY b.bill_date DESC
            '''
            
            bills = self.db_manager.execute_query(query)
            
            for bill in bills:
                balance = float(bill['total_amount']) - float(bill['paid_amount'])
                
                # Determine status tag
                status = bill['payment_status'].lower()
                tag = status if status in ['paid', 'pending', 'partial'] else 'overdue'
                
                # Check if overdue
                if bill['due_date'] and datetime.strptime(bill['due_date'], '%Y-%m-%d') < datetime.now() and status != 'paid':
                    tag = 'overdue'
                    
                self.tree.insert('', 'end', values=(
                    bill['bill_id'],
                    bill['bill_date'][:10],  # Show only date part
                    bill['patient_name'],
                    f"${bill['total_amount']:,.2f}",
                    f"${bill['paid_amount']:,.2f}",
                    f"${balance:,.2f}",
                    bill['payment_status'].title(),
                    bill['due_date'] or 'N/A'
                ), tags=(tag,))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bills: {str(e)}")
            
    def on_filter(self, *args):
        """Handle status filter"""
        self.load_bills()  # Simplified - could implement actual filtering
        
    def apply_date_filter(self):
        """Apply date range filter"""
        self.load_bills()  # Simplified - could implement actual filtering
        
    def on_item_double_click(self, event):
        """Handle double-click on bill item"""
        self.view_bill_details()
        
    def create_bill(self):
        """Open create bill dialog"""
        CreateBillDialog(self.parent, self.db_manager, self.load_bills)
        
    def record_payment(self):
        """Record payment for selected bill"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a bill to record payment.")
            return
            
        bill_id = self.tree.item(selected[0])['values'][0]
        RecordPaymentDialog(self.parent, self.db_manager, bill_id, self.load_bills)
        
    def print_bill(self):
        """Print selected bill"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a bill to print.")
            return
            
        bill_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Print bill {bill_id} - Implementation in progress")
        
    def show_reports(self):
        """Show billing reports"""
        messagebox.showinfo("Info", "Billing reports - Implementation in progress")
        
    def view_bill_details(self):
        """View detailed bill information"""
        selected = self.tree.selection()
        if not selected:
            return
            
        bill_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Bill details for {bill_id} - Implementation in progress")
        
    def refresh(self):
        """Refresh bills list"""
        self.load_bills()
        self.create_summary_cards()  # Refresh summary as well

class CreateBillDialog:
    def __init__(self, parent, db_manager, callback):
        self.db_manager = db_manager
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Bill")
        self.dialog.geometry("600x500")
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
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
    def create_widgets(self):
        """Create form widgets"""
        # Header
        header = tk.Label(
            self.dialog,
            text="💰 Create New Bill",
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
        
        # Total amount
        tk.Label(
            form_frame,
            text="Total Amount*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(
            form_frame,
            textvariable=self.amount_var,
            width=35,
            font=('Arial', 10)
        )
        self.amount_entry.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        
        # Due date
        tk.Label(
            form_frame,
            text="Due Date",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        self.due_date_var = tk.StringVar(value=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
        self.due_date_entry = tk.Entry(
            form_frame,
            textvariable=self.due_date_var,
            width=35,
            font=('Arial', 10)
        )
        self.due_date_entry.grid(row=2, column=1, sticky='w', padx=10, pady=10)
        
        # Notes
        tk.Label(
            form_frame,
            text="Notes",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).grid(row=3, column=0, sticky='nw', pady=10)
        
        self.notes_text = tk.Text(
            form_frame,
            width=35,
            height=5,
            font=('Arial', 10),
            wrap='word'
        )
        self.notes_text.grid(row=3, column=1, sticky='w', padx=10, pady=10)
        
        # Load patients
        self.load_patients()
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Create Bill",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_bill
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
            
    def save_bill(self):
        """Save new bill to database"""
        try:
            # Validate required fields
            if not self.patient_var.get():
                messagebox.showerror("Validation", "Please select a patient.")
                return
                
            if not self.amount_var.get():
                messagebox.showerror("Validation", "Please enter total amount.")
                return
                
            # Get data
            patient_id = self.patient_data[self.patient_var.get()]
            total_amount = float(self.amount_var.get())
            due_date = self.due_date_var.get() if self.due_date_var.get() else None
            notes = self.notes_text.get(1.0, 'end-1c').strip()
            
            # Validate amount
            if total_amount <= 0:
                messagebox.showerror("Validation", "Amount must be greater than 0.")
                return
                
            # Insert bill
            query = '''
                INSERT INTO billing (
                    patient_id, total_amount, paid_amount, payment_status,
                    bill_date, due_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            self.db_manager.execute_insert(
                query, 
                (patient_id, total_amount, 0, 'pending', 
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), due_date, notes)
            )
            
            messagebox.showinfo("Success", "Bill created successfully!")
            self.callback()  # Refresh bills list
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid amount.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")

class RecordPaymentDialog:
    def __init__(self, parent, db_manager, bill_id, callback):
        self.db_manager = db_manager
        self.bill_id = bill_id
        self.callback = callback
        
        # Get bill details
        self.load_bill_details()
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Record Payment")
        self.dialog.geometry("400x300")
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
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
    def load_bill_details(self):
        """Load bill details"""
        try:
            query = '''
                SELECT b.total_amount, b.paid_amount, 
                       (p.first_name || ' ' || p.last_name) as patient_name
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.bill_id = ?
            '''
            
            result = self.db_manager.execute_query(query, (self.bill_id,))
            
            if result:
                self.bill_data = result[0]
                self.remaining_amount = float(self.bill_data['total_amount']) - float(self.bill_data['paid_amount'])
            else:
                messagebox.showerror("Error", "Bill not found.")
                self.dialog.destroy()
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bill details: {str(e)}")
            self.dialog.destroy()
            
    def create_widgets(self):
        """Create payment form widgets"""
        # Header
        header = tk.Label(
            self.dialog,
            text="💳 Record Payment",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header.pack(pady=20)
        
        # Bill info
        info_frame = tk.Frame(self.dialog, bg='#ecf0f1')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Patient: {self.bill_data['patient_name']}",
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text=f"Total Amount: ${self.bill_data['total_amount']:,.2f}",
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=2)
        
        tk.Label(
            info_frame,
            text=f"Already Paid: ${self.bill_data['paid_amount']:,.2f}",
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=2)
        
        tk.Label(
            info_frame,
            text=f"Remaining: ${self.remaining_amount:,.2f}",
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#e74c3c'
        ).pack(pady=5)
        
        # Payment form
        form_frame = tk.Frame(self.dialog, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Payment amount
        tk.Label(
            form_frame,
            text="Payment Amount*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w', pady=(0, 5))
        
        self.payment_var = tk.StringVar(value=str(self.remaining_amount))
        self.payment_entry = tk.Entry(
            form_frame,
            textvariable=self.payment_var,
            width=30,
            font=('Arial', 11)
        )
        self.payment_entry.pack(anchor='w', pady=(0, 15))
        
        # Payment method
        tk.Label(
            form_frame,
            text="Payment Method*",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w', pady=(0, 5))
        
        self.method_var = tk.StringVar(value="Cash")
        method_combo = ttk.Combobox(
            form_frame,
            textvariable=self.method_var,
            values=["Cash", "Credit Card", "Debit Card", "Check", "Bank Transfer", "Insurance"],
            width=28,
            state="readonly"
        )
        method_combo.pack(anchor='w')
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Record Payment",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_payment
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
        
    def save_payment(self):
        """Save payment record"""
        try:
            # Validate payment amount
            payment_amount = float(self.payment_var.get())
            
            if payment_amount <= 0:
                messagebox.showerror("Validation", "Payment amount must be greater than 0.")
                return
                
            if payment_amount > self.remaining_amount:
                messagebox.showerror("Validation", "Payment amount cannot exceed remaining balance.")
                return
                
            # Calculate new totals
            new_paid_amount = float(self.bill_data['paid_amount']) + payment_amount
            total_amount = float(self.bill_data['total_amount'])
            
            # Determine new payment status
            if new_paid_amount >= total_amount:
                new_status = 'paid'
            elif new_paid_amount > 0:
                new_status = 'partial'
            else:
                new_status = 'pending'
                
            # Update bill
            update_query = '''
                UPDATE billing 
                SET paid_amount = ?, payment_status = ?, payment_method = ?
                WHERE bill_id = ?
            '''
            
            self.db_manager.execute_update(
                update_query, 
                (new_paid_amount, new_status, self.method_var.get(), self.bill_id)
            )
            
            messagebox.showinfo("Success", f"Payment of ${payment_amount:,.2f} recorded successfully!")
            self.callback()  # Refresh bills list
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid payment amount.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record payment: {str(e)}")
