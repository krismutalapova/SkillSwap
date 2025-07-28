#!/usr/bin/env python3
"""
Comprehensive Django Test Runner for SkillSwap Platform

This script runs all Django tests with detailed reporting and coverage analysis.
Covers models, views, forms, templates, integration tests, and more.

Usage:
    python core/tests/run_all_tests.py
    python core/tests/run_all_tests.py --coverage
    python core/tests/run_all_tests.py --specific test_models
    python core/tests/run_all_tests.py --verbose
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")

import django
from django.test.utils import get_runner
from django.conf import settings
from django.core.management import execute_from_command_line

django.setup()


class ColoredOutput:
    """Utility class for colored terminal output"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def print_header(cls, text):
        print(f"\n{cls.HEADER}{cls.BOLD}{'='*60}{cls.ENDC}")
        print(f"{cls.HEADER}{cls.BOLD}{text.center(60)}{cls.ENDC}")
        print(f"{cls.HEADER}{cls.BOLD}{'='*60}{cls.ENDC}\n")

    @classmethod
    def print_success(cls, text):
        print(f"{cls.OKGREEN}✓ {text}{cls.ENDC}")

    @classmethod
    def print_warning(cls, text):
        print(f"{cls.WARNING}⚠ {text}{cls.ENDC}")

    @classmethod
    def print_error(cls, text):
        print(f"{cls.FAIL}✗ {text}{cls.ENDC}")

    @classmethod
    def print_info(cls, text):
        print(f"{cls.OKBLUE}ℹ {text}{cls.ENDC}")


