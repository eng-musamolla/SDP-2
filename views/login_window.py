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
        window_height = 650
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
        
        # Modern header section with gradient effect
        header_frame = tk.Frame(self, bg="#f5f7fa")
        header_frame.pack(pady=(30, 15))
        
        # Modern icon and title
        icon_title_frame = tk.Frame(header_frame, bg="#f5f7fa")
        icon_title_frame.pack()
        
        # System icon
        icon_label = tk.Label(
            icon_title_frame,
            text="🏢",
            bg="#f5f7fa",
            font=("Segoe UI", 24)
        )
        icon_label.pack()
        
        # App title with modern styling
        title_label = tk.Label(
            header_frame, 
            text="Employee Management System", 
            bg="#f5f7fa", 
            fg="#2c3e50",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(5, 0))
        
        # Modern subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Version 2.0 - Professional Edition",
            bg="#f5f7fa",
            fg="#7f8c8d",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack()
        
        # Welcome message with modern styling
        welcome_frame = tk.Frame(self, bg="#f5f7fa")
        welcome_frame.pack(pady=(10, 20))
        
        welcome_label = tk.Label(
            welcome_frame,
            text="🔐 Please sign in to your account",
            bg="#f5f7fa",
            fg="#34495e",
            font=("Segoe UI", 12)
        )
        welcome_label.pack()
        

        

        
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
        
        # Rounded username entry container
        username_container = tk.Frame(form_frame, bg="#f5f7fa", height=50)
        username_container.pack(fill="x", pady=(0, 15))
        username_container.pack_propagate(False)
        
        # Top rounded corners for username
        username_top = tk.Frame(username_container, bg="#f5f7fa", height=4)
        username_top.pack(fill="x", padx=6)
        
        # Username entry with rounded appearance
        username_wrapper = tk.Frame(
            username_container,
            bg="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightcolor="#3498db",
            highlightbackground="#e8ecf0"
        )
        username_wrapper.pack(fill="x", padx=3, pady=(0, 4))
        
        # Bottom rounded corners for username
        username_bottom = tk.Frame(username_container, bg="#f5f7fa", height=4)
        username_bottom.pack(fill="x", padx=6)
        
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
        
        # Rounded password entry container
        password_container = tk.Frame(form_frame, bg="#f5f7fa", height=50)
        password_container.pack(fill="x", pady=(0, 20))
        password_container.pack_propagate(False)
        
        # Top rounded corners for password
        password_top = tk.Frame(password_container, bg="#f5f7fa", height=4)
        password_top.pack(fill="x", padx=6)
        
        # Password entry with rounded appearance
        password_wrapper = tk.Frame(
            password_container,
            bg="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightcolor="#3498db",
            highlightbackground="#e8ecf0"
        )
        password_wrapper.pack(fill="x", padx=3, pady=(0, 4))
        
        # Bottom rounded corners for password
        password_bottom = tk.Frame(password_container, bg="#f5f7fa", height=4)
        password_bottom.pack(fill="x", padx=6)
        
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
        
        # Rounded login button container
        login_container = tk.Frame(form_frame, bg="#f5f7fa", height=60)
        login_container.pack(fill="x", pady=(20, 0))
        login_container.pack_propagate(False)
        
        # Top rounded corners for login button
        login_top = tk.Frame(login_container, bg="#f5f7fa", height=5)
        login_top.pack(fill="x", padx=8)
        
        # Login button with rounded appearance
        self.login_btn = tk.Button(
            login_container, 
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
        self.login_btn.pack(fill="x", padx=4, pady=(0, 5))
        
        # Bottom rounded corners for login button
        login_bottom = tk.Frame(login_container, bg="#f5f7fa", height=5)
        login_bottom.pack(fill="x", padx=8)
        
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
    
    def show_signup(self):
        """Show signup dialog with modern design"""
        signup_window = tk.Toplevel(self)
        signup_window.title("Create New Account")
        signup_window.configure(bg="#f5f7fa")
        signup_window.geometry("450x600")
        signup_window.resizable(False, False)
        
        # Center the window
        signup_window.transient(self)
        signup_window.grab_set()
        
        # Modern header
        header_frame = tk.Frame(signup_window, bg="#f5f7fa")
        header_frame.pack(pady=(30, 20))
        
        icon_label = tk.Label(header_frame, text="👤", bg="#f5f7fa", font=("Segoe UI", 28))
        icon_label.pack()
        
        title_label = tk.Label(
            header_frame,
            text="Create Your Account",
            bg="#f5f7fa",
            fg="#2c3e50",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Join our employee management system",
            bg="#f5f7fa",
            fg="#7f8c8d",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack()
        
        # Form frame
        form_frame = tk.Frame(signup_window, bg="#f5f7fa")
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Rounded information message container
        info_container = tk.Frame(form_frame, bg="#f5f7fa")
        info_container.pack(fill="x", pady=(20, 20))
        
        # Top rounded corners for info panel
        info_top = tk.Frame(info_container, bg="#f5f7fa", height=4)
        info_top.pack(fill="x", padx=6)
        
        # Information message with rounded appearance
        info_label = tk.Label(
            info_container,
            text="⚠️ Contact Administrator\n\nNew accounts must be created by system administrators.\nPlease contact your IT department or system admin\nto create your employee account.",
            bg="#fff3cd",
            fg="#856404",
            font=("Segoe UI", 11),
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=15,
            justify="center"
        )
        info_label.pack(fill="x", padx=3, pady=(0, 4))
        
        # Bottom rounded corners for info panel
        info_bottom = tk.Frame(info_container, bg="#f5f7fa", height=4)
        info_bottom.pack(fill="x", padx=6)
        
        # Rounded contact admin button container
        contact_container = tk.Frame(form_frame, bg="#f5f7fa", height=60)
        contact_container.pack(pady=(10, 20))
        contact_container.pack_propagate(False)
        
        # Top rounded corners for contact button
        contact_top = tk.Frame(contact_container, bg="#f5f7fa", height=5)
        contact_top.pack(fill="x", padx=8)
        
        # Contact admin button with rounded appearance
        contact_btn = tk.Button(
            contact_container,
            text="📧 Contact Administrator",
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2",
            bd=0,
            highlightthickness=0,
            command=lambda: messagebox.showinfo(
                "Contact Information",
                "Please contact:\n\n📧 Email: eng.musamolla@gmail.com\n👤 Admin: Musa Molla\n\nProvide your employee details for account creation."
            )
        )
        contact_btn.pack(fill="x", padx=4, pady=(0, 5))
        
        # Bottom rounded corners for contact button
        contact_bottom = tk.Frame(contact_container, bg="#f5f7fa", height=5)
        contact_bottom.pack(fill="x", padx=8)
        
        # Rounded close button container
        close_container = tk.Frame(form_frame, bg="#f5f7fa", height=50)
        close_container.pack()
        close_container.pack_propagate(False)
        
        # Top rounded corners for close button
        close_top = tk.Frame(close_container, bg="#f5f7fa", height=4)
        close_top.pack(fill="x", padx=6)
        
        # Close button with rounded appearance
        close_btn = tk.Button(
            close_container,
            text="✖️ Close",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            cursor="hand2",
            bd=0,
            highlightthickness=0,
            command=signup_window.destroy
        )
        close_btn.pack(fill="x", padx=3, pady=(0, 4))
        
        # Bottom rounded corners for close button
        close_bottom = tk.Frame(close_container, bg="#f5f7fa", height=4)
        close_bottom.pack(fill="x", padx=6)
    
    def show_forgot_password(self):
        """Show forgot password dialog with modern design"""
        forgot_window = tk.Toplevel(self)
        forgot_window.title("Password Recovery")
        forgot_window.configure(bg="#f5f7fa")
        forgot_window.geometry("450x500")
        forgot_window.resizable(False, False)
        
        # Center the window
        forgot_window.transient(self)
        forgot_window.grab_set()
        
        # Modern header
        header_frame = tk.Frame(forgot_window, bg="#f5f7fa")
        header_frame.pack(pady=(30, 20))
        
        icon_label = tk.Label(header_frame, text="🔐", bg="#f5f7fa", font=("Segoe UI", 28))
        icon_label.pack()
        
        title_label = tk.Label(
            header_frame,
            text="Password Recovery",
            bg="#f5f7fa",
            fg="#2c3e50",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Reset your account password",
            bg="#f5f7fa",
            fg="#7f8c8d",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack()
        
        # Form frame
        form_frame = tk.Frame(forgot_window, bg="#f5f7fa")
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Information message
        info_label = tk.Label(
            form_frame,
            text="🔒 Password Reset Required\n\nFor security reasons, password resets must be\nhandled by system administrators.\n\nPlease contact your administrator with:\n• Your username\n• Employee ID\n• Reason for reset",
            bg="#e7f3ff",
            fg="#0c5460",
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            padx=20,
            pady=15,
            justify="center"
        )
        info_label.pack(fill="x", pady=(20, 20))
        
        # Demo credentials reminder
        demo_label = tk.Label(
            form_frame,
            text="🎯 Demo Access\n\nFor demonstration purposes, use:\n• Admin: admin / admin123\n• Test: test / test",
            bg="#d4edda",
            fg="#155724",
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=12,
            justify="center"
        )
        demo_label.pack(fill="x", pady=(10, 20))
        
        # Contact admin button
        contact_btn = tk.Button(
            form_frame,
            text="📧 Contact Administrator",
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=lambda: messagebox.showinfo(
                "Administrator Contact",
                "Password Reset Support:\n\n📧 Email: eng.musamolla@gmail.com\n👤 Admin: Musa Molla\n🏢 System Administrator\n\nInclude your username and employee details."
            )
        )
        contact_btn.pack(pady=(10, 10))
        
        # Close button
        close_btn = tk.Button(
            form_frame,
            text="✖️ Close",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10,
            command=forgot_window.destroy
        )
        close_btn.pack()

if __name__ == "__main__":
    # For testing the login window independently
    app = LoginWindow()
    app.mainloop()