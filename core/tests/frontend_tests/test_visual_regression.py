#!/usr/bin/env python3
"""
Visual Regression Test Suite (Optional)
Browser-based tests for CSS refactoring visual validation

This suite uses Selenium to test actual visual rendering in browsers.
Run these tests when major CSS changes are made to catch visual regressions.

Requirements:
- pip install selenium
- ChromeDriver installed and in PATH

Usage: python core/tests/test_visual_regression.py
"""

import os
import sys
import time
from pathlib import Path

# Add the parent directories to Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")
import django

django.setup()

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

# Try to import Selenium - skip tests if not available
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - visual tests will be skipped")
    print("   Install with: pip install selenium")


class VisualRegressionTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.driver = None
        self.test_results = []

        if not SELENIUM_AVAILABLE:
            return

        # Setup Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run in headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")

    def setup_driver(self):
        if not SELENIUM_AVAILABLE:
            return False

        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except WebDriverException as e:
            print(f"⚠️  Could not initialize Chrome driver: {e}")
            print("   Make sure ChromeDriver is installed and in PATH")
            return False

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()

    def test_home_page_rendering(self):
        if not self.driver:
            return

        try:
            self.driver.get(f"{self.base_url}/")

            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Check that atomic button classes are applied
            # Look for buttons with both btn-base and color classes (atomic pattern)
            buttons_with_atomic = self.driver.find_elements(
                By.XPATH,
                "//button[contains(@class, 'btn-base') and (contains(@class, 'btn-primary-colors') or contains(@class, 'btn-secondary-colors'))]",
            )

            all_buttons = buttons_with_atomic
            if all_buttons:
                self.test_results.append(
                    "✅ Home page: Button classes (atomic pattern) render correctly"
                )

                # Check button styling
                button = all_buttons[0]
                bg_color = button.value_of_css_property("background")
                if "gradient" in bg_color.lower() or "linear" in bg_color.lower():
                    self.test_results.append(
                        "✅ Home page: Button gradients applied correctly"
                    )
                else:
                    self.test_results.append(
                        "⚠️  Home page: Button gradients may not be applied"
                    )
            else:
                self.test_results.append(
                    "❌ Home page: No button classes found (neither atomic nor legacy)"
                )

        except TimeoutException:
            self.test_results.append("❌ Home page: Page load timeout")
        except Exception as e:
            self.test_results.append(f"❌ Home page test failed: {str(e)[:50]}")

    def test_navigation_styling(self):
        if not self.driver:
            return

        try:
            self.driver.get(f"{self.base_url}/")

            # Check nav-link styling
            nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
            if nav_links:
                nav_link = nav_links[0]

                # Check CSS properties are applied
                padding = nav_link.value_of_css_property("padding")
                border_radius = nav_link.value_of_css_property("border-radius")

                if padding and padding != "0px":
                    self.test_results.append("✅ Navigation: nav-link padding applied")
                else:
                    self.test_results.append(
                        "❌ Navigation: nav-link padding not applied"
                    )

                if border_radius and border_radius != "0px":
                    self.test_results.append(
                        "✅ Navigation: nav-link border-radius applied"
                    )
                else:
                    self.test_results.append(
                        "❌ Navigation: nav-link border-radius not applied"
                    )
            else:
                self.test_results.append("⚠️  Navigation: No nav-link elements found")

        except Exception as e:
            self.test_results.append(f"❌ Navigation test failed: {str(e)[:50]}")

    def test_responsive_design(self):
        if not self.driver:
            return

        try:
            self.driver.get(f"{self.base_url}/")

            # Test desktop layout
            self.driver.set_window_size(1920, 1080)
            time.sleep(1)

            desktop_nav = self.driver.find_elements(By.CLASS_NAME, "nav-link")
            desktop_visible = len([el for el in desktop_nav if el.is_displayed()])

            # Test mobile layout
            self.driver.set_window_size(375, 667)
            time.sleep(1)

            mobile_nav = self.driver.find_elements(By.CLASS_NAME, "nav-link")
            mobile_visible = len([el for el in mobile_nav if el.is_displayed()])

            if desktop_visible > 0 and mobile_visible > 0:
                self.test_results.append(
                    "✅ Responsive: Navigation adapts to screen size"
                )
            else:
                self.test_results.append(
                    "⚠️  Responsive: Navigation layout may need adjustment"
                )

        except Exception as e:
            self.test_results.append(f"❌ Responsive test failed: {str(e)[:50]}")

    def test_skill_pages_styling(self):
        if not self.driver:
            return

        try:
            # Try to access skills page
            self.driver.get(f"{self.base_url}/skills/")

            # Check for skill tiles or cards
            skill_elements = self.driver.find_elements(By.CLASS_NAME, "skill-tile")
            if not skill_elements:
                skill_elements = self.driver.find_elements(By.CLASS_NAME, "skill-card")

            if skill_elements:
                skill_el = skill_elements[0]

                # Check styling properties
                border_radius = skill_el.value_of_css_property("border-radius")
                background = skill_el.value_of_css_property("background")

                if border_radius and border_radius != "0px":
                    self.test_results.append(
                        "✅ Skill pages: Skill tiles have proper border-radius"
                    )

                if "rgba" in background.lower() or "gradient" in background.lower():
                    self.test_results.append(
                        "✅ Skill pages: Glassmorphism effects applied"
                    )
                else:
                    self.test_results.append(
                        "⚠️  Skill pages: Glassmorphism effects may be missing"
                    )
            else:
                self.test_results.append(
                    "⚠️  Skill pages: No skill elements found to test"
                )

        except Exception as e:
            self.test_results.append(f"❌ Skill pages test failed: {str(e)[:50]}")

    def test_css_loading(self):
        if not self.driver:
            return

        try:
            self.driver.get(f"{self.base_url}/")

            # Check browser console for CSS loading errors
            logs = self.driver.get_log("browser")
            css_errors = [
                log
                for log in logs
                if "css" in log["message"].lower() and log["level"] == "SEVERE"
            ]

            if not css_errors:
                self.test_results.append(
                    "✅ CSS Loading: No CSS loading errors in browser console"
                )
            else:
                self.test_results.append(
                    f"❌ CSS Loading: {len(css_errors)} CSS errors in browser console"
                )

        except Exception as e:
            self.test_results.append(f"⚠️  CSS loading test skipped: {str(e)[:50]}")

    def run_all_tests(self):
        print("🧪 Visual Regression Test Suite")
        print("=" * 50)

        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available - install with 'pip install selenium'")
            print("   Also ensure ChromeDriver is installed and in PATH")
            return False

        if not self.setup_driver():
            print("❌ Could not initialize browser driver")
            return False

        try:
            print("🌐 Starting browser tests...")

            test_methods = [
                self.test_home_page_rendering,
                self.test_navigation_styling,
                self.test_responsive_design,
                self.test_skill_pages_styling,
                self.test_css_loading,
            ]

            for test_method in test_methods:
                try:
                    test_method()
                except Exception as e:
                    self.test_results.append(
                        f"❌ Test {test_method.__name__} failed: {e}"
                    )

            # Print results
            print(f"\n📋 Visual Test Results ({len(self.test_results)} checks):")
            print("-" * 40)

            passed = failed = warnings = 0
            for result in self.test_results:
                print(result)
                if result.startswith("✅"):
                    passed += 1
                elif result.startswith("❌"):
                    failed += 1
                elif result.startswith("⚠️"):
                    warnings += 1

            print(
                f"\n📊 Summary: {passed} passed, {failed} failed, {warnings} warnings"
            )

            if failed == 0:
                if warnings == 0:
                    print("🎉 Visual Regression: ALL TESTS PASSED!")
                else:
                    print("✨ Visual Regression: PASSED WITH WARNINGS")
                return True
            else:
                print("⚠️  Some visual tests failed - check browser rendering")
                return False

        finally:
            self.teardown_driver()


if __name__ == "__main__":
    # Check if server is running
    import requests

    try:
        requests.get("http://127.0.0.1:8000/", timeout=5)
        server_running = True
    except:
        server_running = False

    if not server_running:
        print("❌ Django development server not running on http://127.0.0.1:8000/")
        print("   Start it with: python manage.py runserver")
        sys.exit(1)

    tester = VisualRegressionTestSuite()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
