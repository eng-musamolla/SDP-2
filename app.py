#!/usr/bin/env python3
"""
Advanced Employee Management System v2.0
Production-grade employee management application with advanced features.

Author: SDP 2 Project
Created: December 2025
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import application modules
from config.database import db_manager
from config.settings import APP_CONFIG
from utils.logger import app_logger
from views.login_window import LoginWindow

def setup_application():
    """Initialize application configuration and database"""
    try:
        # Create necessary directories
        directories = ['logs', 'exports', 'assets/icons', 'temp']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize database tables
        db_manager.create_tables()
        
        # Insert default admin user if not exists
        from models.user import User
        admin_exists = db_manager.execute_query(
            "SELECT COUNT(*) FROM Users WHERE Role='admin'", fetch='one'
        )
        
        if not admin_exists or admin_exists[0] == 0:
            admin_user = User(username='admin', password='admin123', role='admin')
            admin_user.save()
            logging.info("Default admin user created (username: admin, password: admin123)")
        
        # Insert sample data if database is empty
        from models.employee import Employee
        employee_count = db_manager.execute_query(
            "SELECT COUNT(*) FROM Employees", fetch='one'
        )
        
        if not employee_count or employee_count[0] == 0:
            create_sample_data()
        
        logging.info("Application setup completed successfully")
        
    except Exception as e:
        logging.error(f"Application setup failed: {e}")
        sys.exit(1)

def create_sample_data():
    """Create sample employee data for demonstration"""
    from models.employee import Employee
    from datetime import date
    
    sample_employees = [
        {
            'name': 'John Smith', 'age': 30, 'department': 'Engineering',
            'salary': 75000.00, 'designation': 'Senior Developer',
            'email': 'john.smith@company.com', 'phone_number': '555-0101',
            'gender': 'Male', 'joining_date': date(2022, 1, 15),
            'date_of_birth': date(1993, 5, 20)
        },
        {
            'name': 'Sarah Johnson', 'age': 28, 'department': 'Human Resources',
            'salary': 65000.00, 'designation': 'HR Manager',
            'email': 'sarah.johnson@company.com', 'phone_number': '555-0102',
            'gender': 'Female', 'joining_date': date(2021, 8, 10),
            'date_of_birth': date(1995, 11, 12)
        },
        {
            'name': 'Michael Chen', 'age': 35, 'department': 'Finance',
            'salary': 85000.00, 'designation': 'Financial Analyst',
            'email': 'michael.chen@company.com', 'phone_number': '555-0103',
            'gender': 'Male', 'joining_date': date(2020, 3, 5),
            'date_of_birth': date(1988, 7, 8)
        }
    ]
    
    for emp_data in sample_employees:
        employee = Employee(**emp_data)
        employee.save()
    
    logging.info("Sample employee data created")

def main():
    """Main application entry point"""
    try:
        # Setup application
        setup_application()
        
        # Start the GUI application
        app = LoginWindow()
        app.mainloop()
        
    except KeyboardInterrupt:
        logging.info("Application terminated by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()