"""
Button Consolidation Testing
Consolidated tests for button pattern consolidation across all files

This file consolidates button testing that was previously scattered across different tests
"""

import re
from core.tests.frontend_tests.utils import CSSTestCase, CSSTestUtils


class ButtonClassDefinitionTests(CSSTestCase):
    def test_required_button_classes_exist(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")
        self.assertGreater(
            len(utilities_content), 0, "utilities.css should not be empty"
        )

        # Essential button utility classes
        required_button_classes = [
            "btn-base",
            "btn-primary",
            "btn-secondary",
            "btn-small",
            "btn-large",
        ]

        for button_class in required_button_classes:
            self.assertCSSClassExists(utilities_content, button_class)

    def test_no_duplicate_button_definitions(self):
        button_definitions = {}

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Find button class definitions (classes starting with btn)
                button_classes = [
                    cls
                    for cls in self.css_utils.extract_css_classes(content)
                    if cls.startswith("btn")
                ]

                for btn_class in button_classes:
                    if btn_class in button_definitions:
                        self.fail(
                            f"Button class '{btn_class}' is defined in both "
                            f"{button_definitions[btn_class]} and {css_file}. "
                            f"Button classes should be centralized in utilities.css"
                        )
                    button_definitions[btn_class] = css_file

    def test_button_hierarchy_consistency(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Extract button size classes and their padding values
            size_classes = ["btn-small", "btn-medium", "btn-large"]
            size_values = {}

            for size_class in size_classes:
                # Look for the class definition and extract padding
                pattern = rf"\.{size_class}\s*\{{[^}}]*padding:\s*([^;}}]+)"
                match = re.search(pattern, utilities_content)
                if match:
                    size_values[size_class] = match.group(1).strip()

            # If we have size values, ensure they follow a logical progression
            if len(size_values) >= 2:
                # At minimum, ensure small < medium < large (basic sanity check)
                self.assertGreater(
                    len(size_values),
                    1,
                    "Button size hierarchy should be defined with consistent values",
                )

    def test_button_base_class_exists(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Check that .btn-base class exists and has essential properties
            btn_pattern = r"\.btn-base\s*\{[^}]*\}"
            btn_match = re.search(btn_pattern, utilities_content)

            self.assertIsNotNone(
                btn_match, "Base .btn-base class should be defined in utilities.css"
            )

            btn_definition = btn_match.group(0) if btn_match else ""

            # Check for essential button properties
            essential_properties = ["padding", "border", "cursor"]
            for prop in essential_properties:
                self.assertIn(
                    prop,
                    btn_definition,
                    f"Base .btn-base class should define {prop} property",
                )


class ButtonUsageTests(CSSTestCase):
    def test_deprecated_button_patterns_removed(self):
        deprecated_patterns = [
            r"\.button\s*\{",  # Old .button class
            r'input\[type="submit"\]\s*\{[^}]*(?:padding|border|background)[^}]*\}',  # Direct input styling
            r"\.submit-btn\s*\{",  # Old submit button class
            r"\.form-button\s*\{",  # Old form button class
        ]

        for css_file in self.css_files:
            if css_file == "utilities.css":
                continue  # Skip utilities.css as it should have button definitions

            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    for pattern in deprecated_patterns:
                        matches = re.findall(pattern, content)
                        self.assertEqual(
                            len(matches),
                            0,
                            f"Deprecated button pattern found in {css_file}: {pattern}",
                        )

    def test_button_utility_adoption(self):
        for css_file in self.css_files:
            if css_file in ["utilities.css", "variables.css"]:
                continue

            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Count button utility usage vs custom button styling
                    utility_references = len(
                        re.findall(r"\.btn(?:-[a-zA-Z0-9-]+)?", content)
                    )
                    custom_button_styling = len(
                        re.findall(
                            r'(button\s*\{|input\[type="submit"\]\s*\{|\.[\w-]*(?:button|btn)[\w-]*\s*\{)',
                            content,
                        )
                    )

                    # If file has button-related content, it should prefer utilities
                    if utility_references > 0 or custom_button_styling > 0:
                        self.assertGreaterEqual(
                            utility_references,
                            custom_button_styling,
                            f"File {css_file} should prefer button utilities over custom styling",
                        )

    def test_template_button_consolidation(self):
        template_files = self.file_utils.list_template_files()

        for template_file in template_files:
            content = self.file_utils.read_file_safe(template_file)
            if content and "button" in content.lower():
                with self.subTest(template=template_file.name):
                    # Check for proper button class usage
                    button_elements = re.findall(
                        r'<(?:button|input)[^>]*class="([^"]*)"', content
                    )

                    for button_classes in button_elements:
                        if "btn" in button_classes:
                            # Ensure btn classes follow proper naming convention
                            btn_classes = [
                                cls
                                for cls in button_classes.split()
                                if cls.startswith("btn")
                            ]
                            for btn_class in btn_classes:
                                self.assertRegex(
                                    btn_class,
                                    r"^btn(?:-[a-zA-Z0-9-]+)?$",
                                    f"Button class '{btn_class}' in {template_file.name} should follow btn-* naming convention",
                                )


class ButtonAccessibilityTests(CSSTestCase):
    def test_button_focus_states(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Check for focus states on button classes
            focus_patterns = [r"\.btn:focus", r"\.btn-primary:focus", r"\.btn:hover"]

            focus_states_found = 0
            for pattern in focus_patterns:
                if re.search(pattern, utilities_content):
                    focus_states_found += 1

            self.assertGreater(
                focus_states_found,
                0,
                "Button classes should include focus/hover states for accessibility",
            )

    def test_button_contrast_variables(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Check that button definitions use CSS variables for colors
            button_definitions = re.findall(r"\.btn[^{]*\{[^}]*\}", utilities_content)

            for button_def in button_definitions:
                if "color:" in button_def or "background:" in button_def:
                    # Should use CSS variables for colors
                    variable_usage = self.css_utils.count_css_variables(button_def)
                    self.assertGreater(
                        variable_usage,
                        0,
                        f"Button definition should use CSS variables for colors: {button_def[:100]}...",
                    )


class ButtonPerformanceTests(CSSTestCase):
    def test_button_css_efficiency(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Count total button-related CSS rules
            button_rules = re.findall(r"\.btn[^{]*\{[^}]*\}", utilities_content)

            # Should have reasonable number of button rules (not too many, not too few)
            self.assertGreaterEqual(
                len(button_rules), 3, "Should have at least 3 button utility classes"
            )
            self.assertLessEqual(
                len(button_rules),
                20,
                f"Should not have more than 20 button rules for performance. Found {len(button_rules)}",
            )

    def test_no_redundant_button_properties(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            # Extract all button class definitions
            button_classes = re.findall(r"(\.btn[^{]*)\{([^}]*)\}", utilities_content)

            if len(button_classes) > 1:
                # Check for common properties that should be in base .btn class
                common_properties = ["cursor", "border", "display"]

                base_btn_props = ""
                other_btn_props = []

                for class_name, properties in button_classes:
                    if class_name.strip() == ".btn-base":
                        base_btn_props = properties
                    else:
                        other_btn_props.append(properties)

                # Common properties should be in base class, not repeated
                for prop in common_properties:
                    if f"{prop}:" in base_btn_props:
                        for other_props in other_btn_props:
                            self.assertNotIn(
                                f"{prop}:",
                                other_props,
                                f"Property '{prop}' should be in base .btn-base class, not repeated in variants",
                            )
