import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.employee import Employee
from utils.helpers import UIHelper
from utils.logger import app_logger
import logging
from datetime import datetime
import os
import json
import csv

logger = logging.getLogger(__name__)

# Optional imports - will work without these if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class ExportWindow(tk.Toplevel):
    """Advanced Export and Reporting Window"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        
        self.title("Data Export & Reports")
        self.configure(bg="#f0f4f8")
        self.geometry("800x600")
        UIHelper.center_window(self, 800, 600)
        
        self.create_widgets()
        
        logger.info(f"Export window opened by {current_user.username}")

    def create_widgets(self):
        """Create export interface"""
        
        # Header
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📊 Data Export & Reports",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        close_btn = tk.Button(
            header_frame,
            text="✖ Close",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.destroy,
            cursor="hand2",
            padx=15,
            pady=5
        )
        close_btn.pack(side="right", padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(self, bg="#f0f4f8")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Export options
        self.create_export_options(main_frame)
        
        # Reports section
        self.create_reports_section(main_frame)

    def create_export_options(self, parent):
        """Create export options section"""
        
        export_frame = tk.LabelFrame(
            parent,
            text="📤 Export Employee Data",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            padx=20,
            pady=15
        )
        export_frame.pack(fill="x", pady=(0, 20))
        
        # Export format selection
        format_frame = tk.Frame(export_frame, bg="#ffffff")
        format_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            format_frame,
            text="Select Export Format:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        self.export_format = tk.StringVar(value="excel")
        
        formats = [
            ("📊 Excel (.xlsx)", "excel"),
            ("📄 PDF Report", "pdf"),
            ("📋 CSV File", "csv"),
            ("💾 JSON Data", "json")
        ]
        
        for text, value in formats:
            tk.Radiobutton(
                format_frame,
                text=text,
                variable=self.export_format,
                value=value,
                font=("Arial", 10),
                bg="#ffffff",
                fg="#34495e"
            ).pack(anchor="w", pady=2)
        
        # Filter options
        filter_frame = tk.Frame(export_frame, bg="#ffffff")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            filter_frame,
            text="Filter Options:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        # Department filter
        dept_frame = tk.Frame(filter_frame, bg="#ffffff")
        dept_frame.pack(fill="x", pady=5)
        
        tk.Label(
            dept_frame,
            text="Department:",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#2c3e50",
            width=12
        ).pack(side="left")
        
        self.dept_filter = ttk.Combobox(
            dept_frame,
            values=["All Departments"] + self.get_departments(),
            font=("Arial", 10),
            width=20,
            state="readonly"
        )
        self.dept_filter.set("All Departments")
        self.dept_filter.pack(side="left", padx=(10, 0))
        
        # Status filter
        status_frame = tk.Frame(filter_frame, bg="#ffffff")
        status_frame.pack(fill="x", pady=5)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#2c3e50",
            width=12
        ).pack(side="left")
        
        self.status_filter = ttk.Combobox(
            status_frame,
            values=["All Statuses", "Active", "Inactive", "Terminated"],
            font=("Arial", 10),
            width=20,
            state="readonly"
        )
        self.status_filter.set("All Statuses")
        self.status_filter.pack(side="left", padx=(10, 0))
        
        # Export button
        export_btn = tk.Button(
            export_frame,
            text="📥 Export Data",
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.export_data,
            cursor="hand2",
            padx=30,
            pady=10
        )
        export_btn.pack(pady=10)

    def create_reports_section(self, parent):
        """Create reports section"""
        
        reports_frame = tk.LabelFrame(
            parent,
            text="📈 Generate Reports",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            padx=20,
            pady=15
        )
        reports_frame.pack(expand=True, fill="both")
        
        # Report buttons
        button_frame = tk.Frame(reports_frame, bg="#ffffff")
        button_frame.pack(expand=True, fill="both", pady=20)
        
        reports = [
            ("👥 Employee Summary Report", self.generate_summary_report, "#3498db"),
            ("💰 Salary Analysis Report", self.generate_salary_report, "#9b59b6"),
            ("🏢 Department Statistics", self.generate_department_report, "#e67e22"),
            ("📊 Employee Analytics", self.generate_analytics_report, "#1abc9c")
        ]
        
        for i, (text, command, color) in enumerate(reports):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                button_frame,
                text=text,
                bg=color,
                fg="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                command=command,
                cursor="hand2",
                width=25,
                pady=15
            )
            btn.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def get_departments(self):
        """Get list of unique departments"""
        try:
            employees = Employee.get_all_employees()
            departments = list(set([emp.department for emp in employees if emp.department]))
            return sorted(departments)
        except:
            return []

    def export_data(self):
        """Export employee data in selected format"""
        try:
            # Get filtered employees
            employees = self.get_filtered_employees()
            
            if not employees:
                messagebox.showwarning("No Data", "No employees match the selected filters")
                return
            
            format_type = self.export_format.get()
            
            # Ask for save location
            file_types = {
                "excel": [("Excel files", "*.xlsx")],
                "pdf": [("PDF files", "*.pdf")],
                "csv": [("CSV files", "*.csv")],
                "json": [("JSON files", "*.json")]
            }
            
            extensions = {
                "excel": ".xlsx",
                "pdf": ".pdf", 
                "csv": ".csv",
                "json": ".json"
            }
            
            # Generate default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"employee_data_{timestamp}{extensions[format_type]}"
            
            filename = filedialog.asksaveasfilename(
                title="Save Export File",
                initialfile=default_name,
                filetypes=file_types[format_type],
                defaultextension=extensions[format_type]
            )
            
            if not filename:
                return
            
            # Export based on format
            if format_type == "excel":
                self.export_to_excel(employees, filename)
            elif format_type == "pdf":
                self.export_to_pdf(employees, filename)
            elif format_type == "csv":
                self.export_to_csv(employees, filename)
            elif format_type == "json":
                self.export_to_json(employees, filename)
            
            messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
            app_logger.log_user_action(self.current_user.id, "EXPORT_DATA", f"Format: {format_type}, File: {filename}")
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def get_filtered_employees(self):
        """Get employees based on selected filters"""
        employees = Employee.get_all_employees(active_only=False)
        
        # Apply department filter
        dept = self.dept_filter.get()
        if dept != "All Departments":
            employees = [emp for emp in employees if emp.department == dept]
        
        # Apply status filter
        status = self.status_filter.get()
        if status != "All Statuses":
            employees = [emp for emp in employees if emp.status == status]
        
        return employees

    def export_to_excel(self, employees, filename):
        """Export to Excel format"""
        try:
            if not PANDAS_AVAILABLE:
                # Fallback to CSV if pandas not available
                csv_filename = filename.replace('.xlsx', '.csv')
                messagebox.showinfo("Excel Export", f"Excel export requires pandas library.\nExporting to CSV instead: {os.path.basename(csv_filename)}")
                return self.export_to_csv_simple(employees, csv_filename)
            
            data = []
            for emp in employees:
                data.append({
                    'Employee Code': emp.employee_code or '',
                    'Name': emp.name,
                    'Age': emp.age or '',
                    'Department': emp.department or '',
                    'Designation': emp.designation or '',
                    'Salary': emp.salary or '',
                    'Email': emp.email or '',
                    'Phone': emp.phone_number or '',
                    'Gender': emp.gender or '',
                    'Date of Birth': self.format_date(emp.date_of_birth),
                    'Joining Date': self.format_date(emp.joining_date),
                    'Status': emp.status,
                    'Address': emp.address or ''
                })
            
            df = pd.DataFrame(data)
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Employees', index=False)
                
                # Add summary sheet
                summary_data = self.get_summary_statistics(employees)
                summary_df = pd.DataFrame(list(summary_data.items()), columns=['Metric', 'Value'])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            # Fallback to CSV
            csv_filename = filename.replace('.xlsx', '.csv')
            messagebox.showwarning("Excel Export Failed", f"Excel export failed: {e}\nExporting to CSV instead: {os.path.basename(csv_filename)}")
            return self.export_to_csv_simple(employees, csv_filename)

    def export_to_csv(self, employees, filename):
        """Export to CSV format"""
        if PANDAS_AVAILABLE:
            data = []
            for emp in employees:
                data.append({
                    'Employee Code': emp.employee_code or '',
                    'Name': emp.name,
                    'Age': emp.age or '',
                    'Department': emp.department or '',
                    'Designation': emp.designation or '',
                    'Salary': emp.salary or '',
                    'Email': emp.email or '',
                    'Phone': emp.phone_number or '',
                    'Gender': emp.gender or '',
                    'Date of Birth': self.format_date(emp.date_of_birth),
                    'Joining Date': self.format_date(emp.joining_date),
                    'Status': emp.status,
                    'Address': emp.address or ''
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
        else:
            # Use built-in CSV writer
            self.export_to_csv_simple(employees, filename)

    def export_to_json(self, employees, filename):
        """Export to JSON format"""
        try:
            employees_data = []
            for emp in employees:
                emp_dict = {
                    'id': emp.id,
                    'employee_code': emp.employee_code,
                    'name': emp.name,
                    'age': emp.age,
                    'department': emp.department,
                    'designation': emp.designation,
                    'salary': float(emp.salary) if emp.salary else None,
                    'email': emp.email,
                    'phone_number': emp.phone_number,
                    'address': emp.address,
                    'gender': emp.gender,
                    'date_of_birth': self.format_date(emp.date_of_birth),
                    'joining_date': self.format_date(emp.joining_date),
                    'status': emp.status,
                    'created_at': self.format_date(emp.created_at),
                    'updated_at': self.format_date(emp.updated_at)
                }
                employees_data.append(emp_dict)
            
            data = {
                'export_date': datetime.now().isoformat(),
                'exported_by': self.current_user.username,
                'total_employees': len(employees),
                'employees': employees_data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            raise Exception(f"Failed to export JSON: {e}")

    def export_to_pdf(self, employees, filename):
        """Export to PDF format"""
        try:
            if not REPORTLAB_AVAILABLE:
                # Fallback to text file if reportlab not available
                txt_filename = filename.replace('.pdf', '.txt')
                messagebox.showinfo("PDF Export", f"PDF export requires reportlab library.\nExporting to text file instead: {os.path.basename(txt_filename)}")
                return self.export_to_text(employees, txt_filename)
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Continue with PDF creation...
            story = []
            
            # Add title
            title = Paragraph("Employee Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Add generation info
            info_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>Generated by: {self.current_user.username}<br/>Total Employees: {len(employees)}"
            info = Paragraph(info_text, styles['Normal'])
            story.append(info)
            story.append(Spacer(1, 12))
            
            # Create table data
            table_data = [['Name', 'Department', 'Designation', 'Email', 'Phone', 'Status']]
            
            for emp in employees:
                table_data.append([
                    emp.name,
                    emp.department or 'N/A',
                    emp.designation or 'N/A', 
                    emp.email or 'N/A',
                    emp.phone_number or 'N/A',
                    emp.status
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            # Fallback to text file
            txt_filename = filename.replace('.pdf', '.txt')
            messagebox.showwarning("PDF Export Failed", f"PDF export failed: {e}\nExporting to text file instead: {os.path.basename(txt_filename)}")
            return self.export_to_text(employees, txt_filename)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        story.append(Paragraph("Employee Report", title_style))
        story.append(Spacer(1, 12))
        
        # Summary info
        info_style = styles['Normal']
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Paragraph(f"Generated by: {self.current_user.username}", info_style))
        story.append(Paragraph(f"Total Employees: {len(employees)}", info_style))
        story.append(Spacer(1, 20))
        
        # Employee table
        data = [['Code', 'Name', 'Department', 'Designation', 'Salary', 'Status']]
        
        for emp in employees:
            data.append([
                emp.employee_code or 'N/A',
                emp.name,
                emp.department or 'N/A',
                emp.designation or 'N/A',
                UIHelper.format_currency(emp.salary) if emp.salary else 'N/A',
                emp.status
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        doc.build(story)

    def get_summary_statistics(self, employees):
        """Get summary statistics for employees"""
        total = len(employees)
        active = len([emp for emp in employees if emp.status == 'Active'])
        male = len([emp for emp in employees if emp.gender == 'Male'])
        female = len([emp for emp in employees if emp.gender == 'Female'])
        
        salaries = [emp.salary for emp in employees if emp.salary]
        avg_salary = sum(salaries) / len(salaries) if salaries else 0
        
        departments = len(set([emp.department for emp in employees if emp.department]))
        
        return {
            'Total Employees': total,
            'Active Employees': active,
            'Male Employees': male,
            'Female Employees': female,
            'Average Salary': f"${avg_salary:,.2f}",
            'Total Departments': departments
        }

    def generate_summary_report(self):
        """Generate employee summary report"""
        messagebox.showinfo("Report", "Employee Summary Report\n\nThis feature generates a comprehensive summary of all employees with statistics and charts.")

    def generate_salary_report(self):
        """Generate salary analysis report"""
        messagebox.showinfo("Report", "Salary Analysis Report\n\nThis feature analyzes salary distribution across departments and roles.")

    def generate_department_report(self):
        """Generate department statistics report"""
        messagebox.showinfo("Report", "Department Statistics Report\n\nThis feature provides detailed statistics for each department.")

    def generate_analytics_report(self):
        """Generate employee analytics report"""
        messagebox.showinfo("Report", "Employee Analytics Report\n\nThis feature provides advanced analytics and insights about employee data.")

    def format_date(self, date_obj):
        """Format date for display"""
        if date_obj:
            return date_obj.strftime('%Y-%m-%d') if hasattr(date_obj, 'strftime') else str(date_obj)
        return ''

    def export_to_csv_simple(self, employees, filename):
        """Simple CSV export using built-in csv module"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Employee Code', 'Name', 'Age', 'Department', 'Designation', 'Salary', 
                             'Email', 'Phone', 'Gender', 'Date of Birth', 'Joining Date', 'Status', 'Address']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for emp in employees:
                    writer.writerow({
                        'Employee Code': emp.employee_code or '',
                        'Name': emp.name,
                        'Age': emp.age or '',
                        'Department': emp.department or '',
                        'Designation': emp.designation or '',
                        'Salary': emp.salary or '',
                        'Email': emp.email or '',
                        'Phone': emp.phone_number or '',
                        'Gender': emp.gender or '',
                        'Date of Birth': self.format_date(emp.date_of_birth),
                        'Joining Date': self.format_date(emp.joining_date),
                        'Status': emp.status,
                        'Address': emp.address or ''
                    })
        except Exception as e:
            raise Exception(f"Failed to write CSV file: {e}")

    def export_to_text(self, employees, filename):
        """Simple text export"""
        try:
            with open(filename, 'w', encoding='utf-8') as txtfile:
                txtfile.write("EMPLOYEE REPORT\n")
                txtfile.write("=" * 80 + "\n")
                txtfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                txtfile.write(f"Generated by: {self.current_user.username}\n")
                txtfile.write(f"Total Employees: {len(employees)}\n\n")
                
                for i, emp in enumerate(employees, 1):
                    txtfile.write(f"{i}. {emp.name}\n")
                    txtfile.write(f"   Employee Code: {emp.employee_code or 'N/A'}\n")
                    txtfile.write(f"   Department: {emp.department or 'N/A'}\n")
                    txtfile.write(f"   Designation: {emp.designation or 'N/A'}\n")
                    txtfile.write(f"   Email: {emp.email or 'N/A'}\n")
                    txtfile.write(f"   Phone: {emp.phone_number or 'N/A'}\n")
                    txtfile.write(f"   Status: {emp.status}\n")
                    txtfile.write("\n")
        except Exception as e:
            raise Exception(f"Failed to write text file: {e}")