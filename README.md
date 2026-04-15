# AI Project

<p align="center">
  <strong>Text Compression and Optimization Toolkit for AI Agents</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/aiproject/ai-project?style=flat" alt="License"></a>
  <a href="https://github.com/aiproject/ai-project/releases"><img src="https://img.shields.io/github/v/release/aiproject/ai-project?style=flat" alt="Release"></a>
  <a href="https://github.com/aiproject/ai-project/actions"><img src="https://img.shields.io/github/actions/workflow/status/aiproject/ai-project/test.yml?style=flat" alt="Build"></a>
</p>

---

A production-ready toolkit for compressing AI agent output and context files, reducing token usage while preserving full technical accuracy.

## Features

- **Text Compression**: Compress natural language files to reduce token usage by ~46%
- **Structural Preservation**: Preserves code blocks, URLs, headings, and file paths
- **Agent Integration**: Hooks for Claude Code, Codex, and other AI agents
- **Validation**: Multi-layer validation ensures no content is lost
- **Configurable**: Environment-based configuration for all settings
- **Production-Ready**: Comprehensive error handling, logging, and testing

## Architecture Overview

```
ai-project/
├── src/ai_project/
│   ├── __init__.py           # Package initialization
│   ├── compression/          # Core compression modules
│   │   ├── __init__.py       # Compression orchestration
│   │   └── detect.py         # File type detection
│   ├── validators/           # Output validation
│   │   └── __init__.py       # Validation logic
│   ├── hooks/                # Agent integration
│   │   ├── __init__.py       # Hook utilities
│   │   └── aiproject-activate.js  # Claude Code hook
│   ├── config/               # Configuration management
│   │   ├── __init__.py       # Settings management
│   │   └── env.py            # Environment loader
│   ├── utils/                # Shared utilities
│   │   └── __init__.py       # Utility functions
│   └── cli.py                # CLI entry point
├── tests/                    # Test suites
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── docs/                     # Documentation
└── pyproject.toml           # Project configuration
```

## Installation

### Python Package

```bash
pip install ai-project
```

### Claude Code Plugin

```bash
claude plugin marketplace add aiproject/ai-project
claude plugin install aiproject@aiproject
```

### Standalone Hooks

```bash
# macOS / Linux / WSL
bash <(curl -s https://raw.githubusercontent.com/aiproject/ai-project/main/hooks/install.sh)

# Windows (PowerShell)
irm https://raw.githubusercontent.com/aiproject/ai-project/main/hooks/install.ps1 | iex
```

## Usage

### CLI

```bash
aiproject <filepath>
```

Example:
```bash
aiproject CLAUDE.md
```

This will:
1. Create a backup at `CLAUDE.original.md`
2. Compress the file content
3. Save compressed version to original path

### Python API

```python
from pathlib import Path
from ai_project import compress_file

success = compress_file(Path("CLAUDE.md"))
```

### Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AIPROJECT_MODEL` | `claude-sonnet-4-5` | LLM model to use |
| `AIPROJECT_MAX_FILE_SIZE` | `500000` | Max file size in bytes |
| `AIPROJECT_MAX_RETRIES` | `2` | Max validation retry attempts |
| `AIPROJECT_ENABLED` | `true` | Enable/disable compression |
| `AIPROJECT_HOOK_AUTO` | `true` | Auto-activate hooks |
| `AIPROJECT_DEFAULT_MODE` | `full` | Default compression intensity |
| `AIPROJECT_LOG_LEVEL` | `INFO` | Logging level |

## Benchmark Results

Real compression results on project documentation files:

| File Type | Original | Compressed | Savings |
|-----------|----------|------------|---------|
| Preferences | 706 tokens | 285 tokens | **59.6%** |
| Project Notes | 1145 tokens | 535 tokens | **53.3%** |
| Project Memory | 1122 tokens | 636 tokens | **43.3%** |
| Todo List | 627 tokens | 388 tokens | **38.1%** |
| Mixed Content | 888 tokens | 560 tokens | **36.9%** |
| **Average** | **898 tokens** | **481 tokens** | **46%** |

## Validation Rules

The compression process validates that these elements are preserved:

- **Code blocks**: Fenced code blocks (``` and ~~~) preserved exactly
- **Headings**: All heading text and order maintained
- **URLs**: All URLs preserved exactly
- **File paths**: All file paths preserved exactly
- **Bullet points**: Count difference must be <15%

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/aiproject/ai-project.git
cd ai-project

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src tests
black --check src tests
mypy src
```

### Running Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=ai_project --cov-report=html
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
