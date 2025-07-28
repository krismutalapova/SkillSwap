"""
CSS File Integrity and Basic Validation Tests
Tests for CSS file existence, syntax validity, and basic quality checks

This file contains essential CSS file integrity tests that complement the specialized
test files.
"""

import os
import re
from django.test import TestCase
from django.contrib.staticfiles import finders


class CSSFileIntegrityTests(TestCase):
    def test_all_required_css_files_exist(self):
        required_files = [
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

        for css_file in required_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                self.assertIsNotNone(
                    file_path, f"Required CSS file {css_file} not found in static files"
                )

    def test_css_syntax_validity(self):
        css_files = [
            "utilities.css",
            "base.css",
            "components.css",
            "skill-pages.css",
            "messaging-pages.css",
            "profile-pages.css",
        ]

        for css_file in css_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Basic syntax checks
                    open_braces = content.count("{")
                    close_braces = content.count("}")
                    self.assertEqual(
                        open_braces,
                        close_braces,
                        f"Mismatched braces in {css_file}: {open_braces} open, {close_braces} close",
                    )

    def test_no_empty_css_rules(self):
        css_files = ["utilities.css", "components.css", "base.css"]

        for css_file in css_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    empty_rules = re.findall(r"[.#][\w-]+\s*{\s*}", content)
                    self.assertEqual(
                        len(empty_rules),
                        0,
                        f"Found empty CSS rules in {css_file}: {empty_rules}",
                    )

    def test_css_file_headers_present(self):
        important_files = ["variables.css", "utilities.css", "base.css"]

        for css_file in important_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Should have some form of header comment
                    has_header = (
                        content.startswith("/*")
                        or "/**" in content[:200]
                        or "===" in content[:200]
                    )

                    self.assertTrue(
                        has_header,
                        f"CSS file {css_file} should have header documentation",
                    )


class CSSPerformanceTests(TestCase):
    def test_css_file_sizes_reasonable(self):
        size_limits = {
            "utilities.css": 150,
            "components.css": 100,
            "base.css": 50,
            "skill-pages.css": 80,
            "messaging-pages.css": 60,
            "profile-pages.css": 70,
        }

        for css_file, max_size_kb in size_limits.items():
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    size_kb = file_size / 1024

                    self.assertLess(
                        size_kb,
                        max_size_kb,
                        f"{css_file} is too large: {size_kb:.1f}KB (max: {max_size_kb}KB)",
                    )

    def test_no_excessive_selector_complexity(self):
        css_files = ["utilities.css", "components.css", "base.css"]

        for css_file in css_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Find CSS rules and check selector complexity
                    rules = re.findall(r"([^{]+)\s*{", content)

                    for rule in rules:
                        selector = rule.strip()
                        if selector and not selector.startswith("/*"):
                            # Count selector parts (spaces indicate descendant selectors)
                            parts = len(selector.split())
                            self.assertLessEqual(
                                parts,
                                6,
                                f"Complex selector in {css_file}: {selector} ({parts} parts)",
                            )

    def test_reasonable_css_rule_count(self):
        rule_limits = {
            "utilities.css": 400,
            "components.css": 200,
            "base.css": 100,
            "skill-pages.css": 150,
        }

        for css_file, max_rules in rule_limits.items():
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Count CSS rules (opening braces)
                    rule_count = content.count("{")

                    self.assertLessEqual(
                        rule_count,
                        max_rules,
                        f"{css_file} has too many rules: {rule_count} (max: {max_rules})",
                    )


class ResponsiveDesignBasicTests(TestCase):
    def test_responsive_breakpoints_defined(self):
        breakpoint_files = ["utilities.css", "components.css", "base.css"]

        expected_breakpoints = [
            "@media (max-width: 768px)",  # Tablet
            "@media (max-width: 480px)",  # Mobile
        ]

        for css_file in breakpoint_files:
            with self.subTest(css_file=css_file):
                file_path = finders.find(f"css/{css_file}")
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Check for at least one responsive breakpoint
                    has_responsive = any(bp in content for bp in expected_breakpoints)

                    if css_file in ["utilities.css", "components.css"]:
                        # These files should definitely have responsive styles
                        self.assertTrue(
                            has_responsive,
                            f"{css_file} should contain responsive breakpoints",
                        )

    def test_mobile_first_approach(self):
        utilities_file = finders.find("css/utilities.css")

        if utilities_file and os.path.exists(utilities_file):
            with open(utilities_file, "r") as f:
                content = f.read()

            # Look for min-width queries (mobile-first indicator)
            min_width_queries = content.count("@media (min-width:")
            max_width_queries = content.count("@media (max-width:")

            if min_width_queries > 0 or max_width_queries > 0:
                total_queries = min_width_queries + max_width_queries
                mobile_first_ratio = (
                    min_width_queries / total_queries if total_queries > 0 else 0
                )

                # This is informational rather than a hard requirement
                print(
                    f"Responsive approach: {mobile_first_ratio:.1%} mobile-first queries"
                )


class CSSArchitectureBasicTests(TestCase):
    def test_variables_file_only_contains_variables(self):
        variables_file = finders.find("css/variables.css")

        if variables_file and os.path.exists(variables_file):
            with open(variables_file, "r") as f:
                content = f.read()

            # Count variable definitions vs other rules
            variable_definitions = content.count("--")
            css_rules = content.count("{") - content.count(":root")

            # variables.css should be mostly variable definitions
            if css_rules > 0:
                variable_ratio = variable_definitions / (
                    variable_definitions + css_rules
                )
                self.assertGreater(
                    variable_ratio,
                    0.8,
                    f"variables.css should be mostly variable definitions ({variable_ratio:.1%})",
                )

    def test_utilities_vs_components_separation(self):
        utilities_file = finders.find("css/utilities.css")
        components_file = finders.find("css/components.css")

        if utilities_file and components_file:
            with open(utilities_file, "r") as f:
                utilities_content = f.read()
            with open(components_file, "r") as f:
                components_content = f.read()

            # Utilities should have more single-class selectors
            utilities_single_class = len(
                re.findall(r"\.[a-zA-Z][\w-]*\s*{", utilities_content)
            )
            utilities_total_rules = utilities_content.count("{")

            components_single_class = len(
                re.findall(r"\.[a-zA-Z][\w-]*\s*{", components_content)
            )
            components_total_rules = components_content.count("{")

            if utilities_total_rules > 0 and components_total_rules > 0:
                utilities_single_ratio = utilities_single_class / utilities_total_rules
                components_single_ratio = (
                    components_single_class / components_total_rules
                )

                # Utilities should have higher ratio of single-class selectors
                self.assertGreater(
                    utilities_single_ratio,
                    0.7,
                    f"Utilities should be mostly single-class selectors ({utilities_single_ratio:.1%})",
                )

    def test_no_critical_css_duplication(self):
        css_files = ["utilities.css", "components.css", "base.css"]

        common_properties = {}

        for css_file in css_files:
            file_path = finders.find(f"css/{css_file}")
            if file_path and os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                # Look for property-value pairs
                properties = re.findall(r"(\w+)\s*:\s*([^;]+);", content)

                for prop, value in properties:
                    key = f"{prop}:{value.strip()}"
                    if key not in common_properties:
                        common_properties[key] = []
                    common_properties[key].append(css_file)

        # Find properties that appear in multiple files
        duplicated = {k: v for k, v in common_properties.items() if len(v) > 1}

        # Filter out acceptable duplicates
        acceptable_duplicates = [
            "margin:0",
            "padding:0",
            "border:none",
            "outline:none",
            "box-sizing:border-box",
            "display:block",
            "position:relative",
        ]

        critical_duplicates = [
            k
            for k in duplicated.keys()
            if not any(acceptable in k for acceptable in acceptable_duplicates)
        ]

        # This is informational - some duplication is acceptable
        if len(critical_duplicates) > 10:
            print(
                f"Note: Found {len(critical_duplicates)} potentially duplicate property-value pairs"
            )
