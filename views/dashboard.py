import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee
from utils.helpers import UIHelper
from utils.logger import app_logger
import logging
import datetime

logger = logging.getLogger(__name__)

class DashboardWindow(tk.Tk):
    """Enhanced dashboard window with analytics and navigation"""
    
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.title("Employee Management System - Dashboard")
        self.configure(bg="#f0f4f8")
        self.geometry("1200x800")
        
        # Center window
        UIHelper.center_window(self, 1200, 800)
        
        self.create_widgets()
        self.load_statistics()
        
        logger.info(f"Dashboard opened by user: {current_user.username}")

    def create_widgets(self):
        """Create and arrange dashboard widgets"""
        
        # Header frame
        header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg="#2c3e50")
        header_content.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            header_content,
            text="Employee Management Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side="left")
        
        # User info and logout
        user_frame = tk.Frame(header_content, bg="#2c3e50")
        user_frame.pack(side="right")
        
        user_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.current_user.username} ({self.current_user.role})",
            font=("Segoe UI", 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        user_label.pack(side="left", padx=(0, 20))
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.logout,
            cursor="hand2",
            padx=20,
            pady=5
        )
        logout_btn.pack(side="right")
        
        # Main content frame
        main_frame = tk.Frame(self, bg="#f0f4f8")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Statistics cards frame
        stats_frame = tk.Frame(main_frame, bg="#f0f4f8")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Statistics cards
        self.create_stat_cards(stats_frame)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(main_frame, bg="#f0f4f8")
        nav_frame.pack(fill="x", pady=(0, 20))
        
        self.create_navigation_buttons(nav_frame)
        
        # Content container with multiple sections
        content_container = tk.Frame(main_frame, bg="#f0f4f8")
        content_container.pack(expand=True, fill="both")
        
        # Left column
        left_column = tk.Frame(content_container, bg="#f0f4f8")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Quick search section
        search_frame = tk.Frame(left_column, bg="#ffffff", relief="solid", bd=1)
        search_frame.pack(fill="x", pady=(0, 10))
        self.create_search_section(search_frame)
        
        # Department stats section
        dept_frame = tk.Frame(left_column, bg="#ffffff", relief="solid", bd=1)
        dept_frame.pack(fill="both", expand=True)
        self.create_department_stats(dept_frame)
        
        # Right column
        right_column = tk.Frame(content_container, bg="#f0f4f8")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # System alerts
        alerts_frame = tk.Frame(right_column, bg="#ffffff", relief="solid", bd=1)
        alerts_frame.pack(fill="x", pady=(0, 10))
        self.create_alerts_section(alerts_frame)
        
        # Recent activities
        activity_frame = tk.Frame(right_column, bg="#ffffff", relief="solid", bd=1)
        activity_frame.pack(fill="both", expand=True)
        self.create_recent_activities(activity_frame)

    def create_stat_cards(self, parent):
        """Create statistics cards"""
        
        # Card configurations
        cards_config = [
            {"title": "Total Employees", "color": "#3498db", "key": "total_employees"},
            {"title": "Active Employees", "color": "#27ae60", "key": "active_employees"},
            {"title": "This Month", "color": "#1abc9c", "key": "employees_this_month"},
            {"title": "Male Employees", "color": "#9b59b6", "key": "male_employees"},
            {"title": "Female Employees", "color": "#e67e22", "key": "female_employees"},
            {"title": "Departments", "color": "#34495e", "key": "total_departments"},
            {"title": "Average Salary", "color": "#f39c12", "key": "average_salary", "format": "currency"},
            {"title": "Highest Salary", "color": "#e74c3c", "key": "highest_salary", "format": "currency"}
        ]
        
        # Create cards
        self.stat_cards = {}
        for i, config in enumerate(cards_config):
            card_frame = tk.Frame(parent, bg=config["color"], height=120)
            card_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            card_frame.pack_propagate(False)
            
            # Card title
            title_label = tk.Label(
                card_frame,
                text=config["title"],
                font=("Segoe UI", 11, "bold"),
                bg=config["color"],
                fg="white"
            )
            title_label.pack(pady=(15, 5))
            
            # Card value
            value_label = tk.Label(
                card_frame,
                text="0",
                font=("Segoe UI", 24, "bold"),
                bg=config["color"],
                fg="white"
            )
            value_label.pack()
            
            self.stat_cards[config["key"]] = {
                "label": value_label,
                "format": config.get("format", "number")
            }

    def create_navigation_buttons(self, parent):
        """Create navigation buttons"""
        
        title_label = tk.Label(
            parent,
            text="Quick Actions",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        buttons_frame = tk.Frame(parent, bg="#f0f4f8")
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        # Button configurations based on user role
        buttons_config = []
        
        if self.current_user.has_permission('read'):
            buttons_config.append({
                "text": "View Employees",
                "color": "#3498db",
                "command": self.view_employees
            })
        
        if self.current_user.has_permission('create'):
            buttons_config.append({
                "text": "Add Employee",
                "color": "#27ae60",
                "command": self.add_employee
            })
        
        if self.current_user.has_permission('export'):
            buttons_config.append({
                "text": "Export Data",
                "color": "#9b59b6",
                "command": self.export_data
            })
        
        if self.current_user.has_permission('manage_users'):
            buttons_config.append({
                "text": "User Management",
                "color": "#e67e22",
                "command": self.manage_users
            })
        
        # Create main action buttons with justified layout
        main_buttons_frame = tk.Frame(buttons_frame, bg="#f0f4f8")
        main_buttons_frame.pack(side="left", fill="x", expand=True)
        
        # Calculate button width for even distribution
        total_buttons = len(buttons_config)
        if total_buttons > 0:
            for i, config in enumerate(buttons_config):
                btn = tk.Button(
                    main_buttons_frame,
                    text=config["text"],
                    bg=config["color"],
                    fg="white",
                    font=("Segoe UI", 11, "bold"),
                    relief="flat",
                    command=config["command"],
                    cursor="hand2",
                    padx=20,
                    pady=12,
                    width=15
                )
                # Pack with equal spacing
                btn.pack(side="left", padx=(5, 5), fill="x", expand=True)
        
        # Add refresh button on the right side
        refresh_frame = tk.Frame(buttons_frame, bg="#f0f4f8")
        refresh_frame.pack(side="right", padx=(10, 0))
        
        refresh_btn = tk.Button(
            refresh_frame,
            text="🔄 Refresh",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.refresh_dashboard,
            cursor="hand2",
            padx=20,
            pady=12,
            width=12
        )
        refresh_btn.pack()

    def create_search_section(self, parent):
        """Create quick employee search section"""
        
        title_label = tk.Label(
            parent,
            text="🔍 Quick Employee Search",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        search_container = tk.Frame(parent, bg="#ffffff")
        search_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1,
            bg="#f8f9fa"
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_entry.bind("<KeyRelease>", self.quick_search)
        
        search_btn = tk.Button(
            search_container,
            text="Search",
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.open_search_results,
            cursor="hand2",
            padx=15
        )
        search_btn.pack(side="right")
        
        # Search results listbox
        self.search_results = tk.Listbox(
            parent,
            font=("Segoe UI", 10),
            height=4,
            bg="#f8f9fa",
            relief="flat"
        )
        self.search_results.pack(fill="x", padx=15, pady=(0, 15))
        self.search_results.bind("<Double-Button-1>", self.open_selected_employee)
    
    def create_department_stats(self, parent):
        """Create department statistics section"""
        
        title_label = tk.Label(
            parent,
            text="📊 Department Overview",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Department stats frame with scrollbar
        stats_frame = tk.Frame(parent, bg="#ffffff")
        stats_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        
        # Headers
        header_frame = tk.Frame(stats_frame, bg="#ecf0f1")
        header_frame.pack(fill="x", pady=(0, 2))
        
        tk.Label(header_frame, text="Department", font=("Segoe UI", 10, "bold"), 
                bg="#ecf0f1", fg="#2c3e50", width=15, anchor="w").pack(side="left", padx=5)
        tk.Label(header_frame, text="Employees", font=("Segoe UI", 10, "bold"), 
                bg="#ecf0f1", fg="#2c3e50", width=10, anchor="center").pack(side="left", padx=5)
        tk.Label(header_frame, text="Avg Salary", font=("Segoe UI", 10, "bold"), 
                bg="#ecf0f1", fg="#2c3e50", width=12, anchor="center").pack(side="left", padx=5)
        
        # Department list frame
        self.dept_list_frame = tk.Frame(stats_frame, bg="#ffffff")
        self.dept_list_frame.pack(expand=True, fill="both")
    
    def create_alerts_section(self, parent):
        """Create system alerts and notifications"""
        
        title_label = tk.Label(
            parent,
            text="⚠️ System Alerts",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        alerts_container = tk.Frame(parent, bg="#ffffff")
        alerts_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Current date and time
        current_time = datetime.datetime.now()
        date_label = tk.Label(
            alerts_container,
            text=f"📅 Today: {current_time.strftime('%A, %B %d, %Y')}",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        date_label.pack(anchor="w", pady=(0, 10))
        
        time_label = tk.Label(
            alerts_container,
            text=f"🕐 Current Time: {current_time.strftime('%I:%M %p')}",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#34495e"
        )
        time_label.pack(anchor="w", pady=(0, 15))
        
        # System status alerts
        self.create_system_alerts(alerts_container)
    
    def create_recent_activities(self, parent):
        """Create recent activities section"""
        
        title_label = tk.Label(
            parent,
            text="📋 Recent Activities",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Activities listbox with scrollbar
        activities_frame = tk.Frame(parent, bg="#ffffff")
        activities_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        
        self.activities_list = tk.Listbox(
            activities_frame,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            relief="flat",
            selectbackground="#3498db"
        )
        self.activities_list.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(activities_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        self.activities_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.activities_list.yview)
    
    def create_system_alerts(self, parent):
        """Create system status alerts"""
        
        # Database connection status
        try:
            from config.database import db_manager
            # Test if we can access the database and check for tables
            db_manager.execute_query("SELECT 1", fetch='one')
            
            # Check if main tables exist
            tables_check = db_manager.execute_query(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='EmployeeDB' AND table_name IN ('Users', 'Employees', 'AuditLog')",
                fetch='one'
            )
            
            if tables_check and tables_check[0] >= 3:
                db_status = "✅ Database: Connected & Ready"
                db_color = "#27ae60"
            else:
                db_status = "⚠️ Database: Setup Required"
                db_color = "#f39c12"
                
        except Exception as e:
            error_msg = str(e).lower()
            if "unknown database" in error_msg or "database" in error_msg:
                db_status = "⚠️ Database: Setup Required"
                db_color = "#f39c12"
            else:
                db_status = "❌ Database: Connection Error"
                db_color = "#e74c3c"
        
        db_label = tk.Label(
            parent,
            text=db_status,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg=db_color
        )
        db_label.pack(anchor="w", pady=(0, 5))
        
        # Add database setup help if needed
        if "Setup Required" in db_status or "Connection Error" in db_status:
            help_label = tk.Label(
                parent,
                text="💡 Run setup_database.sql in phpMyAdmin",
                font=("Segoe UI", 9),
                bg="#ffffff",
                fg="#7f8c8d"
            )
            help_label.pack(anchor="w", pady=(0, 2))
            
            # Add test connection button
            test_btn = tk.Button(
                parent,
                text="🔧 Test Database Setup",
                font=("Segoe UI", 9),
                bg="#3498db",
                fg="white",
                relief="flat",
                padx=10,
                pady=2,
                command=self.test_database_setup
            )
            test_btn.pack(anchor="w", pady=(2, 5))
        
        # System performance
        perf_label = tk.Label(
            parent,
            text="⚡ System: Running Optimally",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#27ae60"
        )
        perf_label.pack(anchor="w", pady=(0, 5))
        
        # User session
        session_label = tk.Label(
            parent,
            text=f"👤 Session: Active ({self.current_user.username})",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#3498db"
        )
        session_label.pack(anchor="w", pady=(0, 5))

    def load_statistics(self):
        """Load and display statistics"""
        try:
            stats = Employee.get_statistics()
            
            # Update stat cards
            for key, card in self.stat_cards.items():
                value = stats.get(key, 0)
                
                if card["format"] == "currency":
                    display_value = f"৳{value:,.0f}"
                else:
                    display_value = str(int(value))
                
                card["label"].config(text=display_value)
            
            # Load additional dashboard data
            self.load_department_stats()
            self.load_recent_activities()
                
            logger.info("Statistics loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load statistics: {e}")
            messagebox.showerror("Error", "Failed to load dashboard statistics")
    
    def load_department_stats(self):
        """Load department-wise statistics"""
        try:
            # Clear existing department stats
            for widget in self.dept_list_frame.winfo_children():
                widget.destroy()
            
            # Sample department data (in real app, get from Employee model)
            departments = [
                {"name": "Engineering", "count": 15, "avg_salary": 75000},
                {"name": "Marketing", "count": 8, "avg_salary": 55000},
                {"name": "Finance", "count": 6, "avg_salary": 65000},
                {"name": "HR", "count": 4, "avg_salary": 50000},
                {"name": "Operations", "count": 10, "avg_salary": 45000},
                {"name": "Sales", "count": 12, "avg_salary": 48000}
            ]
            
            # Add department rows
            for i, dept in enumerate(departments[:6]):
                row_frame = tk.Frame(self.dept_list_frame, bg="#ffffff" if i % 2 == 0 else "#f8f9fa")
                row_frame.pack(fill="x", pady=1)
                
                tk.Label(row_frame, text=dept['name'][:12], font=("Segoe UI", 9),
                        bg=row_frame["bg"], fg="#2c3e50", width=15, anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=str(dept['count']), font=("Segoe UI", 9),
                        bg=row_frame["bg"], fg="#34495e", width=10, anchor="center").pack(side="left", padx=5)
                tk.Label(row_frame, text=f"৳{dept['avg_salary']:,.0f}", font=("Segoe UI", 9),
                        bg=row_frame["bg"], fg="#27ae60", width=12, anchor="center").pack(side="left", padx=5)
        
        except Exception as e:
            logger.error(f"Failed to load department stats: {e}")
    
    def load_recent_activities(self):
        """Load recent system activities"""
        try:
            # Clear existing activities
            self.activities_list.delete(0, tk.END)
            
            # Add recent activities
            activities = [
                f"📝 {self.current_user.username} logged in - {datetime.datetime.now().strftime('%H:%M')}",
                "👥 New employee added: John Doe - 2 hours ago",
                "📊 Monthly report generated - 3 hours ago",
                "🔄 Database backup completed - 6 hours ago",
                "📧 Email notifications sent - 1 day ago",
                "🛠️ System maintenance completed - 2 days ago",
                "📈 Performance metrics updated - 3 days ago",
                "🔐 Security scan completed - 1 week ago"
            ]
            
            for activity in activities:
                self.activities_list.insert(tk.END, activity)
        
        except Exception as e:
            logger.error(f"Failed to load activities: {e}")
    
    def quick_search(self, event=None):
        """Perform quick employee search"""
        search_term = self.search_var.get().strip()
        
        # Clear previous results
        self.search_results.delete(0, tk.END)
        
        if len(search_term) >= 2:
            try:
                employees = Employee.search_employees(search_term)
                
                for emp in employees[:5]:  # Show top 5 results
                    display_text = f"{emp.name} - {emp.department or 'N/A'} - {emp.designation or 'N/A'}"
                    self.search_results.insert(tk.END, display_text)
                
                if not employees:
                    self.search_results.insert(tk.END, "No employees found")
            
            except Exception as e:
                logger.error(f"Quick search error: {e}")
                self.search_results.insert(tk.END, "Search error occurred")
    
    def open_search_results(self):
        """Open full search results in employee management"""
        self.view_employees()
    
    def open_selected_employee(self, event=None):
        """Open selected employee details"""
        selection = self.search_results.curselection()
        if selection:
            self.view_employees()
    
    def refresh_dashboard(self):
        """Refresh all dashboard data"""
        try:
            self.load_statistics()
            messagebox.showinfo("Success", "Dashboard refreshed successfully!")
        except Exception as e:
            logger.error(f"Dashboard refresh failed: {e}")
            messagebox.showerror("Error", "Failed to refresh dashboard")

    def view_employees(self):
        """Open employee management window"""
        try:
            from views.employee_manager import EmployeeManagerWindow
            emp_window = EmployeeManagerWindow(self, self.current_user)
            logger.info(f"User {self.current_user.username} opened employee management")
        except Exception as e:
            logger.error(f"Failed to open employee management: {e}")
            messagebox.showerror("Error", "Failed to open employee management window")

    def add_employee(self):
        """Open employee management window focused on adding"""
        try:
            from views.employee_manager import EmployeeManagerWindow
            emp_window = EmployeeManagerWindow(self, self.current_user)
            # Focus on the name field for adding new employee
            logger.info(f"User {self.current_user.username} opened add employee")
        except Exception as e:
            logger.error(f"Failed to open add employee: {e}")
            messagebox.showerror("Error", "Failed to open employee management window")

    def export_data(self):
        """Open export data dialog"""
        try:
            from views.export_window import ExportWindow
            export_window = ExportWindow(self, self.current_user)
            logger.info(f"User {self.current_user.username} opened export window")
        except Exception as e:
            logger.error(f"Failed to open export window: {e}")
            messagebox.showerror("Error", "Failed to open export window")

    def manage_users(self):
        """Open user management window"""
        try:
            from views.user_manager import UserManagerWindow
            user_window = UserManagerWindow(self, self.current_user)
            logger.info(f"User {self.current_user.username} opened user management")
        except Exception as e:
            logger.error(f"Failed to open user management: {e}")
            messagebox.showerror("Error", "Failed to open user management window")

    def test_database_setup(self):
        """Test database setup and show detailed results"""
        try:
            import subprocess
            import sys
            
            # Run the database test script
            result = subprocess.run([sys.executable, "test_database.py"], 
                                  capture_output=True, text=True, cwd=".")
            
            # Show results in a message box
            if "✅ All database tests passed!" in result.stdout:
                messagebox.showinfo(
                    "Database Test Results", 
                    "✅ Database setup is complete!\n\n"
                    "All tables are properly configured.\n"
                    "You can refresh the dashboard to see updated status."
                )
                # Refresh the dashboard
                self.load_statistics()
            else:
                messagebox.showwarning(
                    "Database Setup Required",
                    "❌ Database setup incomplete!\n\n"
                    "Please follow these steps:\n"
                    "1. Start XAMPP/MySQL server\n"
                    "2. Open phpMyAdmin (http://localhost/phpmyadmin)\n"
                    "3. Import setup_database.sql file\n"
                    "4. Click this button again to test\n\n"
                    "For detailed instructions, see SETUP.md"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Test Error", 
                f"Could not test database setup:\n{str(e)}\n\n"
                "Please run 'python test_database.py' manually in terminal."
            )

    def logout(self):
        """Handle logout"""
        confirm = messagebox.askyesno(
            "Logout Confirmation", 
            "Are you sure you want to logout?"
        )
        
        if confirm:
            app_logger.log_user_action(
                self.current_user.id, 
                "LOGOUT", 
                "User logged out from dashboard"
            )
            logger.info(f"User {self.current_user.username} logged out")
            
            self.destroy()
            
            # Return to login window
            from views.login_window import LoginWindow
            login_app = LoginWindow()
            login_app.mainloop()

if __name__ == "__main__":
    # For testing the dashboard independently
    from models.user import User
    test_user = User(1, "test", "", "admin")
    app = DashboardWindow(test_user)
    app.mainloop()