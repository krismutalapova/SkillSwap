#!/usr/bin/env python3
"""
Comprehensive Django Test Runner for SkillSwap Platform

This script runs all Django and frontend tests with detailed reporting and coverage analysis.
Covers models, views, forms, templates, integration tests, CSS tests, and visual regression.

Usage:
    python core/tests/test_runners/run_all_tests.py
    python core/tests/test_runners/run_all_tests.py --coverage
    python core/tests/test_runners/run_all_tests.py --specific models
    python core/tests/test_runners/run_all_tests.py --specific css_integration
    python core/tests/test_runners/run_all_tests.py --verbose
    python core/tests/test_runners/run_all_tests.py --check-env
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")

import django
from django.test.utils import get_runner
from django.conf import settings
from django.core.management import execute_from_command_line

django.setup()


class ColoredOutput:
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
    def __init__(self):
        self.project_root = project_root
        self.test_categories = {
            "models": "core.tests.django_tests.test_models",
            "views": "core.tests.django_tests.test_views",
            "forms": "core.tests.django_tests.test_forms",
            "templates": "core.tests.django_tests.test_templates",
            "integration": "core.tests.django_tests.test_integration",
        }
        self.frontend_categories = {
            "css_integration": "core.tests.frontend_tests.test_css_integration",
            "css_refactoring_suite": "core.tests.frontend_tests.test_css_refactoring_suite",
            "css_duplicates": "core.tests.frontend_tests.test_css_duplicate_classes",
            "css_variables": "core.tests.frontend_tests.test_css_variables",
            "css_architecture": "core.tests.frontend_tests.test_css_architecture",
            "css_integrity": "core.tests.frontend_tests.test_css_integrity",
            "css_performance": "core.tests.frontend_tests.test_css_performance",
            "button_consolidation": "core.tests.frontend_tests.test_button_consolidation",
            "hardcoded_values": "core.tests.frontend_tests.test_hardcoded_values",
            "responsive_design": "core.tests.frontend_tests.test_responsive_design",
            "template_css_integration": "core.tests.frontend_tests.test_template_css_integration",
            "visual_regression": "core.tests.frontend_tests.test_visual_regression",
        }
        self.results = {}

    def run_specific_test(self, test_name, verbose=False):
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
        ColoredOutput.print_header("SkillSwap Platform - Comprehensive Test Suite")

        all_passed = True
        start_time = time.time()

        # Run Django tests
        ColoredOutput.print_info("Running Django Tests...")
        for category, module in self.test_categories.items():
            ColoredOutput.print_header(f"Running {category.title()} Tests")
            success = self._run_django_tests([module], verbose)
            self.results[f"django_{category}"] = success
            all_passed = all_passed and success

        # Run Frontend tests
        ColoredOutput.print_info("Running Frontend Tests...")
        for category, module in self.frontend_categories.items():
            ColoredOutput.print_header(
                f"Running {category.replace('_', ' ').title()} Tests"
            )
            success = self._run_django_tests([module], verbose)
            self.results[f"frontend_{category}"] = success
            all_passed = all_passed and success

        end_time = time.time()
        duration = end_time - start_time

        self._print_summary(duration)
        return all_passed

    def run_with_coverage(self, verbose=False):
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
        try:
            import subprocess

            # Build command
            cmd = [sys.executable, "manage.py", "test"]

            # Add test modules
            cmd.extend(test_modules)

            # Add verbosity
            if verbose:
                cmd.extend(["--verbosity", "2"])

            # Run tests
            start_time = time.time()
            result = subprocess.run(
                cmd, cwd=str(self.project_root), capture_output=True, text=True
            )
            end_time = time.time()

            duration = end_time - start_time

            if result.returncode == 0:
                ColoredOutput.print_success(f"All tests passed in {duration:.2f}s")
                return True
            else:
                ColoredOutput.print_error(
                    f"Tests failed (return code: {result.returncode}) in {duration:.2f}s"
                )
                if verbose and result.stderr:
                    print(f"Error output: {result.stderr}")
                return False

        except Exception as e:
            ColoredOutput.print_error(f"Error running tests: {str(e)}")
            return False

    def _print_summary(self, duration):
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
        import django

        version = django.get_version()
        if not version:
            raise Exception("Django not properly installed")
        return f"Django {version}"

    def _check_database(self):
        from django.db import connection

        connection.ensure_connection()
        return "Database connection successful"

    def _check_test_files(self):
        django_test_dir = self.project_root / "core" / "tests" / "django_tests"
        frontend_test_dir = self.project_root / "core" / "tests" / "frontend_tests"

        required_django_files = [
            "test_models.py",
            "test_views.py",
            "test_forms.py",
            "test_templates.py",
            "test_integration.py",
        ]

        required_frontend_files = [
            "test_css_integration.py",
            "test_css_refactoring_suite.py",
            "test_css_duplicate_classes.py",
            "test_css_variables.py",
            "test_css_architecture.py",
            "test_css_integrity.py",
            "test_css_performance.py",
            "test_button_consolidation.py",
            "test_hardcoded_values.py",
            "test_responsive_design.py",
            "test_template_css_integration.py",
            "test_visual_regression.py",
        ]

        missing_files = []

        # Check Django test files
        for file_name in required_django_files:
            if not (django_test_dir / file_name).exists():
                missing_files.append(f"django_tests/{file_name}")

        # Check Frontend test files
        for file_name in required_frontend_files:
            if not (frontend_test_dir / file_name).exists():
                missing_files.append(f"frontend_tests/{file_name}")

        if missing_files:
            raise Exception(f"Missing test files: {missing_files}")

        total_files = len(required_django_files) + len(required_frontend_files)
        return f"All {total_files} test files found in organized structure"

    def _check_models(self):
        from core.models import Profile, Skill, Message, Rating

        return "All models importable"

    def _check_views(self):
        from core.views import home, view_my_profile, add_skill

        return "All views importable"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive Django Test Runner for SkillSwap Platform"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage analysis"
    )
    parser.add_argument(
        "--specific",
        choices=[
            "models",
            "views",
            "forms",
            "templates",
            "integration",
            "css_integration",
            "css_refactoring_suite",
            "css_duplicates",
            "css_variables",
            "css_architecture",
            "css_integrity",
            "css_performance",
            "button_consolidation",
            "hardcoded_values",
            "responsive_design",
            "template_css_integration",
            "visual_regression",
        ],
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
        # Check if it's a Django or frontend test
        if args.specific in runner.test_categories:
            success = runner.run_specific_test(args.specific, args.verbose)
        elif args.specific in runner.frontend_categories:
            ColoredOutput.print_header(
                f"Running {args.specific.replace('_', ' ').title()} Tests"
            )
            test_module = runner.frontend_categories[args.specific]
            success = runner._run_django_tests([test_module], args.verbose)
        else:
            ColoredOutput.print_error(f"Unknown test category: {args.specific}")
            success = False
    elif args.coverage:
        success = runner.run_with_coverage(args.verbose)
    else:
        success = runner.run_all_tests(args.verbose)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
