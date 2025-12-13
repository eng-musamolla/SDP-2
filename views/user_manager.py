import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from utils.validators import Validator, ValidationError
from utils.helpers import UIHelper, SecurityManager
from utils.logger import app_logger
import logging

logger = logging.getLogger(__name__)

class UserManagerWindow(tk.Toplevel):
    """User Management Window for admin users"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_user = None
        
        # Check permissions
        if not self.current_user.has_permission('manage_users'):
            messagebox.showerror("Access Denied", "You don't have permission to manage users")
            self.destroy()
            return
        
        self.title("User Management")
        self.configure(bg="#f0f4f8")
        self.geometry("1000x700")
        UIHelper.center_window(self, 1000, 700)
        
        self.create_widgets()
        self.load_users()
        
        logger.info(f"User management opened by {current_user.username}")

    def create_widgets(self):
        """Create user management interface"""
        
        # Header
        header_frame = tk.Frame(self, bg="#8e44ad", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="👥 User Management",
            font=("Arial", 16, "bold"),
            bg="#8e44ad",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        close_btn = tk.Button(
            header_frame,
            text="← Back",
            bg="#c0392b",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.destroy,
            cursor="hand2",
            padx=15,
            pady=5
        )
        close_btn.pack(side="right", padx=20, pady=15)
        
        # Main container
        main_container = tk.Frame(self, bg="#f0f4f8")
        main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel - User form
        left_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_user_form(left_panel)
        
        # Right panel - User list
        right_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        right_panel.pack(side="right", expand=True, fill="both")
        
        self.create_user_list(right_panel)

    def create_user_form(self, parent):
        """Create user input form"""
        
        # Form title
        form_title = tk.Label(
            parent,
            text="User Information",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        form_title.pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(parent, bg="#ffffff")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Username
        tk.Label(
            form_frame,
            text="Username *",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).grid(row=0, column=0, sticky="w", pady=(10, 2))
        
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Arial", 10),
            relief="solid",
            bd=1,
            width=25
        )
        self.username_entry.grid(row=0, column=1, pady=(10, 2), padx=(10, 0))
        
        # Password
        tk.Label(
            form_frame,
            text="Password *",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).grid(row=1, column=0, sticky="w", pady=(10, 2))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=("Arial", 10),
            relief="solid",
            bd=1,
            width=25,
            show="*"
        )
        self.password_entry.grid(row=1, column=1, pady=(10, 2), padx=(10, 0))
        
        # Role
        tk.Label(
            form_frame,
            text="Role *",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).grid(row=2, column=0, sticky="w", pady=(10, 2))
        
        self.role_var = tk.StringVar()
        role_combo = ttk.Combobox(
            form_frame,
            textvariable=self.role_var,
            values=["admin", "manager", "employee"],
            font=("Arial", 10),
            width=23,
            state="readonly"
        )
        role_combo.grid(row=2, column=1, pady=(10, 2), padx=(10, 0))
        
        # Status
        tk.Label(
            form_frame,
            text="Status",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).grid(row=3, column=0, sticky="w", pady=(10, 2))
        
        self.status_var = tk.BooleanVar(value=True)
        status_check = tk.Checkbutton(
            form_frame,
            text="Active User",
            variable=self.status_var,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#2c3e50"
        )
        status_check.grid(row=3, column=1, pady=(10, 2), padx=(10, 0), sticky="w")
        
        # Password strength indicator
        self.password_strength_label = tk.Label(
            form_frame,
            text="",
            font=("Arial", 8),
            bg="#ffffff"
        )
        self.password_strength_label.grid(row=4, column=0, columnspan=2, pady=(5, 10))
        
        # Bind password change to strength checker
        self.password_var.trace("w", self.check_password_strength)
        
        # Role permissions info
        permissions_frame = tk.LabelFrame(
            parent,
            text="Role Permissions",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        permissions_frame.pack(padx=20, pady=10, fill="x")
        
        permissions_text = tk.Text(
            permissions_frame,
            font=("Arial", 8),
            bg="#f8f9fa",
            relief="flat",
            height=8,
            wrap="word"
        )
        permissions_text.pack(padx=10, pady=10, fill="x")
        
        permissions_info = """Admin:
• Full system access
• Create, edit, delete employees
• Manage users and roles
• Export and import data
• System configuration

Manager:
• Create, edit, delete employees
• Export employee data
• View all employees
• Generate reports

