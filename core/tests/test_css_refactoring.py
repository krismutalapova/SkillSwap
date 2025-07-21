"""
CSS Refactoring Tests - Phase 4.1: skill-pages.css

Tests specifically for the Phase 4.1 refactoring of skill-pages.css to ensure:
1. All hardcoded values have been replaced with CSS variables
2. No visual regressions in skill-related pages
3. Glassmorphism and design system consistency
"""

import os
import re
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings


class SkillPagesRefactoringTests(TestCase):
    """Tests for skill-pages.css refactoring compliance"""

    def setUp(self):
        self.static_root = os.path.join(settings.BASE_DIR, "static", "css")
        self.skill_pages_path = os.path.join(self.static_root, "skill-pages.css")

    def test_skill_pages_css_exists(self):
        """Test that skill-pages.css file exists"""
        self.assertTrue(
            os.path.exists(self.skill_pages_path),
            "skill-pages.css should exist in static/css/",
        )

    def test_no_hardcoded_primary_gradient(self):
        """Test that hardcoded primary gradient has been replaced with variables"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should not contain hardcoded gradient
        hardcoded_gradient = "linear-gradient(to right, #6441a5, #2a0845)"
        self.assertNotIn(
            hardcoded_gradient,
            content,
            "Hardcoded primary gradient should be replaced with var(--color-primary-gradient)",
        )

        # Should contain variable usage
        self.assertIn(
            "var(--color-primary-gradient)",
            content,
            "Should use CSS variable for primary gradient",
        )

    def test_no_hardcoded_colors(self):
        """Test that common hardcoded colors have been replaced"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Common hardcoded colors that should be replaced
        hardcoded_colors = {
            "#f8f9fa": "var(--color-background-muted)",
            "#e9ecef": "var(--color-border-muted)",
            "#6c757d": "var(--color-text-light)",
            "rgba(255, 255, 255, 0.95)": "var(--color-background-glass)",
            "rgba(255, 255, 255, 0.9)": "var(--color-background-glass-light)",
        }

        for hardcoded, expected_var in hardcoded_colors.items():
            # Allow some flexibility in spacing and case
            pattern = re.escape(hardcoded).replace(r"\ ", r"\s*")
            matches = re.findall(pattern, content, re.IGNORECASE)

            if matches:
                self.fail(
                    f"Found hardcoded color '{hardcoded}' in skill-pages.css. "
                    f"Should be replaced with '{expected_var}'. Found {len(matches)} instances."
                )

    def test_consistent_spacing_variables(self):
        """Test that consistent spacing variables are used"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use spacing variables
        spacing_vars = [
            "var(--space-xs)",
            "var(--space-sm)",
            "var(--space-md)",
            "var(--space-lg)",
            "var(--space-xl)",
            "var(--space-2xl)",
            "var(--space-4xl)",
        ]

        has_spacing_vars = any(var in content for var in spacing_vars)
        self.assertTrue(
            has_spacing_vars, "skill-pages.css should use CSS spacing variables"
        )

    def test_consistent_border_radius_variables(self):
        """Test that border radius variables are used consistently"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use border radius variables
        radius_vars = [
            "var(--radius-button)",
            "var(--radius-card)",
            "var(--radius-large)",
            "var(--radius-round)",
        ]

        has_radius_vars = any(var in content for var in radius_vars)
        self.assertTrue(
            has_radius_vars, "skill-pages.css should use CSS border-radius variables"
        )

    def test_consistent_font_variables(self):
        """Test that font size and weight variables are used"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use font variables
        font_vars = [
            "var(--font-size-sm)",
            "var(--font-size-base)",
            "var(--font-size-lg)",
            "var(--font-size-4xl)",
            "var(--font-weight-medium)",
            "var(--font-weight-semibold)",
        ]

        has_font_vars = any(var in content for var in font_vars)
        self.assertTrue(has_font_vars, "skill-pages.css should use CSS font variables")

    def test_transition_variables(self):
        """Test that transition variables are used consistently"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use transition variables instead of hardcoded values
        transition_vars = [
            "var(--transition-all)",
            "var(--transition-color)",
        ]

        has_transition_vars = any(var in content for var in transition_vars)
        self.assertTrue(
            has_transition_vars, "skill-pages.css should use CSS transition variables"
        )

    def test_transform_variables(self):
        """Test that transform variables are used for hover effects"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use transform variables instead of hardcoded translateY
        self.assertIn(
            "var(--transform-hover-up)",
            content,
            "skill-pages.css should use transform hover variables",
        )

        # Should not contain hardcoded translateY
        hardcoded_transforms = [
            "translateY(-2px)",
            "translateY(-1px)",
        ]

        for transform in hardcoded_transforms:
            transform_count = content.count(transform)
            if transform_count > 0:
                self.fail(
                    f"Found {transform_count} instances of hardcoded transform '{transform}'. "
                    f"Should use var(--transform-hover-up) instead."
                )

    def test_glassmorphism_variables(self):
        """Test that glassmorphism effects use consistent variables"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        with open(self.skill_pages_path, "r") as f:
            content = f.read()

        # Should use glassmorphism variables
        glass_vars = [
            "var(--color-background-glass)",
            "var(--glass-backdrop-filter)",
            "var(--shadow-strong)",
            "var(--shadow-hover-strong)",
        ]

        for var in glass_vars:
            if var not in content:
                # Only warn if the file seems to use glassmorphism at all
                if "backdrop-filter" in content or "rgba(255, 255, 255" in content:
                    print(
                        f"Warning: {var} not found in skill-pages.css but glassmorphism detected"
                    )

    def test_file_size_reasonable(self):
        """Test that the refactored file size is reasonable (not bloated)"""
        if not os.path.exists(self.skill_pages_path):
            self.skipTest("skill-pages.css not found")

        file_size = os.path.getsize(self.skill_pages_path)
        # Expect the file to be under 100KB after refactoring
        max_size = 100 * 1024  # 100KB

        self.assertLess(
            file_size,
            max_size,
            f"skill-pages.css is {file_size} bytes, should be under {max_size} bytes after refactoring",
        )


