"""
CSS Test Helper Utilities
Common functionality for CSS testing across all test files
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from django.contrib.staticfiles import finders


class CSSTestUtils:

    @staticmethod
    def find_css_file(filename: str) -> Optional[str]:
        """
        Find CSS file using Django staticfiles finders
        Args:
            filename: CSS filename (e.g., 'variables.css' or 'css/variables.css')
        Returns:
            Full path to CSS file or None if not found
        """
        # Try with css/ prefix if not already present
        if not filename.startswith("css/"):
            filename = f"css/{filename}"

        return finders.find(filename)

    @staticmethod
    def read_css_file(filename: str) -> str:
        """
        Read CSS file content safely
        Args:
            filename: CSS filename
        Returns:
            File content as string, empty string if file not found
        """
        file_path = CSSTestUtils.find_css_file(filename)
        if not file_path or not os.path.exists(file_path):
            return ""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    @staticmethod
    def extract_css_classes(css_content: str) -> List[str]:
        """
        Extract all CSS class definitions from content
        Args:
            css_content: CSS file content
        Returns:
            List of class names (without the . prefix)
        """
        # Match CSS class selectors
        class_pattern = r"\.([a-zA-Z][a-zA-Z0-9_-]*)"
        classes = re.findall(class_pattern, css_content)
        return list(set(classes))  # Remove duplicates

    @staticmethod
    def find_hardcoded_values(
        css_content: str, exclude_patterns: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Find hardcoded values that should potentially be CSS variables
        Args:
            css_content: CSS file content
            exclude_patterns: List of patterns to exclude (e.g., ['1px', '0px'])
        Returns:
            Dictionary with categories of hardcoded values found
        """
        exclude_patterns = exclude_patterns or ["0px", "1px", "100%", "0%"]

        patterns = {
            "colors": r"#[0-9a-fA-F]{3,6}",
            "pixels": r"\b\d+(?:\.\d+)?px\b",
            "rems": r"\b\d+(?:\.\d+)?rem\b",
            "ems": r"\b\d+(?:\.\d+)?em\b",
            "percentages": r"\b\d+(?:\.\d+)?%\b",
            "border_radius": r"border-radius:\s*\d+(?:\.\d+)?(?:px|rem|em|%)",
        }

        results = {}
        for category, pattern in patterns.items():
            matches = re.findall(pattern, css_content)
            # Filter out excluded patterns
            filtered_matches = [
                match
                for match in matches
                if not any(exclude in match for exclude in exclude_patterns)
            ]
            if filtered_matches:
                results[category] = list(set(filtered_matches))

        return results

    @staticmethod
    def count_css_variables(css_content: str) -> int:
        """
        Count CSS variable usage in content
        Args:
            css_content: CSS file content
        Returns:
            Number of CSS variable references found
        """
        variable_pattern = r"var\(--[a-zA-Z0-9-]+\)"
        variables = re.findall(variable_pattern, css_content)
        return len(variables)

    @staticmethod
    def detect_button_patterns(css_content: str) -> Dict[str, List[str]]:
        """
        Detect button class patterns and analyze usage
        Args:
            css_content: CSS file content
        Returns:
            Dictionary with button patterns categorized
        """
        patterns = {
            "button_classes": r"\.btn(?:-[a-zA-Z0-9-]+)?",
            "button_properties": r"(\.[\w-]+)\s*\{[^}]*(?:padding|border|background)[^}]*\}",
            "button_utility_classes": r"\.(?:btn|button)(?:-[a-zA-Z0-9-]+)*",
        }

        results = {}
        for category, pattern in patterns.items():
            matches = re.findall(pattern, css_content)
            if matches:
                results[category] = list(set(matches))

        return results

    @staticmethod
    def validate_css_syntax(css_content: str) -> Tuple[bool, List[str]]:
        """
        Basic CSS syntax validation
        Args:
            css_content: CSS file content
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check for matching braces
        open_braces = css_content.count("{")
        close_braces = css_content.count("}")
        if open_braces != close_braces:
            errors.append(
                f"Mismatched braces: {open_braces} opening, {close_braces} closing"
            )

        # Check for empty selectors
        empty_selectors = re.findall(r"([^}]+)\{\s*\}", css_content)
        if empty_selectors:
            errors.append(f"Empty selectors found: {len(empty_selectors)}")

        # Check for duplicate semicolons
        duplicate_semicolons = re.findall(r";;+", css_content)
        if duplicate_semicolons:
            errors.append(f"Duplicate semicolons found: {len(duplicate_semicolons)}")

        return len(errors) == 0, errors

    @staticmethod
    def extract_css_variables_definitions(css_content: str) -> Dict[str, str]:
        """
        Extract CSS variable definitions with their values
        Args:
            css_content: CSS file content
        Returns:
            Dictionary mapping variable names to their values
        """
        # Match CSS variable definitions
        variable_pattern = r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);"
        matches = re.findall(variable_pattern, css_content)
        return dict(matches)

    @staticmethod
    def find_unused_css_classes(css_content: str, template_content: str) -> List[str]:
        """
        Find CSS classes that are defined but not used in templates
        Args:
            css_content: CSS file content
            template_content: Combined template content to search
        Returns:
            List of unused class names
        """
        defined_classes = CSSTestUtils.extract_css_classes(css_content)
        unused_classes = []

        for class_name in defined_classes:
            # Check if class is used in templates
            if class_name not in template_content:
                unused_classes.append(class_name)

        return unused_classes

    @staticmethod
    def get_css_file_size_stats(filename: str) -> Dict[str, any]:
        """
        Get size statistics for a CSS file
        Args:
            filename: CSS filename
        Returns:
            Dictionary with file size statistics
        """
        file_path = CSSTestUtils.find_css_file(filename)
        if not file_path or not os.path.exists(file_path):
            return {"error": "File not found"}

        content = CSSTestUtils.read_css_file(filename)

        return {
            "file_size_bytes": os.path.getsize(file_path),
            "lines_total": len(content.split("\n")),
            "lines_non_empty": len(
                [line for line in content.split("\n") if line.strip()]
            ),
            "css_rules": len(re.findall(r"\{[^}]*\}", content)),
            "css_variables_count": CSSTestUtils.count_css_variables(content),
            "classes_count": len(CSSTestUtils.extract_css_classes(content)),
        }
