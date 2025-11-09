# Contributing to PyGraphile

Thank you for your interest in contributing to PyGraphile! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and inclusive. We want this to be a welcoming community for everyone.

## How to Contribute

### Reporting Bugs

- Use the GitHub Issues tracker
- Describe the bug in detail
- Include steps to reproduce
- Mention your Python version and OS

### Suggesting Features

- Open an issue with the "enhancement" label
- Clearly describe the feature and its use case
- Explain why it would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or fix
3. Write clear, commented code
4. Add tests if applicable
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

### AI Usage Disclosure

Contributors are welcome to use AI tools to assist with their contributions. However, **you must disclose any AI-generated changes** in your pull request:

- **List which changes were made with AI assistance** in the PR description
- **Explain what those changes do in your own words** - do not use AI to write the explanation
- Be transparent about the extent of AI involvement (e.g., "AI generated the initial structure", "AI helped refactor function X")
- Take full responsibility for reviewing and understanding all AI-generated code before submitting

This policy ensures transparency and helps maintain code quality and understanding across the project.

## Development Setup

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/dshaw0004/pygraphile.git
cd pygraphile

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linter
uv run ruff check .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/dshaw0004/pygraphile.git
cd pygraphile

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and concise
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Use pytest for testing

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update examples if needed

## Questions?

Feel free to open an issue for any questions or clarifications!
