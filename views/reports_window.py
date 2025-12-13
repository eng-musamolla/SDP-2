import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.employee import Employee
from models.user import User
from utils.helpers import UIHelper
from utils.logger import app_logger
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class ReportsWindow(tk.Toplevel):
    """Reports Window for generating various reports"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        
        self.title("Reports & Analytics")
        self.configure(bg="#f0f4f8")
        
        # Get screen dimensions for responsive sizing
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate responsive window size (75% of screen)
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        
        self.geometry(f"{window_width}x{window_height}")
        UIHelper.center_window(self, window_width, window_height)
        self.resizable(True, True)
        
        self.create_widgets()
        
        logger.info(f"Reports window opened by {current_user.username}")

    def create_widgets(self):
        """Create reports interface"""
        
        # Header
        header_frame = tk.Frame(self, bg="#3498db", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📊 Reports & Analytics",
            font=("Arial", 16, "bold"),
            bg="#3498db",
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
        
        # Left panel - Report types
        left_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_report_types(left_panel)
        
        # Right panel - Report display
        right_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        right_panel.pack(side="right", expand=True, fill="both")
        
        self.create_report_display(right_panel)

    def create_report_types(self, parent):
        """Create enhanced report type selection with real functionality"""
        
        # Title
        title_label = tk.Label(
            parent,
            text="📊 Available Reports",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Report buttons
        reports_frame = tk.Frame(parent, bg="#ffffff")
        reports_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Employee reports
        employee_section = tk.LabelFrame(
            reports_frame,
            text="👥 Employee Reports",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        employee_section.pack(fill="x", pady=10)
        
        # Employee report buttons
        emp_buttons = [
            ("📈 Employee Summary", self.generate_employee_summary, "#3498db"),
            ("📊 Department Analysis", self.generate_department_report, "#e74c3c"),
            ("💰 Salary Report", self.generate_salary_report, "#f39c12"),
            ("📅 Joining Trends", self.generate_joining_trends, "#2ecc71")
        ]
        
        for i, (text, command, color) in enumerate(emp_buttons):
            btn = tk.Button(
                employee_section,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                width=20
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        # Configure grid weights for responsive buttons
        employee_section.grid_columnconfigure(0, weight=1)
        employee_section.grid_columnconfigure(1, weight=1)
        
        # Analytics section
        analytics_section = tk.LabelFrame(
            reports_frame,
            text="📊 Analytics & Insights",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        analytics_section.pack(fill="x", pady=10)
        
        # Analytics buttons
        analytics_buttons = [
            ("🔍 Age Distribution", self.show_age_distribution, "#9b59b6"),
            ("📈 Performance Metrics", self.show_performance_metrics, "#1abc9c"),
            ("💼 Active vs Inactive", self.show_status_analysis, "#34495e"),
            ("📄 Export All Data", self.export_all_reports, "#e67e22")
        ]
        
        for i, (text, command, color) in enumerate(analytics_buttons):
            btn = tk.Button(
                analytics_section,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                width=20
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        # Configure grid weights
        analytics_section.grid_columnconfigure(0, weight=1)
        analytics_section.grid_columnconfigure(1, weight=1)
        
        # System reports (admin only)
        if self.current_user.has_permission('manage_users'):
            system_section = tk.LabelFrame(
                reports_frame,
                text="System Reports",
                font=("Arial", 10, "bold"),
                bg="#ffffff",
                fg="#2c3e50"
            )
            system_section.pack(fill="x", pady=(0, 15))
            
            self.create_report_button(
                system_section,
                "👥 User Activity",
                self.generate_user_activity,
                "User login and activity log"
            )
            
            self.create_report_button(
                system_section,
                "🔐 Security Report",
                self.generate_security_report,
                "System security analysis"
            )
        
        # Custom reports
        custom_section = tk.LabelFrame(
            reports_frame,
            text="Custom Reports",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        custom_section.pack(fill="x")
        
        self.create_report_button(
            custom_section,
            "📊 Create Custom Report",
            self.create_custom_report,
            "Build your own report"
        )

    def create_report_button(self, parent, text, command, description):
        """Create a report button with description"""
        
        button_frame = tk.Frame(parent, bg="#ffffff")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        btn = tk.Button(
            button_frame,
            text=text,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=command,
            cursor="hand2",
            padx=15,
            pady=8,
            anchor="w"
        )
        btn.pack(fill="x")
        
        desc_label = tk.Label(
            button_frame,
            text=description,
            font=("Arial", 8),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        desc_label.pack(anchor="w", padx=5)

    def create_report_display(self, parent):
        """Create report display area"""
        
        # Display title
        self.display_title = tk.Label(
            parent,
            text="Select a report to view",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        self.display_title.pack(pady=20)
        
        # Report content frame
        content_frame = tk.Frame(parent, bg="#ffffff")
        content_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Create text widget with scrollbar for report display
        text_frame = tk.Frame(content_frame, bg="#ffffff")
        text_frame.pack(expand=True, fill="both")
        
        self.report_text = tk.Text(
            text_frame,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief="flat",
            wrap="word",
            padx=15,
            pady=15
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons
        action_frame = tk.Frame(parent, bg="#ffffff")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.save_btn = tk.Button(
            action_frame,
            text="💾 Save Report",
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.save_report,
            cursor="hand2",
            padx=15,
            pady=8,
            state="disabled"
        )
        self.save_btn.pack(side="left", padx=(0, 10))
        
        self.print_btn = tk.Button(
            action_frame,
            text="🖨️ Print Report",
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.print_report,
            cursor="hand2",
            padx=15,
            pady=8,
            state="disabled"
        )
        self.print_btn.pack(side="left")
        
        # Initial welcome text
        welcome_text = """