class SkillPagesVariableCompatibilityTests(TestCase):
    """Test that required variables exist for skill-pages.css"""

    def setUp(self):
        self.static_root = os.path.join(settings.BASE_DIR, "static", "css")
        self.variables_path = os.path.join(self.static_root, "variables.css")

    def test_skill_pages_required_variables_exist(self):
        """Test that all variables used by skill-pages.css exist in variables.css"""
        if not os.path.exists(self.variables_path):
            self.skipTest("variables.css not found")

        with open(self.variables_path, "r") as f:
            variables_content = f.read()

        # Variables that skill-pages.css should be using
        required_variables = [
            "--color-primary-gradient",
            "--color-text-white",
            "--color-text-white-muted",  # New variable we added
            "--color-text-primary",
            "--color-text-secondary",
            "--color-text-light",
            "--color-background-glass",
            "--color-background-glass-light",
            "--color-background-muted",
            "--color-border-muted",
            "--color-border-light",
            "--color-success",
            "--space-xs",
            "--space-sm",
            "--space-md",
            "--space-lg",
            "--space-xl",
            "--space-2xl",
            "--space-4xl",
            "--radius-button",
            "--radius-card",
            "--radius-round",
            "--font-size-sm",
            "--font-size-base",
            "--font-size-lg",
            "--font-size-4xl",
            "--font-weight-semibold",
            "--transition-all",
            "--transform-hover-up",
            "--shadow-strong",
            "--shadow-hover-strong",
        ]

        missing_variables = []
        for variable in required_variables:
            if variable not in variables_content:
                missing_variables.append(variable)

        if missing_variables:
            self.fail(
                f"Missing required CSS variables in variables.css: {missing_variables}"
            )


class SkillPagesIntegrationTests(StaticLiveServerTestCase):
    """Integration tests for skill-pages functionality"""

    def test_skill_listing_page_loads(self):
        """Test that skills listing page loads without errors"""
        response = self.client.get("/skills/")
        self.assertEqual(response.status_code, 200)
        # The page should contain either skills-grid (with skills) or no-results (without skills)
        has_grid = "skills-grid" in response.content.decode()
        has_no_results = "no-results" in response.content.decode()
        self.assertTrue(
            has_grid or has_no_results,
            "Skills page should contain either skills-grid or no-results section",
        )

    def test_skill_create_page_loads(self):
        """Test that skill create page loads without errors"""
        # Need to be logged in to create skills
        from django.contrib.auth.models import User

        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get("/skills/create/")
        self.assertEqual(response.status_code, 200)

    def test_my_skills_page_loads(self):
        """Test that my skills page loads without errors"""
        from django.contrib.auth.models import User

        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get("/my-skills/")
        self.assertEqual(response.status_code, 200)


