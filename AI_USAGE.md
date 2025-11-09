# AI Usage Records

This file documents all AI-assisted contributions to the PyGraphile project, promoting transparency and accountability.

## Purpose

We believe in transparency when it comes to AI-assisted development. This file tracks:
- Which changes were made with AI assistance
- What those changes accomplish
- Who was responsible for the contribution

## Format

Each entry should include:
- **Date**: When the contribution was made
- **Contributor**: GitHub username
- **AI Tool**: Which AI tool was used (e.g., GitHub Copilot, ChatGPT, etc.)
- **Changes Made**: Description of what was changed
- **Explanation**: What the changes do (in contributor's own words)
- **Commit(s)**: Related commit hash(es)

---

## Contribution Records

### 2025-11-09 - Initial Package Structure

**Contributor**: @copilot (GitHub Copilot Workspace Agent)  
**AI Tool**: GitHub Copilot Workspace  
**Commit**: 27bbaa4

**Changes Made**:
- Project initialization using `uv init --lib`
- Complete package structure setup with src-layout
- Configuration files (pyproject.toml, .python-version, .gitattributes)
- Documentation files (README.md, LICENSE, CONTRIBUTING.md)
- Test infrastructure (tests/ directory with basic tests)
- Directory structure (src/pygraphile/, examples/, docs/, .github/workflows/)

**What These Changes Do**:
This AI-generated contribution established the foundational structure for the PyGraphile package. It created a modern Python package using the src-layout pattern, which separates source code from tests and configuration. The package is configured to work with both `uv` (a fast Python package manager) and traditional `pip`, ensuring broad compatibility. 

Key components include:
- **src/pygraphile/**: Main package directory containing `__init__.py` with package metadata
- **pyproject.toml**: Project configuration defining dependencies, build system (hatchling for pip compatibility), development tools (pytest, ruff), and project metadata
- **LICENSE**: MIT license for open-source distribution
- **README.md**: User-facing documentation with installation instructions, features, and roadmap
- **CONTRIBUTING.md**: Guidelines for contributors on how to set up development environment and contribute code
- **tests/**: Test infrastructure using pytest with basic validation tests
- **py.typed**: Marker file indicating the package supports type hints (PEP 561)

The structure follows Python packaging best practices and provides a solid foundation for building the GraphQL API generation features.

---

## Guidelines for Future Entries

When adding entries to this file:

1. **Be Specific**: Clearly state what files or features were modified/created
2. **Own Your Work**: Even if AI generated code, you must understand and explain it
3. **No AI Explanations**: The "Explanation" section must be written by you, not AI
4. **Be Honest**: Disclose the full extent of AI involvement
5. **Update Promptly**: Add entries when you submit your PR, not after merge

---

## Questions?

If you're unsure whether to disclose AI usage or how to format your entry, feel free to ask in your pull request or open an issue.
