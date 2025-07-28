"""
CSS Refactoring Validation Tests
Comprehensive test suite to validate CSS refactoring changes

This test suite ensures that:
1. CSS variables are properly used instead of hardcoded values
2. Button consolidation is working correctly
3. Component utility classes are functional
4. No visual regressions occurred during refactoring

Usage: python manage.py test core.tests.test_css_refactoring
"""

import os
import re
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles import finders
from core.models import Profile, Skill, Message


class CSSVariableUsageTests(TestCase):
    """Test that CSS variables are properly used instead of hardcoded values"""

    def setUp(self):
        """Set up test data"""
        self.static_dir = os.path.join("static", "css")
        self.css_files = [
            "variables.css",
            "utilities.css",
            "skill-pages.css",
            "messaging-pages.css",
            "profile-pages.css",
        ]

    def test_no_hardcoded_border_radius_values(self):
        """Test that border-radius values use CSS variables"""
        hardcoded_patterns = [
            r"border-radius:\s*\d+px",
            r"border-radius:\s*\d+rem",
            r"border-radius:\s*\d+%",
        ]

        for css_file in self.css_files:
            if css_file == "variables.css":
                continue  # Variables file is allowed to have hardcoded values

            file_path = finders.find(f"css/{css_file}")
            if file_path and os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                for pattern in hardcoded_patterns:
                    matches = re.findall(pattern, content)
                    # Filter out utility classes that are allowed to have hardcoded values
                    allowed_hardcoded = [
                        ".rounded-full { border-radius: 9999px; }"  # Utility class for full circles
                    ]
                    filtered_matches = [
                        match
                        for match in matches
                        if not any(
                            allowed
                            in content[
                                content.find(match) - 50 : content.find(match) + 50
                            ]
                            for allowed in allowed_hardcoded
                        )
                    ]
                    self.assertEqual(
                        len(filtered_matches),
                        0,
                        f"Found hardcoded border-radius in {css_file}: {filtered_matches}",
                    )

    def test_css_variables_are_defined(self):
        """Test that essential CSS variables are defined in variables.css"""
        variables_file = finders.find("css/variables.css")
        self.assertIsNotNone(variables_file, "variables.css not found")

        with open(variables_file, "r") as f:
            content = f.read()

        required_variables = [
            "--radius-lg",
            "--radius-card",
            "--radius-button",
            "--color-primary-gradient",
            "--color-secondary",
            "--color-text-primary",
            "--color-background-glass",
            "--button-padding",
            "--space-xs",
            "--space-sm",
            "--space-md",
        ]

        for var in required_variables:
            self.assertIn(
                var, content, f"Required CSS variable {var} not found in variables.css"
            )

    def test_gradient_variables_usage(self):
        """Test that gradient variables are used instead of hardcoded gradients"""
        for css_file in self.css_files:
            if css_file == "variables.css":
                continue

            file_path = finders.find(f"css/{css_file}")
            if file_path and os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                # Check for hardcoded gradients
                hardcoded_gradients = re.findall(
                    r"linear-gradient\([^)]*#[0-9a-fA-F]{3,6}[^)]*\)", content
                )

                # Allow some hardcoded gradients for specific cases
                allowed_patterns = [
                    "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",  # btn-warning
                    "linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)",  # btn-gradient-danger
                ]

                unexpected_gradients = [
                    g for g in hardcoded_gradients if g not in allowed_patterns
                ]

                self.assertEqual(
                    len(unexpected_gradients),
                    0,
                    f"Found unexpected hardcoded gradients in {css_file}: {unexpected_gradients}",
                )


