# File Operations MCP Server

A Model Context Protocol (MCP) server that provides tools for common file processing operations. Built with FastMCP and ready for deployment on Smithery.

## Features

This server provides the following file operation tools:

- **read_file**: Read and return the contents of text files
- **list_directory**: List files and directories with optional glob pattern filtering
- **search_in_files**: Search for text across multiple files with pattern matching
- **get_file_info**: Get detailed information about files (size, type, permissions, etc.)
- **count_lines**: Count the number of lines in text files

## Configuration

The server supports session-specific configuration:

- **base_path**: Base directory for file operations (default: current directory)
- **max_file_size**: Maximum file size in bytes to process (default: 1MB)

## Security Features

- Path traversal protection (prevents accessing files outside base_path)
- File size limits to prevent memory issues
- Binary file detection and handling
- Error handling for permissions and encoding issues

## Local Development

### Prerequisites

- Python 3.12 or higher
- `uv` (recommended), `poetry`, or `pip` package manager

### Setup

1. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Using poetry
   poetry install
   
   # Using pip
   pip install -e .
   ```

2. Run the development server with interactive playground:
   ```bash
   # Using uv
   uv run playground
   
   # Using poetry
   poetry run playground
   ```

3. Or run the server without playground:
   ```bash
   # Using uv
   uv run dev
   
   # Using poetry
   poetry run dev
   ```

The playground provides an interactive interface to test all server tools in real-time.

## Deployment to Smithery

### Prerequisites

- GitHub account
- Smithery account (connect at [smithery.ai](https://smithery.ai))

### Steps

1. **Initialize Git repository** (if not already done):
   ```bash
   cd fileops-server
   git init
   git add .
   git commit -m "Initial commit: File operations MCP server"
   ```

2. **Create GitHub repository**:
   - Go to [github.com](https://github.com) and create a new repository
   - Follow GitHub's instructions to push your local repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/fileops-server.git
   git branch -M main
   git push -u origin main
   ```

3. **Connect to Smithery**:
   - Visit [smithery.ai](https://smithery.ai)
   - Connect your GitHub account
   - Find your `fileops-server` repository

4. **Deploy**:
   - Navigate to the Deployments tab on your server page
   - Click "Deploy" to build and host your server
   - Smithery will automatically containerize and deploy your server

### Post-Deployment

Once deployed, you can:
- Share your server with others
- Configure per-user settings (base_path, max_file_size)
- Monitor usage and logs through the Smithery dashboard
- Update the server by pushing changes to GitHub

## Project Structure

```
fileops-server/
├── smithery.yaml              # Smithery runtime configuration
├── pyproject.toml            # Python project configuration
├── README.md                 # This file
└── src/
    └── fileops_server/
        ├── __init__.py       # Package initialization
        └── server.py         # MCP server implementation
```

## Usage Examples

### Read a File
```python
# Tool: read_file
# Parameters: file_path="example.txt"
# Returns: Contents of example.txt
```

### List Directory
```python
# Tool: list_directory
# Parameters: directory_path=".", pattern="*.py"
# Returns: List of all Python files in the directory
```

### Search in Files
```python
# Tool: search_in_files
# Parameters: search_term="TODO", directory_path=".", file_pattern="*.py"
# Returns: All lines containing "TODO" in Python files
```

### Get File Info
```python
# Tool: get_file_info
# Parameters: file_path="example.txt"
# Returns: Detailed file information (size, type, permissions, etc.)
```

### Count Lines
```python
# Tool: count_lines
# Parameters: file_path="example.txt"
# Returns: Number of lines in the file
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
