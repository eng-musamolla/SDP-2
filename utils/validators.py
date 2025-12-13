import re
from datetime import datetime
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validator:
    """Comprehensive input validation system"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
        """Validate and parse date string"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, format_str).date()
        except ValueError:
            raise ValidationError(f"Invalid date format. Expected {format_str}")
    
    @staticmethod
    def validate_age(age: Union[str, int]) -> int:
        """Validate age"""
        try:
            age_int = int(age)
            if age_int < 16 or age_int > 100:
                raise ValidationError("Age must be between 16 and 100")
            return age_int
        except ValueError:
            raise ValidationError("Age must be a valid number")
    
    @staticmethod
    def validate_salary(salary: Union[str, float]) -> float:
        """Validate salary"""
        try:
            salary_float = float(salary)
            if salary_float < 0:
                raise ValidationError("Salary cannot be negative")
            if salary_float > 10000000:  # 10 million limit
                raise ValidationError("Salary exceeds maximum allowed limit")
            return salary_float
        except ValueError:
            raise ValidationError("Salary must be a valid number")
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: list) -> None:
        """Validate that required fields are not empty"""
        missing_fields = []
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(f"Required fields missing: {', '.join(missing_fields)}")
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and numeric characters"
        
        return True, "Password is strong"
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize input string to prevent injection attacks"""
        if not isinstance(input_str, str):
            return str(input_str)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()

class EmployeeValidator:
    """Specialized validator for employee data"""
    
    REQUIRED_FIELDS = ['Name', 'Department', 'Designation']
    
    @staticmethod
    def validate_employee_data(data: dict) -> dict:
        """Validate complete employee data"""
        validator = Validator()
        validated_data = {}
        
        # Validate required fields
        validator.validate_required_fields(data, EmployeeValidator.REQUIRED_FIELDS)
        
        # Validate and sanitize each field
        validated_data['Name'] = validator.sanitize_input(data.get('Name', ''))
        validated_data['Department'] = validator.sanitize_input(data.get('Department', ''))
        validated_data['Designation'] = validator.sanitize_input(data.get('Designation', ''))
        validated_data['Address'] = validator.sanitize_input(data.get('Address', ''))
        
        # Validate optional numeric fields
        if data.get('Age'):
            validated_data['Age'] = validator.validate_age(data['Age'])
        
        if data.get('Salary'):
            validated_data['Salary'] = validator.validate_salary(data['Salary'])
        
        # Validate email if provided
        if data.get('Email'):
            email = data['Email'].strip()
            if email and not validator.validate_email(email):
                raise ValidationError("Invalid email format")
            validated_data['Email'] = email
        
        # Validate phone if provided
        if data.get('Phone Number'):
            phone = data['Phone Number'].strip()
            if phone and not validator.validate_phone(phone):
                raise ValidationError("Invalid phone number format")
            validated_data['PhoneNumber'] = phone
        
        # Validate dates
        for date_field, db_field in [
            ('Joining Date (YYYY-MM-DD)', 'JoiningDate'),
            ('Date of Birth (YYYY-MM-DD)', 'DateOfBirth')
        ]:
            if data.get(date_field):
                validated_data[db_field] = validator.validate_date(data[date_field])
        
        # Validate gender
        if data.get('Gender'):
            gender = data['Gender'].strip()
            if gender and gender not in ['Male', 'Female', 'Other']:
                raise ValidationError("Gender must be Male, Female, or Other")
            validated_data['Gender'] = gender
        
        return validated_data