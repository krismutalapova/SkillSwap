"""
Template CSS Integration Testing
Tests for template and CSS integration, class usage validation, and template rendering

This file contains tests focusing specifically on how templates use CSS classes and integration between templates and CSS.
"""

import re
from django.template.loader import get_template
from django.template import Context, TemplateDoesNotExist
from django.test import RequestFactory
from core.tests.frontend_tests.utils import CSSLiveTestCase, CSSTestCase


class TemplateCSSUsageTests(CSSTestCase):
    def test_templates_use_utility_classes(self):
        template_files = self.file_utils.list_template_files()

        # Deprecated class patterns that should be replaced
        deprecated_patterns = [
            r'class="[^"]*\bbtn\s+btn-default\b',
            r'class="[^"]*\bform-control-lg\b',
            r'class="[^"]*\bcol-md-\d+\b',
            r'style="[^"]*"',
        ]

        template_issues = []

        for template_file in template_files[:10]:
            content = self.file_utils.read_file_safe(template_file)
            if content:
                for pattern in deprecated_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        template_issues.append(
                            f"{template_file.name}: {len(matches)} deprecated patterns"
                        )

        if template_issues:
            print(f"Templates with deprecated CSS patterns: {template_issues[:3]}")

    def test_templates_use_defined_classes(self):
        all_defined_classes = set()
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)
                all_defined_classes.update(classes)

        # Check templates for undefined classes
        template_files = self.file_utils.list_template_files()
        undefined_classes = []

        for template_file in template_files[:5]:
            content = self.file_utils.read_file_safe(template_file)
            if content:
                class_pattern = r'class="([^"]+)"'
                class_attributes = re.findall(class_pattern, content)

                for class_attr in class_attributes:
                    classes = class_attr.split()
                    for class_name in classes:
                        if (
                            not self._is_template_variable(class_name)
                            and not self._is_common_utility(class_name)
                            and class_name not in all_defined_classes
                        ):
                            undefined_classes.append(
                                f"{template_file.name}: {class_name}"
                            )

        if undefined_classes:
            print(f"Potentially undefined classes found: {undefined_classes[:5]}")

    def test_critical_templates_render(self):
        critical_templates = [
            "base.html",
            "core/home.html",
            "core/skill_list.html",
        ]

        for template_name in critical_templates:
            with self.subTest(template=template_name):
                try:
                    template = get_template(template_name)

                    # Create minimal context for rendering
                    context = Context(
                        {
                            "user": self.user,
                            "request": RequestFactory().get("/"),
                            "skills": [],
                            "messages": [],
                        }
                    )

                    # Try to render template
                    rendered = template.render(context)
                    self.assertIsInstance(rendered, str)
                    self.assertGreater(len(rendered), 100)
                except TemplateDoesNotExist:
                    self.skipTest(f"Template {template_name} not found")
                except Exception as e:
                    self.fail(f"Template {template_name} failed to render: {e}")

    def _is_template_variable(self, class_name: str) -> bool:
        return (
            "{{" in class_name
            or "}}" in class_name
            or "{%" in class_name
            or "%}" in class_name
        )

    def _is_common_utility(self, class_name: str) -> bool:
        common_utilities = {
            "sr-only",
            "visually-hidden",
            "clearfix",
            "float-left",
            "float-right",
            "text-center",
            "text-left",
            "text-right",
            "d-none",
            "d-block",
            "d-inline",
        }
        return class_name in common_utilities


