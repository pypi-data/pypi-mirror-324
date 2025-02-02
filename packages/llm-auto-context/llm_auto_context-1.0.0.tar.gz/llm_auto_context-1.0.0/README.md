# Auto-Context

A CLI tool for generating code snapshots for LLM context windows.

## Installation

Using UV (recommended):
```bash
uv pip install llm-auto-context
```

Using pip:
```bash
pip install llm-auto-context
```

## Usage

Basic usage:
```bash
codesnapshot
```

This will use the default config file `.codesnapshot.json` in your current directory.

### Configuration

Create a `.codesnapshot.json` file in your project root:

```json
{
    "directories": ["src", "lib"],
    "output_file": "code_snapshot.md",
    "include_extensions": [".py", ".js", ".ts"],
    "exclude_dirs": ["node_modules", ".git", "build"],
    "exclude_files": ["secrets.env"]
}
```

### CLI Options

- `--config`: Path to config file (default: .codesnapshot.json)
- `-d, --directory`: Override directories to scan (can be used multiple times)
- `-o, --output`: Override output file path
- `--include`: Override file extensions to include (can be used multiple times)
- `--exclude-dir`: Additional directories to exclude (can be used multiple times)
- `--exclude-file`: Additional files to exclude (can be used multiple times)

Example:
```bash
codesnapshot -d src -d lib -o snapshot.md --exclude-dir tests
```

## Development

1. Clone the repository
2. Create a virtual environment:
```bash
uv venv
```

3. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## License

MIT