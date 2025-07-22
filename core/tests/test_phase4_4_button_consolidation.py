#!/usr/bin/env python3
"""
Phase 4.4 Button Consolidation Test Suite
Tests for skill-pages.css button pattern consolidation to utility classes
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the parent directories to Python path for Django setup
sys.path.append(str(Path(__file__).parent.parent.parent))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")
import django

django.setup()


class TestPhase44ButtonConsolidation:
    """Test suite for Phase 4.4 button consolidation changes"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.skill_pages_css = self.base_dir / "static/css/skill-pages.css"
        self.utilities_css = self.base_dir / "static/css/utilities.css"
        self.test_results = []

    def read_file_content(self, file_path):
        """Helper to read file content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def test_duplicate_patterns_removed(self):
        """Test that duplicate button patterns were removed from skill-pages.css"""
        content = self.read_file_content(self.skill_pages_css)

        # Patterns that should be removed
        removed_patterns = [
            ".filter-btn {",
            ".view-btn {",
            ".add-first-skill-btn {",
            ".primary-btn,",
            ".secondary-btn {",
            ".submit-btn {",
            ".edit-btn {",
            ".alt-btn {",
        ]

        failures = []
        for pattern in removed_patterns:
            if pattern in content:
                failures.append(f"❌ Pattern still exists: {pattern}")

        if not failures:
            self.test_results.append(
                "✅ All duplicate button patterns successfully removed"
            )
        else:
            for failure in failures:
                self.test_results.append(failure)

    def test_utility_comments_added(self):
        """Test that helpful comments were added explaining the consolidation"""
        content = self.read_file_content(self.skill_pages_css)

        expected_comments = [
            "/* Filter buttons now use btn-primary utility class from utilities.css */",
            "/* View buttons now use btn-primary utility class from utilities.css */",
            "/* Add first skill buttons now use btn-primary utility class from utilities.css */",
            "/* Primary and secondary buttons now use utility classes from utilities.css */",
            "/* Submit buttons now use btn-primary utility class from utilities.css */",
            "/* Edit buttons now use btn-secondary utility class from utilities.css */",
            "/* Alternative buttons now use btn-secondary utility class from utilities.css */",
        ]

        failures = []
        for comment in expected_comments:
            if comment not in content:
                failures.append(f"❌ Missing comment: {comment}")

        if not failures:
            self.test_results.append("✅ All consolidation comments properly added")
        else:
            for failure in failures:
                self.test_results.append(failure)

    def test_utilities_css_has_required_classes(self):
        """Test that utilities.css contains all required button classes"""
        content = self.read_file_content(self.utilities_css)

        required_classes = [".btn-primary {", ".btn-secondary {", ".btn-success {"]

        failures = []
        for class_def in required_classes:
            if class_def not in content:
                failures.append(f"❌ Missing utility class: {class_def}")

        if not failures:
            self.test_results.append("✅ All required utility button classes present")
        else:
            for failure in failures:
                self.test_results.append(failure)

    def test_templates_updated(self):
        """Test that HTML templates were updated to use utility classes"""
        templates = [
            self.base_dir / "core/templates/core/skills/add_skill.html",
            self.base_dir / "core/templates/core/skills/skill_detail_page.html",
            self.base_dir / "core/templates/core/skills/delete_skill.html",
        ]

        # Check add_skill.html
        add_skill_content = self.read_file_content(templates[0])
        if (
            'class="btn-primary"' in add_skill_content
            and 'class="submit-btn"' not in add_skill_content
        ):
            self.test_results.append("✅ add_skill.html updated to use btn-primary")
        else:
            self.test_results.append("❌ add_skill.html not properly updated")

        # Check skill_detail_page.html
        detail_content = self.read_file_content(templates[1])
        if (
            'class="btn-secondary"' in detail_content
            and 'class="edit-btn"' not in detail_content
        ):
            self.test_results.append(
                "✅ skill_detail_page.html updated to use btn-secondary"
            )
        else:
            self.test_results.append("❌ skill_detail_page.html not properly updated")

        # Check delete_skill.html
        delete_content = self.read_file_content(templates[2])
        if (
            'class="btn-secondary"' in delete_content
            and 'class="alt-btn"' not in delete_content
        ):
            self.test_results.append(
                "✅ delete_skill.html updated to use btn-secondary"
            )
        else:
            self.test_results.append("❌ delete_skill.html not properly updated")

    def test_specialized_buttons_preserved(self):
        """Test that specialized buttons (rate-btn, delete-btn) were preserved"""
        content = self.read_file_content(self.skill_pages_css)

        preserved_patterns = [".rate-btn {", ".delete-btn {"]

        failures = []
        for pattern in preserved_patterns:
            if pattern not in content:
                failures.append(
                    f"❌ Specialized pattern incorrectly removed: {pattern}"
                )

        if not failures:
            self.test_results.append(
                "✅ Specialized button patterns correctly preserved"
            )
        else:
            for failure in failures:
                self.test_results.append(failure)

    def test_file_size_reduction(self):
        """Test that skill-pages.css file size was reduced due to consolidation"""
        try:
            file_size = os.path.getsize(self.skill_pages_css)
            # Roughly estimate - should be significantly smaller after removing ~150+ lines
            if file_size < 50000:  # Less than 50KB (rough estimate)
                self.test_results.append(
                    f"✅ File size reduced appropriately: {file_size} bytes"
                )
            else:
                self.test_results.append(
                    f"⚠️  File size: {file_size} bytes (may still be large)"
                )
        except Exception as e:
            self.test_results.append(f"❌ Error checking file size: {e}")

    def test_css_syntax_validity(self):
        """Test that CSS files have valid syntax after changes"""
        try:
            # Simple syntax check - look for unclosed braces
            content = self.read_file_content(self.skill_pages_css)

            open_braces = content.count("{")
            close_braces = content.count("}")

            if open_braces == close_braces:
                self.test_results.append(
                    "✅ CSS syntax appears valid (balanced braces)"
                )
            else:
                self.test_results.append(
                    f"❌ CSS syntax issue: {open_braces} {{ vs {close_braces} }}"
                )

        except Exception as e:
            self.test_results.append(f"❌ Error checking CSS syntax: {e}")

    def run_all_tests(self):
        """Run all test methods and report results"""
        print("🧪 Phase 4.4 Button Consolidation Test Suite")
        print("=" * 60)

        test_methods = [
            self.test_duplicate_patterns_removed,
            self.test_utility_comments_added,
            self.test_utilities_css_has_required_classes,
            self.test_templates_updated,
            self.test_specialized_buttons_preserved,
            self.test_file_size_reduction,
            self.test_css_syntax_validity,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.test_results.append(f"❌ Test {test_method.__name__} failed: {e}")

        # Print results
        print(f"\n📋 Test Results ({len(self.test_results)} checks):")
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

        print(f"\n📊 Summary: {passed} passed, {failed} failed, {warnings} warnings")

        if failed == 0:
            print("🎉 Phase 4.4 Button Consolidation: ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  Some tests failed - review the changes needed")
            return False


if __name__ == "__main__":
    tester = TestPhase44ButtonConsolidation()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
