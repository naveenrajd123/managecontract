# Contributing to Contract Management System

First off, thank you for considering contributing to the Contract Management System! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and constructive in your interactions.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any alternatives** you've considered

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests if applicable
3. Ensure your code follows the project's style guidelines
4. Update documentation as needed
5. Write a clear commit message

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ManageContract.git
cd ManageContract

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # Add your API keys

# Run the application
python main.py
```

## 📁 Project Structure

```
ManageContract/
├── src/                 # Core application code
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database models
│   ├── rag_system.py    # RAG implementation
│   ├── early_warning.py # Warning system
│   ├── config.py        # Configuration
│   └── schemas.py       # Pydantic schemas
├── scripts/             # Utility scripts
├── static/              # Frontend files
└── data/                # Sample data
```

### Key Modules

- **`src/main.py`** - FastAPI routes and application setup
- **`src/database.py`** - SQLAlchemy models and database connection
- **`src/rag_system.py`** - RAG implementation with Google Gemini
- **`src/early_warning.py`** - Contract monitoring and alerts
- **`src/config.py`** - Environment configuration
- **`src/schemas.py`** - Request/response schemas

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Example

```python
async def get_contract_by_id(
    contract_id: int,
    db: AsyncSession
) -> Contract:
    """
    Retrieve a contract by its ID.
    
    Args:
        contract_id: The unique identifier of the contract
        db: Database session
    
    Returns:
        Contract object if found
    
    Raises:
        HTTPException: If contract not found
    """
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return contract
```

### Import Organization

```python
# Standard library imports
import os
from datetime import datetime
from typing import List, Dict, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from sqlalchemy import select

# Local imports
from src.database import Contract
from src.config import settings
```

## 💬 Commit Messages

Use clear and meaningful commit messages:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(rag): add semantic search for contract clauses

Implemented enhanced semantic search using keyword expansion
and relevance scoring for better contract clause retrieval.

Closes #123
```

```
fix(database): resolve connection pool timeout issue

Fixed issue where database connections were not being
properly released, causing timeout errors under load.
```

## 🔄 Pull Request Process

1. **Update documentation** - Ensure README and other docs reflect your changes
2. **Add tests** - If applicable, add tests for new functionality
3. **Update CHANGELOG** - Add entry describing your changes
4. **Follow template** - Use the PR template when creating your pull request
5. **Request review** - Tag maintainers for review
6. **Address feedback** - Make requested changes promptly
7. **Squash commits** - Clean up commit history before merging

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated (if applicable)
- [ ] All tests passing
- [ ] Dependent changes merged

## 🧪 Testing

```bash
# Run tests (when test suite is available)
pytest

# Run with coverage
pytest --cov=src

# Run linting
flake8 src/
black src/ --check
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Python Best Practices](https://docs.python-guide.org/)

## ❓ Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute! 🎉
