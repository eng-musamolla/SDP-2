# 🚀 Quick Setup Guide - Employee Management System

This guide will help you get the Employee Management System up and running quickly on your machine.

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] XAMPP or MySQL server installed
- [ ] Git installed (for version control)
- [ ] A text editor or IDE (VS Code recommended)

## ⚡ 5-Minute Setup

### Step 1: Download and Extract
1. Download the project files
2. Extract to a folder like `C:\EmployeeManagement\`
3. Open command prompt/terminal in that folder

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
1. **Start XAMPP** (or your MySQL server)
2. **Open phpMyAdmin** (http://localhost/phpmyadmin)
3. **Import database**:
   - Click "Import" tab
   - Choose file: `setup_database.sql`
   - Click "Go"

### Step 4: Test Database Connection
```bash
python test_database.py
```
You should see: ✅ All database tests passed!

### Step 5: Run the Application
```bash
python app.py
```

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 🛠️ Detailed Setup Instructions

### Windows Setup with XAMPP

1. **Install XAMPP**
   - Download from: https://www.apachefriends.org/
   - Install and start Apache + MySQL services

2. **Database Configuration**
   - Open XAMPP Control Panel
   - Click "Admin" next to MySQL (opens phpMyAdmin)
   - Import `setup_database.sql` file

3. **Python Environment**
   ```cmd
   # Create virtual environment (optional but recommended)
   python -m venv venv
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```cmd
   python app.py
   ```

### Linux/Mac Setup

1. **Install MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server
   
   # macOS (with Homebrew)
   brew install mysql
   ```

2. **Setup Database**
   ```bash
   mysql -u root -p < setup_database.sql
   ```

3. **Python Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

## 🔧 Configuration

### Database Settings
Edit `config/settings.py` if you need to change:
- Database host (default: localhost)
- Database port (default: 3306)
- Username (default: root)
- Password (default: empty)

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Set your MySQL password here
    'database': 'employee_management'
}
```

### Application Settings
- Window size: 1200x700 (fixed for stability)
- Currency: ৳ (Bangladesh Taka)
- Default export location: `exports/` folder

## 📊 Sample Data

The system comes with 8 pre-loaded Bangladeshi employees:
- **Md. Rahul Ahmed** - Software Engineer, Dhaka
- **Fatima Khatun** - HR Manager, Chittagong  
- **Arif Hassan** - Marketing Manager, Dhaka
- **Nasreen Sultana** - Accountant, Sylhet
- **Karim Uddin** - Sales Executive, Dhaka
- **Rashida Begum** - Admin Assistant, Chittagong
- **Tariq Rahman** - IT Support, Dhaka
- **Salma Khatun** - Customer Service, Sylhet

## 🧪 Testing Your Setup

### 1. Database Connection Test
```bash
python test_database.py
```
**Expected Output:**
```
🔍 Testing Database Connection...
✅ Database connection successful
✅ Employee Management database exists
✅ All required tables exist
✅ Sample data loaded (8 employees found)
✅ All database tests passed!
```

### 2. Application Launch Test
```bash
python app.py
```
- Login window should appear
- Use admin/admin123 to login
- Dashboard should load with employee statistics

### 3. Feature Test Checklist
- [ ] Login with admin credentials
- [ ] View dashboard statistics (should show ৳ currency)
- [ ] Navigate to Employee Management
- [ ] Search for "Rahul" - should find Md. Rahul Ahmed
- [ ] Try exporting data (CSV/Excel/PDF)
- [ ] Check if files are created with timestamps

## ❌ Troubleshooting

### Common Issues & Solutions

#### "No module named 'tkinter'"
**Solution:** Install tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

#### "Can't connect to MySQL server"
**Solutions:**
1. Ensure MySQL is running (check XAMPP control panel)
2. Verify database credentials in `config/settings.py`
3. Run `python test_database.py` for detailed diagnostics

#### "Database 'employee_management' doesn't exist"
**Solution:** Import the database schema
```bash
# Method 1: Using MySQL command line
mysql -u root -p < setup_database.sql

# Method 2: Using phpMyAdmin
# Open phpMyAdmin → Import → Choose setup_database.sql
```

#### "Permission denied" errors
**Solution:** Run with administrator privileges
```bash
# Windows
# Right-click Command Prompt → "Run as administrator"

# Linux/Mac
sudo python app.py
```

#### Application crashes on startup
**Solutions:**
1. Check Python version: `python --version` (needs 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check logs in the console for specific error messages

### Getting Help

If you encounter issues:
1. **Check the console output** for error messages
2. **Run the database test**: `python test_database.py`
3. **Verify all dependencies**: `pip list`
4. **Check MySQL service status** in XAMPP
5. **Create an issue** on GitHub with error details

### Contact & Support
- **GitHub Issues**: For bug reports and feature requests
- **Email**: Include error logs and system information
- **Documentation**: Check README.md for detailed information

## 🎯 Next Steps

Once setup is complete:

1. **Explore the Dashboard**
   - View real-time employee statistics
   - Use quick search functionality
   - Check system alerts and recent activities

2. **Manage Employees**
   - Add new employees with Bangladesh-specific data
   - Update existing employee information
   - Export reports in various formats

3. **Customize Settings**
   - Modify database configuration if needed
   - Adjust application preferences
   - Set up automated backups

4. **Advanced Features**
   - Set up user roles and permissions
   - Configure automated reports
   - Implement backup schedules

## 🚀 Ready to Use!

Your Employee Management System is now ready! 

**Login Credentials:**
- **Username:** admin
- **Password:** admin123

**Key Features to Try:**
- 📊 Enhanced Dashboard with ৳ currency
- 👥 Employee Management with Bangladeshi sample data
- 📈 Real-time statistics and department overview
- 📤 Export functionality with auto-timestamps
- 🔍 Quick search and advanced filtering

Enjoy managing your employees efficiently! 🎉