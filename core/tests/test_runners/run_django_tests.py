#!/usr/bin/env python3
"""
Simple Django Test Runner for SkillSwap Platform

This script runs Django tests with organized output and basic reporting.

Usage:
    python core/tests/run_django_tests.py
    python core/tests/run_django_tests.py models
    python core/tests/run_django_tests.py views
    python core/tests/run_django_tests.py forms
    python core/tests/run_django_tests.py templates
    python core/tests/run_django_tests.py integration
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# Colors for output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def run_django_tests(test_app=None):
    """Run Django tests"""
    os.chdir(project_root)

    # Set environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")

    if test_app:
        test_target = f"core.tests.test_{test_app}"
        print_header(f"Running {test_app.title()} Tests")
    else:
        test_target = "core.tests"
        print_header("Running All Django Tests")

    try:
        # Run tests using Django's manage.py
        cmd = [sys.executable, "manage.py", "test", test_target, "--verbosity=2"]
        result = subprocess.run(cmd, capture_output=False, text=True)

        if result.returncode == 0:
            print_success("Tests completed successfully!")
            return True
        else:
            print_error("Some tests failed!")
            return False

    except Exception as e:
        print_error(f"Error running tests: {str(e)}")
        return False


def main():
    """Main function"""
    if len(sys.argv) > 1:
        test_category = sys.argv[1]
        valid_categories = ["models", "views", "forms", "templates", "integration"]

        if test_category not in valid_categories:
            print_error(f"Invalid test category: {test_category}")
            print(f"Valid categories: {', '.join(valid_categories)}")
            sys.exit(1)

        success = run_django_tests(test_category)
    else:
        success = run_django_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
