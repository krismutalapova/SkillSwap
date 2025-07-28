#!/usr/bin/env python3
"""
Organized Test Runner for SkillSwap Platform

Runs tests from the organized test structure with colored output.

Usage:
    python core/tests/run_organized_tests.py                    # All tests
    python core/tests/run_organized_tests.py --django           # Django tests only
    python core/tests/run_organized_tests.py --frontend         # Frontend tests only
    python core/tests/run_organized_tests.py --models           # Model tests only
    python core/tests/run_organized_tests.py --views            # View tests only
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


# Color codes for output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message, color):
    print(f"{color}{message}{Colors.ENDC}")


def run_test_command(test_path, description):
    """Run a Django test command and return success/failure"""
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"Running: {description}", Colors.HEADER)
    print_colored(f"Path: {test_path}", Colors.OKBLUE)
    print_colored(f"{'='*60}", Colors.HEADER)

    try:
        result = subprocess.run(
            ["python", "manage.py", "test", test_path, "--verbosity=2"],
            capture_output=False,
            text=True,
        )

        if result.returncode == 0:
            print_colored(f"✅ {description} - PASSED", Colors.OKGREEN)
            return True
        else:
            print_colored(f"❌ {description} - FAILED", Colors.FAIL)
            return False

    except Exception as e:
        print_colored(f"💥 {description} - ERROR: {str(e)}", Colors.FAIL)
        return False


def main():
    parser = argparse.ArgumentParser(description="Run organized SkillSwap tests")
    parser.add_argument("--django", action="store_true", help="Run Django tests only")
    parser.add_argument(
        "--frontend", action="store_true", help="Run frontend tests only"
    )
    parser.add_argument("--models", action="store_true", help="Run model tests only")
    parser.add_argument("--views", action="store_true", help="Run view tests only")
    parser.add_argument("--forms", action="store_true", help="Run form tests only")
    parser.add_argument(
        "--templates", action="store_true", help="Run template tests only"
    )
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests only"
    )

    args = parser.parse_args()

    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)

    print_colored("🚀 SkillSwap Organized Test Runner", Colors.HEADER)
    print_colored(f"Working directory: {os.getcwd()}", Colors.OKBLUE)

    test_results = []

    if args.django or not any(
        [
            args.django,
            args.frontend,
            args.models,
            args.views,
            args.forms,
            args.templates,
            args.integration,
        ]
    ):
        # Run all Django tests or specific ones
        django_tests = [
            ("core.tests.django_tests.test_models", "Model Tests", args.models),
            ("core.tests.django_tests.test_views", "View Tests", args.views),
            ("core.tests.django_tests.test_forms", "Form Tests", args.forms),
            (
                "core.tests.django_tests.test_templates",
                "Template Tests",
                args.templates,
            ),
            (
                "core.tests.django_tests.test_integration",
                "Integration Tests",
                args.integration,
            ),
        ]

        for test_path, description, should_run in django_tests:
            if (
                not any(
                    [
                        args.models,
                        args.views,
                        args.forms,
                        args.templates,
                        args.integration,
                    ]
                )
                or should_run
            ):
                success = run_test_command(test_path, description)
                test_results.append((description, success))

    if args.frontend:
        # Run frontend tests
        frontend_tests = [
            (
                "core.tests.frontend_tests.test_css_duplicate_classes",
                "CSS Duplicate Classes",
            ),
            ("core.tests.frontend_tests.test_css_integration", "CSS Integration"),
            ("core.tests.frontend_tests.test_css_refactoring", "CSS Refactoring"),
            (
                "core.tests.frontend_tests.test_profile_pages_optimization",
                "Profile Page Optimization",
            ),
            ("core.tests.frontend_tests.test_visual_regression", "Visual Regression"),
        ]

        for test_path, description in frontend_tests:
            success = run_test_command(test_path, description)
            test_results.append((description, success))

    # Print summary
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored("📊 TEST SUMMARY", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)

    passed = sum(1 for _, success in test_results if success)
    failed = len(test_results) - passed

    for description, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        color = Colors.OKGREEN if success else Colors.FAIL
        print_colored(f"{status:<10} {description}", color)

    print_colored(
        f"\nTotal: {len(test_results)} | Passed: {passed} | Failed: {failed}",
        Colors.HEADER,
    )

    if failed > 0:
        print_colored(
            f"\n⚠️  {failed} test suite(s) failed. Check the output above for details.",
            Colors.WARNING,
        )
        sys.exit(1)
    else:
        print_colored(
            f"\n🎉 All {passed} test suite(s) passed successfully!", Colors.OKGREEN
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
