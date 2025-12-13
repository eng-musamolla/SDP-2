import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.employee import Employee
from models.user import User
from utils.validators import EmployeeValidator, ValidationError
from utils.helpers import UIHelper, DateHelper
from utils.logger import app_logger
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmployeeManagerWindow(tk.Toplevel):
    """Complete Employee Management Window with full CRUD operations"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_employee = None
        
        self.title("Employee Management")
        self.configure(bg="#f0f4f8")
        
        # Set fixed window size
        window_width = 1200
        window_height = 700
        
        self.geometry(f"{window_width}x{window_height}")
        UIHelper.center_window(self, window_width, window_height)
        
        # Make window non-resizable
        self.resizable(False, False)
        
        self.create_widgets()
        self.load_employees()
        self.show_form_placeholder()
        
        logger.info(f"Employee management opened by {current_user.username}")

    def create_widgets(self):
        """Create the complete employee management interface"""
        
        # Header
        header_frame = tk.Frame(self, bg="#34495e", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Employee Management System",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        close_btn = tk.Button(
            header_frame,
            text="← Back to Dashboard",
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
        
        # Main container
        main_container = tk.Frame(self, bg="#f0f4f8")
        main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel - Employee form (fixed width)
        left_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1, width=500)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_employee_form(left_panel)
        
        # Right panel - Employee list and actions (fixed width)
        right_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.create_employee_list(right_panel)

    def create_employee_form(self, parent):
        """Create employee input form"""
        
        # Form title
        form_title = tk.Label(
            parent,
            text="Employee Information",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        form_title.pack(pady=20)
        
        # Scrollable form frame
        canvas = tk.Canvas(parent, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        self.form_vars = {}
        fields = [
            ("Employee Code", "employee_code", "readonly"),
            ("Full Name *", "name", "entry"),
            ("Age", "age", "entry"),
            ("Department *", "department", "entry"), 
            ("Designation *", "designation", "entry"),
            ("Salary", "salary", "entry"),
            ("Email", "email", "entry"),
            ("Phone Number", "phone", "entry"),
            ("Address", "address", "text"),
            ("Gender", "gender", "combo"),
            ("Date of Birth", "dob", "entry"),
            ("Joining Date", "joining_date", "entry")
        ]
        
        for i, (label, key, field_type) in enumerate(fields):
            # Label
            tk.Label(
                scrollable_frame,
                text=label,
                font=("Arial", 10, "bold"),
                bg="#ffffff",
                fg="#2c3e50"
            ).grid(row=i, column=0, sticky="w", padx=20, pady=(10, 2))
            
            # Input field
            if field_type == "entry":
                var = tk.StringVar()
                entry = tk.Entry(
                    scrollable_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    relief="solid",
                    bd=1
                )
                entry.grid(row=i, column=1, padx=20, pady=(2, 10), sticky="ew")
                self.form_vars[key] = var
                
                # Add focus events to clear placeholder text
                entry.bind("<FocusIn>", lambda event, k=key: self.on_entry_focus_in(event, k))
                entry.bind("<FocusOut>", lambda event, k=key: self.on_entry_focus_out(event, k))
                
            elif field_type == "readonly":
                var = tk.StringVar()
                entry = tk.Entry(
                    scrollable_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    relief="solid",
                    bd=1,
                    state="readonly",
                    bg="#f8f9fa"
                )
                entry.grid(row=i, column=1, padx=20, pady=(2, 10), sticky="ew")
                self.form_vars[key] = var
                
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(
                    scrollable_frame,
                    textvariable=var,
                    values=["Male", "Female", "Other"],
                    font=("Arial", 10),
                    state="readonly"
                )
                combo.grid(row=i, column=1, padx=20, pady=(2, 10), sticky="ew")
                self.form_vars[key] = var
                
                # Add focus event for combobox
                def on_combo_focus(event, field_key=key):
                    if self.selected_employee is None:
                        pass  # Combobox handles its own placeholder via selection
                
                combo.bind("<<ComboboxSelected>>", on_combo_focus)
                
            elif field_type == "text":
                text_widget = tk.Text(
                    scrollable_frame,
                    font=("Arial", 10),
                    relief="solid",
                    bd=1,
                    height=3,
                    wrap="word"
                )
                text_widget.grid(row=i, column=1, padx=20, pady=(2, 10), sticky="ew")
                self.form_vars[key] = text_widget  # Store widget, not StringVar
                
                # Add focus events for text widget
                text_widget.bind("<FocusIn>", lambda event, w=text_widget: self.on_text_focus_in(event, w))
                text_widget.bind("<FocusOut>", lambda event, w=text_widget: self.on_text_focus_out(event, w))
        
        # Action buttons - fixed layout
        button_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=30, sticky="ew")
        
        # Create buttons in a row layout with proper spacing
        button_row = tk.Frame(button_frame, bg="#ffffff")
        button_row.pack(anchor="w", pady=10)
        
        # Clear button - always visible and placed first for better UX
        clear_btn = tk.Button(
            button_row,
            text="🗑️ Clear Form",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat",
            command=self.clear_form,
            cursor="hand2",
            padx=15,
            pady=5,
            width=14,
            activebackground="#c0392b"
        )
        clear_btn.pack(side="left", padx=8)
        
        if self.current_user.has_permission('create'):
            save_btn = tk.Button(
                button_row,
                text="💾 Save Employee",
                bg="#27ae60",
                fg="white",
                font=("Arial", 8, "bold"),
                relief="flat",
                command=self.save_employee,
                cursor="hand2",
                padx=15,
                pady=5,
                width=14,
                activebackground="#229954"
            )
            save_btn.pack(side="left", padx=8)
        
        if self.current_user.has_permission('update'):
            update_btn = tk.Button(
                button_row,
                text="✏️ Update Employee",
                bg="#3498db",
                fg="white",
                font=("Arial", 8, "bold"),
                relief="flat",
                command=self.update_employee,
                cursor="hand2",
                padx=15,
                pady=5,
                width=14,
                activebackground="#2980b9"
            )
            update_btn.pack(side="left", padx=8)
        
        # Make canvas responsive
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Configure fixed scrolling
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        scrollable_frame.bind('<Configure>', configure_scroll_region)

    def create_employee_list(self, parent):
        """Create employee list with search and actions"""
        
        # List header with quick actions
        list_header = tk.Frame(parent, bg="#ffffff")
        list_header.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            list_header,
            text="Employee Directory",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(side="left")
        
        # Quick Actions
        quick_actions = tk.Frame(list_header, bg="#ffffff")
        quick_actions.pack(side="right")
        
        if self.current_user.has_permission('delete'):
            delete_btn = tk.Button(
                quick_actions,
                text="🗑️ Delete",
                bg="#e74c3c",
                fg="white",
                font=("Arial", 9, "bold"),
                relief="flat",
                command=self.delete_employee,
                cursor="hand2",
                padx=10,
                pady=4
            )
            delete_btn.pack(side="right", padx=5)
        
        export_btn = tk.Button(
            quick_actions,
            text="📄 Export",
            bg="#f39c12",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.open_export_window,
            cursor="hand2",
            padx=10,
            pady=4
        )
        export_btn.pack(side="right", padx=5)
        
        reports_btn = tk.Button(
            quick_actions,
            text="📊 Reports",
            bg="#9b59b6",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.open_reports_window,
            cursor="hand2",
            padx=10,
            pady=4
        )
        reports_btn.pack(side="right", padx=5)
        
        refresh_btn = tk.Button(
            quick_actions,
            text="🔄 Refresh",
            bg="#1abc9c",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.load_employees,
            cursor="hand2",
            padx=10,
            pady=4
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Search frame
        search_frame = tk.Frame(parent, bg="#ffffff")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(side="left")
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        search_entry.pack(side="left", padx=(10, 20), fill="x", expand=True)
        search_entry.bind("<KeyRelease>", self.search_employees)
        
        # Action buttons for selected employee
        action_frame = tk.Frame(search_frame, bg="#ffffff")
        action_frame.pack(side="right")
        
        if self.current_user.has_permission('delete'):
            delete_btn = tk.Button(
                action_frame,
                text="❌ Delete Selected",
                bg="#e74c3c",
                fg="white",
                font=("Arial", 9, "bold"),
                relief="flat",
                command=self.delete_employee,
                cursor="hand2",
                padx=10,
                pady=5
            )
            delete_btn.pack(side="right", padx=5)
        
        view_btn = tk.Button(
            action_frame,
            text="👁️ View Details",
            bg="#9b59b6",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.view_employee_details,
            cursor="hand2",
            padx=10,
            pady=5
        )
        view_btn.pack(side="right", padx=5)
        
        # Employee treeview
        tree_frame = tk.Frame(parent, bg="#ffffff")
        tree_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 9))
        style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"))
        
        columns = ("ID", "Code", "Name", "Department", "Designation", "Salary", "Email", "Phone", "Status")
        self.employee_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            height=15
        )
        
        # Configure fixed column widths
        column_widths = {
            "ID": 50,
            "Code": 80,
            "Name": 120,
            "Department": 100,
            "Designation": 120,
            "Salary": 100,
            "Email": 150,
            "Phone": 100,
            "Status": 70
        }
        
        for col in columns:
            self.employee_tree.heading(col, text=col)
            self.employee_tree.column(
                col, 
                width=column_widths[col], 
                minwidth=column_widths[col],
                anchor="w" if col in ["Name", "Email", "Department", "Designation"] else "center",
                stretch=False
            )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.employee_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.employee_tree.xview)
        self.employee_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.employee_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.employee_tree.bind("<<TreeviewSelect>>", self.on_employee_select)

    def load_employees(self):
        """Load all employees into the treeview"""
        try:
            # Clear existing items
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            
            # Load employees from database
            employees = Employee.get_all_employees(active_only=False)
            
            if not employees:
                logger.warning("No employees found in database")
                return
            
            for emp in employees:
                try:
                    salary_display = f"${emp.salary:,.2f}" if emp.salary else "N/A"
                    self.employee_tree.insert("", "end", values=(
                        emp.id,
                        emp.employee_code or "N/A",
                        emp.name,
                        emp.department or "N/A",
                        emp.designation or "N/A",
                        salary_display,
                        emp.email or "N/A",
                        emp.phone_number or "N/A",
                        emp.status
                    ))
                except Exception as row_error:
                    logger.error(f"Error adding employee {emp.name}: {row_error}")
                    continue
            
            logger.info(f"Loaded {len(employees)} employees")
            
        except Exception as e:
            logger.error(f"Failed to load employees: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load employees from database: {e}")

    def search_employees(self, event=None):
        """Search employees based on search term"""
        search_term = self.search_var.get().strip()
        
        try:
            if search_term:
                employees = Employee.search_employees(search_term)
            else:
                employees = Employee.get_all_employees(active_only=False)
            
            # Clear and repopulate treeview
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            
            for emp in employees:
                try:
                    salary_display = f"${emp.salary:,.2f}" if emp.salary else "N/A"
                    self.employee_tree.insert("", "end", values=(
                        emp.id,
                        emp.employee_code or "N/A",
                        emp.name,
                        emp.department or "N/A", 
                        emp.designation or "N/A",
                        salary_display,
                        emp.email or "N/A",
                        emp.phone_number or "N/A",
                        emp.status
                    ))
                except Exception as row_error:
                    logger.error(f"Error adding employee {emp.name} to search results: {row_error}")
                    continue
            
        except Exception as e:
            logger.error(f"Search failed: {e}")

    def on_employee_select(self, event):
        """Handle employee selection"""
        try:
            selection = self.employee_tree.selection()
            if not selection:
                return
                
            item = self.employee_tree.item(selection[0])
            values = item['values']
            
            # Check if we have valid data
            if not values or len(values) == 0:
                return
                
            employee_id = values[0]
                
            # Load employee details
            self.selected_employee = Employee.get_by_id(employee_id)
            if self.selected_employee:
                self.populate_form(self.selected_employee)
                logger.info(f"Selected employee: {self.selected_employee.name}")
            else:
                messagebox.showwarning("Warning", "Could not load employee details")
                
        except Exception as e:
            logger.error(f"Failed to load employee details: {e}")
            messagebox.showerror("Error", f"Failed to load employee: {str(e)}")

    def populate_form(self, employee):
        """Populate form with employee data"""
        try:
            # Generate employee code if not exists
            employee_code = employee.employee_code or f"EMP{str(employee.id).zfill(3)}"
            
            self.form_vars["employee_code"].set(employee_code)
            self.form_vars["name"].set(employee.name or "")
            self.form_vars["age"].set(str(employee.age) if employee.age else "")
            self.form_vars["department"].set(employee.department or "")
            self.form_vars["designation"].set(employee.designation or "")
            self.form_vars["salary"].set(str(employee.salary) if employee.salary else "")
            self.form_vars["email"].set(employee.email or "")
            self.form_vars["phone"].set(employee.phone_number or "")
            self.form_vars["gender"].set(employee.gender or "")
            
            # Handle dates safely
            dob_display = ""
            if employee.date_of_birth:
                try:
                    if hasattr(employee.date_of_birth, 'strftime'):
                        dob_display = employee.date_of_birth.strftime('%Y-%m-%d')
                    else:
                        dob_display = str(employee.date_of_birth)
                except:
                    dob_display = ""
            self.form_vars["dob"].set(dob_display)
            
            joining_display = ""
            if employee.joining_date:
                try:
                    if hasattr(employee.joining_date, 'strftime'):
                        joining_display = employee.joining_date.strftime('%Y-%m-%d')
                    else:
                        joining_display = str(employee.joining_date)
                except:
                    joining_display = ""
            self.form_vars["joining_date"].set(joining_display)
            
            # Handle address text widget
            try:
                address_widget = self.form_vars["address"]
                address_widget.delete("1.0", tk.END)
                if employee.address:
                    address_widget.insert("1.0", employee.address)
            except Exception as addr_error:
                logger.error(f"Failed to populate address: {addr_error}")
                
        except Exception as e:
            logger.error(f"Failed to populate form: {e}")
            import traceback
            traceback.print_exc()

    def clear_form(self):
        """Clear all form fields and reset to placeholder state"""
        try:
            # Clear the selected employee first
            self.selected_employee = None
            
            # Clear employee selection in treeview
            for item in self.employee_tree.selection():
                self.employee_tree.selection_remove(item)
            
            # Reset to placeholder text for better UX
            self.show_form_placeholder()
            
            # Focus on first field for better user experience
            if hasattr(self, 'form_vars') and 'name' in self.form_vars:
                # Find the name entry widget and focus on it
                for widget in self.winfo_children():
                    if hasattr(widget, 'winfo_children'):
                        for child in widget.winfo_children():
                            if hasattr(child, 'winfo_children'):
                                for subchild in child.winfo_children():
                                    if isinstance(subchild, tk.Entry) and subchild.cget('textvariable') == str(self.form_vars['name']):
                                        subchild.focus_set()
                                        break
            
            logger.info("Form cleared and reset to placeholder state")
            
        except Exception as e:
            logger.error(f"Failed to clear form: {e}")
            # Don't show error popup to user unless it's critical

    def show_form_placeholder(self):
        """Show placeholder text in form when no employee is selected"""
        try:
            # Set left-aligned placeholder text for all fields
            placeholders = {
                "employee_code": "Auto-generated (e.g., EMP001)",
                "name": "Enter full name (e.g., John Smith)",
                "age": "Age (e.g., 25)",
                "department": "Department (e.g., Engineering)",
                "designation": "Job title (e.g., Software Engineer)",
                "salary": "Salary (e.g., 50000)",
                "email": "Email (e.g., john@company.com)",
                "phone": "Phone (e.g., +1-555-0123)",
                "gender": "",  # Combobox will show options
                "dob": "Date of birth: YYYY-MM-DD (e.g., 1990-01-15)",
                "joining_date": "Joining date: YYYY-MM-DD (e.g., 2023-01-01)"
            }
            
            # Set placeholder text for all entry fields
            for field_key, placeholder_text in placeholders.items():
                if field_key in self.form_vars and hasattr(self.form_vars[field_key], 'set'):
                    self.form_vars[field_key].set(placeholder_text)
            
            # Set placeholder for address text widget with left alignment
            if "address" in self.form_vars:
                address_widget = self.form_vars["address"]
                address_widget.delete("1.0", tk.END)
                address_widget.insert("1.0", "Enter complete address...\nStreet Address\nCity, State, ZIP Code\nCountry")
            
            logger.info("Placeholder text set for all fields")
            
        except Exception as e:
            logger.error(f"Failed to show form placeholder: {e}")

    def on_entry_focus_in(self, event, field_key):
        """Handle entry field focus in event"""
        try:
            if self.selected_employee is None:  # Only clear if no employee selected
                current_value = self.form_vars[field_key].get()
                if "Enter " in current_value or "e.g.," in current_value or "Auto-generated" in current_value:
                    self.form_vars[field_key].set("")
        except Exception as e:
            logger.error(f"Focus in error for {field_key}: {e}")

    def on_entry_focus_out(self, event, field_key):
        """Handle entry field focus out event"""
        try:
            if self.selected_employee is None and not self.form_vars[field_key].get().strip():
                self.show_form_placeholder()
        except Exception as e:
            logger.error(f"Focus out error for {field_key}: {e}")

    def on_text_focus_in(self, event, widget):
        """Handle text widget focus in event"""
        try:
            if self.selected_employee is None:
                current_text = widget.get("1.0", tk.END).strip()
                if "Enter complete address" in current_text or "Street Address" in current_text:
                    widget.delete("1.0", tk.END)
        except Exception as e:
            logger.error(f"Text focus in error: {e}")

    def on_text_focus_out(self, event, widget):
        """Handle text widget focus out event"""
        try:
            if self.selected_employee is None and not widget.get("1.0", tk.END).strip():
                widget.delete("1.0", tk.END)
                widget.insert("1.0", "Enter complete address...\nStreet Address\nCity, State ZIP Code\nCountry")
        except Exception as e:
            logger.error(f"Text focus out error: {e}")

    def save_employee(self):
        """Save new employee"""
        if not self.current_user.has_permission('create'):
            messagebox.showerror("Permission Denied", "You don't have permission to create employees")
            return
        
        try:
            # Collect form data
            data = self.collect_form_data()
            
            # Validate data
            validated_data = EmployeeValidator.validate_employee_data(data)
            
            # Create new employee
            employee = Employee(
                name=validated_data.get('Name'),
                age=validated_data.get('Age'),
                department=validated_data.get('Department'),
                salary=validated_data.get('Salary'),
                designation=validated_data.get('Designation'),
                address=validated_data.get('Address'),
                email=validated_data.get('Email'),
                phone_number=validated_data.get('PhoneNumber'),
                joining_date=validated_data.get('JoiningDate'),
                gender=validated_data.get('Gender'),
                date_of_birth=validated_data.get('DateOfBirth')
            )
            
            if employee.save(self.current_user.id):
                messagebox.showinfo("Success", f"Employee {employee.name} saved successfully!")
                app_logger.log_user_action(self.current_user.id, "CREATE_EMPLOYEE", f"Employee: {employee.name}")
                self.clear_form()
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to save employee")
                
        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            logger.error(f"Save employee failed: {e}")
            messagebox.showerror("Error", f"Failed to save employee: {e}")

    def update_employee(self):
        """Update selected employee"""
        if not self.current_user.has_permission('update'):
            messagebox.showerror("Permission Denied", "You don't have permission to update employees")
            return
        
        if not self.selected_employee:
            messagebox.showwarning("No Selection", "Please select an employee to update")
            return
        
        try:
            # Collect form data
            data = self.collect_form_data()
            
            # Validate data
            validated_data = EmployeeValidator.validate_employee_data(data)
            
            # Update employee
            for key, value in validated_data.items():
                if hasattr(self.selected_employee, key.lower()):
                    setattr(self.selected_employee, key.lower(), value)
            
            if self.selected_employee.save(self.current_user.id):
                messagebox.showinfo("Success", f"Employee {self.selected_employee.name} updated successfully!")
                app_logger.log_user_action(self.current_user.id, "UPDATE_EMPLOYEE", f"Employee: {self.selected_employee.name}")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to update employee")
                
        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            logger.error(f"Update employee failed: {e}")
            messagebox.showerror("Error", f"Failed to update employee: {e}")

    def delete_employee(self):
        """Delete selected employee"""
        if not self.current_user.has_permission('delete'):
            messagebox.showerror("Permission Denied", "You don't have permission to delete employees")
            return
        
        if not self.selected_employee:
            messagebox.showwarning("No Selection", "Please select an employee to delete")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete employee '{self.selected_employee.name}'?\n\nThis action cannot be undone."
        )
        
        if confirm:
            try:
                if self.selected_employee.delete():
                    messagebox.showinfo("Success", f"Employee {self.selected_employee.name} deleted successfully!")
                    app_logger.log_user_action(self.current_user.id, "DELETE_EMPLOYEE", f"Employee: {self.selected_employee.name}")
                    self.clear_form()
                    self.load_employees()
                else:
                    messagebox.showerror("Error", "Failed to delete employee")
                    
            except Exception as e:
                logger.error(f"Delete employee failed: {e}")
                messagebox.showerror("Error", f"Failed to delete employee: {e}")

    def view_employee_details(self):
        """View detailed employee information"""
        if not self.selected_employee:
            messagebox.showwarning("No Selection", "Please select an employee to view details")
            return
        
        # Create details window
        details_window = tk.Toplevel(self)
        details_window.title(f"Employee Details - {self.selected_employee.name}")
        details_window.configure(bg="#ffffff")
        details_window.geometry("500x600")
        UIHelper.center_window(details_window, 500, 600)
        
        # Employee details content
        details_frame = tk.Frame(details_window, bg="#ffffff")
        details_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            details_frame,
            text=f"📋 {self.selected_employee.name}",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Details - with proper error handling
        try:
            # Calculate age safely
            calculated_age = "N/A"
            if hasattr(self.selected_employee, 'date_of_birth') and self.selected_employee.date_of_birth:
                from datetime import date
                today = date.today()
                birth_date = self.selected_employee.date_of_birth
                if isinstance(birth_date, str):
                    from datetime import datetime
                    birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            # Calculate tenure safely
            tenure = "N/A"
            if hasattr(self.selected_employee, 'joining_date') and self.selected_employee.joining_date:
                from datetime import date
                today = date.today()
                join_date = self.selected_employee.joining_date
                if isinstance(join_date, str):
                    from datetime import datetime
                    join_date = datetime.strptime(join_date, '%Y-%m-%d').date()
                years = today.year - join_date.year - ((today.month, today.day) < (join_date.month, join_date.day))
                months = today.month - join_date.month
                if months < 0:
                    months += 12
                tenure = f"{years} years, {months} months"
            
            # Format salary safely
            salary_display = "N/A"
            if hasattr(self.selected_employee, 'salary') and self.selected_employee.salary:
                try:
                    salary_display = f"${float(self.selected_employee.salary):,.2f}"
                except (ValueError, TypeError):
                    salary_display = str(self.selected_employee.salary)
            
            details = [
                ("Employee ID", getattr(self.selected_employee, 'id', 'N/A')),
                ("Employee Code", getattr(self.selected_employee, 'employee_code', 'N/A') or 'N/A'),
                ("Full Name", getattr(self.selected_employee, 'name', 'N/A') or 'N/A'),
                ("Department", getattr(self.selected_employee, 'department', 'N/A') or 'N/A'),
                ("Designation", getattr(self.selected_employee, 'designation', 'N/A') or 'N/A'),
                ("Age (from DOB)", str(calculated_age)),
                ("Salary", salary_display),
                ("Email Address", getattr(self.selected_employee, 'email', 'N/A') or 'N/A'),
                ("Phone Number", getattr(self.selected_employee, 'phone_number', 'N/A') or 'N/A'),
                ("Gender", getattr(self.selected_employee, 'gender', 'N/A') or 'N/A'),
                ("Date of Birth", DateHelper.format_date_for_display(getattr(self.selected_employee, 'date_of_birth', None))),
                ("Joining Date", DateHelper.format_date_for_display(getattr(self.selected_employee, 'joining_date', None))),
                ("Work Tenure", tenure),
                ("Employment Status", getattr(self.selected_employee, 'status', 'N/A') or 'Active'),
                ("Address", getattr(self.selected_employee, 'address', 'N/A') or 'N/A')
            ]
            
        except Exception as e:
            logger.error(f"Error preparing employee details: {e}")
            # Fallback details with basic information
            details = [
                ("Employee ID", str(getattr(self.selected_employee, 'id', 'N/A'))),
                ("Full Name", str(getattr(self.selected_employee, 'name', 'N/A'))),
                ("Department", str(getattr(self.selected_employee, 'department', 'N/A'))),
                ("Email", str(getattr(self.selected_employee, 'email', 'N/A'))),
                ("Status", "Active")
            ]
        
        # Create scrollable frame for details
        canvas = tk.Canvas(details_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scrollable_details_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_details_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_details_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display details with better formatting
        for i, (label, value) in enumerate(details):
            try:
                row_frame = tk.Frame(scrollable_details_frame, bg="#ffffff" if i % 2 == 0 else "#f8f9fa")
                row_frame.pack(fill="x", pady=2, padx=10)
                
                # Label
                label_widget = tk.Label(
                    row_frame,
                    text=f"{label}:",
                    font=("Arial", 11, "bold"),
                    bg=row_frame["bg"],
                    fg="#2c3e50",
                    width=18,
                    anchor="w"
                )
                label_widget.pack(side="left", padx=(10, 0), pady=5)
                
                # Value - handle long text properly
                value_text = str(value) if value is not None else "N/A"
                if len(value_text) > 50:
                    value_text = value_text[:50] + "..."
                
                value_widget = tk.Label(
                    row_frame,
                    text=value_text,
                    font=("Arial", 11),
                    bg=row_frame["bg"],
                    fg="#34495e",
                    anchor="w",
                    justify="left",
                    wraplength=250
                )
                value_widget.pack(side="left", padx=(5, 10), pady=5, fill="x", expand=True)
                
            except Exception as e:
                logger.error(f"Error displaying detail {label}: {e}")
                continue
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add close button at bottom
        button_frame = tk.Frame(details_window, bg="#ffffff")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        close_button = tk.Button(
            button_frame,
            text="✖ Close",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=details_window.destroy,
            cursor="hand2",
            padx=20,
            pady=5
        )
        close_button.pack(side="right")

    def collect_form_data(self):
        """Collect data from form fields, filtering out placeholder text"""
        data = {}
        
        def is_placeholder_text(text):
            """Check if text is placeholder text"""
            placeholder_indicators = ["Enter ", "e.g.,", "Auto-generated", "Date of birth:", "Joining date:", "(e.g.", "Age (", "Department (", "Job title ("]
            return any(indicator in text for indicator in placeholder_indicators)
        
        for key, var in self.form_vars.items():
            try:
                if key == "address":
                    address_text = var.get("1.0", tk.END).strip()
                    # Don't include placeholder text
                    if not is_placeholder_text(address_text) and "Enter complete address" not in address_text:
                        data["Address"] = address_text
                    else:
                        data["Address"] = ""
                else:
                    field_value = var.get().strip()
                    # Don't include placeholder text
                    if not is_placeholder_text(field_value):
                        # Map form keys to data keys
                        field_mapping = {
                            "name": "Name",
                            "department": "Department", 
                            "designation": "Designation",
                            "age": "Age",
                            "salary": "Salary",
                            "email": "Email",
                            "phone": "Phone Number",
                            "gender": "Gender",
                            "dob": "Date of Birth (YYYY-MM-DD)",
                            "joining_date": "Joining Date (YYYY-MM-DD)"
                        }
                        if key in field_mapping:
                            data[field_mapping[key]] = field_value
                    else:
                        # Set empty value for placeholder text
                        field_mapping = {
                            "name": "Name",
                            "department": "Department",
                            "designation": "Designation",
                            "age": "Age",
                            "salary": "Salary",
                            "email": "Email",
                            "phone": "Phone Number",
                            "gender": "Gender",
                            "dob": "Date of Birth (YYYY-MM-DD)",
                            "joining_date": "Joining Date (YYYY-MM-DD)"
                        }
                        if key in field_mapping:
                            data[field_mapping[key]] = ""
            except Exception as e:
                logger.error(f"Error collecting data for {key}: {e}")
                continue
        
        return data

    def open_export_window(self):
        """Open export window"""
        try:
            from views.export_window import ExportWindow
            export_window = ExportWindow(self, self.current_user)
            
        except Exception as e:
            logger.error(f"Failed to open export window: {e}")
            messagebox.showerror("Error", f"Failed to open export window: {e}")

    def open_reports_window(self):
        """Open reports window"""
        try:
            from views.reports_window import ReportsWindow
            reports_window = ReportsWindow(self, self.current_user)
            
        except Exception as e:
            logger.error(f"Failed to open reports window: {e}")
            messagebox.showerror("Error", f"Failed to open reports window: {e}")