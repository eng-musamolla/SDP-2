import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
from datetime import datetime


def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Default XAMPP MySQL password is empty
        database='EmployeeDB',
        autocommit=True
    )


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Manager Login")
        self.configure(bg="#f5f7fa")


        window_width = 420
        window_height = 380
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self, text="Welcome Back", bg="#f5f7fa", fg="#333333",
                 font=("Helvetica", 18, "bold")).pack(pady=(30, 5))

        tk.Label(self, text="Login to your account", bg="#f5f7fa", fg="#666666",
                 font=("Helvetica", 11)).pack(pady=(0, 25))

        # ===== Form Frame =====
        form_frame = tk.Frame(self, bg="#f5f7fa")
        form_frame.pack(pady=10, padx=20)

        entry_width = 35

        # Username
        tk.Label(form_frame, text="Username", bg="#f5f7fa", fg="#555555", font=("Helvetica", 10)).pack(anchor="w")
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=entry_width, bd=0,
                                       bg="#e8ecf3", fg="#333333", highlightthickness=1, relief="flat")
        self.username_entry.pack(pady=(0, 15), ipady=6)
        self.username_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.username_entry))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.username_entry))

        # Password
        tk.Label(form_frame, text="Password", bg="#f5f7fa", fg="#555555", font=("Helvetica", 10)).pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 11), width=entry_width, bd=0,
                                       bg="#e8ecf3", fg="#333333", highlightthickness=1, relief="flat")
        self.password_entry.pack(pady=(0, 20), ipady=6)
        self.password_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.password_entry))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.password_entry))

        # ===== Login Button =====
        self.login_btn = tk.Button(form_frame, text="Login", bg="#4a90e2", fg="white",
                                   font=("Helvetica", 12, "bold"), relief="flat", command=self.check_login)
        self.login_btn.pack(fill="x", pady=(5, 10), ipady=6)
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#357ABD"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#4a90e2"))

        # Bind enter key
        self.password_entry.bind("<Return>", lambda event: self.check_login())
        self.username_entry.focus_set()


    def on_focus_in(self, entry):
        entry.config(highlightbackground="#4a90e2", highlightcolor="#4a90e2")

    def on_focus_out(self, entry):
        entry.config(highlightbackground="#d0d0d0", highlightcolor="#d0d0d0")

    #  Login
    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Users WHERE Username = %s AND Password = %s",
                (username, password)
            )
            (count,) = cursor.fetchone()
            cursor.close()
            conn.close()

            if count == 1:
                messagebox.showinfo("Login Success", f"Welcome {username}!")
                self.destroy()
                app = DashboardPage()
                app.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                self.password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error during login:\n{e}")



class EmployeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Manager")
        self.geometry("1200x800")
        self.configure(bg="#f0f4f8")
        self.selected_employee_id = None
        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        form_frame = tk.Frame(self, bg="#e1e7ef", bd=2, relief="groove")
        form_frame.pack(pady=10, padx=10, fill='x')

        labels = [
            "Name", "Age", "Department", "Salary",
            "Designation", "Address", "Email", "Phone Number",
            "Joining Date (YYYY-MM-DD)", "Gender", "Date of Birth (YYYY-MM-DD)"
        ]

        self.vars = {}
        for idx, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#e1e7ef", fg="#333333", font=("Helvetica", 10, "bold"))\
                .grid(row=idx, column=0, sticky="e", padx=5, pady=6)
            var = tk.StringVar()
            self.vars[label] = var
            entry = tk.Entry(form_frame, textvariable=var, font=("Helvetica", 10))
            entry.grid(row=idx, column=1, padx=5, pady=6, sticky="ew")
            entry.configure(relief="flat", bg="white")

        form_frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg="#f0f4f8")
        btn_frame.pack(pady=5)

        btn_bg = "#4a90e2"
        btn_fg = "white"
        btn_font = ("Helvetica", 10, "bold")

        save_btn = tk.Button(btn_frame, text="Save Employee", command=self.save_employee,
                             bg=btn_bg, fg=btn_fg, font=btn_font, relief="flat", padx=12, pady=6)
        save_btn.pack(side="left", padx=5)

        edit_btn = tk.Button(btn_frame, text="Edit Employee", command=self.edit_employee,
                             bg=btn_bg, fg=btn_fg, font=btn_font, relief="flat", padx=12, pady=6)
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee,
                               bg="#d9534f", fg="white", font=btn_font, relief="flat", padx=12, pady=6)
        delete_btn.pack(side="left", padx=5)

        logout_btn = tk.Button(btn_frame, text="Logout", command=self.logout,
                               bg="#f44336", fg="white", font=btn_font, relief="flat", padx=12, pady=6)
        logout_btn.pack(side="left", padx=5)

        # Button to open EmployeeApp
        dash_btn = tk.Button(self, text="Go to Dashbard", bg="#5cb85c", fg="white",
                            font=("Helvetica", 12, "bold"), relief="flat",
                            command=self.open_dash_app)
        dash_btn.pack(pady=20, ipadx=10, ipady=5)




        search_frame = tk.Frame(self, bg="#f0f4f8")
        search_frame.pack(pady=(5, 0))

        tk.Label(search_frame, text="Search:", bg="#f0f4f8", font=("Helvetica", 10, "bold")).pack(side="left", padx=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Helvetica", 10))
        search_entry.pack(side="left", padx=5)

        # Bind real-time search
        search_entry.bind("<KeyRelease>", self.search_employee)

        columns = (
            "Id", "Name", "Age", "Department", "Salary", "Designation",
            "Address", "Email", "PhoneNumber", "JoiningDate", "Gender", "DateOfBirth"
        )

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        rowheight=25,
                        fieldbackground="#ffffff",
                        font=("Helvetica", 10))
        style.map('Treeview', background=[('selected', '#4a90e2')], foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        headings = {
            "Id": "ID", "Name": "Name", "Age": "Age", "Department": "Department", "Salary": "Salary",
            "Designation": "Designation", "Address": "Address", "Email": "Email",
            "PhoneNumber": "Phone Number", "JoiningDate": "Joining Date",
            "Gender": "Gender", "DateOfBirth": "Date of Birth"
        }

        for col in columns:
            self.tree.heading(col, text=headings.get(col, col))
            width = 50 if col == "Id" else 120
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def open_dash_app(self):
        self.destroy()  # Dashboard window close
        dash_window = DashboardPage()  # EmployeeApp open
        dash_window.mainloop()

    def logout(self):

        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
        if confirm:
            self.destroy()
            login_win = LoginWindow()
            login_win.mainloop()

    def search_employee(self, event):
        keyword = self.search_var.get().lower()

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filter data
        for row in self.all_employees:
            row_str = " ".join(str(x).lower() for x in row)

            if keyword in row_str:
                join_date = row[9].strftime("%Y-%m-%d") if row[9] else ""
                dob = row[11].strftime("%Y-%m-%d") if row[11] else ""

                self.tree.insert("", "end", values=(
                    row[0], row[1], row[2], row[3], row[4], row[5],
                    row[6], row[7], row[8], join_date, row[10], dob
                ))

    def validate_date(self, date_str):
        if not date_str:
            return None
        try:
            valid_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            return False



    def clear_form(self):
        for var in self.vars.values():
            var.set("")
        self.selected_employee_id = None

    def load_employees(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Name, Age, Department, Salary, Designation, Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth FROM Employees")
            rows = cursor.fetchall()
            self.all_employees = rows
            cursor.close()
            conn.close()

            for i in self.tree.get_children():
                self.tree.delete(i)

            for row in rows:
                join_date = row[9].strftime("%Y-%m-%d") if row[9] else ""
                dob = row[11].strftime("%Y-%m-%d") if row[11] else ""
                self.tree.insert("", "end", values=(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                    row[7], row[8], join_date, row[10], dob
                ))

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load employees:\n{e}")

    def save_employee(self):
        data = {}
        required_fields = ["Name", "Age", "Department", "Salary"]
        for key, var in self.vars.items():
            data[key] = var.get().strip()

        for field in required_fields:
            if not data[field]:
                messagebox.showwarning("Input Error", f"Please fill the required field: {field}.")
                return

        try:
            data["Age"] = int(data["Age"])
            data["Salary"] = float(data["Salary"])
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be integer and Salary must be a number.")
            return

        for date_field in ["Joining Date (YYYY-MM-DD)", "Date of Birth (YYYY-MM-DD)"]:
            if data[date_field]:
                valid_date = self.validate_date(data[date_field])
                if valid_date is False:
                    messagebox.showwarning("Input Error", f"Invalid date format for {date_field}. Use YYYY-MM-DD.")
                    return
                data[date_field] = valid_date
            else:
                data[date_field] = None

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO Employees 
                (Name, Age, Department, Salary, Designation, Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    data["Name"], data["Age"], data["Department"], data["Salary"],
                    data["Designation"], data["Address"], data["Email"], data["Phone Number"],
                    data["Joining Date (YYYY-MM-DD)"], data["Gender"], data["Date of Birth (YYYY-MM-DD)"]
                )
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Employee saved successfully!")
            self.clear_form()
            self.load_employees()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save employee:\n{e}")

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_employee_id = values[0]
            mapping = {
                "Name": 1, "Age": 2, "Department": 3, "Salary": 4, "Designation": 5,
                "Address": 6, "Email": 7, "Phone Number": 8, "Joining Date (YYYY-MM-DD)": 9,
                "Gender": 10, "Date of Birth (YYYY-MM-DD)": 11
            }
            for key, idx in mapping.items():
                self.vars[key].set(values[idx] if values[idx] else "")

    def edit_employee(self):
        if not self.selected_employee_id:
            messagebox.showwarning("Selection Error", "Please select an employee to edit.")
            return

        data = {}
        required_fields = ["Name", "Age", "Department", "Salary"]
        for key, var in self.vars.items():
            data[key] = var.get().strip()

        for field in required_fields:
            if not data[field]:
                messagebox.showwarning("Input Error", f"Please fill the required field: {field}.")
                return

        try:
            data["Age"] = int(data["Age"])
            data["Salary"] = float(data["Salary"])
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be integer and Salary must be a number.")
            return

        for date_field in ["Joining Date (YYYY-MM-DD)", "Date of Birth (YYYY-MM-DD)"]:
            if data[date_field]:
                valid_date = self.validate_date(data[date_field])
                if valid_date is False:
                    messagebox.showwarning("Input Error", f"Invalid date format for {date_field}. Use YYYY-MM-DD.")
                    return
                data[date_field] = valid_date
            else:
                data[date_field] = None

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE Employees SET 
                Name=%s, Age=%s, Department=%s, Salary=%s, Designation=%s, Address=%s, Email=%s, PhoneNumber=%s, JoiningDate=%s, Gender=%s, DateOfBirth=%s
                WHERE Id=%s""",
                (
                    data["Name"], data["Age"], data["Department"], data["Salary"],
                    data["Designation"], data["Address"], data["Email"], data["Phone Number"],
                    data["Joining Date (YYYY-MM-DD)"], data["Gender"], data["Date of Birth (YYYY-MM-DD)"],
                    self.selected_employee_id
                )
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Employee updated successfully!")
            self.clear_form()
            self.load_employees()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update employee:\n{e}")

    def delete_employee(self):
        if not self.selected_employee_id:
            messagebox.showwarning("Selection Error", "Please select an employee to delete.")
            return

        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this employee?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Employees WHERE Id=%s", (self.selected_employee_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Deleted", "Employee deleted successfully!")
                self.clear_form()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete employee:\n{e}")



class DashboardPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Dashboard")
        self.configure(bg="#f0f4f8")
        self.geometry("900x600")
        self.create_widgets()
        self.load_counts()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg="#93c5fd")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="Employee Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg="#93c5fd",
            fg="#222"
        ).pack(anchor="w", pady=10, padx=20)

        self.cards_frame = tk.Frame(self, bg="#f0f4f8")
        self.cards_frame.pack(pady=10, padx=20, fill="both", expand=True)

        card_opts = {"bd": 2, "relief": "ridge", "width": 200, "height": 100, "bg": "white"}
        label_font = ("Helvetica", 12, "bold")
        number_font = ("Helvetica", 28, "bold")

        # Total Employees
        self.total_card = tk.Frame(self.cards_frame, bg="#e0f2fe", bd=0, relief="flat",
                                   width=250, height=150)
        self.total_card.pack(side="left", padx=20, pady=20)
        self.total_card.pack_propagate(False)

        tk.Label(self.total_card,
                 text="Total Employees",
                 font=("Segoe UI", 12, "bold"),
                 bg="#e0f2fe",
                 fg="#0c4a6e").pack(pady=(15, 5))

        self.total_label = tk.Label(self.total_card,
                                    text="0",
                                    font=("Segoe UI", 26, "bold"),
                                    bg="#e0f2fe",
                                    fg="#0369a1")
        self.total_label.pack()

        # Male Employees
        self.male_card = tk.Frame(self.cards_frame, bg="#e8f5e9", bd=0, relief="flat",
                                  width=250, height=150)
        self.male_card.pack(side="left", padx=20, pady=20)
        self.male_card.pack_propagate(False)

        tk.Label(self.male_card,
                 text="Male Employees",
                 font=("Segoe UI", 12, "bold"),
                 bg="#e8f5e9",
                 fg="#1b5e20").pack(pady=(15, 5))

        self.male_label = tk.Label(self.male_card,
                                   text="0",
                                   font=("Segoe UI", 26, "bold"),
                                   bg="#e8f5e9",
                                   fg="#2e7d32")
        self.male_label.pack()

        # Female Employees
        self.female_card = tk.Frame(self.cards_frame, bg="#fff4e5", bd=0, relief="flat",
                                    width=250, height=150)
        self.female_card.pack(side="left", padx=20, pady=20)
        self.female_card.pack_propagate(False)

        tk.Label(self.female_card,
                 text="Female Employees",
                 font=("Segoe UI", 12, "bold"),
                 bg="#fff4e5",
                 fg="#a24c00").pack(pady=(15, 5))

        self.female_label = tk.Label(self.female_card,
                                     text="0",
                                     font=("Segoe UI", 26, "bold"),
                                     bg="#fff4e5",
                                     fg="#e67e22")
        self.female_label.pack()


        # Button Frame (to align side by side)
        btn_frame = tk.Frame(self, bg="#f0f4f8")
        btn_frame.pack(pady=30)

        # Go to Employees Button
        emp_btn = tk.Button(btn_frame, text="Employees",
                            bg="#22c55e", fg="white",
                            font=("Segoe UI", 12, "bold"),
                            relief="flat", cursor="hand2",
                            command=self.open_employee_app)
        emp_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

        # Logout Button
        logout_btn = tk.Button(btn_frame, text="Logout",
                               bg="#ef4444", fg="white",
                               font=("Segoe UI", 12, "bold"),
                               relief="flat", cursor="hand2",
                               command=self.logout)
        logout_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

    def logout(self):
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
        if confirm:
            self.destroy()
            login_win = LoginWindow()
            login_win.mainloop()

    def open_employee_app(self):
        self.destroy()  # Dashboard window close
        emp_window = EmployeeApp()  # EmployeeApp open
        emp_window.mainloop()

    def load_counts(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) AS TotalEmployees,
                    SUM(CASE WHEN Gender='Male' THEN 1 ELSE 0 END) AS MaleEmployees,
                    SUM(CASE WHEN Gender='Female' THEN 1 ELSE 0 END) AS FemaleEmployees
                FROM Employees
            """)
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            total = row[0] if row[0] else 0
            male = row[1] if row[1] else 0
            female = row[2] if row[2] else 0

            self.total_label.config(text=f"{total}")
            self.male_label.config(text=f"{male}")
            self.female_label.config(text=f"{female}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load counts:\n{e}")

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
