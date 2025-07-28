"""
CSS Variables Testing
Consolidated tests for CSS variable definitions and usage across all files

This file consolidates CSS variable testing that was previously scattered across different tests
"""

from django.test import TestCase
from core.tests.frontend_tests.utils import CSSTestCase, CSSTestUtils, FileTestUtils


class CSSVariableDefinitionTests(CSSTestCase):
    def test_essential_variables_defined(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        self.assertGreater(
            len(variables_content), 0, "variables.css should not be empty"
        )

        # Essential color system variables
        required_color_variables = [
            "--color-primary",
            "--color-primary-gradient",
            "--color-secondary",
            "--color-text-primary",
            "--color-text-secondary",
            "--color-background",
            "--color-background-glass",
            "--color-border-light",
        ]

        self.assertCSSVariablesDefined(variables_content, required_color_variables)

    def test_spacing_system_completeness(self):
        variables_content = self.css_utils.read_css_file("variables.css")

        required_spacing_variables = [
            "--nav-link-padding",
            "--nav-link-padding-mobile",
            "--button-padding-small",
            "--button-padding-large",
            "--card-padding",
            "--form-field-padding",
            "--space-md",
        ]

        self.assertCSSVariablesDefined(variables_content, required_spacing_variables)

    def test_border_radius_system(self):
        variables_content = self.css_utils.read_css_file("variables.css")

        required_radius_variables = [
            "--radius-sm",
            "--radius-md",
            "--radius-lg",
            "--radius-circle",
        ]

        self.assertCSSVariablesDefined(variables_content, required_radius_variables)

    def test_no_circular_references(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        variable_definitions = self.css_utils.extract_css_variables_definitions(
            variables_content
        )

        for var_name, var_value in variable_definitions.items():
            self.assertNotIn(
                f"var({var_name})",
                var_value,
                f"Variable {var_name} should not reference itself",
            )


class CSSVariableUsageTests(CSSTestCase):
    def test_hardcoded_colors_replaced(self):
        # Skip variables.css as it's allowed to have hardcoded values
        css_files_to_test = [f for f in self.css_files if f != "variables.css"]

        for css_file in css_files_to_test:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    hardcoded_values = self.css_utils.find_hardcoded_values(content)

                    if "colors" in hardcoded_values:
                        # Allow some exceptions like transparent, inherit, etc.
                        allowed_colors = ["transparent", "inherit", "initial", "unset"]
                        problematic_colors = [
                            color
                            for color in hardcoded_values["colors"]
                            if not any(
                                allowed in color.lower() for allowed in allowed_colors
                            )
                        ]

                        self.assertEqual(
                            len(problematic_colors),
                            0,
                            f"File {css_file} should not contain hardcoded colors: {problematic_colors}",
                        )

    def test_hardcoded_spacing_replaced(self):
        css_files_to_test = [f for f in self.css_files if f != "variables.css"]

        for css_file in css_files_to_test:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    hardcoded_values = self.css_utils.find_hardcoded_values(
                        content,
                        exclude_patterns=["0px", "1px", "2px", "100%", "0%", "calc("],
                    )

                    # Count variables vs hardcoded values
                    variables_count = self.css_utils.count_css_variables(content)
                    hardcoded_pixels = len(hardcoded_values.get("pixels", []))

                    # Variables should be used more than hardcoded values for mature files
                    if variables_count > 0:
                        self.assertGreaterEqual(
                            variables_count,
                            hardcoded_pixels,
                            f"File {css_file} should use more CSS variables ({variables_count}) than hardcoded pixels ({hardcoded_pixels})",
                        )

    def test_variable_consistency_across_files(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        defined_variables = list(
            self.css_utils.extract_css_variables_definitions(variables_content).keys()
        )

        # Check each CSS file for variable usage
        for css_file in self.css_files:
            if css_file == "variables.css":
                continue

            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Find all variable references in the file
                    import re

                    used_variables = re.findall(r"var\((--[a-zA-Z0-9-]+)\)", content)

                    # Check that all used variables are defined
                    for used_var in used_variables:
                        self.assertIn(
                            used_var,
                            defined_variables,
                            f"Variable {used_var} used in {css_file} should be defined in variables.css",
                        )

    def test_undefined_variable_references(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        defined_variables = set(
            self.css_utils.extract_css_variables_definitions(variables_content).keys()
        )

        for css_file in self.css_files:
            if css_file == "variables.css":
                continue

            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    import re

                    # Find all var() references
                    var_references = re.findall(
                        r"var\((--[a-zA-Z0-9-]+)(?:,\s*[^)]+)?\)", content
                    )

                    for var_ref in var_references:
                        self.assertIn(
                            var_ref,
                            defined_variables,
                            f"Undefined variable {var_ref} referenced in {css_file}",
                        )


class CSSVariableIntegrationTests(CSSTestCase):
    def test_variables_render_in_templates(self):
        # Test that variables.css is loaded in base template
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        # Check that CSS variables file is referenced
        self.assertContains(response, "variables.css")

    def test_critical_variables_not_empty(self):
        variables_content = self.css_utils.read_css_file("variables.css")
        variable_definitions = self.css_utils.extract_css_variables_definitions(
            variables_content
        )

        critical_variables = ["--color-primary", "--color-background", "--radius-md"]

        for critical_var in critical_variables:
            if critical_var in variable_definitions:
                value = variable_definitions[critical_var].strip()
                self.assertGreater(
                    len(value),
                    0,
                    f"Critical variable {critical_var} should have a non-empty value",
                )
                self.assertNotEqual(
                    value,
                    "initial",
                    f"Critical variable {critical_var} should have a specific value, not 'initial'",
                )


class CSSVariablePerformanceTests(CSSTestCase):
    """Test CSS variable performance and optimization"""

    def test_reasonable_variable_count(self):
        """Test that variable count is reasonable for performance"""
        variables_content = self.css_utils.read_css_file("variables.css")
        variable_count = len(
            self.css_utils.extract_css_variables_definitions(variables_content)
        )

        # Should have enough variables to be useful, but not so many as to be unwieldy
        self.assertGreaterEqual(
            variable_count,
            20,
            "Should have at least 20 CSS variables for a design system",
        )
        self.assertLessEqual(
            variable_count,
            200,
            "Should not have more than 200 CSS variables for performance",
        )

    def test_variable_usage_distribution(self):
        total_variable_usage = 0
        files_using_variables = 0

        for css_file in self.css_files:
            if css_file == "variables.css":
                continue

            content = self.css_utils.read_css_file(css_file)
            if content:
                usage_count = self.css_utils.count_css_variables(content)
                if usage_count > 0:
                    files_using_variables += 1
                    total_variable_usage += usage_count

        # At least half of CSS files should use variables
        self.assertGreaterEqual(
            files_using_variables,
            len(self.css_files) // 2,
            f"At least half of CSS files should use variables. Only {files_using_variables} out of {len(self.css_files)} files use them",
        )

        # Should have reasonable total usage
        self.assertGreaterEqual(
            total_variable_usage,
            50,
            f"Total CSS variable usage should be at least 50, but found {total_variable_usage}",
        )