Employee:
• View employee directory
• Read-only access
• Limited functionality"""
        
        permissions_text.insert("1.0", permissions_info)
        permissions_text.config(state="disabled")
        
        # Action buttons
        button_frame = tk.Frame(parent, bg="#ffffff")
        button_frame.pack(padx=20, pady=20)
        
        create_btn = tk.Button(
            button_frame,
            text="👤 Create User",
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.create_user,
            cursor="hand2",
            padx=15,
            pady=8
        )
        create_btn.pack(pady=5, fill="x")
        
        update_btn = tk.Button(
            button_frame,
            text="✏️ Update User",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.update_user,
            cursor="hand2",
            padx=15,
            pady=8
        )
        update_btn.pack(pady=5, fill="x")
        
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Deactivate User",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.deactivate_user,
            cursor="hand2",
            padx=15,
            pady=8
        )
        delete_btn.pack(pady=5, fill="x")
        
        clear_btn = tk.Button(
            button_frame,
            text="🔄 Clear Form",
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.clear_form,
            cursor="hand2",
            padx=15,
            pady=8
        )
        clear_btn.pack(pady=5, fill="x")

    def create_user_list(self, parent):
        """Create user list with actions"""
        
        # List header
        list_header = tk.Frame(parent, bg="#ffffff")
        list_header.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            list_header,
            text="System Users",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(side="left")
        
        # User treeview
        tree_frame = tk.Frame(parent, bg="#ffffff")
        tree_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        columns = ("ID", "Username", "Role", "Status", "Created", "Last Updated")
        self.user_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        column_widths = {"ID": 50, "Username": 120, "Role": 100, "Status": 80, "Created": 150, "Last Updated": 150}
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.user_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.user_tree.xview)
        self.user_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.user_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # Bind selection event
        self.user_tree.bind("<<TreeviewSelect>>", self.on_user_select)

    def check_password_strength(self, *args):
        """Check and display password strength"""
        password = self.password_var.get()
        if not password:
            self.password_strength_label.config(text="", fg="black")
            return
        
        is_strong, message = Validator.validate_password_strength(password)
        
        if is_strong:
            self.password_strength_label.config(text="✅ " + message, fg="green")
        else:
            self.password_strength_label.config(text="⚠️ " + message, fg="red")

    def load_users(self):
        """Load all users into the treeview"""
        try:
            # Clear existing items
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
            
            # Load users from database
            users = User.get_all_users()
            
            for user in users:
                status_text = "Active" if user.is_active else "Inactive"
                created_date = user.created_at.strftime("%Y-%m-%d %H:%M") if user.created_at else "N/A"
                updated_date = user.updated_at.strftime("%Y-%m-%d %H:%M") if user.updated_at else "N/A"
                
                self.user_tree.insert("", "end", values=(
                    user.id,
                    user.username,
                    user.role.title(),
                    status_text,
                    created_date,
                    updated_date
                ))
            
            logger.info(f"Loaded {len(users)} users")
            
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            messagebox.showerror("Error", "Failed to load users from database")

    def on_user_select(self, event):
        """Handle user selection"""
        selection = self.user_tree.selection()
        if selection:
            item = self.user_tree.item(selection[0])
            user_id = item['values'][0]
            
            # Load user details
            try:
                self.selected_user = User.get_by_id(user_id)
                if self.selected_user:
                    self.populate_form(self.selected_user)
                    logger.info(f"Selected user: {self.selected_user.username}")
                    
            except Exception as e:
                logger.error(f"Failed to load user details: {e}")

    def populate_form(self, user):
        """Populate form with user data"""
        self.username_var.set(user.username)
        self.password_var.set("")  # Don't show actual password
        self.role_var.set(user.role)
        self.status_var.set(user.is_active)

    def clear_form(self):
        """Clear all form fields"""
        self.username_var.set("")
        self.password_var.set("")
        self.role_var.set("")
        self.status_var.set(True)
        self.selected_user = None

    def create_user(self):
        """Create new user"""
        try:
            # Validate input
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            role = self.role_var.get()
            is_active = self.status_var.get()
            
            if not username or not password or not role:
                messagebox.showerror("Validation Error", "Please fill in all required fields")
                return
            
            # Check password strength
            is_strong, message = Validator.validate_password_strength(password)
            if not is_strong:
                result = messagebox.askyesno("Weak Password", f"{message}\n\nDo you want to continue anyway?")
                if not result:
                    return
            
            # Check if username exists
            existing_users = User.get_all_users()
            if any(u.username.lower() == username.lower() for u in existing_users):
                messagebox.showerror("Validation Error", "Username already exists")
                return
            
            # Create user
            user = User(
                username=username,
                password=password,  # Will be hashed in save method
                role=role,
                is_active=is_active
            )
            
            if user.save():
                messagebox.showinfo("Success", f"User '{username}' created successfully!")
                app_logger.log_user_action(self.current_user.id, "CREATE_USER", f"Username: {username}, Role: {role}")
                self.clear_form()
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to create user")
                
        except Exception as e:
            logger.error(f"Create user failed: {e}")
            messagebox.showerror("Error", f"Failed to create user: {e}")

    def update_user(self):
        """Update selected user"""
        if not self.selected_user:
            messagebox.showwarning("No Selection", "Please select a user to update")
            return
        
        try:
            # Update user properties
            self.selected_user.username = self.username_var.get().strip()
            self.selected_user.role = self.role_var.get()
            self.selected_user.is_active = self.status_var.get()
            
            # Update password if provided
            password = self.password_var.get().strip()
            if password:
                if not self.selected_user.change_password(password):
                    messagebox.showerror("Error", "Failed to update password")
                    return
            
            if self.selected_user.save():
                messagebox.showinfo("Success", f"User '{self.selected_user.username}' updated successfully!")
                app_logger.log_user_action(self.current_user.id, "UPDATE_USER", f"Username: {self.selected_user.username}")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to update user")
                
        except Exception as e:
            logger.error(f"Update user failed: {e}")
            messagebox.showerror("Error", f"Failed to update user: {e}")

    def deactivate_user(self):
        """Deactivate selected user"""
        if not self.selected_user:
            messagebox.showwarning("No Selection", "Please select a user to deactivate")
            return
        
        if self.selected_user.id == self.current_user.id:
            messagebox.showerror("Error", "You cannot deactivate your own account")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Deactivation",
            f"Are you sure you want to deactivate user '{self.selected_user.username}'?\n\nThey will no longer be able to log in."
        )
        
        if confirm:
            try:
                if self.selected_user.delete():  # This performs soft delete (deactivation)
                    messagebox.showinfo("Success", f"User '{self.selected_user.username}' deactivated successfully!")
                    app_logger.log_user_action(self.current_user.id, "DEACTIVATE_USER", f"Username: {self.selected_user.username}")
                    self.clear_form()
                    self.load_users()
                else:
                    messagebox.showerror("Error", "Failed to deactivate user")
                    
            except Exception as e:
                logger.error(f"Deactivate user failed: {e}")
                messagebox.showerror("Error", f"Failed to deactivate user: {e}")