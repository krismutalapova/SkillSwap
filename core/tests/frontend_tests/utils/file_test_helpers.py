"""
File Test Helper Utilities
Common file operations for testing
"""

import os
from pathlib import Path
from typing import List, Optional
from django.conf import settings
from django.contrib.staticfiles import finders


class FileTestUtils:
    """Utility class for file operations in tests"""

    @staticmethod
    def get_project_root() -> Path:
        """
        Get consistent project root path

        Returns:
            Path object pointing to project root
        """
        # Get the directory containing manage.py
        current_file = Path(__file__)
        # Navigate up from utils/ → frontend_tests/ → tests/ → core/ → project_root/
        return current_file.parent.parent.parent.parent.parent

    @staticmethod
    def get_file_size(file_path) -> int | None:
        """
        Get file size in bytes
        Args:
            file_path: Path object or string path to file
        Returns:
            File size in bytes, or None if file doesn't exist
        """
        try:
            if hasattr(file_path, "stat"):
                return file_path.stat().st_size
            else:
                return Path(file_path).stat().st_size
        except (OSError, FileNotFoundError):
            return None

    @staticmethod
    def read_static_file(file_path: str) -> str:
        """
        Read file from static directory with error handling
        Args:
            file_path: Relative path to file in static directory
        Returns:
            File content as string, empty string if error
        """
        try:
            found_file = finders.find(file_path)
            if found_file and os.path.exists(found_file):
                with open(found_file, "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception as e:
            print(f"Error reading static file {file_path}: {e}")
            return ""

    @staticmethod
    def read_file_safe(file_path: Path) -> str:
        """
        Read any file safely with error handling
        Args:
            file_path: Path object or string path to file
        Returns:
            File content as string, empty string if error
        """
        try:
            file_path = Path(file_path)
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    @staticmethod
    def list_css_files() -> List[str]:
        """
        List all CSS files in static directory
        Returns:
            List of CSS file paths relative to static directory
        """
        css_files = []
        project_root = FileTestUtils.get_project_root()
        static_css_dir = project_root / "static" / "css"

        if static_css_dir.exists():
            for css_file in static_css_dir.glob("*.css"):
                css_files.append(f"css/{css_file.name}")

        return sorted(css_files)

    @staticmethod
    def list_template_files() -> List[Path]:
        """
        List all template files in the project
        Returns:
            List of Path objects pointing to template files
        """
        template_files = []
        project_root = FileTestUtils.get_project_root()
        templates_dir = project_root / "core" / "templates"

        if templates_dir.exists():
            # Find all .html files recursively
            for template_file in templates_dir.rglob("*.html"):
                template_files.append(template_file)

        return sorted(template_files)

    @staticmethod
    def get_static_dir() -> Path:
        """
        Get the static files directory path
        Returns:
            Path object pointing to static directory
        """
        return FileTestUtils.get_project_root() / "static"

    @staticmethod
    def get_templates_dir() -> Path:
        """
        Get the templates directory path
        Returns:
            Path object pointing to templates directory
        """
        return FileTestUtils.get_project_root() / "core" / "templates"

    @staticmethod
    def file_exists_in_static(file_path: str) -> bool:
        """
        Check if file exists in static directory
        Args:
            file_path: Relative path to file in static directory
        Returns:
            True if file exists, False otherwise
        """
        found_file = finders.find(file_path)
        return found_file is not None and os.path.exists(found_file)

    @staticmethod
    def get_file_stats(file_path: Path) -> dict:
        """
        Get basic statistics about a file
        Args:
            file_path: Path to the file
        Returns:
            Dictionary with file statistics
        """
        try:
            if not file_path.exists():
                return {"error": "File not found"}

            stat = file_path.stat()
            content = FileTestUtils.read_file_safe(file_path)

            return {
                "size_bytes": stat.st_size,
                "lines_total": len(content.split("\n")) if content else 0,
                "lines_non_empty": (
                    len([line for line in content.split("\n") if line.strip()])
                    if content
                    else 0
                ),
                "character_count": len(content),
                "exists": True,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def find_files_by_pattern(directory: Path, pattern: str) -> List[Path]:
        """
        Find files matching a pattern in a directory
        Args:
            directory: Directory to search in
            pattern: Glob pattern to match (e.g., '*.css', '**/*.html')
        Returns:
            List of Path objects matching the pattern
        """
        try:
            if directory.exists():
                return list(directory.glob(pattern))
            return []
        except Exception:
            return []

    @staticmethod
    def read_multiple_files(file_paths: List[Path]) -> dict:
        """
        Read multiple files and return their contents
        Args:
            file_paths: List of Path objects to read
        Returns:
            Dictionary mapping file names to their contents
        """
        results = {}
        for file_path in file_paths:
            results[file_path.name] = FileTestUtils.read_file_safe(file_path)
        return results