class SkillSwapTestRunner:
    """Comprehensive test runner for SkillSwap platform"""

    def __init__(self):
        self.project_root = project_root
        self.test_categories = {
            "models": "core.tests.test_models",
            "views": "core.tests.test_views",
            "forms": "core.tests.test_forms",
            "templates": "core.tests.test_templates",
            "integration": "core.tests.test_integration",
        }
        self.results = {}

    def run_specific_test(self, test_name, verbose=False):
        """Run a specific test category"""
        if test_name not in self.test_categories:
            ColoredOutput.print_error(f"Unknown test category: {test_name}")
            ColoredOutput.print_info(
                f"Available categories: {list(self.test_categories.keys())}"
            )
            return False

        ColoredOutput.print_header(f"Running {test_name.title()} Tests")

        test_module = self.test_categories[test_name]
        return self._run_django_tests([test_module], verbose)

    def run_all_tests(self, verbose=False):
        """Run all test categories"""
        ColoredOutput.print_header("SkillSwap Platform - Comprehensive Test Suite")

        all_passed = True
        start_time = time.time()

        for category, module in self.test_categories.items():
            ColoredOutput.print_header(f"Running {category.title()} Tests")
            success = self._run_django_tests([module], verbose)
            self.results[category] = success
            all_passed = all_passed and success

        end_time = time.time()
        duration = end_time - start_time

        self._print_summary(duration)
        return all_passed

    def run_with_coverage(self, verbose=False):
        """Run tests with coverage analysis"""
        ColoredOutput.print_header("Running Tests with Coverage Analysis")

        try:
            import coverage
        except ImportError:
            ColoredOutput.print_error(
                "Coverage.py not installed. Install with: pip install coverage"
            )
            return False

        # Start coverage
        cov = coverage.Coverage(source=["core"])
        cov.start()

        # Run tests
        all_passed = self.run_all_tests(verbose)

        # Stop coverage and generate report
        cov.stop()
        cov.save()

        ColoredOutput.print_header("Coverage Report")
        cov.report()

        # Generate HTML report
        html_dir = self.project_root / "htmlcov"
        cov.html_report(directory=str(html_dir))
        ColoredOutput.print_success(f"HTML coverage report generated in: {html_dir}")

        return all_passed

    def _run_django_tests(self, test_modules, verbose=False):
        """Run Django tests for specified modules"""
        try:
            from django.core.management.commands.test import Command as TestCommand
            from io import StringIO
            from django.core.management.base import CommandError

            # Prepare command
            cmd = TestCommand()
            cmd.verbosity = 2 if verbose else 1
            cmd.interactive = False
            cmd.failfast = False
            cmd.keepdb = False
            cmd.reverse = False
            cmd.debug_mode = False
            cmd.debug_sql = False
            cmd.parallel = 1
            cmd.tags = set()
            cmd.exclude_tags = set()

            # Run tests
            start_time = time.time()
            result = cmd.run_tests(test_modules)
            end_time = time.time()

            duration = end_time - start_time

            if result == 0:
                ColoredOutput.print_success(f"All tests passed in {duration:.2f}s")
                return True
            else:
                ColoredOutput.print_error(
                    f"Tests failed ({result} failures) in {duration:.2f}s"
                )
                return False

        except Exception as e:
            ColoredOutput.print_error(f"Error running tests: {str(e)}")
            return False

    def _print_summary(self, duration):
        """Print test summary"""
        ColoredOutput.print_header("Test Summary")

        total_categories = len(self.test_categories)
        passed_categories = sum(1 for success in self.results.values() if success)

        for category, success in self.results.items():
            if success:
                ColoredOutput.print_success(f"{category.title()} Tests: PASSED")
            else:
                ColoredOutput.print_error(f"{category.title()} Tests: FAILED")

        print(f"\n{ColoredOutput.BOLD}Overall Results:{ColoredOutput.ENDC}")
        print(f"Categories Passed: {passed_categories}/{total_categories}")
        print(f"Total Duration: {duration:.2f}s")

        if passed_categories == total_categories:
            ColoredOutput.print_success("🎉 ALL TESTS PASSED!")
        else:
            ColoredOutput.print_warning(
                f"⚠️  {total_categories - passed_categories} test categories failed"
            )

    def check_test_environment(self):
        """Check if test environment is properly set up"""
        ColoredOutput.print_header("Environment Check")

        checks = [
            ("Django installation", self._check_django),
            ("Database configuration", self._check_database),
            ("Test files exist", self._check_test_files),
            ("Models can be imported", self._check_models),
            ("Views can be imported", self._check_views),
        ]

        all_passed = True
        for check_name, check_func in checks:
            try:
                check_func()
                ColoredOutput.print_success(check_name)
            except Exception as e:
                ColoredOutput.print_error(f"{check_name}: {str(e)}")
                all_passed = False

        return all_passed

    def _check_django(self):
        """Check Django installation"""
        import django

        version = django.get_version()
        if not version:
            raise Exception("Django not properly installed")
        return f"Django {version}"

    def _check_database(self):
        """Check database configuration"""
        from django.db import connection

        connection.ensure_connection()
        return "Database connection successful"

    def _check_test_files(self):
        """Check test files exist"""
        test_dir = self.project_root / "core" / "tests"
        required_files = [
            "test_models.py",
            "test_views.py",
            "test_forms.py",
            "test_templates.py",
            "test_integration.py",
        ]

        missing_files = []
        for file_name in required_files:
            if not (test_dir / file_name).exists():
                missing_files.append(file_name)

        if missing_files:
            raise Exception(f"Missing test files: {missing_files}")

        return f"All {len(required_files)} test files found"

    def _check_models(self):
        """Check models can be imported"""
        from core.models import Profile, Skill, Message, Rating

        return "All models importable"

    def _check_views(self):
        """Check views can be imported"""
        from core.views import home, view_my_profile, add_skill

        return "All views importable"


def main():
    """Main function to handle command line arguments and run tests"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive Django Test Runner for SkillSwap Platform"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage analysis"
    )
    parser.add_argument(
        "--specific",
        choices=["models", "views", "forms", "templates", "integration"],
        help="Run specific test category only",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--check-env", action="store_true", help="Check test environment setup"
    )

    args = parser.parse_args()

    runner = SkillSwapTestRunner()

    # Check environment if requested
    if args.check_env:
        success = runner.check_test_environment()
        sys.exit(0 if success else 1)

    # Run tests based on arguments
    if args.specific:
        success = runner.run_specific_test(args.specific, args.verbose)
    elif args.coverage:
        success = runner.run_with_coverage(args.verbose)
    else:
        success = runner.run_all_tests(args.verbose)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
