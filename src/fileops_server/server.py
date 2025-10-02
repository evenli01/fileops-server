"""File operations MCP server with tools for common file processing tasks."""

import os
import glob
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field


class ConfigSchema(BaseModel):
    """Configuration schema for the file operations server."""
    base_path: str = Field(
        default=".",
        description="Base directory path for file operations (defaults to current directory)"
    )
    max_file_size: int = Field(
        default=1048576,  # 1MB
        description="Maximum file size in bytes to read (default: 1MB)"
    )


@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and return a FastMCP server instance for file operations."""
    
    server = FastMCP(name="File Operations Server")

    @server.tool()
    def read_file(file_path: str, ctx: Context) -> str:
        """Read and return the contents of a text file.
        
        Args:
            file_path: Path to the file to read (relative to base_path)
            ctx: Context containing session configuration
            
        Returns:
            The contents of the file as a string
        """
        config = ctx.session_config
        base_path = Path(config.base_path)
        full_path = base_path / file_path
        
        # Security check: ensure the path doesn't escape base_path
        try:
            full_path = full_path.resolve()
            base_path = base_path.resolve()
            if not str(full_path).startswith(str(base_path)):
                return f"Error: Access denied - path escapes base directory"
        except Exception as e:
            return f"Error resolving path: {str(e)}"
        
        # Check file size
        try:
            file_size = full_path.stat().st_size
            if file_size > config.max_file_size:
                return f"Error: File size ({file_size} bytes) exceeds maximum ({config.max_file_size} bytes)"
        except FileNotFoundError:
            return f"Error: File not found: {file_path}"
        except Exception as e:
            return f"Error checking file: {str(e)}"
        
        # Read file
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            return f"Error: File is not a valid text file (encoding issue)"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @server.tool()
    def list_directory(directory_path: str = ".", pattern: str = "*", ctx: Context = None) -> str:
        """List files and directories in a specified path.
        
        Args:
            directory_path: Path to the directory to list (relative to base_path)
            pattern: Glob pattern to filter results (default: "*" for all files)
            ctx: Context containing session configuration
            
        Returns:
            A formatted string listing files and directories
        """
        config = ctx.session_config
        base_path = Path(config.base_path)
        full_path = base_path / directory_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            base_path = base_path.resolve()
            if not str(full_path).startswith(str(base_path)):
                return f"Error: Access denied - path escapes base directory"
        except Exception as e:
            return f"Error resolving path: {str(e)}"
        
        # List directory
        try:
            if not full_path.is_dir():
                return f"Error: Not a directory: {directory_path}"
            
            items = []
            for item in sorted(full_path.glob(pattern)):
                rel_path = item.relative_to(full_path)
                if item.is_dir():
                    items.append(f"[DIR]  {rel_path}/")
                else:
                    size = item.stat().st_size
                    items.append(f"[FILE] {rel_path} ({size} bytes)")
            
            if not items:
                return f"No items found matching pattern '{pattern}' in {directory_path}"
            
            return f"Contents of {directory_path}:\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    @server.tool()
    def search_in_files(
        search_term: str,
        directory_path: str = ".",
        file_pattern: str = "*.txt",
        ctx: Context = None
    ) -> str:
        """Search for a term in files matching a pattern.
        
        Args:
            search_term: The text to search for
            directory_path: Directory to search in (relative to base_path)
            file_pattern: Glob pattern for files to search (default: "*.txt")
            ctx: Context containing session configuration
            
        Returns:
            A formatted string with search results
        """
        config = ctx.session_config
        base_path = Path(config.base_path)
        full_path = base_path / directory_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            base_path = base_path.resolve()
            if not str(full_path).startswith(str(base_path)):
                return f"Error: Access denied - path escapes base directory"
        except Exception as e:
            return f"Error resolving path: {str(e)}"
        
        # Search files
        try:
            if not full_path.is_dir():
                return f"Error: Not a directory: {directory_path}"
            
            results = []
            file_count = 0
            match_count = 0
            
            for file_path in full_path.rglob(file_pattern):
                if not file_path.is_file():
                    continue
                
                # Skip files that are too large
                if file_path.stat().st_size > config.max_file_size:
                    continue
                
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_term in line:
                                rel_path = file_path.relative_to(full_path)
                                results.append(f"{rel_path}:{line_num}: {line.strip()}")
                                match_count += 1
                except (UnicodeDecodeError, PermissionError):
                    continue
            
            if not results:
                return f"No matches found for '{search_term}' in {file_count} files"
            
            header = f"Found {match_count} matches in {file_count} files searched:\n\n"
            return header + "\n".join(results[:50])  # Limit to first 50 results
        except Exception as e:
            return f"Error searching files: {str(e)}"

    @server.tool()
    def get_file_info(file_path: str, ctx: Context) -> str:
        """Get detailed information about a file.
        
        Args:
            file_path: Path to the file (relative to base_path)
            ctx: Context containing session configuration
            
        Returns:
            A formatted string with file information
        """
        config = ctx.session_config
        base_path = Path(config.base_path)
        full_path = base_path / file_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            base_path = base_path.resolve()
            if not str(full_path).startswith(str(base_path)):
                return f"Error: Access denied - path escapes base directory"
        except Exception as e:
            return f"Error resolving path: {str(e)}"
        
        # Get file info
        try:
            if not full_path.exists():
                return f"Error: File not found: {file_path}"
            
            stat = full_path.stat()
            info = [
                f"File: {file_path}",
                f"Type: {'Directory' if full_path.is_dir() else 'File'}",
                f"Size: {stat.st_size} bytes",
                f"Modified: {stat.st_mtime}",
                f"Permissions: {oct(stat.st_mode)[-3:]}",
            ]
            
            if full_path.is_file():
                # Try to determine if it's a text file
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        first_chars = f.read(100)
                        info.append(f"Text file: Yes")
                        info.append(f"Preview: {first_chars[:50]}...")
                except UnicodeDecodeError:
                    info.append(f"Text file: No (binary file)")
            
            return "\n".join(info)
        except Exception as e:
            return f"Error getting file info: {str(e)}"

    @server.tool()
    def count_lines(file_path: str, ctx: Context) -> str:
        """Count the number of lines in a text file.
        
        Args:
            file_path: Path to the file (relative to base_path)
            ctx: Context containing session configuration
            
        Returns:
            The number of lines in the file
        """
        config = ctx.session_config
        base_path = Path(config.base_path)
        full_path = base_path / file_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            base_path = base_path.resolve()
            if not str(full_path).startswith(str(base_path)):
                return f"Error: Access denied - path escapes base directory"
        except Exception as e:
            return f"Error resolving path: {str(e)}"
        
        # Count lines
        try:
            if not full_path.is_file():
                return f"Error: Not a file: {file_path}"
            
            # Check file size
            if full_path.stat().st_size > config.max_file_size:
                return f"Error: File too large to process"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            
            return f"File '{file_path}' has {line_count} lines"
        except UnicodeDecodeError:
            return f"Error: File is not a valid text file"
        except Exception as e:
            return f"Error counting lines: {str(e)}"

    return server