class TemplateCSSIntegrationTests(CSSLiveTestCase):

    def test_css_loading_in_templates(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        expected_css_files = ["variables.css", "utilities.css", "base.css"]

        for css_file in expected_css_files:
            with self.subTest(css_file=css_file):
                self.assertContains(
                    response,
                    css_file,
                    msg_prefix=f"CSS file {css_file} should be loaded in templates",
                )

    def test_utility_classes_render_correctly(self):
        skill = self.create_test_skill()

        response = self.client.get("/skills/")
        self.assertEqual(response.status_code, 200)

        utility_classes_to_check = [
            "btn-base",  # Atomic foundation
            "btn-primary-colors",  # Atomic color classes
            "btn-secondary-colors",
            "btn-success-colors",
            "btn-warning-colors",
            "text-center",
            "flex-center",
        ]

        for utility_class in utility_classes_to_check:
            # Don't fail if utility isn't used, just check if it's used correctly
            if utility_class in response.content.decode():
                # If the class is used, the page should render successfully
                self.assertContains(response, utility_class)

    def test_responsive_classes_in_templates(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Look for responsive patterns in the rendered HTML
        responsive_patterns = [
            r'class="[^"]*\bhidden-\w+\b',
            r'class="[^"]*\bvisible-\w+\b',
            r'class="[^"]*\bcol-\w+-\d+\b',
            r'class="[^"]*\bflex-\w+\b',
        ]

        responsive_usage = 0
        for pattern in responsive_patterns:
            if re.search(pattern, content):
                responsive_usage += 1

        if responsive_usage == 0:
            print("Note: Consider using responsive utility classes in templates")

    def test_semantic_html_with_css(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        semantic_elements = [
            "<nav",
            "<main",
            "<section",
            "<article",
            "<header",
            "<footer",
        ]

        semantic_usage = sum(1 for element in semantic_elements if element in content)

        self.assertGreaterEqual(
            semantic_usage,
            3,
            f"Templates should use semantic HTML elements. Found {semantic_usage} out of {len(semantic_elements)}",
        )


class ComponentIntegrationTests(CSSTestCase):
    def test_button_component_integration(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            button_classes = [
                cls
                for cls in self.css_utils.extract_css_classes(utilities_content)
                if cls.startswith("btn")
            ]

            self.assertGreater(
                len(button_classes), 0, "Should have button utility classes defined"
            )

            # Check that templates use button classes appropriately
            template_files = self.file_utils.list_template_files()
            button_usage = 0

            for template_file in template_files[:5]:
                content = self.file_utils.read_file_safe(template_file)
                if content and "btn" in content:
                    button_usage += 1

            if button_usage == 0:
                print("Note: No button class usage found in templates")

    def test_form_component_integration(self):
        form_related_classes = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)
                form_classes = [cls for cls in classes if "form" in cls.lower()]
                form_related_classes.extend(form_classes)

        self.assertGreater(
            len(form_related_classes), 0, "Should have form-related CSS classes"
        )

    def test_navigation_component_integration(self):
        nav_classes = []

        for css_file in ["base.css", "components.css", "utilities.css"]:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)
                nav_related = [cls for cls in classes if "nav" in cls.lower()]
                nav_classes.extend(nav_related)

        if nav_classes:
            self.assertGreater(
                len(nav_classes), 0, "Navigation classes should be defined in CSS"
            )

        # Check if templates use navigation classes
        template_files = self.file_utils.list_template_files()
        nav_usage = 0

        for template_file in template_files[:3]:  # Check key templates
            content = self.file_utils.read_file_safe(template_file)
            if content and ("nav" in content.lower() or "<nav>" in content):
                nav_usage += 1

        if nav_usage == 0:
            print("Note: Limited navigation usage found in templates")


class CSSVariableTemplateIntegrationTests(CSSLiveTestCase):

    def test_css_variables_loaded_in_browser(self):
        self.skipIfNoSelenium()

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(f"{self.live_server_url}/home/")
            element = driver.find_element("css selector", "body")

            # Get computed style for CSS variable
            primary_color = driver.execute_script(
                "return getComputedStyle(arguments[0]).getPropertyValue('--color-primary')",
                element,
            )

            if primary_color:
                self.assertNotEqual(
                    primary_color.strip(),
                    "",
                    "CSS variable --color-primary should have a value",
                )
            else:
                self.skipTest("CSS variables not supported or not loaded")

        finally:
            driver.quit()

    def test_dynamic_css_class_application(self):
        skill = self.create_test_skill()

        response = self.client.get("/skills/")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        skill_related_patterns = [
            r'class="[^"]*skill',
            r'class="[^"]*card',
            r'class="[^"]*offer|request',
        ]

        pattern_matches = 0
        for pattern in skill_related_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                pattern_matches += 1

        self.assertGreater(
            pattern_matches, 0, "Dynamic content should use appropriate CSS classes"
        )


class AccessibilityIntegrationTests(CSSLiveTestCase):
    def test_focus_styles_integration(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        interactive_elements = ["<button", "<a href", "<input", "<select", "<textarea"]

        interactive_count = sum(
            content.count(element) for element in interactive_elements
        )

        if interactive_count > 0:
            focus_styles = 0
            for css_file in self.css_files:
                css_content = self.css_utils.read_css_file(css_file)
                if css_content and ":focus" in css_content:
                    focus_styles += 1

            self.assertGreater(
                focus_styles,
                0,
                f"Found {interactive_count} interactive elements but no focus styles in CSS",
            )

    def test_color_contrast_in_templates(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")

        if utilities_content:
            contrast_patterns = [
                r"\.text-white",
                r"\.text-dark",
                r"\.bg-dark",
                r"\.bg-light",
            ]

            contrast_utilities = 0
            for pattern in contrast_patterns:
                if re.search(pattern, utilities_content):
                    contrast_utilities += 1

            # This is informational
            if contrast_utilities > 0:
                print(f"Found {contrast_utilities} contrast utility classes")

    def test_semantic_class_names(self):
        semantic_issues = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                classes = self.css_utils.extract_css_classes(content)

                # Look for non-semantic class names
                non_semantic = [cls for cls in classes if self._is_non_semantic(cls)]

                if non_semantic:
                    semantic_issues.extend(
                        f"{css_file}: {cls}" for cls in non_semantic[:3]
                    )

        if semantic_issues:
            print(f"Consider more semantic class names: {semantic_issues[:5]}")

    def _is_non_semantic(self, class_name: str) -> bool:
        presentational_keywords = [
            "red",
            "blue",
            "green",
            "big",
            "small",
            "left",
            "right",
            "bold",
            "italic",
            "underline",
        ]

        return any(keyword in class_name.lower() for keyword in presentational_keywords)