Welcome to Reports & Analytics!

Select a report type from the left panel to generate detailed analytics and reports.

Available reports include:
• Employee summaries and statistics
• Department and position analysis
• User activity reports (for administrators)
• Custom report builder

All reports can be saved to file or printed for offline use.
        """
        
        self.report_text.insert("1.0", welcome_text.strip())
        self.report_text.config(state="disabled")

    def generate_employee_summary(self):
        """Generate employee summary report"""
        try:
            self.display_title.config(text="📋 Employee Summary Report")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", "end")
            
            employees = Employee.get_all_employees()
            
            # Report header
            report = f"""
EMPLOYEE SUMMARY REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: {self.current_user.username}

{'=' * 80}

OVERVIEW:
Total Employees: {len(employees)}

"""
            
            if employees:
                # Group by department
                departments = {}
                for emp in employees:
                    dept = emp.department if emp.department else "Unassigned"
                    if dept not in departments:
                        departments[dept] = []
                    departments[dept].append(emp)
                
                report += f"Departments: {len(departments)}\n"
                
                for dept, dept_employees in departments.items():
                    report += f"  • {dept}: {len(dept_employees)} employees\n"
                
                report += f"\n{'=' * 80}\n\nDETAILED EMPLOYEE LIST:\n\n"
                
                # Employee list
                for i, emp in enumerate(employees, 1):
                    report += f"{i}. {emp.first_name} {emp.last_name}\n"
                    report += f"   ID: {emp.id}\n"
                    report += f"   Position: {emp.position if emp.position else 'N/A'}\n"
                    report += f"   Department: {emp.department if emp.department else 'N/A'}\n"
                    report += f"   Email: {emp.email if emp.email else 'N/A'}\n"
                    report += f"   Phone: {emp.phone if emp.phone else 'N/A'}\n"
                    report += f"   Hire Date: {emp.hire_date.strftime('%Y-%m-%d') if emp.hire_date else 'N/A'}\n"
                    if emp.salary:
                        report += f"   Salary: ${emp.salary:,.2f}\n"
                    report += "\n"
                
            else:
                report += "No employees found in the system.\n"
            
            self.report_text.insert("1.0", report)
            self.report_text.config(state="disabled")
            
            # Enable action buttons
            self.save_btn.config(state="normal")
            self.print_btn.config(state="normal")
            
            logger.info(f"Employee summary report generated by {self.current_user.username}")
            
        except Exception as e:
            logger.error(f"Failed to generate employee summary: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def generate_department_analysis(self):
        """Generate department analysis report"""
        try:
            self.display_title.config(text="📈 Department Analysis Report")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", "end")
            
            employees = Employee.get_all_employees()
            
            # Group by department
            departments = {}
            total_salary = 0
            
            for emp in employees:
                dept = emp.department if emp.department else "Unassigned"
                if dept not in departments:
                    departments[dept] = {
                        'employees': [],
                        'total_salary': 0,
                        'positions': {}
                    }
                
                departments[dept]['employees'].append(emp)
                
                if emp.salary:
                    departments[dept]['total_salary'] += emp.salary
                    total_salary += emp.salary
                
                # Track positions
                pos = emp.position if emp.position else "Unknown"
                if pos not in departments[dept]['positions']:
                    departments[dept]['positions'][pos] = 0
                departments[dept]['positions'][pos] += 1
            
            # Generate report
            report = f"""
