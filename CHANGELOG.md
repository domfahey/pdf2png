# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of pdf2png CLI tool
- Support for converting scanned PDF pages to lossless PNG images
- Command-line options for custom prefixes and overwrite behavior
- Comprehensive test suite with pytest
- Type checking with mypy
- Code formatting and linting with ruff
- CI/CD pipeline with GitHub Actions

### Changed
- Adopted src/ layout for proper Python packaging structure
- Migrated to modern pyproject.toml configuration with PEP 621 compliance
- Replaced legacy requirements.txt files with dependency-groups in pyproject.toml
- Renamed AGENTS.md to CONTRIBUTING.md following standard conventions
- Reorganized sample files into examples/ directory
- Enhanced .gitignore with comprehensive Python development patterns
- Updated Makefile for modern UV/Python workflow

### Added
- GitHub Actions CI/CD pipeline for automated testing, linting, and security checks
- Pre-commit hooks configuration for code quality enforcement
- SECURITY.md for responsible disclosure policy
- Enhanced CONTRIBUTING.md with development setup and PR guidelines
- Ruff configuration for consistent code styling and linting
- MyPy strict mode configuration for type checking
- UV-based tooling integration for dependency management
- Comprehensive dependency version pinning in pyproject.toml
- Script entry points for package installs
- CHANGELOG.md for version tracking

### Fixed
- Lint issues and type checking warnings
- Import path updates to support new package structure
- Test dependencies and coverage configuration improvements

### Security
- Input validation improvements for PDF file processing
- Secure coding practices applied throughout codebase
- Dependency vulnerability scanning in CI/CD pipeline
