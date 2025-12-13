#!/usr/bin/env python3
"""
Database Setup and Test Script
This will setup the database properly and test the connection
"""

import mysql.connector
import hashlib
import secrets

def hash_password(password):
    """Simple password hashing for demo"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"

def setup_database():
    """Setup database with proper structure"""
    print("Setting up Employee Management Database...")
    
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            autocommit=True
        )
        cursor = conn.cursor()
        
        # Create database
        print("1. Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS EmployeeDB")
        cursor.execute("USE EmployeeDB")
        
        # Drop existing tables if they exist (for clean setup)
        print("2. Setting up tables...")
        cursor.execute("DROP TABLE IF EXISTS AuditLog")
        cursor.execute("DROP TABLE IF EXISTS Employees")  
        cursor.execute("DROP TABLE IF EXISTS Users")
        
        # Create Users table
        cursor.execute("""
            CREATE TABLE Users (
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
            CREATE TABLE Employees (
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
                Status ENUM('Active', 'Inactive', 'Terminated') DEFAULT 'Active',
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Insert users with proper password hashing
        print("3. Creating user accounts...")
        
        # Simple password for demo (in production, use proper bcrypt)
        admin_pass = hash_password('admin123')
        test_pass = hash_password('test')
        
        cursor.execute(
            "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
            ('admin', admin_pass, 'admin')
        )
        cursor.execute(
            "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
            ('test', test_pass, 'employee')
        )
        
        # Insert sample employees
        print("4. Adding sample employees...")
        employees = [
            ('EMP001', 'John Smith', 30, 'Engineering', 75000, 'Senior Developer', 'john@company.com', '555-0101', '2022-01-15', 'Male', '1993-05-20'),
            ('EMP002', 'Sarah Johnson', 28, 'HR', 65000, 'HR Manager', 'sarah@company.com', '555-0102', '2021-08-10', 'Female', '1995-08-12'),
            ('EMP003', 'Michael Chen', 35, 'Finance', 85000, 'Financial Analyst', 'michael@company.com', '555-0103', '2020-03-05', 'Male', '1988-07-08'),
        ]
        
        for emp in employees:
            cursor.execute("""
                INSERT INTO Employees (EmployeeCode, Name, Age, Department, Salary, Designation, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, emp)
        
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed successfully!")
        print("\nLogin Credentials:")
        print("• Admin: username=admin, password=admin123")
        print("• Test User: username=test, password=test")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL/XAMPP is running")
        print("2. Check if MySQL is accessible on localhost:3306")
        print("3. Verify MySQL root user has no password (default XAMPP setup)")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_connection():
    """Test database connection and data"""
    print("\nTesting database connection...")
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='EmployeeDB'
        )
        cursor = conn.cursor()
        
        # Test user count
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users in database: {user_count}")
        
        # Test employee count  
        cursor.execute("SELECT COUNT(*) FROM Employees")
        emp_count = cursor.fetchone()[0]
        print(f"✅ Employees in database: {emp_count}")
        
        # Test specific user
        cursor.execute("SELECT Username, Role FROM Users WHERE Username='admin'")
        admin_user = cursor.fetchone()
        if admin_user:
            print(f"✅ Admin user found: {admin_user[0]} (Role: {admin_user[1]})")
        
        cursor.close()
        conn.close()
        
        print("✅ Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    print("Employee Management System - Database Setup")
    print("=" * 50)
    
    # Setup database
    if setup_database():
        # Test connection
        test_connection()
        
        print("\n" + "=" * 50)
        print("🚀 Ready to run the application!")
        print("Run: python simple_test.py")
        print("Look for the BLUE 'Sign In' button")
    else:
        print("\n❌ Setup failed. Please check your MySQL installation.")

if __name__ == "__main__":
    main()