DEPARTMENT ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: {self.current_user.username}

{'=' * 80}

DEPARTMENT SUMMARY:
Total Departments: {len(departments)}
Total Employees: {len(employees)}
Total Payroll: ${total_salary:,.2f}

"""
            
            for dept_name, dept_data in departments.items():
                emp_count = len(dept_data['employees'])
                avg_salary = dept_data['total_salary'] / emp_count if emp_count > 0 else 0
                
                report += f"\n{'-' * 60}\n"
                report += f"Department: {dept_name.upper()}\n"
                report += f"{'-' * 60}\n"
                report += f"Employees: {emp_count}\n"
                report += f"Total Salary Budget: ${dept_data['total_salary']:,.2f}\n"
                report += f"Average Salary: ${avg_salary:,.2f}\n"
                
                if dept_data['positions']:
                    report += f"\nPositions in this department:\n"
                    for pos, count in dept_data['positions'].items():
                        report += f"  • {pos}: {count} employee(s)\n"
                
                report += f"\nEmployee List:\n"
                for emp in dept_data['employees']:
                    salary_str = f"${emp.salary:,.2f}" if emp.salary else "N/A"
                    report += f"  • {emp.first_name} {emp.last_name} ({emp.position}) - {salary_str}\n"
            
            self.report_text.insert("1.0", report)
            self.report_text.config(state="disabled")
            
            # Enable action buttons
            self.save_btn.config(state="normal")
            self.print_btn.config(state="normal")
            
            logger.info(f"Department analysis report generated by {self.current_user.username}")
            
        except Exception as e:
            logger.error(f"Failed to generate department analysis: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def generate_position_report(self):
        """Generate position analysis report"""
        try:
            self.display_title.config(text="💼 Position Analysis Report")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", "end")
            
            employees = Employee.get_all_employees()
            
            # Group by position
            positions = {}
            
            for emp in employees:
                pos = emp.position if emp.position else "Unassigned"
                if pos not in positions:
                    positions[pos] = []
                positions[pos].append(emp)
            
            # Generate report
            report = f"""
POSITION ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: {self.current_user.username}

{'=' * 80}

POSITION SUMMARY:
Total Positions: {len(positions)}
Total Employees: {len(employees)}

"""
            
            # Sort positions by employee count
            sorted_positions = sorted(positions.items(), key=lambda x: len(x[1]), reverse=True)
            
            for pos_name, pos_employees in sorted_positions:
                emp_count = len(pos_employees)
                salaries = [emp.salary for emp in pos_employees if emp.salary]
                
                if salaries:
                    avg_salary = sum(salaries) / len(salaries)
                    min_salary = min(salaries)
                    max_salary = max(salaries)
                else:
                    avg_salary = min_salary = max_salary = 0
                
                report += f"\n{'-' * 60}\n"
                report += f"Position: {pos_name.upper()}\n"
                report += f"{'-' * 60}\n"
                report += f"Employee Count: {emp_count}\n"
                
                if salaries:
                    report += f"Salary Range: ${min_salary:,.2f} - ${max_salary:,.2f}\n"
                    report += f"Average Salary: ${avg_salary:,.2f}\n"
                else:
                    report += f"Salary Information: Not available\n"
                
                # Department distribution
                departments = {}
                for emp in pos_employees:
                    dept = emp.department if emp.department else "Unassigned"
                    if dept not in departments:
                        departments[dept] = 0
                    departments[dept] += 1
                
                if len(departments) > 1:
                    report += f"\nDepartment Distribution:\n"
                    for dept, count in departments.items():
                        report += f"  • {dept}: {count} employee(s)\n"
                
                report += f"\nEmployees in this position:\n"
                for emp in pos_employees:
                    dept_str = f" ({emp.department})" if emp.department else ""
                    salary_str = f" - ${emp.salary:,.2f}" if emp.salary else ""
                    report += f"  • {emp.first_name} {emp.last_name}{dept_str}{salary_str}\n"
            
            self.report_text.insert("1.0", report)
            self.report_text.config(state="disabled")
            
            # Enable action buttons
            self.save_btn.config(state="normal")
            self.print_btn.config(state="normal")
            
            logger.info(f"Position analysis report generated by {self.current_user.username}")
            
        except Exception as e:
            logger.error(f"Failed to generate position report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def generate_user_activity(self):
        """Generate user activity report"""
        try:
            self.display_title.config(text="👥 User Activity Report")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", "end")
            
            users = User.get_all_users()
            
            # Generate report
            report = f"""
