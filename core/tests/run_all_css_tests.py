#!/usr/bin/env python3
"""
Comprehensive CSS Test Runner
Master test runner for all CSS refactoring validation

This script runs all CSS-related tests in the correct order:
1. CSS Refactoring Suite (standalone tests)
2. Django CSS Integration Tests (Django TestCase)
3. Visual Regression Tests (Selenium, optional)

Note: JavaScript browser tests in ../test_utilities.js should be run manually
      in browser console for real-time validation.

Usage:
    python core/tests/run_all_css_tests.py
    python core/tests/run_all_css_tests.py --visual    # Include visual tests
    python core/tests/run_all_css_tests.py --quick     # Skip visual tests
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))


def run_css_refactoring_suite():
    print("🚀 Running CSS Refactoring Suite...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "core/tests/test_css_refactoring_suite.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run CSS refactoring suite: {e}")
        return False


def run_django_integration_tests():
    print("\n🐍 Running Django CSS Integration Tests...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "manage.py",
                "test",
                "core.tests.test_css_integration",
                "--verbosity=2",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run Django integration tests: {e}")
        return False


def run_profile_pages_optimization_test():
    print("\n📄 Running Profile Pages Optimization Test...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "core/tests/test_profile_pages_optimization.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run profile pages optimization test: {e}")
        return False


def run_css_duplicate_classes_test():
    print("\n🔍 Running CSS Duplicate Classes Detection Test...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "core/tests/test_css_duplicate_classes.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run CSS duplicate classes test: {e}")
        return False


def run_visual_regression_tests():
    print("\n🌐 Running Visual Regression Tests...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "core/tests/test_visual_regression.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run visual regression tests: {e}")
        return False


def check_server_running():
    try:
        import requests

        requests.get("http://127.0.0.1:8000/", timeout=5)
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description="Run CSS refactoring test suite")
    parser.add_argument(
        "--visual", action="store_true", help="Include visual regression tests"
    )
    parser.add_argument(
        "--quick", action="store_true", help="Skip visual regression tests"
    )
    parser.add_argument(
        "--integration-only",
        action="store_true",
        help="Only run Django integration tests",
    )
    parser.add_argument(
        "--refactoring-only", action="store_true", help="Only run CSS refactoring tests"
    )

    args = parser.parse_args()

    print("🧪 CSS Test Suite - Comprehensive Testing")
    print("=" * 70)

    results = {}

    # Run CSS refactoring suite (standalone)
    if not args.integration_only:
        results["refactoring"] = run_css_refactoring_suite()

    # Run profile pages optimization test
    if not args.integration_only:
        results["profile_optimization"] = run_profile_pages_optimization_test()

    # Run CSS duplicate classes detection test
    if not args.integration_only:
        results["duplicate_classes"] = run_css_duplicate_classes_test()

    # Run Django integration tests
    if not args.refactoring_only:
        results["integration"] = run_django_integration_tests()

    # Run visual tests if requested and server is running
    if args.visual and not args.quick:
        if check_server_running():
            results["visual"] = run_visual_regression_tests()
        else:
            print("\n⚠️  Skipping visual tests - Django server not running")
            print("   Start with: python manage.py runserver")
            results["visual"] = None

    # Print overall summary
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)

    total_passed = 0
    total_run = 0

    for test_type, passed in results.items():
        if passed is None:
            status = "⚠️  SKIPPED"
        elif passed:
            status = "✅ PASSED"
            total_passed += 1
        else:
            status = "❌ FAILED"
        total_run += 1 if passed is not None else 0

        print(f"{test_type.capitalize():15} {status}")

    print("-" * 70)

    if total_run == 0:
        print("⚠️  No tests were run")
        return 1
    elif total_passed == total_run:
        print("🎉 ALL TESTS PASSED! CSS refactoring is complete and validated.")
        return 0
    else:
        failed_count = total_run - total_passed
        print(f"⚠️  {failed_count} of {total_run} test suites failed - review required")
        return 1


if __name__ == "__main__":
    sys.exit(main())
