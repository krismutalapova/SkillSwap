#!/usr/bin/env python3
"""
Visual Testing Script for Button Consolidation
Tests that all button styles work correctly after cross-file consolidation
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Add the parent directory to the path so we can import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.test import Client, TestCase


class ButtonConsolidationVisualTests:
    """Visual tests for button consolidation across all pages"""

    def __init__(self):
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Remove this to see browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            self.base_url = "http://localhost:8000"

            # Create test user
            self.create_test_user()

        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Make sure you have ChromeDriver installed and in PATH")
            sys.exit(1)

    def create_test_user(self):
        """Create a test user for authentication"""
        try:
            self.user = User.objects.get(username="visual_test_user")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username="visual_test_user",
                password="testpass123",
                email="test@example.com",
                first_name="Visual",
                last_name="Tester",
            )
            print("✅ Created test user: visual_test_user")

    def login(self):
        """Login to the application"""
        print("🔐 Logging in...")
        self.driver.get(f"{self.base_url}/login/")

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )

        username_field.send_keys("visual_test_user")
        password_field.send_keys("testpass123")
        login_button.click()

        # Wait for redirect
        WebDriverWait(self.driver, 10).until(
            lambda driver: "/login/" not in driver.current_url
        )
        print("✅ Successfully logged in")

    def test_utility_buttons(self):
        """Test that consolidated utility buttons render correctly"""
        print("\n🔘 Testing Utility Buttons...")

        button_tests = [
            {
                "page": "/skills/",
                "buttons": [".btn-primary"],
                "description": "Skills listing primary buttons",
            },
            {
                "page": "/my-skills/",
                "buttons": [".btn-primary", ".btn-warning", ".btn-gradient-danger"],
                "description": "My skills action buttons",
            },
            {
                "page": "/skills/create/",
                "buttons": [".btn-muted"],
                "description": "Create skill cancel button",
            },
        ]

        for test in button_tests:
            print(f"  Testing: {test['description']}")

            try:
                self.driver.get(f"{self.base_url}{test['page']}")

                for button_selector in test["buttons"]:
                    buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, button_selector
                    )

                    if buttons:
                        print(
                            f"    ✅ Found {len(buttons)} {button_selector} button(s)"
                        )

                        # Test button styling
                        for i, button in enumerate(buttons):
                            # Check if button is visible
                            if button.is_displayed():
                                # Get computed styles
                                bg_color = self.driver.execute_script(
                                    "return window.getComputedStyle(arguments[0]).backgroundColor",
                                    button,
                                )
                                print(
                                    f"      Button {i+1}: background-color = {bg_color}"
                                )
                            else:
                                print(f"      ⚠️  Button {i+1} is not visible")
                    else:
                        print(f"    ❌ No {button_selector} buttons found")

            except Exception as e:
                print(f"    ❌ Error testing {test['page']}: {e}")

    def test_specific_button_classes(self):
        """Test specific consolidated button classes"""
        print("\n🔘 Testing Specific Consolidated Button Classes...")

        # Test pages that should have consolidated buttons
        consolidated_button_tests = [
            {
                "page": "/inbox/",
                "button_class": ".back-btn",
                "description": "Back button in messaging",
            }
        ]

        for test in consolidated_button_tests:
            print(f"  Testing: {test['description']}")

            try:
                self.driver.get(f"{self.base_url}{test['page']}")

                buttons = self.driver.find_elements(
                    By.CSS_SELECTOR, test["button_class"]
                )

                if buttons:
                    print(
                        f"    ✅ Found {len(buttons)} {test['button_class']} button(s)"
                    )

                    # Check if buttons use the consolidated styles
                    for i, button in enumerate(buttons):
                        if button.is_displayed():
                            # Check for CSS variables (indirect test)
                            styles = self.driver.execute_script(
                                """
                                var styles = window.getComputedStyle(arguments[0]);
                                return {
                                    backgroundColor: styles.backgroundColor,
                                    borderRadius: styles.borderRadius,
                                    transition: styles.transition
                                };
                            """,
                                button,
                            )
                            print(f"      Button {i+1} styles: {styles}")

                else:
                    print(f"    ❌ No {test['button_class']} buttons found")

            except Exception as e:
                print(f"    ❌ Error testing {test['page']}: {e}")

    def test_button_hover_effects(self):
        """Test that button hover effects work"""
        print("\n🔘 Testing Button Hover Effects...")

        try:
            self.driver.get(f"{self.base_url}/skills/")

            # Find a primary button
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-primary")
            if buttons:
                button = buttons[0]

                # Get initial styles
                initial_transform = self.driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).transform", button
                )

                # Hover over button
                webdriver.ActionChains(self.driver).move_to_element(button).perform()
                time.sleep(0.5)

                # Get hover styles
                hover_transform = self.driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).transform", button
                )

                print(f"    Initial transform: {initial_transform}")
                print(f"    Hover transform: {hover_transform}")

                if initial_transform != hover_transform:
                    print("    ✅ Hover effect detected!")
                else:
                    print("    ⚠️  No hover transform detected")

        except Exception as e:
            print(f"    ❌ Error testing hover effects: {e}")

    def run_all_tests(self):
        """Run all visual tests"""
        print("🚀 Starting Button Consolidation Visual Tests\n")

        try:
            self.login()
            self.test_utility_buttons()
            self.test_specific_button_classes()
            self.test_button_hover_effects()

            print("\n✅ All visual tests completed!")

        except Exception as e:
            print(f"\n❌ Visual tests failed: {e}")

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, "driver"):
            self.driver.quit()
        print("🧹 Cleaned up browser resources")


if __name__ == "__main__":
    tester = ButtonConsolidationVisualTests()
    tester.run_all_tests()
