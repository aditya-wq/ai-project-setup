# Contributing to AI Project

Thank you for your interest in contributing to AI Project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and constructive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- An Anthropic API key (for running integration tests)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/aiproject/ai-project.git
cd ai-project

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write your code following our style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests Locally

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_project --cov-report=html

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
```

### 4. Run Linters and Type Checkers

```bash
# Ruff (linting)
ruff check src tests

# Black (formatting)
black --check src tests

# MyPy (type checking)
mypy src
```

### 5. Format Your Code

```bash
# Auto-format with Black
black src tests

# Auto-fix linting issues
ruff check --fix src tests
```

## Code Style Guidelines

### Python

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings for all public modules, functions, and classes
- Keep lines under 100 characters
- Use meaningful variable and function names

### Example

```python
def compress_file(filepath: Path, model: Optional[str] = None) -> bool:
    """Compress a text file using LLM-based compression.

    Args:
        filepath: Path to the file to compress
        model: Optional LLM model override

    Returns:
        True if compression succeeded, False otherwise

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file is too large
    """
    pass
```

## Testing Guidelines

### Test Structure

- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- End-to-end tests go in `tests/e2e/`
- Test files should be named `test_<module_name>.py`

### Writing Tests

```python
import pytest
from pathlib import Path
from ai_project.validators import extract_headings


class TestExtractHeadings:
    """Test suite for heading extraction."""

    def test_extracts_single_heading(self):
        """Test extraction of a single heading."""
        text = "# Hello World"
        result = extract_headings(text)
        assert result == [("#", "Hello World")]

    def test_extracts_multiple_headings(self):
        """Test extraction of multiple headings."""
        text = "# Heading 1\n## Heading 2\n### Heading 3"
        result = extract_headings(text)
        assert len(result) == 3
```

### Coverage Requirements

- Minimum 90% code coverage required
- All new features must include tests
- Bug fixes should include regression tests

## Documentation Guidelines

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed, explaining the purpose
    and behavior of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When this exception is raised
    """
    pass
```

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features

## Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(compression): add support for custom LLM models
fix(validators): correct URL extraction for special characters
docs: update installation instructions
test(hooks): add integration tests for Claude Code hook
```

## Pull Request Process

### Before Submitting

1. Ensure all tests pass locally
2. Run linters and type checkers
3. Update documentation if needed
4. Add entry to CHANGELOG.md

### Creating a Pull Request

1. Fill out the PR template completely
2. Reference any related issues
3. Ensure CI passes
4. Request review from maintainers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Test addition

## Testing
Describe testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment
- Error messages if applicable

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Potential implementation ideas
- Any constraints or considerations

## Questions?

Feel free to:
- Open an issue for questions
- Join project discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
