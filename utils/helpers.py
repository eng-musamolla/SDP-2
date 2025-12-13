import hashlib
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional
import json

class SecurityManager:
    """Handle password hashing, session management, and security features"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = hashed_password.split(':')
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return hash_value == password_hash
        except ValueError:
            return False
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)

class FileManager:
    """Handle file operations, exports, and imports"""
    
    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        """Create directory if it doesn't exist"""
        os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def save_export_file(data, filename: str, file_type: str) -> str:
        """Save exported data to file"""
        export_dir = "exports"
        FileManager.ensure_directory_exists(export_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(export_dir, f"{filename}_{timestamp}.{file_type}")
        
        if file_type == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        
        return filepath

class DateHelper:
    """Helper functions for date operations"""
    
    @staticmethod
    def format_date_for_display(date_obj) -> str:
        """Format date for UI display"""
        if date_obj:
            return date_obj.strftime("%Y-%m-%d")
        return ""
    
    @staticmethod
    def calculate_age(birth_date) -> int:
        """Calculate age from birth date"""
        if not birth_date:
            return 0
        today = datetime.now().date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    @staticmethod
    def calculate_tenure(joining_date) -> str:
        """Calculate employment tenure"""
        if not joining_date:
            return "N/A"
        
        today = datetime.now().date()
        delta = today - joining_date
        
        years = delta.days // 365
        months = (delta.days % 365) // 30
        
        if years > 0:
            return f"{years} years, {months} months"
        elif months > 0:
            return f"{months} months"
        else:
            return f"{delta.days} days"

class UIHelper:
    """Helper functions for UI operations"""
    
    @staticmethod
    def center_window(window, width: int, height: int) -> None:
        """Center window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format currency for display"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 30) -> str:
        """Truncate text for display in tables"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."