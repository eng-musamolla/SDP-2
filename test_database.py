#!/usr/bin/env python3
"""
Database Connection Test Tool
Advanced Employee Management System v2.0.0

This script tests the database connection and provides setup guidance.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import DatabaseManager
from config.settings import DB_CONFIG
import mysql.connector

def test_mysql_server():
    """Test MySQL server connection"""
    print("🔍 Testing MySQL Server Connection...")
    try:
        # Test without database
        test_config = DB_CONFIG.copy()
        test_config.pop('database', None)
        
        conn = mysql.connector.connect(**test_config)
        conn.close()
        print("✅ MySQL server is running and accessible")
        return True
    except mysql.connector.Error as e:
        print(f"❌ MySQL server connection failed: {e}")
        return False

def test_database_exists():
    """Test if database exists"""
    print(f"🔍 Checking if database '{DB_CONFIG['database']}' exists...")
    try:
        test_config = DB_CONFIG.copy()
        test_config.pop('database', None)
        
        conn = mysql.connector.connect(**test_config)
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{DB_CONFIG['database']}'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            print(f"✅ Database '{DB_CONFIG['database']}' exists")
            return True
        else:
            print(f"❌ Database '{DB_CONFIG['database']}' does not exist")
            return False
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def test_tables():
    """Test if required tables exist"""
    print("🔍 Checking required tables...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        required_tables = ['Users', 'Employees', 'AuditLog']
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✅ {table}")
            else:
                print(f"  ❌ {table} (missing)")
                missing_tables.append(table)
        
        cursor.close()
        conn.close()
        
        if not missing_tables:
            print("✅ All required tables exist")
            return True
        else:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def test_sample_data():
    """Test if sample data exists"""
    print("🔍 Checking sample data...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        print(f"  👥 Users: {user_count}")
        
        # Check employees
        cursor.execute("SELECT COUNT(*) FROM Employees")
        emp_count = cursor.fetchone()[0]
        print(f"  👨‍💼 Employees: {emp_count}")
        
        cursor.close()
        conn.close()
        
        if user_count > 0 and emp_count > 0:
            print("✅ Sample data exists")
            return True
        else:
            print("⚠️ No sample data found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking sample data: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n" + "="*60)
    print("🛠️  DATABASE SETUP REQUIRED")
    print("="*60)
    print()
    print("📋 Steps to set up the database:")
    print()
    print("1️⃣  Start MySQL Server:")
    print("   • XAMPP: Start MySQL from control panel")
    print("   • WAMP: Start MySQL service")
    print("   • Standalone: Run 'mysqld' or start MySQL service")
    print()
    print("2️⃣  Open phpMyAdmin:")
    print("   • Open browser: http://localhost/phpmyadmin")
    print("   • Or use MySQL Workbench")
    print()
    print("3️⃣  Import Database:")
    print("   • Click 'Import' tab in phpMyAdmin")
    print("   • Choose file: setup_database.sql")
    print("   • Click 'Go' to execute")
    print()
    print("4️⃣  Verify Setup:")
    print("   • Check if 'EmployeeDB' database is created")
    print("   • Verify tables: Users, Employees, AuditLog")
    print()
    print("5️⃣  Run Application:")
    print("   • python app.py")
    print("   • Login: admin / admin123")
    print()
    print("🔧 Current Configuration:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   User: {DB_CONFIG['user']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print()

def main():
    """Run complete database test"""
    print("🚀 Advanced Employee Management System - Database Test")
    print("="*60)
    print()
    
    # Test MySQL server
    server_ok = test_mysql_server()
    if not server_ok:
        print("\n❌ MySQL server is not running or not accessible")
        print("Please start MySQL server (XAMPP/WAMP) and try again")
        return False
    
    print()
    
    # Test database
    db_ok = test_database_exists()
    if not db_ok:
        show_setup_instructions()
        return False
    
    print()
    
    # Test tables
    tables_ok = test_tables()
    if not tables_ok:
        show_setup_instructions()
        return False
    
    print()
    
    # Test sample data
    data_ok = test_sample_data()
    
    print()
    print("="*60)
    if server_ok and db_ok and tables_ok:
        print("🎉 DATABASE READY! You can now run the application.")
        print("   Command: python app.py")
        print("   Login: admin / admin123")
    else:
        print("❌ Database setup incomplete. Please follow the instructions above.")
    print("="*60)
    
    return server_ok and db_ok and tables_ok

if __name__ == "__main__":
    try:
        success = main()
        input("\nPress Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)