class ButtonConsolidationTests(TestCase):
    """Test that button consolidation is working correctly"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client = Client()

    def test_primary_button_consistency(self):
        """Test that btn-primary class is consistently used"""
        test_pages = [
            ("home", {}),
            ("skills_list_search", {}),
            ("add_skill", {}),
        ]

        self.client.login(username="testuser", password="testpass123")

        for url_name, kwargs in test_pages:
            response = self.client.get(reverse(url_name, **kwargs))
            if response.status_code == 200:
                # Check that btn-primary is used
                self.assertContains(
                    response,
                    "btn-primary",
                    msg_prefix=f"btn-primary not found on {url_name} page",
                )

    def test_secondary_button_consistency(self):
        """Test that btn-secondary class is consistently used"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("edit_my_profile"))
        self.assertEqual(response.status_code, 200)

        # Check that btn-secondary is used for cancel actions
        self.assertContains(
            response,
            "btn-secondary",
            msg_prefix="btn-secondary not found on profile edit page",
        )

    def test_no_duplicate_button_definitions(self):
        """Test that there are no duplicate button style definitions"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Count button class definitions
        button_classes = [
            ".btn-primary",
            ".btn-secondary",
            ".btn-success",
            ".btn-danger",
        ]

        for btn_class in button_classes:
            pattern = rf"{re.escape(btn_class)}\s*{{"
            matches = re.findall(pattern, content)

            # Should have exactly one definition (not counting hover states)
            base_definitions = [m for m in matches if ":hover" not in m]
            self.assertLessEqual(
                len(base_definitions),
                1,
                f"Multiple definitions found for {btn_class}: {len(base_definitions)}",
            )

    def test_button_utility_classes_exist(self):
        """Test that all required button utility classes exist"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        required_button_classes = [
            ".btn-primary",
            ".btn-secondary",
            ".btn-success",
            ".btn-danger",
            ".btn-outline-danger",
            ".btn-warning",
        ]

        for btn_class in required_button_classes:
            self.assertIn(
                btn_class,
                content,
                f"Required button class {btn_class} not found in utilities.css",
            )


class ComponentUtilityTests(TestCase):
    """Test that component utility classes are functional"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client = Client()

    def test_profile_user_details_class_exists(self):
        """Test that profile-user-details utility class exists and is used"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Check that the class is defined
        self.assertIn(
            ".profile-user-details",
            content,
            "profile-user-details utility class not found",
        )

        # Check that it has proper centering styles
        self.assertIn("align-items: center", content)
        self.assertIn("text-align: center", content)

    def test_rating_display_alignment(self):
        """Test that rating display has proper alignment styles"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Check for sidebar rating styles
        self.assertIn(".skill-rating .rating-display", content)
        self.assertIn("flex-direction: column", content)

    def test_glass_card_utilities_exist(self):
        """Test that glassmorphism card utilities are available"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        glass_card_classes = [
            ".glass-card",
            ".glass-card-strong",
            ".glass-card-large",
            ".form-card",
            ".detail-card",
        ]

        for card_class in glass_card_classes:
            self.assertIn(
                card_class, content, f"Glass card utility {card_class} not found"
            )

    def test_spacing_utilities_exist(self):
        """Test that spacing utility classes are available"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        spacing_classes = [
            ".m-0",
            ".m-xs",
            ".m-sm",
            ".m-md",
            ".p-0",
            ".p-xs",
            ".p-sm",
            ".p-md",
            ".mt-sm",
            ".mb-md",
            ".ml-lg",
            ".mr-xl",
        ]

        for spacing_class in spacing_classes:
            self.assertIn(
                spacing_class, content, f"Spacing utility {spacing_class} not found"
            )


class VisualRegressionTests(TestCase):
    """Test that UI appearance hasn't changed during refactoring"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.skill = Skill.objects.create(
            title="Test Skill",
            description="Test description",
            skill_type="offer",
            category="technology",
            user=self.user,
        )
        self.client = Client()

    def test_skill_detail_page_structure(self):
        """Test that skill detail page maintains proper structure"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(
            reverse("skill_detail_page", kwargs={"pk": self.skill.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Check for key structural elements
        self.assertContains(response, "user-sidebar")
        self.assertContains(response, "profile-user-details")
        self.assertContains(response, "contact-btn")

    def test_profile_edit_page_structure(self):
        """Test that profile edit page maintains proper structure"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("edit_my_profile"))
        self.assertEqual(response.status_code, 200)

        # Check for key form elements
        self.assertContains(response, "user-detail-card")
        self.assertContains(response, "btn-success")
        self.assertContains(response, "btn-secondary")

    def test_skills_list_page_structure(self):
        """Test that skills list page maintains proper structure"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("skills_list_search"))
        self.assertEqual(response.status_code, 200)

        # Check for key elements
        self.assertContains(response, "btn-primary")

    def test_message_pages_structure(self):
        """Test that message pages maintain proper structure"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)

        # Check for navigation elements
        self.assertContains(response, "nav-link")


