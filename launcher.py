#!/usr/bin/env python3
"""
Simple launcher for the Advanced Employee Management System
This will create the database and tables automatically if they don't exist
"""

import mysql.connector
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_database_and_tables():
    """Create database and tables if they don't exist"""
    try:
        # Connect to MySQL without specifying database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            autocommit=True
        )
        cursor = conn.cursor()
        
        print("Creating database and tables...")
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS EmployeeDB")
        cursor.execute("USE EmployeeDB")
        
        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(50) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Role ENUM('admin', 'manager', 'employee') DEFAULT 'employee',
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                IsActive BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Create Employees table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                EmployeeCode VARCHAR(20) UNIQUE,
                Name VARCHAR(100) NOT NULL,
                Age INT,
                Department VARCHAR(100),
                Salary DECIMAL(10,2),
                Designation VARCHAR(100),
                Address TEXT,
                Email VARCHAR(100),
                PhoneNumber VARCHAR(20),
                JoiningDate DATE,
                Gender ENUM('Male', 'Female', 'Other'),
                DateOfBirth DATE,
                Photo LONGBLOB,
                Status ENUM('Active', 'Inactive', 'Terminated') DEFAULT 'Active',
                CreatedBy INT,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Create AuditLog table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AuditLog (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                UserId INT,
                Action VARCHAR(100),
                TableName VARCHAR(50),
                RecordId INT,
                OldValues JSON,
                NewValues JSON,
                Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert default users if they don't exist
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            print("Creating default users...")
            
            # Hash passwords (simple version for demo)
            import hashlib
            import secrets
            
            def hash_password(password):
                salt = secrets.token_hex(32)
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                return f"{salt}:{password_hash}"
            
            admin_password = hash_password('admin123')
            test_password = hash_password('test')
            
            cursor.execute(
                "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                ('admin', admin_password, 'admin')
            )
            cursor.execute(
                "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                ('test', test_password, 'employee')
            )
            
        # Insert sample employees if table is empty
        cursor.execute("SELECT COUNT(*) FROM Employees")
        emp_count = cursor.fetchone()[0]
        
        if emp_count == 0:
            print("Creating sample employee data...")
            sample_employees = [
                ('EMP00001', 'John Smith', 30, 'Engineering', 75000.00, 'Senior Developer', '123 Main St', 'john@company.com', '555-0101', '2022-01-15', 'Male', '1993-05-20'),
                ('EMP00002', 'Sarah Johnson', 28, 'Human Resources', 65000.00, 'HR Manager', '456 Oak Ave', 'sarah@company.com', '555-0102', '2021-08-10', 'Female', '1995-08-12'),
                ('EMP00003', 'Michael Chen', 35, 'Finance', 85000.00, 'Financial Analyst', '789 Pine St', 'michael@company.com', '555-0103', '2020-03-05', 'Male', '1988-07-08')
            ]
            
            for emp in sample_employees:
                cursor.execute("""
                    INSERT INTO Employees (EmployeeCode, Name, Age, Department, Salary, Designation, Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, emp)
        
        cursor.close()
        conn.close()
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Database setup failed: {e}")
        return False

def main():
    """Main launcher function"""
    print("Advanced Employee Management System v2.0")
    print("=" * 50)
    
    # Setup database
    if not create_database_and_tables():
        print("\nFailed to setup database. Please check your MySQL connection.")
        input("Press Enter to exit...")
        return
    
    print("\nStarting application...")
    
    try:
        # Import and start the application
        from views.login_window import LoginWindow
        
        app = LoginWindow()
        app.mainloop()
        
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()