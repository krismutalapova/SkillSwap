#!/usr/bin/env python3
"""
CSS Refactoring Test Suite - Comprehensive
Consolidated test suite for all CSS refactoring validation

This replaces all the phase-specific test files with a single comprehensive suite that:
- Tests CSS variable usage and design system consistency
- Validates button consolidation across all CSS files
- Checks for duplicate patterns and hardcoded values
- Ensures proper utility class implementation
- Validates template updates and responsive design

Usage: python core/tests/test_css_refactoring_suite.py
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Add the parent directories to Python path for Django setup
sys.path.append(str(Path(__file__).parent.parent.parent))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")
import django

django.setup()


class CSSRefactoringTestSuite:
    """Comprehensive test suite for CSS refactoring validation"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.static_css_dir = self.base_dir / "static/css"
        self.templates_dir = self.base_dir / "core/templates"
        self.test_results = []

        # CSS files to test
        self.css_files = {
            "variables": self.static_css_dir / "variables.css",
            "utilities": self.static_css_dir / "utilities.css",
            "base": self.static_css_dir / "base.css",
            "components": self.static_css_dir / "components.css",
            "skill_pages": self.static_css_dir / "skill-pages.css",
            "messaging_pages": self.static_css_dir / "messaging-pages.css",
            "home_pages": self.static_css_dir / "home-pages.css",
            "profile_pages": self.static_css_dir / "profile-pages.css",
        }

        # Template files to test
        self.template_files = {
            "base": self.templates_dir / "base.html",
            "home": self.templates_dir / "core/home.html",
            "skill_list": self.templates_dir / "core/skill_list.html",
            "skill_create": self.templates_dir / "core/skill_create.html",
            "profile_edit": self.templates_dir / "core/profile_edit.html",
            "message_inbox": self.templates_dir / "core/message_inbox.html",
        }

    def read_file_content(self, file_path: Path) -> str:
        """Helper to read file content safely"""
        try:
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception as e:
            return f"Error reading {file_path}: {e}"

    # ============================================================================
    # DESIGN SYSTEM TESTS
    # ============================================================================

    def test_css_variables_defined(self):
        """Test that all required CSS variables are properly defined"""
        variables_content = self.read_file_content(self.css_files["variables"])

        if not variables_content:
            self.test_results.append("❌ variables.css file not found or empty")
            return

        required_variables = [
            # Color system
            "--color-primary",
            "--color-primary-gradient",
            "--color-secondary",
            "--color-text-primary",
            "--color-text-secondary",
            "--color-background",
            # Spacing system
            "--nav-link-padding",
            "--nav-link-padding-mobile",
            "--button-padding-small",
            # Typography
            "--font-weight-medium",
            "--font-size-sm",
            # Layout
            "--radius-card",
            "--transition-all",
            "--nav-gap",
        ]

        missing_vars = []
        for var in required_variables:
            if var not in variables_content:
                missing_vars.append(var)

        if not missing_vars:
            self.test_results.append(
                f"✅ All {len(required_variables)} required CSS variables defined"
            )
        else:
            self.test_results.append(
                f"❌ Missing CSS variables: {', '.join(missing_vars[:3])}{'...' if len(missing_vars) > 3 else ''}"
            )

    def test_utility_classes_available(self):
        """Test that utility button classes are properly implemented"""
        utilities_content = self.read_file_content(self.css_files["utilities"])

        if not utilities_content:
            self.test_results.append("❌ utilities.css file not found or empty")
            return

        required_utilities = [
            ".btn-primary {",
            ".btn-secondary {",
            ".btn-success {",
            ".btn-danger {",
        ]

        missing_utils = []
        for util in required_utilities:
            if util not in utilities_content:
                missing_utils.append(util.replace(" {", ""))

        if not missing_utils:
            self.test_results.append(
                f"✅ All {len(required_utilities)} utility button classes available"
            )
        else:
            self.test_results.append(
                f"❌ Missing utility classes: {', '.join(missing_utils)}"
            )

    # ============================================================================
    # BUTTON CONSOLIDATION TESTS
    # ============================================================================

    def test_duplicate_button_patterns_removed(self):
        """Test that duplicate button patterns have been consolidated"""
        all_css_content = ""
        for name, path in self.css_files.items():
            if (
                name != "utilities"
            ):  # Skip utilities.css as it's supposed to have button definitions
                content = self.read_file_content(path)
                all_css_content += f"\n/* {name} */\n{content}"

        # Patterns that should not exist (consolidated into utilities)
        deprecated_patterns = [
            ".profile-btn {",
            ".profile-btn-gradient {",
            ".search-btn {",
            ".add-skill-btn {",
            ".cancel-btn {",
            ".edit-btn {",
            ".delete-btn {",
            ".contact-btn {",
        ]

        found_duplicates = []
        for pattern in deprecated_patterns:
            if pattern in all_css_content:
                found_duplicates.append(pattern.replace(" {", ""))

        if not found_duplicates:
            self.test_results.append(
                "✅ All duplicate button patterns successfully consolidated"
            )
        else:
            self.test_results.append(
                f"❌ Found duplicate button patterns: {', '.join(found_duplicates[:3])}{'...' if len(found_duplicates) > 3 else ''}"
            )

    def test_hardcoded_values_replaced(self):
        """Test that hardcoded values have been replaced with CSS variables"""
        hardcoded_issues = []

        for name, path in self.css_files.items():
            if name in ["variables", "utilities"]:
                continue  # Skip files that legitimately have hardcoded values

            content = self.read_file_content(path)
            if not content:
                continue

            # Check for hardcoded values that should be variables
            hardcoded_checks = [
                (
                    "linear-gradient(to right, #6441a5, #2a0845)",
                    "var(--color-primary-gradient)",
                ),
                ("padding: 10px 20px", "var(--nav-link-padding)"),
                ("border-radius: 15px", "var(--radius-card)"),
                ("color: #6c757d", "var(--color-text-secondary)"),
            ]

            for hardcoded, should_be in hardcoded_checks:
                if hardcoded in content and should_be not in content:
                    hardcoded_issues.append(f"{name}: {hardcoded[:30]}...")

        if not hardcoded_issues:
            self.test_results.append(
                "✅ Hardcoded values properly replaced with CSS variables"
            )
        else:
            self.test_results.append(
                f"❌ Found hardcoded values in: {', '.join(hardcoded_issues[:2])}{'...' if len(hardcoded_issues) > 2 else ''}"
            )

    def test_nav_link_consolidation(self):
        """Test that .nav-link definitions are properly consolidated"""
        nav_link_definitions = []

        for name, path in self.css_files.items():
            content = self.read_file_content(path)
            if not content:
                continue

            # Count .nav-link definitions and check their nature
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if ".nav-link {" in line.strip():
                    # Get the next few lines to understand the definition
                    definition_lines = []
                    for j in range(i + 1, min(i + 10, len(lines))):
                        definition_lines.append(lines[j].strip())
                        if lines[j].strip() == "}":
                            break

                    nav_link_definitions.append(
                        {"file": name, "line": i + 1, "properties": definition_lines}
                    )

        # Analyze definitions for duplicates
        legitimate_count = 0
        duplicate_count = 0
        main_definition_count = 0

        for defn in nav_link_definitions:
            props = " ".join(defn["properties"])
            # Check if it's a legitimate responsive override or main definition
            is_main_definition = (
                "color: var(--color-text-primary)" in props
                or "text-decoration: none" in props
                or "display: flex" in props
            )
            is_responsive_override = (
                "justify-content: center" in props
                or "padding: var(--nav-link-padding-mobile)" in props
                or len([p for p in defn["properties"] if p and p != "}"]) <= 2
            )

            if is_main_definition:
                main_definition_count += 1
                if main_definition_count == 1:
                    legitimate_count += 1  # First main definition is legitimate
                else:
                    duplicate_count += 1  # Additional main definitions are duplicates
            elif is_responsive_override:
                legitimate_count += 1
            else:
                duplicate_count += 1

        if duplicate_count == 0:
            self.test_results.append(
                f"✅ .nav-link definitions properly consolidated ({legitimate_count} legitimate overrides)"
            )
        else:
            self.test_results.append(
                f"❌ Found {duplicate_count} duplicate .nav-link definitions"
            )

    # ============================================================================
    # TEMPLATE TESTS
    # ============================================================================

    def test_templates_use_utility_classes(self):
        """Test that templates have been updated to use utility classes"""
        template_issues = []

        for name, path in self.template_files.items():
            content = self.read_file_content(path)
            if not content:
                continue

            # Check for deprecated class usage
            deprecated_classes = [
                "profile-btn-gradient",
                "profile-btn",
                "search-btn",
                "add-skill-btn",
                "cancel-btn",
                "edit-btn",
            ]

            found_deprecated = []
            for dep_class in deprecated_classes:
                if dep_class in content:
                    found_deprecated.append(dep_class)

            if found_deprecated:
                template_issues.append(f"{name}: {', '.join(found_deprecated[:2])}")

        if not template_issues:
            self.test_results.append("✅ Templates updated to use utility classes")
        else:
            self.test_results.append(
                f"❌ Templates still use deprecated classes: {'; '.join(template_issues)}"
            )

    # ============================================================================
    # FILE INTEGRITY TESTS
    # ============================================================================

    def test_css_syntax_validity(self):
        """Test that all CSS files have valid syntax"""
        syntax_issues = []

        for name, path in self.css_files.items():
            content = self.read_file_content(path)
            if not content:
                continue

            # Basic syntax checks
            open_braces = content.count("{")
            close_braces = content.count("}")

            if open_braces != close_braces:
                syntax_issues.append(f"{name} (braces: {open_braces}/{close_braces})")
                continue

            # Check for common syntax errors
            if ";;" in content:
                syntax_issues.append(f"{name} (double semicolons)")

            if re.search(r"\{\s*\}", content):
                syntax_issues.append(f"{name} (empty rules)")

        if not syntax_issues:
            self.test_results.append("✅ All CSS files have valid syntax")
        else:
            self.test_results.append(
                f"❌ CSS syntax issues in: {', '.join(syntax_issues)}"
            )

    def test_file_size_optimization(self):
        """Test that CSS file sizes are reasonable after consolidation"""
        file_sizes = {}
        large_files = []

        for name, path in self.css_files.items():
            if path.exists():
                size = os.path.getsize(path)
                file_sizes[name] = size

                # Flag files larger than 20KB as potentially bloated
                if size > 20000:
                    large_files.append(f"{name} ({size // 1000}KB)")

        total_size = sum(file_sizes.values())

        if total_size < 50000:  # Less than 50KB total is good
            self.test_results.append(
                f"✅ CSS file sizes optimized (total: {total_size // 1000}KB)"
            )
        else:
            self.test_results.append(
                f"⚠️  CSS files are large (total: {total_size // 1000}KB)"
            )

        if large_files:
            self.test_results.append(f"⚠️  Large CSS files: {', '.join(large_files)}")

    def test_color_contrast_accessibility(self):
        """Test for proper color contrast - no white text on white backgrounds"""
        print("\n🎨 Testing Color Contrast Accessibility...")

        issues = []

        # Define problematic color combinations
        light_backgrounds = [
            "var(--color-background-glass)",
            "var(--color-background-white)",
            "var(--color-background)",
            "var(--color-background-glass-light)",
            "var(--color-background-glass-strong)",
            "#ffffff",
            "#f8f9fa",
        ]

        light_text_colors = [
            "var(--color-text-light)",
            "var(--color-text-white)",
            "#f8f9fa",
            "#ffffff",
            "rgba(255, 255, 255, 0.9)",
        ]

        # Check all CSS files for contrast issues
        css_files = [
            "static/css/home-pages.css",
            "static/css/utilities.css",
            "static/css/main.css",
        ]

        for css_file in css_files:
            if os.path.exists(css_file):
                with open(css_file, "r") as f:
                    content = f.read()

                # Look for potential contrast issues
                lines = content.split("\n")
                current_selector = None
                current_background = None
                current_color = None

                for i, line in enumerate(lines, 1):
                    line = line.strip()

                    # Track current selector
                    if line.endswith("{") and not line.startswith("/*"):
                        current_selector = line.replace(" {", "")
                        current_background = None
                        current_color = None

                    # Check for background properties
                    if "background:" in line or "background-color:" in line:
                        for bg in light_backgrounds:
                            if bg in line:
                                current_background = bg
                                break

                    # Check for color properties
                    if line.startswith("color:"):
                        for color in light_text_colors:
                            if color in line:
                                current_color = color
                                break

                    # Flag potential issues
                    if current_background and current_color and current_selector:
                        issues.append(
                            {
                                "file": css_file,
                                "line": i,
                                "selector": current_selector,
                                "issue": f"Light text ({current_color}) on light background ({current_background})",
                                "severity": "HIGH",
                            }
                        )

        # Specific checks for home-pages.css critical sections
        home_css_file = "static/css/home-pages.css"
        if os.path.exists(home_css_file):
            with open(home_css_file, "r") as f:
                content = f.read()

            # Check hero section specifically
            if "color: var(--color-text-light)" in content:
                # Check if it's in a glassmorphism context
                hero_section = content[
                    content.find(".hero-") : (
                        content.find(".features-section")
                        if ".features-section" in content
                        else len(content)
                    )
                ]
                if "var(--color-text-light)" in hero_section:
                    issues.append(
                        {
                            "file": home_css_file,
                            "section": "hero-section",
                            "issue": "Using --color-text-light in glassmorphism context (white background)",
                            "severity": "CRITICAL",
                            "fix": "Use --color-text-secondary or --color-text-muted instead",
                        }
                    )

        # Report results
        if issues:
            print(f"\n❌ Found {len(issues)} color contrast issues:")
            for issue in issues:
                print(f"   • {issue.get('file', 'Unknown')}: {issue['issue']}")
                if "fix" in issue:
                    print(f"     Fix: {issue['fix']}")
            return False
        else:
            print("✅ No color contrast issues found")
            return True

    def test_css_semantic_color_usage(self):
        """Test that semantic color variables are used appropriately"""
        print("\n🏷️  Testing Semantic Color Usage...")

        recommendations = []

        # Check home-pages.css for appropriate semantic color usage
        home_css_file = "static/css/home-pages.css"
        if os.path.exists(home_css_file):
            with open(home_css_file, "r") as f:
                content = f.read()

            # Check current usage patterns
            color_usage = {
                "var(--color-text-primary)": content.count("var(--color-text-primary)"),
                "var(--color-text-secondary)": content.count(
                    "var(--color-text-secondary)"
                ),
                "var(--color-text-muted)": content.count("var(--color-text-muted)"),
                "var(--color-text-light)": content.count("var(--color-text-light)"),
                "var(--color-text-dark)": content.count("var(--color-text-dark)"),
            }

            print(f"   Color usage in home-pages.css:")
            for color, count in color_usage.items():
                status = "⚠️" if count > 0 and "light" in color else "✅"
                print(f"   {status} {color}: {count} uses")

            # Verify no problematic usage remains
            if color_usage["var(--color-text-light)"] > 0:
                recommendations.append(
                    "Replace remaining var(--color-text-light) uses with var(--color-text-secondary) for better contrast"
                )

        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"   • {rec}")
            return True  # This is advisory, not a failure
        else:
            print("✅ Semantic color usage follows best practices")
            return True

    def test_equal_height_card_layouts(self):
        """Test that card grids use align-items: stretch for equal heights"""
        print("\n📐 Testing Equal Height Card Layouts...")

        issues = []

        # Define grid layouts that should have equal height cards
        grid_patterns = {
            "static/css/home-pages.css": [".users-grid"],
            "static/css/skill-pages.css": [".skills-grid"],
            "static/css/components.css": [".skills-grid"],
            "static/css/profile-pages.css": [".profile-skills-grid"],
        }

        for css_file, selectors in grid_patterns.items():
            if os.path.exists(css_file):
                with open(css_file, "r") as f:
                    content = f.read()

                for selector in selectors:
                    # Find the selector and check if it has align-items: stretch
                    if selector in content:
                        # Extract the CSS rule for this selector
                        start_pos = content.find(selector)
                        if start_pos != -1:
                            # Find the opening brace
                            brace_pos = content.find("{", start_pos)
                            if brace_pos != -1:
                                # Find the closing brace
                                closing_brace_pos = content.find("}", brace_pos)
                                if closing_brace_pos != -1:
                                    rule_content = content[
                                        brace_pos : closing_brace_pos + 1
                                    ]

                                    # Check for display: grid and align-items: stretch
                                    has_grid = "display: grid" in rule_content
                                    has_stretch = "align-items: stretch" in rule_content

                                    if has_grid and not has_stretch:
                                        issues.append(
                                            {
                                                "file": css_file,
                                                "selector": selector,
                                                "issue": "Grid layout missing align-items: stretch for equal height cards",
                                            }
                                        )
                                    elif has_grid and has_stretch:
                                        print(
                                            f"   ✅ {css_file}: {selector} has equal height configuration"
                                        )
                    else:
                        issues.append(
                            {
                                "file": css_file,
                                "selector": selector,
                                "issue": "Expected grid selector not found",
                            }
                        )

        # Check for flex cards that should fill height
        flex_card_patterns = {
            "static/css/home-pages.css": [".user-card"],
            "static/css/components.css": [".skill-card"],
        }

        for css_file, selectors in flex_card_patterns.items():
            if os.path.exists(css_file):
                with open(css_file, "r") as f:
                    content = f.read()

                for selector in selectors:
                    if selector in content:
                        start_pos = content.find(selector)
                        if start_pos != -1:
                            brace_pos = content.find("{", start_pos)
                            if brace_pos != -1:
                                closing_brace_pos = content.find("}", brace_pos)
                                if closing_brace_pos != -1:
                                    rule_content = content[
                                        brace_pos : closing_brace_pos + 1
                                    ]

                                    has_flex = "display: flex" in rule_content
                                    has_column = (
                                        "flex-direction: column" in rule_content
                                    )
                                    has_height = "height: 100%" in rule_content

                                    if has_flex and has_column and has_height:
                                        print(
                                            f"   ✅ {css_file}: {selector} configured for equal height"
                                        )
                                    elif has_flex and has_column and not has_height:
                                        issues.append(
                                            {
                                                "file": css_file,
                                                "selector": selector,
                                                "issue": "Flex card missing height: 100% for equal height",
                                            }
                                        )

        if issues:
            print(f"\n❌ Found {len(issues)} equal height layout issues:")
            for issue in issues:
                print(f"   • {issue['file']}: {issue['selector']} - {issue['issue']}")
            return False
        else:
            print("✅ All card grids configured for equal heights")
            return True

    def test_home_pages_css_hardcoded_values(self):
        """Test that home-pages.css has no hardcoded values"""
        home_pages_content = self.read_file_content(self.css_files["home_pages"])

        if not home_pages_content:
            self.test_results.append("❌ home-pages.css file not found or empty")
            return

        # Hardcoded values that should be replaced with variables
        hardcoded_patterns = [
            # Spacing values
            r"\b60px\b",
            r"\b40px\b",
            r"\b30px\b",
            r"\b25px\b",
            r"\b20px\b",
            r"\b15px\b",
            r"\b10px\b",
            r"\b5px\b",
            r"\b3px\b",
            # Font sizes in em units
            r"\b3em\b",
            r"\b2\.5em\b",
            r"\b1\.2em\b",
            # Hardcoded colors
            r"#333\b",
            r"#495057\b",
            r"#dee2e6\b",
            # Hardcoded shadows
            r"0 8px 32px rgba\(0, 0, 0, 0\.1\)",
            r"0 8px 25px rgba\(0, 0, 0, 0\.1\)",
            r"0 4px 20px rgba\(0, 0, 0, 0\.1\)",
            # Hardcoded blur
            r"blur\(10px\)",
            # Max widths
            r"max-width: 600px",
            r"max-width: 1200px",
        ]

        found_hardcoded = []
        for pattern in hardcoded_patterns:
            import re

            matches = re.findall(pattern, home_pages_content)
            if matches:
                found_hardcoded.extend(matches)

        if found_hardcoded:
            self.test_results.append(
                f"❌ home-pages.css contains hardcoded values: {', '.join(set(found_hardcoded))}"
            )
        else:
            self.test_results.append(
                "✅ home-pages.css uses CSS variables consistently"
            )

    def test_home_pages_css_variable_usage(self):
        """Test that home-pages.css uses appropriate CSS variables"""
        home_pages_content = self.read_file_content(self.css_files["home_pages"])

        if not home_pages_content:
            self.test_results.append("❌ home-pages.css file not found or empty")
            return

        # Variables that should be used
        expected_variables = [
            "--space-6xl",  # For 60px padding
            "--space-4xl",  # For 40px padding
            "--space-xxl",  # For 30px spacing
            "--space-xl",  # For 25px spacing
            "--space-lg",  # For 20px spacing
            "--space-md",  # For 15px spacing
            "--space-sm",  # For smaller gaps
            "--color-text-primary",  # For #333 colors
            "--color-text-secondary",  # For muted text
            "--font-size-3xl",  # For large titles
            "--font-size-2xl",  # For section titles
            "--font-size-lg",  # For subtitles
            "--shadow-glass-card",  # For glassmorphism shadows
            "--glass-backdrop-filter",  # For backdrop filter
            "--transform-hover-lift",  # For hover effects
        ]

        missing_variables = []
        for variable in expected_variables:
            if variable not in home_pages_content:
                missing_variables.append(variable)

        if missing_variables:
            self.test_results.append(
                f"⚠️  home-pages.css missing recommended variables: {', '.join(missing_variables)}"
            )
        else:
            self.test_results.append("✅ home-pages.css uses recommended CSS variables")

    # ============================================================================
    # TEST RUNNER
    # ============================================================================

    def run_all_tests(self):
        """Run all test methods and report results"""
        print("🧪 CSS Refactoring Comprehensive Test Suite")
        print("=" * 60)
        print("Testing CSS variable usage, button consolidation, template updates,")
        print("hardcoded value replacement, and file integrity.\n")

        test_methods = [
            # Design System Tests
            self.test_css_variables_defined,
            self.test_utility_classes_available,
            # Button Consolidation Tests
            self.test_duplicate_button_patterns_removed,
            self.test_hardcoded_values_replaced,
            self.test_nav_link_consolidation,
            # Template Tests
            self.test_templates_use_utility_classes,
            # File Integrity Tests
            self.test_css_syntax_validity,
            self.test_file_size_optimization,
            # Accessibility Tests
            self.test_color_contrast_accessibility,
            self.test_css_semantic_color_usage,
            self.test_equal_height_card_layouts,
            # Home Pages Specific Tests
            self.test_home_pages_css_hardcoded_values,
            self.test_home_pages_css_variable_usage,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.test_results.append(f"❌ Test {test_method.__name__} failed: {e}")

        # Print results
        print(f"📋 Test Results ({len(self.test_results)} checks):")
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
            if warnings == 0:
                print("🎉 CSS Refactoring: ALL TESTS PASSED!")
            else:
                print("✨ CSS Refactoring: PASSED WITH WARNINGS")
            return True
        else:
            print("⚠️  Some tests failed - review the refactoring work needed")
            return False


if __name__ == "__main__":
    tester = CSSRefactoringTestSuite()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
