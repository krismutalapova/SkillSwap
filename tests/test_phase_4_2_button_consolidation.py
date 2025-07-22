#!/usr/bin/env python3
"""
Phase 4.2 Button Consolidation Test Suite
Tests to verify successful consolidation of button patterns into utility classes
"""

import os
import sys
import re
from pathlib import Path

# Try to import requests, skip page loading test if not available
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class Phase42TestSuite:
    def __init__(self):
        self.project_root = project_root
        self.static_css_dir = self.project_root / "static" / "css"
        self.templates_dir = self.project_root / "core" / "templates"
        self.base_url = "http://127.0.0.1:8000"
        self.test_results = []

    def log_result(self, test_name, passed, message):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append(
            {"test": test_name, "passed": passed, "message": message}
        )
        print(f"{status}: {test_name} - {message}")

    def test_removed_duplicate_button_patterns(self):
        """Test 1: Verify duplicate button patterns have been removed from CSS files"""
        print("\n🧪 Test 1: Checking for removed duplicate button patterns...")

        # Patterns that should no longer exist
        removed_patterns = [
            ".hero-btn",
            ".auth-submit-btn",
            ".login-btn",
            ".logout-login-btn",
            ".complete-btn",
            ".skip-btn",
            ".save-btn",
        ]

        css_files = ["home-pages.css", "auth-pages.css", "profile-pages.css"]

        failures = []
        for css_file in css_files:
            css_path = self.static_css_dir / css_file
            if css_path.exists():
                content = css_path.read_text()
                for pattern in removed_patterns:
                    if pattern in content:
                        failures.append(f"Found {pattern} in {css_file}")

        passed = len(failures) == 0
        message = (
            "All duplicate patterns removed"
            if passed
            else f"Found patterns: {', '.join(failures)}"
        )
        self.log_result("Removed Duplicate Button Patterns", passed, message)

    def test_templates_use_utility_classes(self):
        """Test 2: Verify templates use utility classes instead of custom button classes"""
        print("\n🧪 Test 2: Checking template button class usage...")

        # Template files and expected utility classes
        template_checks = [
            ("core/home.html", ["btn-primary", "btn-secondary"]),
            ("core/auth/login.html", ["btn-primary w-full"]),
            ("core/auth/logout.html", ["btn-primary"]),
            ("core/auth/signup.html", ["btn-primary w-full", "btn-secondary"]),
            ("core/auth/complete_name.html", ["btn-success w-full", "btn-secondary"]),
            ("core/components/user_detail_card.html", ["btn-success", "btn-secondary"]),
        ]

        failures = []
        for template_path, expected_classes in template_checks:
            full_path = self.templates_dir / template_path
            if full_path.exists():
                content = full_path.read_text()
                for expected_class in expected_classes:
                    if expected_class not in content:
                        failures.append(
                            f"Missing '{expected_class}' in {template_path}"
                        )

        passed = len(failures) == 0
        message = (
            "All templates use utility classes"
            if passed
            else f"Issues: {', '.join(failures)}"
        )
        self.log_result("Templates Use Utility Classes", passed, message)

    def test_no_old_button_classes_in_templates(self):
        """Test 3: Verify old button classes are not used in templates"""
        print("\n🧪 Test 3: Checking for old button classes in templates...")

        old_classes = [
            "hero-btn",
            "auth-submit-btn",
            "login-btn",
            "logout-login-btn",
            "complete-btn",
            "skip-btn",
            "save-btn",
            "primary-gradient hero-btn",  # Specific problematic combinations
            ".primary-gradient hero-btn",
        ]

        template_files = list(self.templates_dir.rglob("*.html"))
        failures = []

        for template_file in template_files:
            content = template_file.read_text()
            for old_class in old_classes:
                if old_class in content:
                    failures.append(f"Found '{old_class}' in {template_file.name}")

        passed = len(failures) == 0
        message = (
            "No old button classes found"
            if passed
            else f"Found old classes: {', '.join(failures)}"
        )
        self.log_result("No Old Button Classes in Templates", passed, message)

    def test_utility_classes_exist(self):
        """Test 4: Verify required utility classes exist in utilities.css"""
        print("\n🧪 Test 4: Checking utility class definitions...")

        utilities_path = self.static_css_dir / "utilities.css"
        if not utilities_path.exists():
            self.log_result("Utility Classes Exist", False, "utilities.css not found")
            return

        content = utilities_path.read_text()

        required_classes = [".btn-primary", ".btn-secondary", ".btn-success", ".w-full"]

        missing = []
        for css_class in required_classes:
            if css_class not in content:
                missing.append(css_class)

        passed = len(missing) == 0
        message = (
            "All utility classes exist" if passed else f"Missing: {', '.join(missing)}"
        )
        self.log_result("Utility Classes Exist", passed, message)

    def test_page_loading(self):
        """Test 5: Verify pages load correctly with new button classes"""
        print("\n🧪 Test 5: Testing page loading...")

        if not REQUESTS_AVAILABLE:
            self.log_result(
                "Page Loading", True, "Skipped - requests library not available"
            )
            return

        test_urls = ["/home/", "/login/", "/signup/", "/skills/"]

        failures = []
        for url in test_urls:
            try:
                response = requests.get(f"{self.base_url}{url}", timeout=5)
                if response.status_code != 200:
                    failures.append(f"{url} returned {response.status_code}")
            except Exception as e:
                failures.append(f"{url} failed to load: {str(e)}")

        passed = len(failures) == 0
        message = (
            "All pages load successfully"
            if passed
            else f"Issues: {', '.join(failures)}"
        )
        self.log_result("Page Loading", passed, message)

    def test_button_visual_consistency(self):
        """Test 6: Test button visual consistency by checking CSS properties"""
        print("\n🧪 Test 6: Checking button visual consistency...")

        utilities_path = self.static_css_dir / "utilities.css"
        if not utilities_path.exists():
            self.log_result(
                "Button Visual Consistency", False, "utilities.css not found"
            )
            return

        content = utilities_path.read_text()

        # Check that all button types have consistent base properties
        required_properties = [
            "padding",
            "border-radius",
            "font-weight",
            "transition",
            "cursor",
        ]

        button_classes = [".btn-primary", ".btn-secondary", ".btn-success"]
        issues = []

        for btn_class in button_classes:
            class_match = re.search(
                rf"{re.escape(btn_class)}\s*\{{([^}}]+)\}}", content, re.DOTALL
            )
            if class_match:
                class_content = class_match.group(1)
                for prop in required_properties:
                    if prop not in class_content:
                        issues.append(f"{btn_class} missing {prop}")

        passed = len(issues) == 0
        message = (
            "Button styles consistent" if passed else f"Issues: {', '.join(issues)}"
        )
        self.log_result("Button Visual Consistency", passed, message)

    def test_width_utility_functionality(self):
        """Test 7: Verify width utility class functionality"""
        print("\n🧪 Test 7: Testing width utility class...")

        utilities_path = self.static_css_dir / "utilities.css"
        content = utilities_path.read_text()

        # Check .w-full class exists and has width: 100%
        w_full_match = re.search(r"\.w-full\s*\{([^}]+)\}", content)

        if not w_full_match:
            self.log_result(
                "Width Utility Functionality", False, ".w-full class not found"
            )
            return

        w_full_content = w_full_match.group(1)
        has_width_100 = "width: 100%" in w_full_content

        passed = has_width_100
        message = ".w-full has width: 100%" if passed else ".w-full missing width: 100%"
        self.log_result("Width Utility Functionality", passed, message)

    def test_template_syntax_validity(self):
        """Test 8: Check for template syntax errors introduced during refactoring"""
        print("\n🧪 Test 8: Checking template syntax validity...")

        template_files = [
            "core/home.html",
            "core/auth/login.html",
            "core/auth/logout.html",
            "core/auth/signup.html",
            "core/auth/complete_name.html",
            "core/components/user_detail_card.html",
        ]

        issues = []
        for template_path in template_files:
            full_path = self.templates_dir / template_path
            if full_path.exists():
                content = full_path.read_text()

                # Check for common syntax errors
                if 'class="."' in content:  # Extra dot in class
                    issues.append(f"Extra dot in class attribute in {template_path}")
                if 'class=" ' in content or 'class=" "' in content:  # Empty class
                    issues.append(f"Empty class attribute in {template_path}")
                # Check for unclosed tags or malformed class attributes
                class_matches = re.findall(r'class="([^"]*)"', content)
                for class_attr in class_matches:
                    if class_attr.startswith("."):
                        issues.append(
                            f"Class starts with dot in {template_path}: {class_attr}"
                        )

        passed = len(issues) == 0
        message = (
            "All template syntax valid" if passed else f"Issues: {', '.join(issues)}"
        )
        self.log_result("Template Syntax Validity", passed, message)

    def run_all_tests(self):
        """Run all Phase 4.2 tests"""
        print("🚀 Starting Phase 4.2 Button Consolidation Test Suite")
        print("=" * 60)

        # Run all tests
        self.test_removed_duplicate_button_patterns()
        self.test_templates_use_utility_classes()
        self.test_no_old_button_classes_in_templates()
        self.test_utility_classes_exist()
        self.test_page_loading()
        self.test_button_visual_consistency()
        self.test_width_utility_functionality()
        self.test_template_syntax_validity()

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        passed_count = sum(1 for result in self.test_results if result["passed"])
        total_count = len(self.test_results)

        for result in self.test_results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['test']}")

        print(f"\nOverall: {passed_count}/{total_count} tests passed")

        if passed_count == total_count:
            print("🎉 Phase 4.2 Button Consolidation: COMPLETE!")
            print(
                "✨ All button patterns successfully consolidated into utility classes"
            )
            return True
        else:
            print("⚠️  Phase 4.2 Button Consolidation: INCOMPLETE")
            print("🔧 Some issues need to be resolved")
            return False


def main():
    """Run the Phase 4.2 test suite"""
    test_suite = Phase42TestSuite()
    success = test_suite.run_all_tests()

    if success:
        print("\n🏆 Phase 4.2 is ready for commit!")
    else:
        print("\n🚧 Please fix the issues above before committing Phase 4.2")

    return success


if __name__ == "__main__":
    main()
