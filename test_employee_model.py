#!/usr/bin/env python3
"""
Quick test to verify Employee model and database connection
"""

import sys
import os

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.employee import Employee
from config.database import db_manager

def test_employee_loading():
    """Test employee loading from database"""
    print("Testing Employee Model...")
    
    try:
        # Test database connection
        print("1. Testing database connection...")
        result = db_manager.execute_query("SELECT COUNT(*) FROM Employees", fetch='one')
        print(f"   Total employees in database: {result[0]}")
        
        # Test Employee.get_all_employees()
        print("2. Testing Employee.get_all_employees()...")
        employees = Employee.get_all_employees(active_only=False)
        print(f"   Loaded employees: {len(employees)}")
        
        for i, emp in enumerate(employees):
            print(f"   Employee {i+1}: {emp.name} - {emp.department} - {emp.designation}")
        
        # Test statistics
        print("3. Testing Employee.get_statistics()...")
        stats = Employee.get_statistics()
        print(f"   Statistics: {stats}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_employee_loading()