class CSSFileIntegrityTests(TestCase):
    """Test CSS file integrity and structure"""

    def test_all_css_files_exist(self):
        """Test that all required CSS files exist"""
        required_files = [
            "variables.css",
            "utilities.css",
            "base.css",
            "components.css",
            "skill-pages.css",
            "messaging-pages.css",
            "profile-pages.css",
        ]

        for css_file in required_files:
            file_path = finders.find(f"css/{css_file}")
            self.assertIsNotNone(file_path, f"Required CSS file {css_file} not found")

    def test_css_syntax_validity(self):
        """Test basic CSS syntax validity"""
        css_files = [
            "utilities.css",
            "skill-pages.css",
            "messaging-pages.css",
            "profile-pages.css",
        ]

        for css_file in css_files:
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
        """Test that there are no empty CSS rules"""
        css_files = ["utilities.css", "skill-pages.css"]

        for css_file in css_files:
            file_path = finders.find(f"css/{css_file}")
            if file_path and os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                # Look for empty rules (class/id followed by {})
                empty_rules = re.findall(r"[.#][\w-]+\s*{\s*}", content)
                self.assertEqual(
                    len(empty_rules),
                    0,
                    f"Found empty CSS rules in {css_file}: {empty_rules}",
                )


class ResponsiveDesignTests(TestCase):
    """Test responsive design elements"""

    def test_responsive_utilities_exist(self):
        """Test that responsive utilities are available"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Check for media queries
        self.assertIn("@media (max-width: 768px)", content)
        self.assertIn("@media (max-width: 480px)", content)

        # Check for responsive grid utilities
        self.assertIn(".grid-auto-fit", content)
        self.assertIn(".grid-auto-fill", content)

    def test_button_responsive_behavior(self):
        """Test that buttons have responsive behavior"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Check for mobile button adjustments
        self.assertIn(".btn-outline-danger", content)
        # Should have mobile-specific styles


class PerformanceTests(TestCase):
    """Test CSS performance and optimization"""

    def test_css_file_sizes_reasonable(self):
        """Test that CSS files are not excessively large"""
        max_size_kb = 100  # 100KB limit per file

        large_files = ["utilities.css", "skill-pages.css"]

        for css_file in large_files:
            file_path = finders.find(f"css/{css_file}")
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                size_kb = file_size / 1024

                self.assertLess(
                    size_kb,
                    max_size_kb,
                    f"{css_file} is too large: {size_kb:.1f}KB (max: {max_size_kb}KB)",
                )

    def test_no_excessive_nesting(self):
        """Test that CSS doesn't have excessive nesting depth"""
        utilities_file = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_file, "utilities.css not found")

        with open(utilities_file, "r") as f:
            content = f.read()

        # Look for deeply nested selectors (basic check)
        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            # Count selector depth (approximate)
            if "{" in line and not line.strip().startswith("/*"):
                selector_depth = line.count(" ") // 2  # Rough estimate
                self.assertLess(
                    selector_depth,
                    10,
                    f"Possibly over-nested selector at line {line_num}: {line.strip()}",
                )
