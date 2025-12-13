#!/usr/bin/env python3
"""
Simple Login Window Test
This will show just the login window to test UI elements
"""

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys
import os

class SimpleLoginWindow(tk.Tk):
    """Simple login window for testing"""
    
    def __init__(self):
        super().__init__()
        self.title("Employee Management System - Login")
        self.configure(bg="#f5f7fa")
        
        # Window size and positioning
        window_width = 450
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange UI widgets"""
        
        # Header
        header_frame = tk.Frame(self, bg="#f5f7fa")
        header_frame.pack(pady=(40, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="Employee Management System", 
            bg="#f5f7fa", 
            fg="#2c3e50",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame, 
            text="Version 2.0 - Please Login", 
            bg="#f5f7fa", 
            fg="#7f8c8d",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(5, 20))
        
        # Form frame
        form_frame = tk.Frame(self, bg="#f5f7fa")
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Username
        tk.Label(
            form_frame, 
            text="Username:", 
            bg="#f5f7fa", 
            fg="#2c3e50", 
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            relief="solid",
            borderwidth=1,
            bg="#ffffff"
        )
        self.username_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(
            form_frame, 
            text="Password:", 
            bg="#f5f7fa", 
            fg="#2c3e50", 
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame, 
            show="*", 
            font=("Arial", 12), 
            relief="solid",
            borderwidth=1,
            bg="#ffffff"
        )
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=8)
        
        # Login button - THIS IS THE BLUE SIGN IN BUTTON
        self.login_btn = tk.Button(
            form_frame, 
            text="Sign In", 
            bg="#3498db",  # BLUE COLOR
            fg="white",
            font=("Arial", 12, "bold"), 
            relief="flat", 
            command=self.test_login,
            cursor="hand2",
            pady=12
        )
        self.login_btn.pack(fill="x", pady=(10, 0))
        
        # Bind Enter key
        self.bind('<Return>', lambda event: self.test_login())
        
        # Instructions
        instructions = tk.Label(
            self, 
            text="Test Credentials:\nUsername: admin | Password: admin123\nUsername: test | Password: test", 
            bg="#f5f7fa", 
            fg="#666666",
            font=("Arial", 9),
            justify="center"
        )
        instructions.pack(pady=20)
        
        # Focus on username
        self.username_entry.focus_set()

    def test_login(self):
        """Test login function"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password")
            return
        
        # Test database connection
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='EmployeeDB'
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT Username, Role FROM Users WHERE Username=%s", (username,))
            result = cursor.fetchone()
            
            if result:
                messagebox.showinfo(
                    "Login Test Success", 
                    f"Database connection working!\n"
                    f"User found: {result[0]}\n"
                    f"Role: {result[1]}\n\n"
                    f"Blue 'Sign In' button is working correctly!"
                )
            else:
                messagebox.showwarning("User Not Found", "User not found in database")
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error", 
                f"Cannot connect to database:\n{e}\n\n"
                f"Please make sure MySQL is running and\n"
                f"run the setup_database.sql file in phpMyAdmin"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

def main():
    print("Starting Simple Login Test...")
    print("=" * 40)
    print("Look for a window with:")
    print("• Employee Management System title")
    print("• Username and Password fields")
    print("• BLUE 'Sign In' button")
    print("=" * 40)
    
    app = SimpleLoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()