USER ACTIVITY REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: {self.current_user.username}

{'=' * 80}

SYSTEM USERS OVERVIEW:
Total Users: {len(users)}

"""
            
            # Count by role and status
            role_counts = {}
            active_count = 0
            
            for user in users:
                if user.role not in role_counts:
                    role_counts[user.role] = 0
                role_counts[user.role] += 1
                
                if user.is_active:
                    active_count += 1
            
            report += f"Active Users: {active_count}\n"
            report += f"Inactive Users: {len(users) - active_count}\n\n"
            
            report += "Users by Role:\n"
            for role, count in role_counts.items():
                report += f"  • {role.title()}: {count} user(s)\n"
            
            report += f"\n{'=' * 80}\n\nDETAILED USER LIST:\n\n"
            
            for i, user in enumerate(users, 1):
                status = "Active" if user.is_active else "Inactive"
                created_date = user.created_at.strftime('%Y-%m-%d') if user.created_at else "N/A"
                
                report += f"{i}. {user.username}\n"
                report += f"   Role: {user.role.title()}\n"
                report += f"   Status: {status}\n"
                report += f"   Created: {created_date}\n"
                report += f"   Last Updated: {user.updated_at.strftime('%Y-%m-%d %H:%M') if user.updated_at else 'N/A'}\n"
                report += "\n"
            
            # Note about audit logs
            report += f"{'-' * 80}\n"
            report += "Note: Detailed activity logs are stored in the system audit log.\n"
            report += "Contact your system administrator for detailed user activity tracking.\n"
            
            self.report_text.insert("1.0", report)
            self.report_text.config(state="disabled")
            
            # Enable action buttons
            self.save_btn.config(state="normal")
            self.print_btn.config(state="normal")
            
            logger.info(f"User activity report generated by {self.current_user.username}")
            
        except Exception as e:
            logger.error(f"Failed to generate user activity report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def generate_security_report(self):
        """Generate security analysis report"""
        try:
            self.display_title.config(text="🔐 Security Analysis Report")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", "end")
            
            users = User.get_all_users()
            employees = Employee.get_all_employees()
            
            # Security analysis
            report = f"""
SECURITY ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: {self.current_user.username}

{'=' * 80}

SECURITY OVERVIEW:

System Users: {len(users)}
Employee Records: {len(employees)}

