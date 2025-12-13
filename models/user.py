from typing import Optional, Dict, Any
from datetime import datetime
from config.database import db_manager
from utils.helpers import SecurityManager
from utils.validators import Validator
import logging

logger = logging.getLogger(__name__)

class User:
    """User model with enhanced security features"""
    
    def __init__(self, user_id: Optional[int] = None, username: str = "", 
                 password: str = "", role: str = "employee", is_active: bool = True):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.is_active = is_active
        self.created_at = None
        self.updated_at = None
    
    def save(self) -> bool:
        """Save user to database"""
        try:
            if self.id:
                # Update existing user
                query = """
                    UPDATE Users SET Username=%s, Password=%s, Role=%s, IsActive=%s, 
                    UpdatedAt=NOW() WHERE Id=%s
                """
                params = (self.username, self.password, self.role, self.is_active, self.id)
            else:
                # Create new user
                hashed_password = SecurityManager.hash_password(self.password)
                query = """
                    INSERT INTO Users (Username, Password, Role, IsActive) 
                    VALUES (%s, %s, %s, %s)
                """
                params = (self.username, hashed_password, self.role, self.is_active)
            
            result = db_manager.execute_query(query, params)
            
            if not self.id and result:
                # Get the new user ID
                self.id = db_manager.execute_query(
                    "SELECT LAST_INSERT_ID()", fetch='one'
                )[0]
            
            logger.info(f"User {self.username} saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save user {self.username}: {e}")
            return False
    
    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        """Authenticate user with username and password - supports both plain text and hashed passwords"""
        try:
            query = """
                SELECT Id, Username, Password, Role, IsActive, CreatedAt, UpdatedAt 
                FROM Users WHERE Username=%s AND IsActive=TRUE
            """
            result = db_manager.execute_query(query, (username,), fetch='one')
            
            if result:
                stored_password = result[2]
                password_valid = False
                
                # Check if password is hashed (contains ':') or plain text
                if ':' in stored_password:
                    # Hashed password - use security manager
                    password_valid = SecurityManager.verify_password(password, stored_password)
                else:
                    # Plain text password - direct comparison for development/demo
                    password_valid = (password == stored_password)
                
                if password_valid:
                    user = cls()
                    user.id = result[0]
                    user.username = result[1]
                    user.password = result[2]
                    user.role = result[3]
                    user.is_active = result[4]
                    user.created_at = result[5]
                    user.updated_at = result[6]
                    
                    logger.info(f"User {username} authenticated successfully")
                    return user
            
            logger.warning(f"Authentication failed for user {username}")
            return None
            
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        try:
            query = """
                SELECT Id, Username, Password, Role, IsActive, CreatedAt, UpdatedAt 
                FROM Users WHERE Id=%s
            """
            result = db_manager.execute_query(query, (user_id,), fetch='one')
            
            if result:
                user = cls()
                user.id = result[0]
                user.username = result[1]
                user.password = result[2]
                user.role = result[3]
                user.is_active = result[4]
                user.created_at = result[5]
                user.updated_at = result[6]
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user by ID {user_id}: {e}")
            return None
    
    @classmethod
    def get_all_users(cls) -> list['User']:
        """Get all users"""
        try:
            query = """
                SELECT Id, Username, Password, Role, IsActive, CreatedAt, UpdatedAt 
                FROM Users ORDER BY Username
            """
            results = db_manager.execute_query(query, fetch='all')
            
            users = []
            for result in results:
                user = cls()
                user.id = result[0]
                user.username = result[1]
                user.password = result[2]
                user.role = result[3]
                user.is_active = result[4]
                user.created_at = result[5]
                user.updated_at = result[6]
                users.append(user)
            
            return users
            
        except Exception as e:
            logger.error(f"Failed to get all users: {e}")
            return []
    
    def delete(self) -> bool:
        """Soft delete user (mark as inactive)"""
        try:
            query = "UPDATE Users SET IsActive=FALSE, UpdatedAt=NOW() WHERE Id=%s"
            db_manager.execute_query(query, (self.id,))
            self.is_active = False
            logger.info(f"User {self.username} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user {self.username}: {e}")
            return False
    
    def change_password(self, new_password: str) -> bool:
        """Change user password"""
        try:
            # Validate password strength
            is_strong, message = Validator.validate_password_strength(new_password)
            if not is_strong:
                logger.warning(f"Password change failed for {self.username}: {message}")
                return False
            
            hashed_password = SecurityManager.hash_password(new_password)
            query = "UPDATE Users SET Password=%s, UpdatedAt=NOW() WHERE Id=%s"
            db_manager.execute_query(query, (hashed_password, self.id))
            
            self.password = hashed_password
            logger.info(f"Password changed successfully for user {self.username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to change password for user {self.username}: {e}")
            return False
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission based on role"""
        permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'export', 'manage_users'],
            'manager': ['create', 'read', 'update', 'delete', 'export'],
            'employee': ['read']
        }
        
        return permission in permissions.get(self.role, [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }