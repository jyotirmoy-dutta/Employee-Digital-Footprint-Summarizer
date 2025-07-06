# Contributing to Employee Digital Footprint Summarizer

Thank you for your interest in contributing to the Employee Digital Footprint Summarizer! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

We welcome contributions from the community! Here are the main ways you can contribute:

### 🐛 Bug Reports
- Use the [GitHub Issues](https://github.com/yourusername/footprintSummarizer/issues) page
- Include detailed steps to reproduce the issue
- Provide system information and error messages
- Check if the issue has already been reported

### 💡 Feature Requests
- Submit feature requests through [GitHub Issues](https://github.com/yourusername/footprintSummarizer/issues)
- Explain the use case and benefits
- Consider if the feature aligns with the project's goals
- Be specific about requirements and implementation ideas

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests for new functionality
- Submit a pull request

### 📚 Documentation
- Improve README files
- Add inline code documentation
- Create tutorials or guides
- Fix typos and clarify instructions

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/footprintSummarizer.git
   cd footprintSummarizer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run Tests**
   ```bash
   python test_app.py
   pytest tests/
   ```

## 📝 Code Style Guidelines

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

### Example Code Style
```python
from typing import List, Dict, Optional
from datetime import datetime

def collect_user_data(user_id: str, start_date: Optional[datetime] = None) -> Dict[str, List]:
    """
    Collect user digital footprint data.
    
    Args:
        user_id: The unique identifier for the user
        start_date: Optional start date for filtering data
        
    Returns:
        Dictionary containing collected data by category
        
    Raises:
        ValueError: If user_id is invalid
        PermissionError: If insufficient permissions
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    # Implementation here
    return {"logins": [], "files": [], "apps": []}
```

### File Organization
- Keep related functionality in the same module
- Use descriptive file names
- Group imports: standard library, third-party, local
- Maintain consistent directory structure

## 🧪 Testing Guidelines

### Test Requirements
- Write tests for all new functionality
- Maintain test coverage above 80%
- Include both unit tests and integration tests
- Test error conditions and edge cases

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_data_collectors.py

# Run with verbose output
pytest -v
```

### Test Structure
```python
import pytest
from unittest.mock import patch, MagicMock
from data_collectors.logins import get_logins

class TestLoginCollector:
    """Test cases for login data collection."""
    
    def test_get_logins_returns_list(self):
        """Test that get_logins returns a list."""
        result = get_logins()
        assert isinstance(result, list)
    
    @patch('data_collectors.logins.psutil.users')
    def test_get_logins_handles_empty_users(self, mock_users):
        """Test handling of empty user list."""
        mock_users.return_value = []
        result = get_logins()
        assert result == []
    
    def test_get_logins_handles_permission_error(self):
        """Test handling of permission errors."""
        with patch('data_collectors.logins.psutil.users', side_effect=PermissionError):
            result = get_logins()
            assert result == []
```

## 🔄 Pull Request Process

### Before Submitting
1. **Test Your Changes**
   ```bash
   python test_app.py
   pytest tests/
   ```

2. **Check Code Style**
   ```bash
   flake8 .
   black --check .
   mypy .
   ```

3. **Update Documentation**
   - Update README if needed
   - Add docstrings for new functions
   - Update API documentation

### Pull Request Guidelines
1. **Create Descriptive Title**
   - Use present tense ("Add feature" not "Added feature")
   - Be specific about the change

2. **Write Detailed Description**
   - Explain what the PR does
   - Link to related issues
   - Include screenshots for UI changes
   - List any breaking changes

3. **Example PR Description**
   ```markdown
   ## Description
   Adds support for collecting macOS login events using the unified logging system.
   
   ## Changes
   - Implemented `_get_logins_macos()` function
   - Added macOS-specific log parsing
   - Updated documentation
   
   ## Testing
   - Added unit tests for macOS login collection
   - Tested on macOS 12.0+
   
   ## Related Issues
   Closes #123
   
   ## Screenshots
   [If applicable]
   ```

### Review Process
1. **Automated Checks**
   - All tests must pass
   - Code style checks must pass
   - No merge conflicts

2. **Code Review**
   - At least one maintainer must approve
   - Address all review comments
   - Update PR based on feedback

3. **Merge**
   - Squash commits if requested
   - Use conventional commit messages
   - Delete feature branch after merge

## 🏷️ Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

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
```
feat: add macOS login event collection

fix(gui): resolve PySide6 signal import error

docs: update installation instructions

test: add unit tests for file share collector
```

## 🐛 Bug Report Template

When reporting bugs, please use this template:

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [Windows/macOS/Linux]
- Python Version: [3.8/3.9/3.10/3.11]
- Application Version: [1.0.0]

## Error Messages
```
[Paste error messages here]
```

## Additional Information
Any other relevant information
```

## 💡 Feature Request Template

```markdown
## Feature Description
Brief description of the requested feature

## Use Case
Explain why this feature is needed

## Proposed Implementation
How you think this could be implemented

## Alternatives Considered
Other approaches you've considered

## Additional Information
Any other relevant information
```

## 📋 Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issue
- `priority: low`: Low priority issue
- `windows`: Windows-specific issue
- `macos`: macOS-specific issue
- `linux`: Linux-specific issue

## 🎯 Areas for Contribution

### High Priority
- macOS data collection implementation
- Linux data collection implementation
- Enhanced error handling and logging
- Performance optimizations

### Medium Priority
- Additional data sources (cloud services, etc.)
- Advanced analytics and visualizations
- Email integration
- API for third-party integrations

### Low Priority
- UI/UX improvements
- Additional report templates
- Localization support
- Plugin system

## 📞 Getting Help

If you need help with contributing:

- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/footprintSummarizer/discussions)
- **Issues**: [Report problems](https://github.com/yourusername/footprintSummarizer/issues)
- **Email**: support@footprintsummarizer.com

## 🙏 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame

Thank you for contributing to the Employee Digital Footprint Summarizer! 🎉 