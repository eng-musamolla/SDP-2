# Contributing to Employee Management System

Thank you for considering contributing to the Employee Management System! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- Git for version control
- Basic knowledge of Tkinter and database management

### Development Setup

1. **Fork the repository**
   ```bash
   git clone <your-fork-url>
   cd employee-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

4. **Set up the database**
   ```bash
   mysql -u root -p < setup_database.sql
   ```

5. **Test the setup**
   ```bash
   python test_database.py
   python app.py
   ```

## 🔄 Development Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/feature-name` - New features
- `bugfix/bug-name` - Bug fixes
- `hotfix/fix-name` - Critical production fixes

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   python -m pytest tests/
   python test_database.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

## 📝 Code Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused (max 50 lines)
- Use type hints where appropriate

### Example Code Style
```python
def validate_employee_data(employee_data: dict) -> tuple[bool, str]:
    """
    Validate employee data before database insertion.
    
    Args:
        employee_data (dict): Dictionary containing employee information
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not employee_data.get('name'):
        return False, "Employee name is required"
    
    return True, ""
```

### Database Guidelines
- Use parameterized queries to prevent SQL injection
- Follow consistent naming conventions for tables and columns
- Add proper indexes for performance
- Include proper error handling for database operations

### UI/UX Guidelines
- Maintain consistency with existing interface design
- Use Bangladesh-appropriate formatting (৳ currency, local addresses)
- Provide clear error messages and user feedback
- Ensure accessibility features are maintained

## 🧪 Testing

### Test Categories
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test database interactions
- **UI Tests**: Test user interface components
- **End-to-End Tests**: Test complete user workflows

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_employee_model.py

# Run database connection test
python test_database.py
```

### Writing Tests
```python
import unittest
from models.employee import Employee

class TestEmployeeModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.employee = Employee()
    
    def test_validate_phone_number(self):
        """Test phone number validation for Bangladesh format."""
        valid_phone = "+8801712345678"
        self.assertTrue(self.employee.validate_phone(valid_phone))
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
```

## 🐛 Bug Reports

### Before Submitting a Bug Report
- Check existing issues to avoid duplicates
- Test with the latest version
- Gather system information and error logs

### Bug Report Template
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**System Information:**
- OS: [e.g. Windows 11]
- Python Version: [e.g. 3.9.7]
- MySQL Version: [e.g. 8.0.27]
- Application Version: [e.g. 2.0.0]

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Before Submitting a Feature Request
- Check if the feature already exists
- Search existing feature requests
- Consider if it fits the project's scope

### Feature Request Template
```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 🌟 Types of Contributions

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test improvements

### Documentation Contributions
- README improvements
- API documentation
- Tutorials and guides
- Code comments
- Translation (Bengali/English)

### Other Contributions
- UI/UX improvements
- Bangladesh localization enhancements
- Database optimization
- Security improvements
- Accessibility features

## 🏷️ Commit Message Guidelines

Use conventional commit format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(dashboard): add Bangladesh currency formatting
fix(database): resolve connection timeout issues
docs(readme): update installation instructions
style(ui): improve button spacing and alignment
```

## 📋 Pull Request Process

1. **Ensure your code passes all tests**
2. **Update documentation** if needed
3. **Add tests** for new functionality
4. **Follow the pull request template**
5. **Link related issues** in the description
6. **Request review** from maintainers

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## Testing
- [ ] Tests pass locally with my changes
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive and welcoming language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Helpful
- Help newcomers get started
- Share knowledge and resources
- Provide constructive feedback
- Celebrate others' contributions

### Be Professional
- Keep discussions focused and productive
- Avoid personal attacks or harassment
- Report inappropriate behavior to maintainers
- Follow the code of conduct

## 📞 Getting Help

If you need help or have questions:

1. **Check the documentation** in the README and wiki
2. **Search existing issues** for similar problems
3. **Join discussions** in existing issues or pull requests
4. **Ask questions** by creating a new issue with the "question" label
5. **Contact maintainers** for urgent matters

## 🎯 Project Roadmap

### Short-term Goals (Next 3 months)
- [ ] Add more comprehensive tests
- [ ] Improve documentation with tutorials
- [ ] Enhance Bangladesh localization
- [ ] Performance optimization
- [ ] Mobile-responsive web version

### Long-term Goals (6-12 months)
- [ ] Multi-language support (Bengali + English)
- [ ] Role-based dashboard customization
- [ ] Advanced reporting and analytics
- [ ] API development for third-party integration
- [ ] Cloud deployment options

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Employee Management System! 🚀
```