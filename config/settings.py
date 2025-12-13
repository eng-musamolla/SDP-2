# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'EmployeeDB',
    'autocommit': True,
    'charset': 'utf8mb4'
}

# Application Settings
APP_CONFIG = {
    'title': 'Advanced Employee Management System',
    'version': '2.0.0',
    'debug': True,
    'window_size': '1400x900',
    'min_window_size': (1200, 800),
    'theme': 'modern'
}

# Security Settings
SECURITY_CONFIG = {
    'password_min_length': 6,
    'session_timeout': 3600,  # 1 hour in seconds
    'max_login_attempts': 3,
    'password_hash_rounds': 12
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'file': 'logs/app.log',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Export Settings
EXPORT_CONFIG = {
    'pdf_template': 'assets/templates/employee_report.html',
    'excel_headers': [
        'ID', 'Name', 'Age', 'Department', 'Salary', 'Designation',
        'Address', 'Email', 'Phone', 'Joining Date', 'Gender', 'Date of Birth'
    ],
    'default_export_path': 'exports/'
}