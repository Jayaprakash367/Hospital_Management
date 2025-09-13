"""
Login Window for Hospital Management System
Modern login interface with validation
"""

import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, parent, auth_manager, on_success_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.on_success = on_success_callback
        
        # Hide main window during login
        self.parent.withdraw()
        
        # Create login window
        self.window = tk.Toplevel(parent)
        self.window.title("HMS Login - Hospital Management System")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        # Create login interface
        self.create_widgets()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def center_window(self):
        """Center the login window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange login widgets"""
        # Main container
        main_frame = tk.Frame(self.window, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Logo/Icon (using text for now)
        logo_label = tk.Label(
            header_frame,
            text="🏥",
            font=('Arial', 48),
            bg='#2c3e50',
            fg='#3498db'
        )
        logo_label.pack()
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Hospital Management System",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Healthcare Management Platform",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack()
        
        # Login form
        form_frame = tk.Frame(main_frame, bg='#34495e', relief='flat', bd=0)
        form_frame.pack(fill='x', pady=20)
        
        # Create rounded effect with padding
        form_inner = tk.Frame(form_frame, bg='#34495e')
        form_inner.pack(padx=20, pady=30)
        
        # Username field
        tk.Label(
            form_inner,
            text="Username",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_inner,
            font=('Arial', 12),
            width=25,
            relief='flat',
            bd=10,
            bg='white',
            fg='#2c3e50'
        )
        self.username_entry.pack(pady=(0, 20), ipady=8)
        self.username_entry.focus()
        
        # Password field
        tk.Label(
            form_inner,
            text="Password",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_inner,
            font=('Arial', 12),
            width=25,
            show='*',
            relief='flat',
            bd=10,
            bg='white',
            fg='#2c3e50'
        )
        self.password_entry.pack(pady=(0, 20), ipady=8)
        
        # Remember me checkbox
        self.remember_var = tk.BooleanVar()
        remember_frame = tk.Frame(form_inner, bg='#34495e')
        remember_frame.pack(fill='x', pady=(0, 20))
        
        tk.Checkbutton(
            remember_frame,
            text="Remember me",
            variable=self.remember_var,
            font=('Arial', 10),
            bg='#34495e',
            fg='#bdc3c7',
            selectcolor='#34495e',
            activebackground='#34495e',
            activeforeground='white'
        ).pack(anchor='w')
        
        # Login button
        self.login_btn = tk.Button(
            form_inner,
            text="LOGIN",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            width=20,
            height=2,
            cursor='hand2',
            command=self.login
        )
        self.login_btn.pack(pady=(10, 0))
        
        # Bind Enter key to login
        self.window.bind('<Return>', lambda e: self.login())
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#2c3e50')
        footer_frame.pack(side='bottom', fill='x', pady=(30, 0))
        
        tk.Label(
            footer_frame,
            text="Default Login: admin / admin123",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#7f8c8d'
        ).pack()
        
        tk.Label(
            footer_frame,
            text="© 2025 Hospital Management System v2.0",
            font=('Arial', 8),
            bg='#2c3e50',
            fg='#95a5a6'
        ).pack(pady=(5, 0))
        
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return
            
        # Disable login button during authentication
        self.login_btn.config(state='disabled', text='Logging in...')
        self.window.update()
        
        # Attempt authentication
        user_data = self.auth_manager.authenticate(username, password)
        
        if user_data:
            # Hide login window
            self.window.withdraw()
            
            # Show main window
            self.parent.deiconify()
            
            # Call success callback
            self.on_success(user_data)
            
            # Close login window
            self.window.destroy()
        else:
            # Re-enable login button
            self.login_btn.config(state='normal', text='LOGIN')
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()
            
    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            self.parent.quit()
