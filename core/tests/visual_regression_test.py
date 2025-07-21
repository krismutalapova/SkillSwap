#!/usr/bin/env python3
"""
Manual Visual Regression Test for CSS Refactoring

This script helps test the skill-pages.css refactoring by:
1. Running automated CSS tests
2. Opening key pages in the browser for manual verification
3. Providing a checklist for visual testing

Usage:
    python core/tests/visual_regression_test.py
"""

import os
import sys
import webbrowser
import subprocess
from time import sleep


# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def run_tests():
    """Run the automated CSS tests"""
    print_header("Running Automated CSS Tests")

    try:
        # Run CSS refactoring tests
        result = subprocess.run(
            [
                sys.executable,
                "manage.py",
                "test",
                "core.tests.test_css_refactoring",
                "-v",
                "2",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print_success("CSS refactoring tests passed!")
            print(result.stdout)
        else:
            print_error("CSS refactoring tests failed!")
            print(result.stderr)
            return False

        # Run updated CSS system tests
        result = subprocess.run(
            [
                sys.executable,
                "manage.py",
                "test",
                "core.tests.test_css_system",
                "-v",
                "2",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print_success("CSS system tests passed!")
            print(result.stdout)
        else:
            print_error("CSS system tests failed!")
            print(result.stderr)
            return False

        return True

    except Exception as e:
        print_error(f"Failed to run tests: {e}")
        return False


def check_server_running():
    """Check if Django development server is running"""
    try:
        import urllib.request

        urllib.request.urlopen("http://127.0.0.1:8000", timeout=1)
        return True
    except:
        return False


def open_test_pages():
    """Open key pages for manual visual testing"""
    print_header("Opening Pages for Visual Testing")

    if not check_server_running():
        print_error("Django development server is not running!")
        print_info("Please start the server with: python manage.py runserver")
        return False

    # List of pages to test
    test_pages = [
        ("Skills Listing", "http://127.0.0.1:8000/skills/"),
        ("Skill Create", "http://127.0.0.1:8000/skills/create/"),
        ("My Skills", "http://127.0.0.1:8000/skills/my_skills/"),
        ("Home Page", "http://127.0.0.1:8000/"),
    ]

    print("Opening pages in your default browser...")
    print("Please review each page for visual consistency.\n")

    for name, url in test_pages:
        print_info(f"Opening {name}: {url}")
        try:
            webbrowser.open(url)
            sleep(1)  # Small delay between opens
        except Exception as e:
            print_error(f"Failed to open {name}: {e}")

    return True


def print_visual_checklist():
    """Print manual testing checklist"""
    print_header("Visual Testing Checklist")

    checklist_items = [
        "✅ Primary gradient buttons display correctly (purple gradient)",
        "✅ Glassmorphism cards have proper transparency and blur",
        "✅ Text colors are consistent and readable",
        "✅ Hover effects work smoothly on buttons and cards",
        "✅ Skill cards maintain their offer/request color coding",
        "✅ Form styling is consistent with design system",
        "✅ Empty states display properly",
        "✅ Pagination controls are styled correctly",
        "✅ No visual regressions compared to before refactoring",
        "✅ Responsive design works on mobile sizes",
        "✅ All interactive elements are clickable",
        "✅ Loading states and animations work properly",
    ]

    for item in checklist_items:
        print(f"  {item}")

    print(
        f"\n{Colors.YELLOW}Please manually verify each item above in your browser.{Colors.END}"
    )
    print(
        f"{Colors.BLUE}Use browser developer tools to inspect CSS variables usage.{Colors.END}"
    )


def print_browser_console_test():
    """Print instructions for browser console testing"""
    print_header("Browser Console Testing")

    console_test = """
// Copy and paste this into your browser's developer console
// to test CSS variable availability

console.log("🧪 Testing CSS Variables...");

const testElement = document.createElement('div');
document.body.appendChild(testElement);

const variables = [
    '--color-primary-gradient',
    '--color-text-white',
    '--color-text-white-muted',
    '--color-background-glass',
    '--space-lg',
    '--radius-button',
    '--transition-all',
    '--transform-hover-up'
];

const computedStyle = getComputedStyle(document.documentElement);
const results = {};

variables.forEach(variable => {
    const value = computedStyle.getPropertyValue(variable);
    results[variable] = value || 'NOT FOUND';
    console.log(`${variable}: ${value || '❌ NOT FOUND'}`);
});

document.body.removeChild(testElement);
console.log("✅ CSS Variable test complete:", results);
    """

    print("Copy and paste this into your browser console (F12):")
    print(f"\n{Colors.BLUE}{console_test}{Colors.END}")


def main():
    """Main test runner"""
    print_header("CSS Refactoring Visual Regression Test")
    print_info("This script will help verify the skill-pages.css refactoring")

    # Step 1: Run automated tests
    if not run_tests():
        print_error("Automated tests failed. Please fix issues before manual testing.")
        return False

    # Step 2: Open pages for visual testing
    if not open_test_pages():
        print_warning("Could not open test pages automatically.")
        print_info("Please manually navigate to the following URLs:")
        print("  - http://127.0.0.1:8000/skills/")
        print("  - http://127.0.0.1:8000/skills/create/")
        print("  - http://127.0.0.1:8000/skills/my_skills/")

    # Step 3: Print testing checklist
    print_visual_checklist()

    # Step 4: Browser console test
    print_browser_console_test()

    print_header("Testing Complete")
    print_success("Automated tests passed!")
    print_info("Please complete the manual visual checklist above.")
    print_info("Run browser console test to verify CSS variables.")

    return True


if __name__ == "__main__":
    main()
