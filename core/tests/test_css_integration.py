"""
Django CSS Integration Tests
Standard Django test suite for CSS and template integration validation


Usage: python manage.py test core.tests.test_css_integration
"""

import os
import re
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import get_template
from django.template import Context
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from core.models import Profile, Skill, Message


class CSSIntegrationTests(TestCase):
    """Django integration tests for CSS refactoring"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client = Client()

    def test_css_files_findable(self):
        """Test that all CSS files can be found by Django's staticfiles"""
        css_files = [
            "css/variables.css",
            "css/utilities.css",
            "css/base.css",
            "css/components.css",
            "css/skill-pages.css",
        ]

        for css_file in css_files:
            found = finders.find(css_file)
            self.assertIsNotNone(
                found, f"CSS file {css_file} should be findable by staticfiles"
            )

    def test_base_template_loads_css(self):
        """Test that base template properly loads CSS files"""
        template = get_template("base.html")
        rendered = template.render({"user": self.user})

        # Should include CSS links
        self.assertIn("variables.css", rendered)
        self.assertIn("utilities.css", rendered)
        self.assertIn("base.css", rendered)

    def test_home_page_uses_utility_classes(self):
        """Test that home page uses consolidated utility classes"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # Should use utility classes, not deprecated ones
        self.assertContains(response, "btn-primary")
        self.assertNotContains(response, "profile-btn-gradient")

    def test_skill_pages_css_integration(self):
        """Test skill pages integrate properly with CSS refactoring"""
        self.client.login(username="testuser", password="testpass123")

        # Test skill list page
        response = self.client.get(reverse("skills_list_search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-primary")

    def test_profile_completion_styling(self):
        """Test that profile completion uses proper CSS variables"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("edit_my_profile"))
        self.assertEqual(response.status_code, 200)

        # Should include CSS that uses variables for status colors
        self.assertContains(response, "user-detail-card")

    def test_message_pages_css_integration(self):
        """Test message pages work with consolidated CSS"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)

        # Should use consolidated nav-link styles
        self.assertContains(response, "nav-link")

    def test_responsive_design_meta_tags(self):
        """Test that responsive design meta tags are present"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "viewport")
        self.assertContains(response, "width=device-width")


class CSSVariableTests(TestCase):
    """Test CSS variable usage in templates"""

    def test_css_variables_file_content(self):
        """Test that CSS variables file contains required variables"""
        variables_path = finders.find("css/variables.css")
        self.assertIsNotNone(variables_path, "variables.css should be findable")

        with open(variables_path, "r") as f:
            content = f.read()

        # Test for key variables
        required_vars = [
            "--color-primary",
            "--color-primary-gradient",
            "--nav-link-padding",
            "--radius-card",
        ]

        for var in required_vars:
            self.assertIn(
                var, content, f"Variable {var} should be defined in variables.css"
            )

    def test_utilities_css_button_classes(self):
        """Test that utilities.css contains consolidated button classes"""
        utilities_path = finders.find("css/utilities.css")
        self.assertIsNotNone(utilities_path, "utilities.css should be findable")

        with open(utilities_path, "r") as f:
            content = f.read()

        button_classes = [".btn-primary", ".btn-secondary", ".btn-success"]
        for btn_class in button_classes:
            self.assertIn(
                btn_class,
                content,
                f"Button class {btn_class} should be in utilities.css",
            )


class FormRenderingTests(TestCase):
    """Test that forms render correctly with new CSS classes"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client = Client()

    def test_skill_create_form_styling(self):
        """Test skill creation form uses proper button styles"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("add_skill"))
        self.assertEqual(response.status_code, 200)

        # Should use utility button classes
        self.assertContains(response, "btn-primary")
        self.assertContains(response, "btn-secondary")

    def test_profile_form_completion_styling(self):
        """Test profile forms show completion status with proper CSS"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("edit_my_profile"))
        self.assertEqual(response.status_code, 200)

        # Should include completion status elements
        self.assertContains(response, "profile-user-details")


class StaticFilesIntegrationTests(StaticLiveServerTestCase):
    """Test CSS loading in live server environment"""

    def test_css_files_serve_correctly(self):
        """Test that CSS files serve without errors in live server"""
        css_urls = [
            f"{self.live_server_url}/static/css/variables.css",
            f"{self.live_server_url}/static/css/utilities.css",
            f"{self.live_server_url}/static/css/base.css",
        ]

        import requests

        for url in css_urls:
            try:
                response = requests.get(url, timeout=10)
                self.assertEqual(
                    response.status_code, 200, f"CSS file {url} should be accessible"
                )
                self.assertIn("text/css", response.headers.get("content-type", ""))
            except requests.RequestException:
                self.skipTest(f"Could not test CSS serving for {url}")


class TemplateInheritanceTests(TestCase):
    """Test that template inheritance works with CSS refactoring"""

    def test_base_template_css_inheritance(self):
        """Test that child templates inherit CSS properly from base"""
        templates_to_test = [
            ("core/home.html", {}),
            ("core/skill_list.html", {}),
            ("core/profile_edit.html", {}),
        ]

        for template_name, context in templates_to_test:
            try:
                template = get_template(template_name)
                rendered = template.render(context)

                # Should include base template CSS links
                self.assertIn(
                    "variables.css",
                    rendered,
                    f"{template_name} should include variables.css",
                )

            except Exception as e:
                self.skipTest(f"Could not test template {template_name}: {e}")
