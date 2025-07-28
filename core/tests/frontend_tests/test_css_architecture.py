"""
CSS Architecture Testing
Tests for CSS file organization, structure, and architecture validation

This file contains tests focusing specifically on CSS architecture, file organization, and structural validation.
"""

import re
import os
from pathlib import Path
from core.tests.frontend_tests.utils import CSSTestCase, CSSTestUtils, FileTestUtils


class CSSFileStructureTests(CSSTestCase):
    def test_css_file_organization(self):
        expected_css_files = [
            "variables.css",
            "utilities.css",
            "base.css",
            "components.css",
            "skill-pages.css",
            "messaging-pages.css",
            "profile-pages.css",
            "home-pages.css",
            "auth-pages.css",
            "search-page.css",
            "error-pages.css",
        ]

        for css_file in expected_css_files:
            with self.subTest(css_file=css_file):
                self.assertCSSFileExists(css_file)

    def test_file_size_optimization(self):
        # Size limits in KB
        size_limits = {
            "variables.css": 50,
            "utilities.css": 100,
            "base.css": 30,
            "components.css": 80,
            "skill-pages.css": 60,
            "messaging-pages.css": 40,
            "profile-pages.css": 50,
            "home-pages.css": 40,
            "auth-pages.css": 30,
            "search-page.css": 40,
            "error-pages.css": 20,
        }

        for css_file, max_size_kb in size_limits.items():
            with self.subTest(css_file=css_file):
                stats = self.css_utils.get_css_file_size_stats(css_file)
                if "error" not in stats:
                    size_kb = stats["file_size_bytes"] / 1024
                    self.assertLessEqual(
                        size_kb,
                        max_size_kb,
                        f"CSS file {css_file} should be under {max_size_kb}KB, but is {size_kb:.1f}KB",
                    )

    def test_css_syntax_validation(self):
        for css_file in self.css_files:
            with self.subTest(css_file=css_file):
                content = self.css_utils.read_css_file(css_file)
                if content:
                    self.assertValidCSSSyntax(content, css_file)

    def test_import_dependencies(self):
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Find @import statements
                    import_pattern = r'@import\s+["\']([^"\']+)["\']'
                    imports = re.findall(import_pattern, content)

                    for imported_file in imports:
                        # Check if imported file exists
                        imported_path = self.css_utils.find_css_file(imported_file)
                        self.assertIsNotNone(
                            imported_path,
                            f"CSS file {css_file} imports {imported_file} which cannot be found",
                        )


