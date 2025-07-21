"""
CSS Variable and Design System Tests

Tests to ensure CSS variables are properly defined and accessible.
Validates the design system consistency and file integrity.
"""

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.template.loader import get_template
import os


class CSSVariableTests(TestCase):
    """Test that CSS variables are properly defined"""

    def setUp(self):
        from django.conf import settings

        self.static_root = os.path.join(settings.BASE_DIR, "static", "css")

    def test_variables_css_exists(self):
        """Test that variables.css file exists"""
        variables_path = os.path.join(self.static_root, "variables.css")
        self.assertTrue(
            os.path.exists(variables_path), "variables.css should exist in static/css/"
        )

    def test_utilities_css_exists(self):
        """Test that utilities.css file exists"""
        utilities_path = os.path.join(self.static_root, "utilities.css")
        self.assertTrue(
            os.path.exists(utilities_path), "utilities.css should exist in static/css/"
        )

    def test_variables_css_content(self):
        """Test that variables.css contains required design tokens"""
        variables_path = os.path.join(self.static_root, "variables.css")

        if not os.path.exists(variables_path):
            self.skipTest("variables.css not found")

        with open(variables_path, "r") as f:
            content = f.read()

        # Test for essential CSS variables
        required_variables = [
            "--color-primary",
            "--color-secondary",
            "--color-background",
            "--color-text",
            "--space-sm",
            "--space-md",
            "--space-lg",
            "--font-size-base",
            "--glass-background",
            "--glass-backdrop-filter",
        ]

        for variable in required_variables:
            self.assertIn(
                variable,
                content,
                f"CSS variable {variable} should be defined in variables.css",
            )

    def test_utilities_css_content(self):
        """Test that utilities.css contains required utility classes"""
        utilities_path = os.path.join(self.static_root, "utilities.css")

        if not os.path.exists(utilities_path):
            self.skipTest("utilities.css not found")

        with open(utilities_path, "r") as f:
            content = f.read()

        # Test for essential utility classes
        required_classes = [
            ".glass-card",
            ".btn-primary",
            ".btn-secondary",
            ".flex-center",
            ".text-gradient",
        ]

        for css_class in required_classes:
            self.assertIn(
                css_class,
                content,
                f"Utility class {css_class} should be defined in utilities.css",
            )


class CSSLoadingTests(TestCase):
    """Test that CSS files are properly loaded"""

    def test_css_files_exist(self):
        """Test that CSS files exist in static directory"""
        from django.conf import settings

        css_files = [
            "css/variables.css",
            "css/utilities.css",
            "css/base.css",
        ]

        for css_file in css_files:
            static_path = os.path.join(settings.BASE_DIR, "static", css_file)
            self.assertTrue(
                os.path.exists(static_path),
                f"CSS file {css_file} should exist in static files",
            )

    def test_base_template_includes_css(self):
        """Test that base.html includes all required CSS files"""
        from django.template import loader

        template_name = "base.html"

        try:
            template = loader.get_template(template_name)
            # Get template source through the origin
            template_source = template.template.source
        except AttributeError:
            # Alternative approach for different Django versions
            import os
            from django.conf import settings

            template_path = os.path.join(
                settings.BASE_DIR, "core", "templates", "base.html"
            )
            with open(template_path, "r") as f:
                template_source = f.read()

        required_css_files = ["variables.css", "utilities.css", "base.css"]

        for css_file in required_css_files:
            self.assertIn(
                css_file, template_source, f"base.html should include {css_file}"
            )


class DesignSystemTests(TestCase):
    """Test design system consistency"""

    def setUp(self):
        from django.conf import settings

        self.static_root = os.path.join(settings.BASE_DIR, "static", "css")

    def test_spacing_consistency(self):
        """Test that spacing follows 4px grid system"""
        variables_path = os.path.join(self.static_root, "variables.css")

        if not os.path.exists(variables_path):
            self.skipTest("variables.css not found")

        with open(variables_path, "r") as f:
            content = f.read()

        # Check that spacing variables follow 4px increments
        import re

        spacing_pattern = r"--space-\w+:\s*(\d+)px"
        matches = re.findall(spacing_pattern, content)

        for px_value in matches:
            px_int = int(px_value)
            self.assertEqual(
                px_int % 4,
                0,
                f"Spacing value {px_int}px should be multiple of 4px for consistency",
            )
