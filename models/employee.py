from typing import Optional, Dict, Any, List
from datetime import datetime, date
from config.database import db_manager
from utils.validators import EmployeeValidator, ValidationError
from utils.helpers import DateHelper
import logging

logger = logging.getLogger(__name__)

class Employee:
    """Enhanced Employee model with validation and additional features"""
    
    def __init__(self, employee_id: Optional[int] = None, employee_code: str = "",
                 name: str = "", age: Optional[int] = None, department: str = "",
                 salary: Optional[float] = None, designation: str = "", address: str = "",
                 email: str = "", phone_number: str = "", joining_date: Optional[date] = None,
                 gender: str = "", date_of_birth: Optional[date] = None, 
                 status: str = "Active"):
        
        self.id = employee_id
        self.employee_code = employee_code
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        self.designation = designation
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.joining_date = joining_date
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.status = status
        self.created_at = None
        self.updated_at = None
    
    def save(self, current_user_id: Optional[int] = None) -> bool:
        """Save employee to database with validation"""
        try:
            if self.id:
                # Update existing employee
                query = """
                    UPDATE Employees SET 
                    EmployeeCode=%s, Name=%s, Age=%s, Department=%s, Salary=%s, 
                    Designation=%s, Address=%s, Email=%s, PhoneNumber=%s, 
                    JoiningDate=%s, Gender=%s, DateOfBirth=%s, Status=%s, 
                    UpdatedAt=NOW() WHERE Id=%s
                """
                params = (
                    self.employee_code, self.name, self.age, self.department, 
                    self.salary, self.designation, self.address, self.email, 
                    self.phone_number, self.joining_date, self.gender, 
                    self.date_of_birth, self.status, self.id
                )
            else:
                # Create new employee
                if not self.employee_code:
                    self.employee_code = self._generate_employee_code()
                
                query = """
                    INSERT INTO Employees 
                    (EmployeeCode, Name, Age, Department, Salary, Designation, 
                     Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth, 
                     Status, CreatedBy) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    self.employee_code, self.name, self.age, self.department, 
                    self.salary, self.designation, self.address, self.email, 
                    self.phone_number, self.joining_date, self.gender, 
                    self.date_of_birth, self.status, current_user_id or self.created_by
                )
            
            result = db_manager.execute_query(query, params)
            
            if not self.id and result:
                # Get the new employee ID
                self.id = db_manager.execute_query(
                    "SELECT LAST_INSERT_ID()", fetch='one'
                )[0]
            
            logger.info(f"Employee {self.name} saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save employee {self.name}: {e}")
            return False
    
    @classmethod
    def get_by_id(cls, employee_id: int) -> Optional['Employee']:
        """Get employee by ID"""
        try:
            query = """
                SELECT Id, EmployeeCode, Name, Age, Department, Salary, Designation,
                       Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth,
                       Status, CreatedAt, UpdatedAt
                FROM Employees WHERE Id=%s
            """
            result = db_manager.execute_query(query, (employee_id,), fetch='one')
            
            if result:
                employee = cls()
                employee.id = result[0]
                employee.employee_code = result[1]
                employee.name = result[2]
                employee.age = result[3]
                employee.department = result[4]
                employee.salary = result[5]
                employee.designation = result[6]
                employee.address = result[7]
                employee.email = result[8]
                employee.phone_number = result[9]
                employee.joining_date = result[10]
                employee.gender = result[11]
                employee.date_of_birth = result[12]
                employee.status = result[13]
                employee.created_at = result[14]
                employee.updated_at = result[15]
                return employee
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get employee by ID {employee_id}: {e}")
            return None
    
    @classmethod
    def get_all_employees(cls, active_only: bool = True) -> List['Employee']:
        """Get all employees"""
        try:
            query = """
                SELECT Id, EmployeeCode, Name, Age, Department, Salary, Designation,
                       Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth,
                       Status, CreatedAt, UpdatedAt
                FROM Employees
            """
            
            if active_only:
                query += " WHERE Status='Active'"
            
            query += " ORDER BY Name"
            
            results = db_manager.execute_query(query, fetch='all')
            
            employees = []
            for result in results:
                employee = cls()
                employee.id = result[0]
                employee.employee_code = result[1]
                employee.name = result[2]
                employee.age = result[3]
                employee.department = result[4]
                employee.salary = result[5]
                employee.designation = result[6]
                employee.address = result[7]
                employee.email = result[8]
                employee.phone_number = result[9]
                employee.joining_date = result[10]
                employee.gender = result[11]
                employee.date_of_birth = result[12]
                employee.status = result[13]
                employee.created_at = result[14]
                employee.updated_at = result[15]
                employees.append(employee)
            
            return employees
            
        except Exception as e:
            logger.error(f"Failed to get all employees: {e}")
            return []
    
    @classmethod
    def search_employees(cls, search_term: str, filters: Dict[str, Any] = None) -> List['Employee']:
        """Advanced employee search with filters"""
        try:
            query = """
                SELECT Id, EmployeeCode, Name, Age, Department, Salary, Designation,
                       Address, Email, PhoneNumber, JoiningDate, Gender, DateOfBirth,
                       Status, CreatedAt, UpdatedAt
                FROM Employees WHERE 1=1
            """
            params = []
            
            # Add search term conditions
            if search_term:
                query += """ AND (
                    Name LIKE %s OR EmployeeCode LIKE %s OR Department LIKE %s 
                    OR Designation LIKE %s OR Email LIKE %s OR PhoneNumber LIKE %s
                )"""
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern] * 6)
            
            # Add filters
            if filters:
                if filters.get('department'):
                    query += " AND Department = %s"
                    params.append(filters['department'])
                
                if filters.get('status'):
                    query += " AND Status = %s"
                    params.append(filters['status'])
                
                if filters.get('gender'):
                    query += " AND Gender = %s"
                    params.append(filters['gender'])
                
                if filters.get('salary_min'):
                    query += " AND Salary >= %s"
                    params.append(filters['salary_min'])
                
                if filters.get('salary_max'):
                    query += " AND Salary <= %s"
                    params.append(filters['salary_max'])
            
            query += " ORDER BY Name"
            
            results = db_manager.execute_query(query, params, fetch='all')
            
            employees = []
            for result in results:
                employee = cls()
                employee.id = result[0]
                employee.employee_code = result[1]
                employee.name = result[2]
                employee.age = result[3]
                employee.department = result[4]
                employee.salary = result[5]
                employee.designation = result[6]
                employee.address = result[7]
                employee.email = result[8]
                employee.phone_number = result[9]
                employee.joining_date = result[10]
                employee.gender = result[11]
                employee.date_of_birth = result[12]
                employee.status = result[13]
                employee.created_at = result[14]
                employee.updated_at = result[15]
                employees.append(employee)
            
            return employees
            
        except Exception as e:
            logger.error(f"Failed to search employees: {e}")
            return []
    
    def delete(self) -> bool:
        """Soft delete employee (mark as inactive)"""
        try:
            query = "UPDATE Employees SET Status='Terminated', UpdatedAt=NOW() WHERE Id=%s"
            db_manager.execute_query(query, (self.id,))
            self.status = 'Terminated'
            logger.info(f"Employee {self.name} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete employee {self.name}: {e}")
            return False
    
    def _generate_employee_code(self) -> str:
        """Generate unique employee code"""
        try:
            # Get count of employees to generate next code
            result = db_manager.execute_query(
                "SELECT COUNT(*) FROM Employees", fetch='one'
            )
            count = result[0] + 1
            return f"EMP{count:05d}"
            
        except Exception:
            # Fallback to timestamp-based code
            return f"EMP{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    @property
    def calculated_age(self) -> int:
        """Calculate age from date of birth"""
        return DateHelper.calculate_age(self.date_of_birth)
    
    @property
    def tenure(self) -> str:
        """Calculate employment tenure"""
        return DateHelper.calculate_tenure(self.joining_date)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert employee to dictionary"""
        return {
            'id': self.id,
            'employee_code': self.employee_code,
            'name': self.name,
            'age': self.age,
            'department': self.department,
            'salary': self.salary,
            'designation': self.designation,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'joining_date': DateHelper.format_date_for_display(self.joining_date),
            'gender': self.gender,
            'date_of_birth': DateHelper.format_date_for_display(self.date_of_birth),
            'status': self.status,
            'calculated_age': self.calculated_age,
            'tenure': self.tenure,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def get_statistics(cls) -> Dict[str, Any]:
        """Get employee statistics for dashboard"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN Gender='Male' THEN 1 ELSE 0 END) as male_count,
                    SUM(CASE WHEN Gender='Female' THEN 1 ELSE 0 END) as female_count,
                    SUM(CASE WHEN Status='Active' THEN 1 ELSE 0 END) as active_count,
                    AVG(Salary) as avg_salary,
                    MAX(Salary) as max_salary,
                    COUNT(DISTINCT Department) as departments,
                    COUNT(CASE WHEN DATE(CreatedAt) >= DATE_FORMAT(NOW(), '%%Y-%%m-01') THEN 1 END) as this_month
                FROM Employees
            """
            result = db_manager.execute_query(query, fetch='one')
            
            return {
                'total_employees': result[0] or 0,
                'male_employees': result[1] or 0,
                'female_employees': result[2] or 0,
                'active_employees': result[3] or 0,
                'average_salary': result[4] or 0,
                'highest_salary': result[5] or 0,
                'total_departments': result[6] or 0,
                'employees_this_month': result[7] or 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get employee statistics: {e}")
            return {
                'total_employees': 0,
                'male_employees': 0,
                'female_employees': 0,
                'active_employees': 0,
                'average_salary': 0,
                'total_departments': 0
            }