class CSSNamingConventionTests(CSSTestCase):
    def test_class_naming_consistency(self):
        naming_violations = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)

                for class_name in classes:
                    # Check for consistent naming patterns
                    if not self._is_valid_class_name(class_name):
                        naming_violations.append(f"{css_file}: {class_name}")

        if naming_violations:
            self.fail(
                f"CSS class naming violations found:\n"
                + "\n".join(naming_violations[:10])
            )

    def test_utility_class_patterns(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")
        if utilities_content:
            classes = self.css_utils.extract_css_classes(utilities_content)

            # Expected utility class patterns
            expected_patterns = [
                r"^btn(-[\w-]+)?$",
                r"^text-(xs|sm|md|lg|xl|2xl)$",
                r"^p-\w+$",
                r"^m-\w+$",
                r"^flex-\w+$",
            ]

            utility_classes = [cls for cls in classes if self._is_utility_class(cls)]

            for utility_class in utility_classes:
                matches_pattern = any(
                    re.match(pattern, utility_class) for pattern in expected_patterns
                )

                if not matches_pattern and not self._is_component_class(utility_class):
                    # This is informational, not a failure
                    print(
                        f"Note: Utility class '{utility_class}' doesn't match expected patterns"
                    )

    def test_component_class_patterns(self):
        components_content = self.css_utils.read_css_file("components.css")
        if components_content:
            classes = self.css_utils.extract_css_classes(components_content)

            # Component classes should be descriptive and follow BEM-like patterns
            for class_name in classes:
                # Should not be utility-style classes in components.css
                self.assertFalse(
                    self._is_utility_class(class_name),
                    f"Utility-style class '{class_name}' should not be in components.css",
                )

    def _is_valid_class_name(self, class_name: str) -> bool:
        if "_" in class_name and not class_name.startswith("__"):
            return False

        # Should not start with numbers
        if class_name[0].isdigit():
            return False

        # Should contain only valid characters
        if not re.match(r"^[a-zA-Z0-9_-]+$", class_name):
            return False

        return True

    def _is_utility_class(self, class_name: str) -> bool:
        utility_prefixes = [
            "btn-",
            "text-",
            "p-",
            "m-",
            "pt-",
            "pb-",
            "pl-",
            "pr-",
            "mt-",
            "mb-",
            "ml-",
            "mr-",
            "flex-",
            "grid-",
            "w-",
            "h-",
            "bg-",
            "border-",
            "rounded-",
            "shadow-",
        ]

        return any(class_name.startswith(prefix) for prefix in utility_prefixes)

    def _is_component_class(self, class_name: str) -> bool:
        component_keywords = [
            "card",
            "modal",
            "nav",
            "form",
            "skill",
            "profile",
            "message",
            "user",
            "rating",
            "badge",
            "section",
            "container",
            "wrapper",
        ]

        return any(keyword in class_name.lower() for keyword in component_keywords)


class CSSArchitectureValidationTests(CSSTestCase):
    def test_css_layers_separation(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        variables_defined = len(
            self.css_utils.extract_css_variables_definitions(variables_content)
        )

        self.assertGreater(
            variables_defined,
            50,
            "variables.css should define a substantial number of CSS variables",
        )

        # Other files shouldn't define many variables
        for css_file in ["utilities.css", "base.css", "components.css"]:
            content = self.css_utils.read_css_file(css_file)
            if content:
                variables_in_file = len(
                    self.css_utils.extract_css_variables_definitions(content)
                )
                self.assertLessEqual(
                    variables_in_file,
                    5,
                    f"File {css_file} should not define many CSS variables (found {variables_in_file}). "
                    f"Variables should be in variables.css",
                )

    def test_utility_classes_available(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")
        if not utilities_content:
            self.skipTest("utilities.css not found")

        classes = self.css_utils.extract_css_classes(utilities_content)

        # Essential utility categories that should be present
        essential_categories = {
            "buttons": ["btn-base", "btn-primary-colors", "btn-secondary-colors"],
            "text": ["text-center", "text-left", "text-right"],
            "spacing": ["m-0", "p-0", "mt-sm", "mb-sm"],
            "layout": ["flex-center", "flex-between"],
            "display": ["hidden", "visible"],
        }

        for category, expected_classes in essential_categories.items():
            with self.subTest(category=category):
                found_classes = [cls for cls in expected_classes if cls in classes]

                if len(found_classes) == 0:
                    self.fail(
                        f"No {category} utility classes found. Expected at least some of: {expected_classes}"
                    )

    def test_css_consistency_across_files(self):
        all_classes = {}

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)
                for class_name in classes:
                    if class_name not in all_classes:
                        all_classes[class_name] = []
                    all_classes[class_name].append(css_file)

        # Find classes that appear in multiple files (potential duplication)
        duplicated_classes = {
            class_name: files
            for class_name, files in all_classes.items()
            if len(files) > 1
        }

        # Some duplication is acceptable (like base styles), but excessive duplication isn't
        excessive_duplicates = [
            class_name
            for class_name, files in duplicated_classes.items()
            if len(files) > 2 and not self._is_acceptable_duplicate(class_name)
        ]

        if excessive_duplicates:
            self.fail(
                f"Classes with excessive duplication found: {excessive_duplicates[:5]}. "
                f"Consider consolidating these classes."
            )

    def _is_acceptable_duplicate(self, class_name: str) -> bool:
        acceptable_duplicates = [
            "active",
            "disabled",
            "hidden",
            "visible",
            "error",
            "success",
            "container",
            "wrapper",
            "content",
        ]

        return class_name in acceptable_duplicates


class CSSPerformanceTests(CSSTestCase):
    def test_css_complexity_metrics(self):
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Count selectors, rules, and nesting depth
                    selectors = len(re.findall(r"[^{}]+\s*\{", content))

                    # Files shouldn't be overly complex
                    max_selectors = {
                        "variables.css": 10,
                        "utilities.css": 300,
                        "base.css": 100,
                        "components.css": 200,
                    }.get(css_file, 150)

                    self.assertLessEqual(
                        selectors,
                        max_selectors,
                        f"CSS file {css_file} has {selectors} selectors, "
                        f"which exceeds the recommended limit of {max_selectors}",
                    )

    def test_css_redundancy_detection(self):
        redundancy_issues = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for duplicate property declarations within the same file
                property_declarations = re.findall(r"(\w+)\s*:\s*([^;]+);", content)
                property_counts = {}

                for prop, value in property_declarations:
                    key = f"{prop}:{value.strip()}"
                    property_counts[key] = property_counts.get(key, 0) + 1

                # Find highly repeated property-value combinations
                high_repeats = [
                    (prop_value, count)
                    for prop_value, count in property_counts.items()
                    if count > 5
                ]

                if high_repeats:
                    redundancy_issues.append(
                        f"{css_file}: {len(high_repeats)} highly repeated patterns"
                    )

        # This is informational rather than a hard failure
        if redundancy_issues:
            print(f"CSS redundancy detected in: {', '.join(redundancy_issues)}")
            print(
                "Consider extracting common patterns to utility classes or CSS variables"
            )