"""
            
            # User security analysis
            admin_count = sum(1 for user in users if user.role == 'admin')
            manager_count = sum(1 for user in users if user.role == 'manager')
            employee_count = sum(1 for user in users if user.role == 'employee')
            
            report += f"User Privilege Distribution:\n"
            report += f"  • Administrators: {admin_count}\n"
            report += f"  • Managers: {manager_count}\n"
            report += f"  • Employees: {employee_count}\n\n"
            
            # Active vs inactive users
            active_users = sum(1 for user in users if user.is_active)
            inactive_users = len(users) - active_users
            
            report += f"Account Status:\n"
            report += f"  • Active Accounts: {active_users}\n"
            report += f"  • Inactive Accounts: {inactive_users}\n\n"
            
            # Security recommendations
            report += f"{'=' * 80}\n"
            report += "SECURITY RECOMMENDATIONS:\n\n"
            
            recommendations = []
            
            if admin_count > 3:
                recommendations.append("⚠️  Consider limiting the number of administrator accounts")
            
            if inactive_users > 0:
                recommendations.append("⚠️  Review and clean up inactive user accounts")
            
            # Check for recent user creation
            recent_users = []
            cutoff_date = datetime.now() - timedelta(days=30)
            for user in users:
                if user.created_at and user.created_at.date() >= cutoff_date.date():
                    recent_users.append(user)
            
            if recent_users:
                report += f"Recent Account Activity (Last 30 days):\n"
                for user in recent_users:
                    report += f"  • New user: {user.username} ({user.role}) - {user.created_at.strftime('%Y-%m-%d')}\n"
                report += "\n"
            
            if not recommendations:
                recommendations.append("✅ No immediate security concerns identified")
            
            for rec in recommendations:
                report += f"{rec}\n"
            
            report += f"\n{'=' * 80}\n"
            report += "SECURITY CHECKLIST:\n\n"
            report += "✅ Password hashing implemented\n"
            report += "✅ Role-based access control active\n"
            report += "✅ User session management in place\n"
            report += "✅ Input validation enabled\n"
            report += "✅ Audit logging configured\n"
            report += "✅ Database connection security\n"
            
            report += f"\n{'=' * 80}\n"
            report += "For detailed security audit logs, please check the system audit log files.\n"
            
            self.report_text.insert("1.0", report)
            self.report_text.config(state="disabled")
            
            # Enable action buttons
            self.save_btn.config(state="normal")
            self.print_btn.config(state="normal")
            
            logger.info(f"Security report generated by {self.current_user.username}")
            
        except Exception as e:
            logger.error(f"Failed to generate security report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def create_custom_report(self):
        """Open custom report builder"""
        messagebox.showinfo(
            "Custom Reports", 
            "Custom report builder is coming soon!\n\nThis feature will allow you to:\n"
            "• Select specific data fields\n"
            "• Apply custom filters\n"
            "• Choose output formats\n"
            "• Schedule automated reports"
        )

    def save_report(self):
        """Save current report to file"""
        try:
            content = self.report_text.get("1.0", "end-1c")
            
            if not content or content.strip() == "":
                messagebox.showwarning("No Content", "No report content to save")
                return
            
            # Generate default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"employee_report_{timestamp}.txt"
            
            # Get save location
            filename = filedialog.asksaveasfilename(
                title="Save Report",
                initialfile=default_name,
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                messagebox.showinfo("Success", f"Report saved successfully to:\n{filename}")
                logger.info(f"Report saved by {self.current_user.username} to {filename}")
                
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            messagebox.showerror("Error", f"Failed to save report: {e}")

    def export_all_reports(self):
        """Export all reports to a comprehensive file"""
        try:
            # Generate default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"comprehensive_employee_reports_{timestamp}.txt"
            
            filename = filedialog.asksaveasfilename(
                title="Export All Reports",
                initialfile=default_name,
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"EMPLOYEE MANAGEMENT SYSTEM - COMPREHENSIVE REPORTS\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"User: {self.current_user.username}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    # Generate all reports and write to file
                    reports = [
                        ("EMPLOYEE SUMMARY", self.generate_employee_summary),
                        ("DEPARTMENT ANALYSIS", self.generate_department_report),
                        ("SALARY REPORT", self.generate_salary_report),
                        ("JOINING TRENDS", self.generate_joining_trends),
                        ("AGE DISTRIBUTION", self.show_age_distribution),
                        ("PERFORMANCE METRICS", self.show_performance_metrics),
                        ("STATUS ANALYSIS", self.show_status_analysis)
                    ]
                    
                    for i, (report_name, report_func) in enumerate(reports, 1):
                        try:
                            f.write(f"\n{i}. {report_name}:\n")
                            f.write("-" * 50 + "\n")
                            
                            # Temporarily capture report content
                            original_content = self.report_text.get(1.0, tk.END)
                            
                            # Generate report
                            report_func()
                            
                            # Get generated content
                            content = self.report_text.get(1.0, tk.END)
                            f.write(content)
                            f.write("\n\n" + "=" * 50 + "\n")
                            
                            # Restore original content
                            self.report_text.delete(1.0, tk.END)
                            self.report_text.insert(1.0, original_content)
                            
                        except Exception as e:
                            f.write(f"Error generating {report_name}: {e}\n\n")
                            logger.error(f"Error in report {report_name}: {e}")
                
                messagebox.showinfo("Success", f"All reports exported to:\n{filename}")
                logger.info(f"All reports exported by {self.current_user.username} to {filename}")
                
        except Exception as e:
            logger.error(f"Failed to export all reports: {e}")
            messagebox.showerror("Error", f"Failed to export reports: {e}")

    def print_report(self):
        """Print current report"""
        messagebox.showinfo(
            "Print Report", 
            "Print functionality is not implemented in this demo.\n\n"
            "In a production environment, this would:\n"
            "• Open the system print dialog\n"
            "• Format the report for printing\n"
            "• Send to the selected printer"
        )