class CrossFileConsolidationTests(TestCase):
    """Test suite for cross-file CSS consolidation"""

    def setUp(self):
        self.css_files = [
            os.path.join(settings.BASE_DIR, "static", "css", "skill-pages.css"),
            os.path.join(settings.BASE_DIR, "static", "css", "skills-pages.css"),
            os.path.join(settings.BASE_DIR, "static", "css", "messaging-pages.css"),
            os.path.join(settings.BASE_DIR, "static", "css", "profile-pages.css"),
            os.path.join(settings.BASE_DIR, "static", "css", "utilities.css"),
        ]

        # Button classes that should only be defined in utilities.css
        self.utility_button_classes = [
            "back-btn",
            "manage-skills-btn",
            "edit-profile-btn",
            "contact-btn",
        ]

    def test_no_duplicate_button_definitions(self):
        """Test that button classes are not duplicated across CSS files"""
        button_definitions = {}

        for css_file in self.css_files:
            if os.path.exists(css_file):
                with open(css_file, "r", encoding="utf-8") as f:
                    content = f.read()

                for button_class in self.utility_button_classes:
                    pattern = f"\\.{button_class}\\s*{{"
                    if re.search(pattern, content):
                        if button_class not in button_definitions:
                            button_definitions[button_class] = []
                        button_definitions[button_class].append(
                            os.path.basename(css_file)
                        )

        # Check that each button class is only defined once
        for button_class, files in button_definitions.items():
            self.assertEqual(
                len(files),
                1,
                f"Button class .{button_class} is defined in multiple files: {files}. Should only be in utilities.css",
            )
            self.assertIn(
                "utilities.css",
                files,
                f"Button class .{button_class} should be defined in utilities.css, found in: {files}",
            )

    def test_utilities_css_has_all_button_variants(self):
        """Test that utilities.css contains all required button variants"""
        utilities_css_path = os.path.join(
            settings.BASE_DIR, "static", "css", "utilities.css"
        )
        self.assertTrue(
            os.path.exists(utilities_css_path), "utilities.css file should exist"
        )

        with open(utilities_css_path, "r", encoding="utf-8") as f:
            content = f.read()

        for button_class in self.utility_button_classes:
            self.assertIn(
                f".{button_class}",
                content,
                f"Button class .{button_class} should be defined in utilities.css",
            )
            self.assertIn(
                f".{button_class}:hover",
                content,
                f"Button hover state .{button_class}:hover should be defined in utilities.css",
            )

    def test_button_styles_use_design_system_variables(self):
        """Test that button styles in utilities.css use design system variables"""
        utilities_css_path = os.path.join(
            settings.BASE_DIR, "static", "css", "utilities.css"
        )

        with open(utilities_css_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract button sections
        for button_class in self.utility_button_classes:
            # Find the button class definition
            pattern = f"\\.{button_class}\\s*{{([^}}]*)}}"
            matches = re.finditer(pattern, content, re.DOTALL)

            for match in matches:
                button_content = match.group(1)

                # Check for design system variable usage
                self.assertRegex(
                    button_content,
                    r"var\(--[^)]+\)",
                    f"Button .{button_class} should use CSS variables for theming",
                )

                # Check for absence of hardcoded colors (allow some exceptions for rgba)
                hardcoded_color_pattern = r"#[0-9a-fA-F]{3,6}"
                hardcoded_colors = re.findall(hardcoded_color_pattern, button_content)
                self.assertEqual(
                    len(hardcoded_colors),
                    0,
                    f"Button .{button_class} contains hardcoded colors: {hardcoded_colors}. Use CSS variables instead.",
                )


if __name__ == "__main__":
    import unittest

    unittest.main()
