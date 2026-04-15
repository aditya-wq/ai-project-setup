# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-15

### Added

- **Core Compression Engine**
  - LLM-based text compression with configurable models
  - Automatic file type detection
  - Structural preservation (code blocks, headings, URLs, paths)
  - Multi-layer validation system

- **Agent Integration**
  - Claude Code hook (SessionStart integration)
  - Mode tracking system (lite, full, ultra, wenyan)
  - Status badge support
  - Hook auto-activation

- **Configuration Management**
  - Environment variable support
  - Singleton settings pattern
  - .env file loading
  - Environment-specific settings

- **Validation System**
  - Heading extraction and validation
  - Code block preservation
  - URL and path extraction
  - Bullet point counting and validation

- **CLI Interface**
  - Command-line compression tool
  - Backup creation
  - Progress reporting
  - Error handling

- **Documentation**
  - Comprehensive README with architecture overview
  - CONTRIBUTING guide with development workflow
  - API documentation from docstrings
  - Benchmark results

- **Testing Infrastructure**
  - Unit tests with >90% coverage target
  - Integration tests for compression workflows
  - End-to-end tests for complete scenarios
  - pytest configuration

- **CI/CD Pipelines**
  - GitHub Actions for testing (Python 3.10-3.12)
  - Linting with Ruff, Black, MyPy
  - Documentation validation
  - Automated releases to PyPI

### Changed

- Refactored from original Caveman codebase with neutral branding
- Removed all human names, personal credits, and original branding
- Improved error handling and logging
- Enhanced configuration management
- Added comprehensive docstrings

### Removed

- Original Caveman-specific naming and branding
- Personal attribution from source code

## [0.0.0] - 2026-04-14

### Added

- Initial extraction from Caveman repository
- Base compression functionality
- Validation system
- Agent hooks
