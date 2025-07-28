"""
Base Test Classes
Common base classes for CSS and frontend testing
"""

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from core.models import Profile, Skill, Message
from .css_test_helpers import CSSTestUtils
from .file_test_helpers import FileTestUtils


class CSSTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        # Create profile (should be automatic but ensure it exists)
        if not hasattr(self.user, "profile"):
            Profile.objects.create(user=self.user)

        self.client = Client()

        # CSS files to test
        self.css_files = [
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

        self.css_utils = CSSTestUtils()
        self.file_utils = FileTestUtils()

    def assertCSSFileExists(self, filename):
        file_path = self.css_utils.find_css_file(filename)
        self.assertIsNotNone(
            file_path, f"CSS file {filename} should be findable by Django staticfiles"
        )

    def assertCSSVariablesDefined(self, css_content, required_variables):
        for variable in required_variables:
            self.assertIn(
                variable, css_content, f"CSS variable {variable} should be defined"
            )

    def assertNoHardcodedValues(
        self, css_content, value_type="colors", exclude_patterns=None
    ):
        hardcoded_values = self.css_utils.find_hardcoded_values(
            css_content, exclude_patterns
        )
        self.assertNotIn(
            value_type,
            hardcoded_values,
            f"No hardcoded {value_type} should be found. Found: {hardcoded_values.get(value_type, [])}",
        )

    def assertCSSClassExists(self, css_content, class_name):
        classes = self.css_utils.extract_css_classes(css_content)
        self.assertIn(
            class_name, classes, f"CSS class '{class_name}' should be defined"
        )

    def assertValidCSSSyntax(self, css_content, filename=""):
        is_valid, errors = self.css_utils.validate_css_syntax(css_content)
        self.assertTrue(
            is_valid, f"CSS syntax should be valid in {filename}. Errors: {errors}"
        )


class CSSLiveTestCase(StaticLiveServerTestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        if not hasattr(self.user, "profile"):
            Profile.objects.create(user=self.user)

        self.client = Client()

        self.css_utils = CSSTestUtils()
        self.file_utils = FileTestUtils()

        # Try to import selenium for browser tests
        self.selenium_available = False
        try:
            from selenium import webdriver

            self.selenium_available = True
        except ImportError:
            pass

    def create_test_skill(self, skill_type="offer"):
        return Skill.objects.create(
            user=self.user,
            title="Test Skill",
            description="Test skill description",
            category="technology",
            skill_type=skill_type,
            availability="flexible",
        )

    def create_test_message(self, sender=None, recipient=None):
        if not sender:
            sender = self.user
        if not recipient:
            recipient = User.objects.create_user(
                username="recipient",
                password="testpass123",
                first_name="Recipient",
                last_name="User",
            )

        return Message.objects.create(
            sender=sender,
            recipient=recipient,
            subject="Test Message",
            content="Test message content",
        )

    def skipIfNoSelenium(self):
        if not self.selenium_available:
            self.skipTest("Selenium not available for browser testing")


class CSSPerformanceTestCase(CSSTestCase):
    def setUp(self):
        super().setUp()

        # Performance thresholds
        self.max_file_size_kb = 50  # 50KB max per CSS file
        self.max_css_rules_per_file = 500
        self.max_css_variables = 100

    def assertFileSize(self, filename, max_size_kb=None):
        max_size = max_size_kb or self.max_file_size_kb
        stats = self.css_utils.get_css_file_size_stats(filename)

        if "error" in stats:
            self.fail(f"Could not get file stats for {filename}: {stats['error']}")

        size_kb = stats["file_size_bytes"] / 1024
        self.assertLessEqual(
            size_kb,
            max_size,
            f"CSS file {filename} should be under {max_size}KB, but is {size_kb:.1f}KB",
        )

    def assertCSSComplexity(self, css_content, filename="", max_rules=None):
        max_rules = max_rules or self.max_css_rules_per_file
        rules_count = len(css_content.split("{")) - 1  # Rough rule count

        self.assertLessEqual(
            rules_count,
            max_rules,
            f"CSS file {filename} should have fewer than {max_rules} rules, but has {rules_count}",
        )
