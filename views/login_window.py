import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from utils.helpers import UIHelper
from utils.logger import app_logger
import logging

logger = logging.getLogger(__name__)

class LoginWindow(tk.Tk):
    """Enhanced login window with modern UI and security features"""
    
    def __init__(self):
        super().__init__()
        self.title("Advanced Employee Management System - Login")
        self.configure(bg="#f5f7fa")
        
        # Window configuration
        window_width = 480
        window_height = 500
        UIHelper.center_window(self, window_width, window_height)
        self.resizable(False, False)
        
        # Login attempt tracking
        self.login_attempts = 0
        self.max_attempts = 3
        
        self.create_widgets()
        
        # Focus on username field
        self.username_entry.focus_set()
        
        logger.info("Login window initialized")

    def create_widgets(self):
        """Create and arrange UI widgets"""
        
        # Header section
        header_frame = tk.Frame(self, bg="#f5f7fa")
        header_frame.pack(pady=(40, 20))
        
        # App title
        title_label = tk.Label(
            header_frame, 
            text="Employee Management System", 
            bg="#f5f7fa", 
            fg="#2c3e50",
            font=("Segoe UI", 20, "bold")
        )
        title_label.pack()
        
        # Version label
        version_label = tk.Label(
            header_frame, 
            text="Version 2.0 - Professional Edition", 
            bg="#f5f7fa", 
            fg="#7f8c8d",
            font=("Segoe UI", 10)
        )
        version_label.pack(pady=(5, 0))
        
        # Welcome text
        welcome_label = tk.Label(
            header_frame, 
            text="Please sign in to your account", 
            bg="#f5f7fa", 
            fg="#34495e",
            font=("Segoe UI", 12)
        )
        welcome_label.pack(pady=(20, 0))
        
        # Form frame
        form_frame = tk.Frame(self, bg="#f5f7fa")
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Username field
        tk.Label(
            form_frame, 
            text="Username", 
            bg="#f5f7fa", 
            fg="#2c3e50", 
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame, 
            font=("Segoe UI", 12), 
            bd=0,
            bg="#ffffff", 
            fg="#2c3e50", 
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor="#3498db",
            highlightbackground="#bdc3c7"
        )
        self.username_entry.pack(fill="x", pady=(0, 15), ipady=10)
        
        # Password field
        tk.Label(
            form_frame, 
            text="Password", 
            bg="#f5f7fa", 
            fg="#2c3e50", 
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame, 
            show="*", 
            font=("Segoe UI", 12), 
            bd=0,
            bg="#ffffff", 
            fg="#2c3e50", 
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor="#3498db",
            highlightbackground="#bdc3c7"
        )
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=10)
        
        # Login button
        self.login_btn = tk.Button(
            form_frame, 
            text="🔐 Sign In", 
            bg="#27ae60", 
            fg="white",
            font=("Segoe UI", 14, "bold"), 
            relief="flat", 
            command=self.handle_login,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="white",
            bd=0,
            highlightthickness=0
        )
        self.login_btn.pack(fill="x", pady=(20, 0), ipady=15)
        
        # Make login button more prominent with hover effects
        def on_enter(e):
            self.login_btn.config(bg="#229954")
        
        def on_leave(e):
            self.login_btn.config(bg="#27ae60")
            
        self.login_btn.bind("<Enter>", on_enter)
        self.login_btn.bind("<Leave>", on_leave)
        
        # Bind Enter key to login for all entry fields
        self.username_entry.bind('<Return>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda event: self.handle_login())
        self.bind('<Return>', lambda event: self.handle_login())
        
        # Set initial focus to username entry
        self.after(100, lambda: self.username_entry.focus())
        
        # Status label for messages
        self.status_label = tk.Label(
            self, 
            text="", 
            bg="#f5f7fa", 
            fg="#e74c3c",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(pady=(10, 0))
        
        # Footer with default credentials info
        footer_frame = tk.Frame(self, bg="#f5f7fa")
        footer_frame.pack(side="bottom", pady=(0, 20))
        
        info_text = "Default: admin/admin123 or test/test"
        tk.Label(
            footer_frame, 
            text=info_text, 
            bg="#f5f7fa", 
            fg="#95a5a6",
            font=("Segoe UI", 9)
        ).pack()

    def handle_login(self):
        """Handle login process with enhanced security"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Clear previous status
        self.status_label.config(text="", fg="#e74c3c")
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Check login attempts
        if self.login_attempts >= self.max_attempts:
            self.show_error("Too many failed attempts. Please restart the application.")
            self.login_btn.config(state="disabled")
            return
        
        # Disable button during authentication
        self.login_btn.config(state="disabled", text="Signing In...")
        self.update()
        
        try:
            # Authenticate user
            user = User.authenticate(username, password)
            
            if user:
                # Successful login
                app_logger.log_user_action(user.id, "LOGIN_SUCCESS", f"Role: {user.role}")
                logger.info(f"Successful login for user: {username}")
                
                # Show success message
                self.show_success(f"Welcome back, {username}!")
                
                # Close login window and open main application
                self.after(1000, lambda: self.open_main_application(user))
                
            else:
                # Failed login
                self.login_attempts += 1
                remaining = self.max_attempts - self.login_attempts
                
                app_logger.log_user_action(None, "LOGIN_FAILED", f"Username: {username}")
                logger.warning(f"Failed login attempt for user: {username}")
                
                if remaining > 0:
                    self.show_error(f"Invalid credentials. {remaining} attempts remaining.")
                else:
                    self.show_error("Too many failed attempts. Application locked.")
                    self.login_btn.config(state="disabled")
                
                # Clear password field
                self.password_entry.delete(0, tk.END)
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            self.show_error("Login system error. Please try again.")
            
        finally:
            # Re-enable button
            if self.login_attempts < self.max_attempts:
                self.login_btn.config(state="normal", text="Sign In")

    def show_error(self, message):
        """Display error message"""
        self.status_label.config(text=message, fg="#e74c3c")

    def show_success(self, message):
        """Display success message"""
        self.status_label.config(text=message, fg="#27ae60")

    def open_main_application(self, user):
        """Open the main application window"""
        try:
            self.destroy()  # Close login window
            
            # Import and open dashboard
            from views.dashboard import DashboardWindow
            main_app = DashboardWindow(user)
            main_app.mainloop()
            
        except ImportError:
            # Fallback to simple message if dashboard not implemented yet
            messagebox.showinfo(
                "Success", 
                f"Login successful!\nWelcome {user.username} ({user.role})\n\n"
                "Dashboard module will be implemented in the next phase."
            )
            logger.info(f"User {user.username} logged in successfully")
            
        except Exception as e:
            logger.error(f"Error opening main application: {e}")
            messagebox.showerror("Error", "Failed to open main application")

if __name__ == "__main__":
    # For testing the login window independently
    app = LoginWindow()
    app.mainloop()