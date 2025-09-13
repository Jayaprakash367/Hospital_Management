#!/usr/bin/env python3
"""
Simple GUI test for Hospital Management System
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_simple_gui():
    """Test basic GUI functionality"""
    try:
        # Create main window
        root = tk.Tk()
        root.title("Hospital Management System - GUI Test")
        root.geometry("600x400")
        root.configure(bg='#f0f0f0')
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (600 // 2)
        y = (root.winfo_screenheight() // 2) - (400 // 2)
        root.geometry(f"600x400+{x}+{y}")
        
        # Header
        header = tk.Label(
            root,
            text="🏥 Hospital Management System v2.0",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            pady=20
        )
        header.pack()
        
        # Status
        status = tk.Label(
            root,
            text="✅ GUI Test Successful!\nYour system can display windows properly.",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#27ae60',
            pady=20
        )
        status.pack()
        
        # Instructions
        instructions = tk.Label(
            root,
            text="If you can see this window, your GUI is working correctly.\n\n" +
                 "Click 'Start Full System' to launch the complete application\n" +
                 "or 'Close' to exit this test.",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#34495e',
            pady=20,
            justify='center'
        )
        instructions.pack()
        
        # Buttons frame
        button_frame = tk.Frame(root, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        # Start full system button
        start_btn = tk.Button(
            button_frame,
            text="🚀 Start Full System",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=lambda: start_full_system(root)
        )
        start_btn.pack(side='left', padx=10)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close Test",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=root.destroy
        )
        close_btn.pack(side='left', padx=10)
        
        # Show success message
        messagebox.showinfo(
            "GUI Test Success", 
            "Hospital Management System GUI is working!\n\n" +
            "Your desktop application will open in a separate window."
        )
        
        # Start the GUI loop
        root.mainloop()
        
    except Exception as e:
        print(f"GUI Error: {e}")
        messagebox.showerror("GUI Error", f"Failed to create GUI: {str(e)}")

def start_full_system(test_window):
    """Start the full hospital management system"""
    try:
        test_window.destroy()  # Close test window
        
        # Import and start main system
        import main
        print("Starting full Hospital Management System...")
        
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start full system: {str(e)}")
        print(f"Error starting full system: {e}")

if __name__ == "__main__":
    print("Testing Hospital Management System GUI...")
    print("A window should open shortly...")
    test_simple_gui()
