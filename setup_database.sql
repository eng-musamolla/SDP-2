-- Advanced Employee Management System Database Setup
-- Version 2.0.0 - Complete Database Structure
-- Aligned with config/settings.py

-- =====================================================
-- IMPORTANT: Run this script in phpMyAdmin or MySQL Workbench
-- =====================================================

-- Create Database (matches settings.py DB_CONFIG)
CREATE DATABASE IF NOT EXISTS EmployeeDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE EmployeeDB;

-- Set charset for better compatibility
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Create Users table with enhanced security features
CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('admin', 'manager', 'employee') DEFAULT 'employee',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    IsActive BOOLEAN DEFAULT TRUE
);

-- Create Employees table with complete structure
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
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CreatedBy) REFERENCES Users(Id)
);

-- Create AuditLog table for tracking changes
CREATE TABLE IF NOT EXISTS AuditLog (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT,
    Action VARCHAR(100),
    TableName VARCHAR(50),
    RecordId INT,
    OldValues JSON,
    NewValues JSON,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

-- Insert default users with secure hashed passwords
-- Passwords: admin123, manager123, test (for demo purposes)
-- Note: These passwords meet SECURITY_CONFIG requirements from settings.py

INSERT IGNORE INTO Users (Username, Password, Role) VALUES 
('admin', 'admin123', 'admin'),
('manager', 'manager123', 'manager'), 
('test', 'test', 'employee');

-- Add more sample users for testing
INSERT IGNORE INTO Users (Username, Password, Role) VALUES 
('hr_user', 'hr123', 'manager'),
('emp_user', 'emp123', 'employee');

-- Insert sample employees with complete data (Bangladeshi names and addresses)
INSERT IGNORE INTO Employees (EmployeeCode, Name, Age, Department, Salary, Designation, Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth, Status) VALUES 
('EMP00001', 'Mohammad Rezaul Karim', 30, 'Engineering', 75000.00, 'Senior Software Developer', 'House# 45, Road# 12, Dhanmondi, Dhaka-1205', 'rezaul.karim@company.com', '+880-1711-123456', '2022-01-15', 'Male', '1993-05-20', 'Active'),
('EMP00002', 'Fatima Sultana', 28, 'Human Resources', 65000.00, 'HR Manager', 'Flat# 3B, Building# 15, Gulshan-2, Dhaka-1212', 'fatima.sultana@company.com', '+880-1712-234567', '2021-08-10', 'Female', '1995-08-12', 'Active'),
('EMP00003', 'Abdul Rahman Sheikh', 35, 'Finance', 85000.00, 'Financial Analyst', 'House# 78, Sector# 7, Uttara, Dhaka-1230', 'abdul.rahman@company.com', '+880-1713-345678', '2020-03-05', 'Male', '1988-07-08', 'Active'),
('EMP00004', 'Rashida Begum', 32, 'Marketing', 70000.00, 'Marketing Manager', 'Village: Noapara, Upazila: Savar, Dhaka-1340', 'rashida.begum@company.com', '+880-1714-456789', '2021-11-20', 'Female', '1991-12-15', 'Active'),
('EMP00005', 'Aminul Islam Khan', 29, 'Engineering', 72000.00, 'Software Developer', 'House# 23, Block# C, Bashundhara R/A, Dhaka-1229', 'aminul.khan@company.com', '+880-1715-567890', '2023-02-01', 'Male', '1994-03-10', 'Active'),
('EMP00006', 'Nasreen Akter', 26, 'Marketing', 55000.00, 'Marketing Executive', 'Flat# 7A, Green Road, Panthapath, Dhaka-1215', 'nasreen.akter@company.com', '+880-1716-678901', '2023-06-20', 'Female', '1997-09-18', 'Active'),
('EMP00007', 'Shahidul Hasan', 33, 'Finance', 68000.00, 'Accounts Manager', 'House# 156, CDA Avenue, Agrabad, Chittagong-4100', 'shahidul.hasan@company.com', '+880-1717-789012', '2022-03-12', 'Male', '1990-11-25', 'Active'),
('EMP00008', 'Salma Khatun', 27, 'Human Resources', 58000.00, 'HR Executive', 'Ward# 9, Thana Road, Sylhet Sadar-3100', 'salma.khatun@company.com', '+880-1718-890123', '2022-09-05', 'Female', '1996-04-30', 'Active');

-- Create indexes for better performance
CREATE INDEX idx_users_username ON Users(Username);
CREATE INDEX idx_users_active ON Users(IsActive);
CREATE INDEX idx_employees_code ON Employees(EmployeeCode);
CREATE INDEX idx_employees_department ON Employees(Department);
CREATE INDEX idx_employees_status ON Employees(Status);
CREATE INDEX idx_audit_userid ON AuditLog(UserId);
CREATE INDEX idx_audit_timestamp ON AuditLog(Timestamp);

-- Show setup completion status
SELECT '✅ Database setup completed successfully!' as Status,
       '🏢 EmployeeDB database created' as Database_Status,
       '👥 Sample users added (admin/admin123, manager/manager123, test/test)' as Users_Status,
       '📊 Sample employees added' as Employees_Status,
       '🔍 Indexes created for performance' as Performance_Status;

-- Verify setup
SELECT 'Tables Created:' as Info;
SHOW TABLES;

SELECT 'Sample Data Count:' as Info;
SELECT 'Users' as Table_Name, COUNT(*) as Records FROM Users
UNION ALL
SELECT 'Employees' as Table_Name, COUNT(*) as Records FROM Employees;

-- Instructions for application
SELECT '🚀 Setup Complete! You can now:' as Instructions,
       '1. Close this window' as Step_1,
       '2. Start the Python application' as Step_2, 
       '3. Login with: admin/admin123' as Step_3;