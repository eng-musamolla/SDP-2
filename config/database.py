import mysql.connector
from mysql.connector import pooling
from config.settings import DB_CONFIG
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Enhanced database manager with connection pooling and error handling"""
    
    def __init__(self):
        self.pool = None
        self._create_connection_pool()
    
    def _create_connection_pool(self):
        """Create a connection pool for better performance"""
        try:
            # First check if we can connect to MySQL server
            self._validate_mysql_connection()
            
            pool_config = DB_CONFIG.copy()
            pool_config.update({
                'pool_name': 'employee_pool',
                'pool_size': 10,
                'pool_reset_session': True,
                'autocommit': True
            })
            self.pool = pooling.MySQLConnectionPool(**pool_config)
            logger.info("Database connection pool created successfully")
            
            # Validate database structure
            self._validate_database_structure()
            
        except mysql.connector.Error as e:
            self._handle_mysql_error(e)
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            self._show_setup_instructions()
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self.pool.get_connection()
        except Exception as e:
            logger.error(f"Failed to get database connection: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query with proper error handling"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                if fetch == 'one':
                    return cursor.fetchone()
                elif fetch == 'all':
                    return cursor.fetchall()
            
            connection.commit()
            return cursor.rowcount
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database query failed: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def _validate_mysql_connection(self):
        """Validate MySQL server connection"""
        try:
            # Test connection without database first
            test_config = DB_CONFIG.copy()
            test_config.pop('database', None)
            
            test_conn = mysql.connector.connect(**test_config)
            test_conn.close()
            logger.info("MySQL server connection validated")
            
        except mysql.connector.Error as e:
            if e.errno == 1049:  # Database doesn't exist
                logger.warning(f"Database '{DB_CONFIG['database']}' does not exist")
                self._show_database_setup_instructions()
            else:
                logger.error(f"MySQL connection failed: {e}")
            raise
    
    def _validate_database_structure(self):
        """Validate database structure exists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if required tables exist
            required_tables = ['Users', 'Employees', 'AuditLog']
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {', '.join(missing_tables)}")
                self._show_setup_instructions()
            else:
                logger.info("Database structure validated successfully")
                
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database structure validation failed: {e}")
    
    def _handle_mysql_error(self, error):
        """Handle specific MySQL errors with helpful messages"""
        error_messages = {
            2003: "❌ Cannot connect to MySQL server. Please ensure MySQL is running.",
            1045: "❌ Access denied. Please check username and password in settings.py",
            1049: f"❌ Database '{DB_CONFIG['database']}' doesn't exist. Please run setup_database.sql",
            2006: "❌ MySQL server has gone away. Please check server configuration.",
            1146: "❌ Required tables don't exist. Please run setup_database.sql"
        }
        
        message = error_messages.get(error.errno, f"❌ MySQL Error ({error.errno}): {error.msg}")
        logger.error(message)
        print(f"\n🔴 DATABASE CONNECTION ERROR:")
        print(f"   {message}")
        
    def _show_database_setup_instructions(self):
        """Show database setup instructions"""
        print(f"\n📋 DATABASE SETUP REQUIRED:")
        print(f"   1. Open phpMyAdmin or MySQL Workbench")
        print(f"   2. Import/Execute the file: setup_database.sql")
        print(f"   3. Verify database '{DB_CONFIG['database']}' is created")
        print(f"   4. Restart the application")
        print(f"\n📄 Current database config:")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   User: {DB_CONFIG['user']}")
        print(f"   Database: {DB_CONFIG['database']}")
    
    def _show_setup_instructions(self):
        """Show complete setup instructions"""
        print(f"\n🛠️  SETUP INSTRUCTIONS:")
        print(f"   1. Start MySQL server (XAMPP/WAMP/standalone MySQL)")
        print(f"   2. Open phpMyAdmin (usually http://localhost/phpmyadmin)")
        print(f"   3. Click 'Import' tab")
        print(f"   4. Choose file: setup_database.sql")
        print(f"   5. Click 'Go' to execute")
        print(f"   6. Verify '{DB_CONFIG['database']}' database is created with tables")
        print(f"   7. Restart this application")
        print(f"\n⚙️  Alternative: Run SQL manually:")
        print(f"   CREATE DATABASE {DB_CONFIG['database']};")
        print(f"   Then execute the complete setup_database.sql content")
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        tables = {
            'Users': """
                CREATE TABLE IF NOT EXISTS Users (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    Username VARCHAR(50) NOT NULL UNIQUE,
                    Password VARCHAR(255) NOT NULL,
                    Role ENUM('admin', 'manager', 'employee') DEFAULT 'employee',
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    IsActive BOOLEAN DEFAULT TRUE
                )
            """,
            'Employees': """
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
                )
            """,
            'AuditLog': """
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
                )
            """
        }
        
        for table_name, query in tables.items():
            try:
                self.execute_query(query)
                logger.info(f"Table {table_name} created/verified successfully")
            except Exception as e:
                logger.error(f"Failed to create table {table_name}: {e}")
    
    def test_connection(self):
        """Test database connection and return status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return True, "Connection successful"
        except Exception as e:
            return False, str(e)

# Global database manager instance
db_manager = DatabaseManager()