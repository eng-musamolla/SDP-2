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
        
        # Username entry with proper padding
        username_wrapper = tk.Frame(
            form_frame,
            bg="#ffffff",
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor="#3498db",
            highlightbackground="#bdc3c7"
        )
        username_wrapper.pack(fill="x", pady=(0, 15))
        
        self.username_entry = tk.Entry(
            username_wrapper, 
            font=("Segoe UI", 12), 
            bd=0,
            bg="#ffffff", 
            fg="#2c3e50", 
            relief="flat",
            highlightthickness=0
        )
        self.username_entry.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Password field
        tk.Label(
            form_frame, 
            text="Password", 
            bg="#f5f7fa", 
            fg="#2c3e50", 
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        # Password entry with proper padding
        password_wrapper = tk.Frame(
            form_frame,
            bg="#ffffff",
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor="#3498db",
            highlightbackground="#bdc3c7"
        )
        password_wrapper.pack(fill="x", pady=(0, 20))
        
        self.password_entry = tk.Entry(
            password_wrapper, 
            show="*", 
            font=("Segoe UI", 12), 
            bd=0,
            bg="#ffffff", 
            fg="#2c3e50", 
            relief="flat",
            highlightthickness=0
        )
        self.password_entry.pack(fill="both", expand=True, padx=12, pady=10)
        
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
        
        # Add focus effects for wrapper frames
        def on_username_focus_in(e):
            username_wrapper.config(highlightcolor="#3498db", highlightthickness=2)
        def on_username_focus_out(e):
            username_wrapper.config(highlightcolor="#bdc3c7", highlightthickness=1)
        def on_password_focus_in(e):
            password_wrapper.config(highlightcolor="#3498db", highlightthickness=2)
        def on_password_focus_out(e):
            password_wrapper.config(highlightcolor="#bdc3c7", highlightthickness=1)
        
        self.username_entry.bind('<FocusIn>', on_username_focus_in)
        self.username_entry.bind('<FocusOut>', on_username_focus_out)
        self.password_entry.bind('<FocusIn>', on_password_focus_in)
        self.password_entry.bind('<FocusOut>', on_password_focus_out)
        
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
        
        # Modern action links section
        actions_frame = tk.Frame(self, bg="#f5f7fa")
        actions_frame.pack(pady=(20, 10))
        
        # Forgot password link
        forgot_link = tk.Label(
            actions_frame,
            text="🔒 Forgot Password?",
            bg="#f5f7fa",
            fg="#3498db",
            font=("Segoe UI", 10, "underline"),
            cursor="hand2"
        )
        forgot_link.pack(side="left", padx=(0, 20))
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())
        forgot_link.bind("<Enter>", lambda e: forgot_link.config(fg="#2980b9"))
        forgot_link.bind("<Leave>", lambda e: forgot_link.config(fg="#3498db"))
        
        # Sign up link
        signup_link = tk.Label(
            actions_frame,
            text="👤 Create New Account",
            bg="#f5f7fa",
            fg="#27ae60",
            font=("Segoe UI", 10, "underline"),
            cursor="hand2"
        )
        signup_link.pack(side="right", padx=(20, 0))
        signup_link.bind("<Button-1>", lambda e: self.show_signup())
        signup_link.bind("<Enter>", lambda e: signup_link.config(fg="#229954"))
        signup_link.bind("<Leave>", lambda e: signup_link.config(fg="#27ae60"))
        
        # Divider line
        divider = tk.Frame(self, height=1, bg="#e1e8ed")
        divider.pack(fill="x", pady=(15, 10), padx=40)
        
        # Footer with default credentials info
        footer_frame = tk.Frame(self, bg="#f5f7fa")
        footer_frame.pack(side="bottom", pady=(0, 20))
        
        # Modern footer design
        demo_label = tk.Label(
            footer_frame,
            text="🎯 Demo Credentials",
            bg="#f5f7fa",
            fg="#7f8c8d",
            font=("Segoe UI", 9, "bold")
        )
        demo_label.pack()
        
        credentials_frame = tk.Frame(footer_frame, bg="#f5f7fa")
        credentials_frame.pack(pady=(5, 0))
        
        # Admin credentials
        admin_label = tk.Label(
            credentials_frame,
            text="Admin: admin / admin123",
            bg="#f5f7fa",
            fg="#95a5a6",
            font=("Segoe UI", 8)
        )
        admin_label.pack(side="left", padx=(0, 15))
        
        # Test credentials  
        test_label = tk.Label(
            credentials_frame,
            text="Test: test / test",
            bg="#f5f7fa",
            fg="#95a5a6",
            font=("Segoe UI", 8)
        )
        test_label.pack(side="right", padx=(15, 0))

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