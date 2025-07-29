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
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

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
            "auth_pages": self.static_css_dir / "auth-pages.css",
            "search_page": self.static_css_dir / "search-page.css",
            "error_pages": self.static_css_dir / "error-pages.css",
            "component_pages": self.static_css_dir / "component-pages.css",
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

    def test_undefined_css_variables(self):
        """Test that all CSS variables used in files are defined in variables.css"""
        variables_content = self.read_file_content(self.css_files["variables"])

        if not variables_content:
            self.test_results.append(
                "❌ variables.css file not found - cannot validate variable usage"
            )
            return

        # Extract all defined variables from variables.css
        defined_variables = set()
        variable_pattern = r"--[\w-]+(?=\s*:)"
        for match in re.finditer(variable_pattern, variables_content):
            defined_variables.add(match.group().strip())

        # Check each CSS file for undefined variables
        undefined_variables = {}
        css_files_to_check = [
            "base",
            "components",
            "utilities",
            "home_pages",
            "profile_pages",
            "messaging_pages",
            "skill_pages",
            "auth_pages",
            "search_page",
            "error_pages",
        ]

        for file_key in css_files_to_check:
            if file_key not in self.css_files:
                continue

            file_path = self.css_files[file_key]
            if not file_path.exists():
                continue

            file_content = self.read_file_content(file_path)
            if not file_content:
                continue

            # Find all var() usage in the file
            used_variables = set()
            var_usage_pattern = r"var\(\s*(--[\w-]+)\s*(?:,.*?)?\)"
            for match in re.finditer(var_usage_pattern, file_content):
                used_variables.add(match.group(1).strip())

            # Check for undefined variables
            file_undefined = used_variables - defined_variables
            if file_undefined:
                undefined_variables[file_key] = sorted(file_undefined)

        if undefined_variables:
            total_undefined = sum(len(vars) for vars in undefined_variables.values())
            self.test_results.append(
                f"❌ {total_undefined} undefined CSS variables found across {len(undefined_variables)} files"
            )

            # Show details for debugging
            for file_key, vars_list in undefined_variables.items():
                print(f"   📁 {file_key}: {', '.join(vars_list[:3])}")
                if len(vars_list) > 3:
                    print(f"      ... and {len(vars_list) - 3} more")
        else:
            self.test_results.append(
                "✅ All CSS variables are properly defined in variables.css"
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
            "var(--color-text-white)",
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
            if "color: var(--color-text-white)" in content:
                # Check if it's in a glassmorphism context
                hero_section = content[
                    content.find(".hero-") : (
                        content.find(".features-section")
                        if ".features-section" in content
                        else len(content)
                    )
                ]
                if "var(--color-text-white)" in hero_section:
                    issues.append(
                        {
                            "file": home_css_file,
                            "section": "hero-section",
                            "issue": "Using --color-text-white in glassmorphism context (white background)",
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

    def test_text_visibility_on_white_backgrounds(self):
        """Test for invisible text elements on white backgrounds with design exceptions"""
        print("\n👁️  Testing Text Visibility on White Backgrounds...")

        css_files = [
            "static/css/utilities.css",
            "static/css/auth-pages.css",
            "static/css/profile-pages.css",
            "static/css/components.css",
            "static/css/component-pages.css",
            "static/css/skill-pages.css",
            "static/css/home-pages.css",
            "static/css/messaging-pages.css",
            "static/css/error-pages.css",
        ]

        # Problematic colors that can be invisible on white backgrounds
        problematic_colors = ["var(--color-text-white)", "var(--color-border-muted)"]

        # Exception classes that are allowed to use light colors for design purposes
        exception_classes = {".star-rating-display .stars i", ".skill-rating .stars i"}

        problematic_text_colors = []

        for css_file in css_files:
            if not os.path.exists(css_file):
                continue

            with open(css_file, "r") as f:
                content = f.read()
                lines = content.split("\n")

            for i, line in enumerate(lines, 1):
                # Only check text color properties (not border or background)
                if re.search(
                    r"^\s*color:\s*var\(--color-(text-light|border-muted)\)",
                    line.strip(),
                ):
                    selector = ""
                    for j in range(i - 1, max(0, i - 10), -1):
                        if "{" in lines[j - 1]:
                            selector = (
                                lines[j - 1].strip().replace(" {", "").replace("{", "")
                            )
                            break

                    if selector not in exception_classes:
                        problematic_text_colors.append(
                            {
                                "file": css_file,
                                "line": i,
                                "selector": selector,
                                "issue": f"Line {i}: {selector} uses {line.strip()}",
                                "fix": "Change to var(--color-text-secondary) for better contrast",
                            }
                        )

        if problematic_text_colors:
            print(f"\n❌ Found {len(problematic_text_colors)} text visibility issues:")
            for issue in problematic_text_colors:
                print(f"   • {issue['file']}: {issue['issue']}")
                print(f"     Fix: {issue['fix']}")
            print(f"\n📝 Note: Exceptions applied for design choices:")
            for exception in exception_classes:
                print(f"   • {exception} (intentionally muted for visual hierarchy)")
            return False
        else:
            print("✅ No text visibility issues found")
            print(
                f"📝 Checked {len([f for f in css_files if os.path.exists(f)])} CSS files"
            )
            if exception_classes:
                print("📝 Applied design exceptions for:")
                for exception in exception_classes:
                    print(f"   • {exception}")
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
                "var(--color-text-white)": content.count("var(--color-text-white)"),
                "var(--color-text-dark)": content.count("var(--color-text-dark)"),
            }

            print(f"   Color usage in home-pages.css:")
            for color, count in color_usage.items():
                status = "⚠️" if count > 0 and "light" in color else "✅"
                print(f"   {status} {color}: {count} uses")

            # Verify no problematic usage remains
            if color_usage["var(--color-text-white)"] > 0:
                recommendations.append(
                    "Replace remaining var(--color-text-white) uses with var(--color-text-secondary) for better contrast"
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

    def test_messaging_pages_css_hardcoded_values(self):
        """Test that messaging-pages.css has no hardcoded values that should be variables"""
        messaging_pages_content = self.read_file_content(
            self.css_files["messaging_pages"]
        )

        if not messaging_pages_content:
            self.test_results.append("❌ messaging-pages.css file not found or empty")
            return

        # Specific hardcoded values that should be replaced in messaging-pages.css
        hardcoded_checks = [
            ("#667eea", "var(--color-secondary)", "Primary brand color"),
            ("#333", "var(--color-text-dark)", "Dark text color"),
            ("#555", "var(--color-text-secondary)", "Secondary text color"),
            ("#495057", "var(--color-text-muted)", "Muted text color"),
            ("#dee2e6", "var(--color-border-muted)", "Border color"),
            ("#e9ecef", "var(--color-border-muted)", "Border color"),
            (
                "rgba(255, 255, 255, 0.95)",
                "var(--color-background-glass)",
                "Glassmorphism background",
            ),
            (
                "backdrop-filter: blur(10px)",
                "var(--glass-backdrop-filter)",
                "Glassmorphism blur",
            ),
            ("padding: 40px", "var(--space-5xl)", "Large padding"),
            ("padding: 30px", "var(--space-4xl)", "Medium-large padding"),
            ("padding: 25px", "var(--space-xl)", "Medium padding"),
            ("padding: 20px", "var(--space-lg)", "Default padding"),
            ("margin-bottom: 25px", "var(--space-xl)", "Spacing"),
            ("margin-bottom: 20px", "var(--space-lg)", "Spacing"),
            ("gap: 15px", "var(--space-md)", "Grid gap"),
            ("gap: 10px", "var(--space-sm)", "Small gap"),
        ]

        found_issues = []
        for hardcoded, replacement, description in hardcoded_checks:
            if hardcoded in messaging_pages_content:
                found_issues.append(f"{description}: {hardcoded} → {replacement}")

        if found_issues:
            self.test_results.append(
                f"❌ messaging-pages.css needs refactoring: {len(found_issues)} hardcoded values found"
            )
            # Add detailed output for debugging
            for issue in found_issues[:5]:  # Show first 5 issues
                print(f"   • {issue}")
            if len(found_issues) > 5:
                print(f"   • ... and {len(found_issues) - 5} more issues")
        else:
            self.test_results.append(
                "✅ messaging-pages.css uses CSS variables consistently"
            )

    def test_profile_pages_css_hardcoded_values(self):
        """Test that profile-pages.css has no hardcoded values that should be variables"""
        profile_pages_content = self.read_file_content(self.css_files["profile_pages"])

        if not profile_pages_content:
            self.test_results.append("❌ profile-pages.css file not found or empty")
            return

        # Specific hardcoded values that should be replaced in profile-pages.css
        hardcoded_checks = [
            ("#667eea", "var(--color-secondary)", "Primary brand color"),
            ("#333", "var(--color-text-dark)", "Dark text color"),
            ("#999", "var(--color-text-white)", "Light text color"),
            ("#666", "var(--color-text-secondary)", "Secondary text color"),
            ("#555", "var(--color-text-secondary)", "Secondary text color"),
            ("#dee2e6", "var(--color-border-muted)", "Border color"),
            ("#e9ecef", "var(--color-border-muted)", "Border color"),
            (
                "rgba(255, 255, 255, 0.95)",
                "var(--color-background-glass)",
                "Glassmorphism background",
            ),
            (
                "backdrop-filter: blur(10px)",
                "var(--glass-backdrop-filter)",
                "Glassmorphism blur",
            ),
            ("padding: 40px", "var(--space-5xl)", "Extra large padding"),
            ("padding: 30px", "var(--space-4xl)", "Large padding"),
            ("padding: 25px", "var(--space-xl)", "Medium-large padding"),
            ("padding: 20px", "var(--space-lg)", "Default padding"),
            ("padding: 15px", "var(--space-md)", "Medium padding"),
            ("padding: 12px", "var(--space-md)", "Medium padding"),
            ("padding: 10px", "var(--space-sm)", "Small padding"),
            ("margin-bottom: 30px", "var(--space-4xl)", "Large spacing"),
            ("margin-bottom: 25px", "var(--space-xl)", "Medium-large spacing"),
            ("margin-bottom: 20px", "var(--space-lg)", "Default spacing"),
            ("margin-bottom: 15px", "var(--space-md)", "Medium spacing"),
            ("margin-bottom: 10px", "var(--space-sm)", "Small spacing"),
            ("gap: 20px", "var(--space-lg)", "Grid gap"),
            ("gap: 15px", "var(--space-md)", "Grid gap"),
            ("gap: 10px", "var(--space-sm)", "Small gap"),
            ("gap: 8px", "var(--space-sm)", "Small gap"),
            ("gap: 5px", "var(--space-xs)", "Extra small gap"),
            ("font-size: 18px", "var(--font-size-lg)", "Large font size"),
            ("font-size: 1.2rem", "var(--font-size-xl)", "Extra large font size"),
            ("font-size: 1.1rem", "var(--font-size-lg)", "Large font size"),
            ("font-size: 0.9rem", "var(--font-size-sm)", "Small font size"),
            ("font-size: 0.8rem", "var(--font-size-xs)", "Extra small font size"),
        ]

        found_issues = []
        for hardcoded, replacement, description in hardcoded_checks:
            if hardcoded in profile_pages_content:
                found_issues.append(f"{description}: {hardcoded} → {replacement}")

        if found_issues:
            self.test_results.append(
                f"❌ profile-pages.css needs refactoring: {len(found_issues)} hardcoded values found"
            )
            # Add detailed output for debugging
            for issue in found_issues[:5]:  # Show first 5 issues
                print(f"   • {issue}")
            if len(found_issues) > 5:
                print(f"   • ... and {len(found_issues) - 5} more issues")
        else:
            self.test_results.append(
                "✅ profile-pages.css uses CSS variables consistently"
            )

    def test_profile_pages_css_optimization_analysis(self):
        """Comprehensive analysis of profile-pages.css optimization opportunities"""
        profile_pages_content = self.read_file_content(self.css_files["profile_pages"])

        if not profile_pages_content:
            self.test_results.append("❌ profile-pages.css file not found or empty")
            return

        print("\n🔍 Profile-Pages.css Optimization Analysis...")

        # 1. Find remaining hardcoded values
        hardcoded_patterns = {
            "colors": re.findall(r"#[0-9a-fA-F]{3,6}", profile_pages_content),
            "px_values": re.findall(r"\b(\d+)px\b", profile_pages_content),
            "rem_values": re.findall(r"\b(\d+\.?\d*)rem\b", profile_pages_content),
            "transform_values": re.findall(
                r"translateY\(([^)]+)\)", profile_pages_content
            ),
            "rgba_values": re.findall(r"rgba?\([^)]+\)", profile_pages_content),
        }

        optimization_opportunities = []

        # Analyze hardcoded pixel values
        px_values = [int(px) for px in hardcoded_patterns["px_values"]]
        common_sizes = {}
        for px in px_values:
            common_sizes[px] = common_sizes.get(px, 0) + 1

        repeating_sizes = {k: v for k, v in common_sizes.items() if v > 1}
        if repeating_sizes:
            optimization_opportunities.append(
                f"Repeating pixel values: {list(repeating_sizes.keys())}"
            )

        # Check for hardcoded responsive breakpoints
        breakpoint_matches = re.findall(
            r"@media[^{]*\(.*?(\d+)px\)", profile_pages_content
        )
        if breakpoint_matches:
            breakpoints = [int(bp) for bp in breakpoint_matches]
            optimization_opportunities.append(
                f"Hardcoded breakpoints: {sorted(set(breakpoints))}"
            )

        # Analyze profile picture sizes - check for repetitive dimensions
        profile_pic_sizes = re.findall(
            r"(?:width|height):\s*120px", profile_pages_content
        )
        if len(profile_pic_sizes) > 2:
            optimization_opportunities.append(
                f"Profile picture size (120px) used {len(profile_pic_sizes)} times - could use --profile-pic-size variable"
            )

        # Check for hardcoded grid values
        grid_matches = re.findall(r"minmax\((\d+px)", profile_pages_content)
        if grid_matches:
            optimization_opportunities.append(
                f"Hardcoded grid minmax values: {grid_matches}"
            )

        # Check for border widths
        border_widths = re.findall(r"border(?:-\w+)?:\s*(\d+)px", profile_pages_content)
        border_width_counts = {}
        for width in border_widths:
            border_width_counts[width] = border_width_counts.get(width, 0) + 1

        repeating_borders = {k: v for k, v in border_width_counts.items() if v > 1}
        if repeating_borders:
            optimization_opportunities.append(
                f"Repeating border widths: {list(repeating_borders.keys())}"
            )

        # Check for transform values that could be variables
        transform_values = hardcoded_patterns["transform_values"]
        if transform_values:
            unique_transforms = list(set(transform_values))
            if len(unique_transforms) > 1:
                optimization_opportunities.append(
                    f"Hardcoded transform values: {unique_transforms}"
                )

        # Analyze variable usage vs hardcoded values ratio
        var_matches = re.findall(r"var\(--[^)]+\)", profile_pages_content)
        hardcoded_values = (
            len(hardcoded_patterns["px_values"])
            + len(hardcoded_patterns["colors"])
            + len(hardcoded_patterns["rem_values"])
        )

        if hardcoded_values > 0:
            variable_ratio = (
                len(var_matches) / (len(var_matches) + hardcoded_values) * 100
            )
            print(
                f"   📊 CSS Variable Usage: {variable_ratio:.1f}% ({len(var_matches)} variables vs {hardcoded_values} hardcoded values)"
            )

        # Check for duplicate CSS rules
        selectors = re.findall(r"^([^{@]+){", profile_pages_content, re.MULTILINE)
        selector_counts = {}
        for selector in selectors:
            clean_selector = selector.strip()
            selector_counts[clean_selector] = selector_counts.get(clean_selector, 0) + 1

        duplicate_selectors = {k: v for k, v in selector_counts.items() if v > 1}
        if duplicate_selectors:
            optimization_opportunities.append(
                f"Duplicate selectors: {list(duplicate_selectors.keys())[:3]}"
            )

        # Check file structure and organization
        lines = profile_pages_content.split("\n")
        comment_sections = [
            line
            for line in lines
            if line.strip().startswith("/*") and "section" in line.lower()
        ]

        if len(comment_sections) < 3:
            optimization_opportunities.append(
                "File lacks proper section organization (comments)"
            )

        # Summary
        if optimization_opportunities:
            print(
                f"   ⚠️  {len(optimization_opportunities)} optimization opportunities found:"
            )
            for i, opportunity in enumerate(optimization_opportunities[:5], 1):
                print(f"   {i}. {opportunity}")
            if len(optimization_opportunities) > 5:
                print(f"   ... and {len(optimization_opportunities) - 5} more")

            # Determine priority level
            if hardcoded_values > 20:
                priority = "HIGH"
            elif hardcoded_values > 10:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            self.test_results.append(
                f"⚠️  profile-pages.css optimization opportunities: {len(optimization_opportunities)} areas ({priority} priority)"
            )
        else:
            print("   ✅ No major optimization opportunities found")
            self.test_results.append("✅ profile-pages.css is well optimized")

    def test_search_pages_css_hardcoded_values(self):
        """Test that search-page.css has no hardcoded values that should be variables"""
        search_pages_content = self.read_file_content(self.css_files["search_page"])

        if not search_pages_content:
            self.test_results.append("❌ search-page.css file not found or empty")
            return

        # Specific hardcoded values that should be replaced in search-page.css
        hardcoded_checks = [
            ("#333", "var(--color-text-dark)", "Dark text color"),
            (
                "rgba(102, 126, 234, 0.1)",
                "var(--color-secondary-light)",
                "Secondary light background",
            ),
            ("rgba(0,0,0,0.15)", "var(--shadow-hover-mild)", "Hover shadow effect"),
            (
                "rgba(40, 167, 69, 0.1)",
                "var(--color-success-light)",
                "Success color background",
            ),
            ("padding: 20px", "var(--space-lg)", "Standard padding"),
            ("padding: 15px", "var(--space-md)", "Medium padding"),
            ("padding: 10px", "var(--space-sm-plus)", "Small-plus padding"),
            ("margin-bottom: 30px", "var(--space-xxl)", "Large spacing"),
            ("margin-bottom: 20px", "var(--space-lg)", "Standard spacing"),
            ("margin-bottom: 15px", "var(--space-md)", "Medium spacing"),
            ("margin-bottom: 10px", "var(--space-sm-plus)", "Small-plus spacing"),
            ("gap: 20px", "var(--space-lg)", "Grid gap"),
            ("gap: 15px", "var(--space-md)", "Medium gap"),
            ("gap: 5px", "var(--space-xs)", "Small gap"),
            ("font-size: 32px", "var(--font-size-3xl)", "Large title font"),
            ("font-size: 18px", "var(--font-size-lg)", "Large font"),
            ("font-size: 16px", "var(--font-size-md)", "Medium font"),
            ("font-size: 14px", "var(--font-size-sm)", "Small font"),
            ("font-size: 12px", "var(--font-size-xs)", "Extra small font"),
            ("max-width: 1200px", "var(--container-max-width)", "Container max width"),
            ("max-width: 600px", "var(--search-bar-max-width)", "Search bar max width"),
            (
                "minmax(350px, 1fr)",
                "minmax(var(--user-card-min-width), 1fr)",
                "User card grid sizing",
            ),
        ]

        found_issues = []
        for hardcoded, replacement, description in hardcoded_checks:
            if hardcoded in search_pages_content:
                found_issues.append(f"{description}: {hardcoded} → {replacement}")

        if found_issues:
            self.test_results.append(
                f"❌ search-page.css needs refactoring: {len(found_issues)} hardcoded values found"
            )
            # Add detailed output for debugging
            for issue in found_issues[:5]:  # Show first 5 issues
                print(f"   • {issue}")
            if len(found_issues) > 5:
                print(f"   • ... and {len(found_issues) - 5} more issues")
        else:
            self.test_results.append(
                "✅ search-page.css uses CSS variables consistently"
            )

    def test_search_pages_css_optimization_analysis(self):
        """Comprehensive analysis of search-page.css optimization opportunities"""
        search_pages_content = self.read_file_content(self.css_files["search_page"])

        if not search_pages_content:
            self.test_results.append("❌ search-page.css file not found or empty")
            return

        print("\n🔍 Search-Page.css Optimization Analysis...")

        # 1. Find remaining hardcoded values
        hardcoded_patterns = {
            "colors": re.findall(r"#[0-9a-fA-F]{3,6}", search_pages_content),
            "px_values": re.findall(r"\b(\d+)px\b", search_pages_content),
            "rem_values": re.findall(r"\b(\d+\.?\d*)rem\b", search_pages_content),
            "rgba_values": re.findall(r"rgba?\([^)]+\)", search_pages_content),
            "percentages": re.findall(r"\b(\d+)%\b", search_pages_content),
        }

        optimization_opportunities = []

        # Analyze hardcoded pixel values
        px_values = [int(px) for px in hardcoded_patterns["px_values"]]
        common_sizes = {}
        for px in px_values:
            common_sizes[px] = common_sizes.get(px, 0) + 1

        repeating_sizes = {k: v for k, v in common_sizes.items() if v > 1}
        if repeating_sizes:
            optimization_opportunities.append(
                f"Repeating pixel values (use spacing variables): {list(repeating_sizes.keys())}"
            )

        # Check for hardcoded grid values that need variables
        grid_matches = re.findall(r"minmax\((\d+px)", search_pages_content)
        if grid_matches:
            optimization_opportunities.append(
                f"Hardcoded grid minmax values: {grid_matches} (use --user-card-min-width)"
            )

        # Check for hardcoded max-widths that should be container variables
        max_width_matches = re.findall(r"max-width:\s*(\d+px)", search_pages_content)
        if max_width_matches:
            optimization_opportunities.append(
                f"Hardcoded max-width values: {max_width_matches} (use container variables)"
            )

        # Check for user avatar sizes - should be standardized
        avatar_sizes = re.findall(r"(?:width|height):\s*60px", search_pages_content)
        if len(avatar_sizes) > 2:
            optimization_opportunities.append(
                f"User avatar size (60px) used {len(avatar_sizes)} times - could use --user-avatar-size variable"
            )

        # Check for empty state icon sizes
        icon_sizes = re.findall(r"(?:width|height):\s*80px", search_pages_content)
        if len(icon_sizes) > 1:
            optimization_opportunities.append(
                f"Large icon size (80px) used {len(icon_sizes)} times - could use --empty-state-icon-size variable"
            )

        # Check for transform values that could be variables
        transform_values = re.findall(r"translateY\(([^)]+)\)", search_pages_content)
        if transform_values:
            unique_transforms = list(set(transform_values))
            if len(unique_transforms) > 1:
                optimization_opportunities.append(
                    f"Hardcoded transform values: {unique_transforms} (use transform variables)"
                )

        # Analyze variable usage vs hardcoded values ratio
        var_matches = re.findall(r"var\(--[^)]+\)", search_pages_content)
        hardcoded_values = (
            len(hardcoded_patterns["px_values"])
            + len(hardcoded_patterns["colors"])
            + len(hardcoded_patterns["rem_values"])
            + len(hardcoded_patterns["rgba_values"])
        )

        if hardcoded_values > 0:
            variable_ratio = (
                len(var_matches) / (len(var_matches) + hardcoded_values) * 100
            )
            print(
                f"   📊 CSS Variable Usage: {variable_ratio:.1f}% ({len(var_matches)} variables vs {hardcoded_values} hardcoded values)"
            )

        # Check for file structure and organization
        lines = search_pages_content.split("\n")
        comment_sections = [
            line
            for line in lines
            if line.strip().startswith("/*")
            and ("====" in line or "section" in line.lower())
        ]

        if len(comment_sections) < 4:
            optimization_opportunities.append(
                "File lacks proper section organization (needs /* ===== SECTION ===== */ structure)"
            )

        # Check for duplicate or similar selectors
        selectors = re.findall(r"^([.#][^{@\s]+)", search_pages_content, re.MULTILINE)
        selector_counts = {}
        for selector in selectors:
            clean_selector = selector.strip()
            selector_counts[clean_selector] = selector_counts.get(clean_selector, 0) + 1

        duplicate_selectors = {k: v for k, v in selector_counts.items() if v > 1}
        if duplicate_selectors:
            optimization_opportunities.append(
                f"Duplicate selectors need consolidation: {list(duplicate_selectors.keys())[:3]}"
            )

        # Summary
        if optimization_opportunities:
            print(
                f"   ⚠️  {len(optimization_opportunities)} optimization opportunities found:"
            )
            for i, opportunity in enumerate(optimization_opportunities[:5], 1):
                print(f"   {i}. {opportunity}")
            if len(optimization_opportunities) > 5:
                print(f"   ... and {len(optimization_opportunities) - 5} more")

            # Determine priority level based on analysis
            if hardcoded_values > 50:
                priority = "CRITICAL"
            elif hardcoded_values > 30:
                priority = "HIGH"
            elif hardcoded_values > 15:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            self.test_results.append(
                f"⚠️  search-page.css optimization opportunities: {len(optimization_opportunities)} areas ({priority} priority)"
            )
        else:
            print("   ✅ No major optimization opportunities found")
            self.test_results.append("✅ search-page.css is well optimized")

    def test_search_pages_css_variable_usage(self):
        """Test that search-page.css uses appropriate CSS variables from the design system"""
        search_pages_content = self.read_file_content(self.css_files["search_page"])

        if not search_pages_content:
            self.test_results.append("❌ search-page.css file not found or empty")
            return

        # Variables that should be used in search-page.css
        expected_variables = [
            "--space-lg",  # For 20px spacing
            "--space-md",  # For 15px spacing
            "--space-sm-plus",  # For 10px spacing
            "--space-sm",  # For 8px spacing
            "--space-xs",  # For 5px spacing
            "--space-xxl",  # For 30px spacing
            "--space-4xl",  # For 40px spacing
            "--color-text-dark",  # For #333 colors
            "--color-text-secondary",  # For muted text
            "--color-secondary-light",  # For secondary backgrounds
            "--font-size-3xl",  # For 32px titles
            "--font-size-lg",  # For 18px text
            "--font-size-md",  # For 16px text
            "--font-size-sm",  # For 14px text
            "--font-size-xs",  # For 12px text
            "--radius-button",  # For border radius
            "--transition-all",  # For transitions
            "--shadow-hover-mild",  # For hover effects
        ]

        missing_variables = []
        for variable in expected_variables:
            if variable not in search_pages_content:
                missing_variables.append(variable)

        if missing_variables:
            self.test_results.append(
                f"⚠️  search-page.css missing recommended variables: {', '.join(missing_variables)}"
            )
        else:
            self.test_results.append(
                "✅ search-page.css uses recommended CSS variables"
            )

    def test_search_pages_css_structure_organization(self):
        """Test that search-page.css has proper file structure and organization"""
        search_pages_content = self.read_file_content(self.css_files["search_page"])

        if not search_pages_content:
            self.test_results.append("❌ search-page.css file not found or empty")
            return

        structure_issues = []

        # Check for proper section organization
        expected_sections = [
            "/* ===== SEARCH CONTAINER =====",
            "/* ===== SEARCH HEADER =====",
            "/* ===== SEARCH BAR =====",
            "/* ===== USER CARDS =====",
            "/* ===== EMPTY STATE =====",
        ]

        missing_sections = []
        for section in expected_sections:
            if section not in search_pages_content:
                missing_sections.append(
                    section.replace("/* ===== ", "").replace(" =====", "")
                )

        if missing_sections:
            structure_issues.append(
                f"Missing section organization: {', '.join(missing_sections)}"
            )

        # Check for alphabetical organization within selectors
        lines = search_pages_content.split("\n")
        css_rules = []
        current_selector = None

        for line in lines:
            line = line.strip()
            if line.endswith("{") and not line.startswith("/*"):
                current_selector = line.replace(" {", "")
            elif line.startswith("/*") and "====" in line:
                current_selector = None  # Reset for new section

        # Check for consistent indentation and formatting
        indentation_issues = 0
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith("/*"):
                if line.startswith("  ") and not line.startswith("    "):
                    # Should be 4-space indentation for consistency
                    pass
                elif line.startswith("\t"):
                    indentation_issues += 1
                    if indentation_issues == 1:  # Only report once
                        structure_issues.append(
                            "Inconsistent indentation (tabs vs spaces)"
                        )

        if not structure_issues:
            self.test_results.append(
                "✅ search-page.css has good structure and organization"
            )
        else:
            self.test_results.append(
                f"⚠️  search-page.css structure improvements needed: {len(structure_issues)} issues"
            )
            for issue in structure_issues[:3]:
                print(f"   {issue}")

    def test_variables_css_optimization(self):
        """Test variables.css for duplicates, unused variables, and optimization opportunities"""
        variables_content = self.read_file_content(self.css_files["variables"])

        if not variables_content:
            self.test_results.append(
                "❌ variables.css file not found - cannot analyze optimization"
            )
            return

        # Extract all defined variables with their values
        defined_variables = {}
        variable_pattern = r"(--[\w-]+)\s*:\s*([^;]+);"
        for match in re.finditer(variable_pattern, variables_content):
            var_name = match.group(1).strip()
            var_value = match.group(2).strip()
            defined_variables[var_name] = var_value

        # Find all variables used across CSS files
        used_variables = set()
        css_files_to_check = [
            "base",
            "components",
            "utilities",
            "home_pages",
            "profile_pages",
            "messaging_pages",
            "skill_pages",
            "auth_pages",
            "search_page",
            "error_pages",
        ]

        for file_key in css_files_to_check:
            if file_key not in self.css_files:
                continue

            file_path = self.css_files[file_key]
            if not file_path.exists():
                continue

            file_content = self.read_file_content(file_path)
            if not file_content:
                continue

            # Find all var() usage in the file
            var_usage_pattern = r"var\(\s*(--[\w-]+)\s*(?:,.*?)?\)"
            for match in re.finditer(var_usage_pattern, file_content):
                used_variables.add(match.group(1).strip())

        # Analysis results
        issues = []

        # 1. Find unused variables
        unused_vars = set(defined_variables.keys()) - used_variables
        if unused_vars:
            issues.append(f"🗑️  {len(unused_vars)} unused variables found")
            print(f"   Unused variables: {', '.join(sorted(list(unused_vars))[:5])}")
            if len(unused_vars) > 5:
                print(f"   ... and {len(unused_vars) - 5} more")

        # 2. Find duplicate values (same value, different variable names)
        value_groups = {}
        for var_name, var_value in defined_variables.items():
            # Normalize values for comparison
            normalized_value = var_value.lower().replace(" ", "")
            if normalized_value not in value_groups:
                value_groups[normalized_value] = []
            value_groups[normalized_value].append(var_name)

        duplicates = {
            value: vars for value, vars in value_groups.items() if len(vars) > 1
        }
        if duplicates:
            issues.append(f"🔄 {len(duplicates)} sets of duplicate values found")
            for value, vars in list(duplicates.items())[:3]:  # Show first 3 sets
                print(f"   Value '{value[:30]}...': {', '.join(vars)}")

        # 3. Find redundant color definitions
        color_redundancies = []
        color_vars = {k: v for k, v in defined_variables.items() if "color" in k}

        # Check for colors that could be consolidated
        similar_colors = [
            (["--color-text-secondary", "--color-text-medium"], "#666666"),
            (["--color-border", "--color-border-muted"], "#dee2e6 vs #e9ecef"),
            (["--color-white", "--color-background-white"], "#ffffff"),
        ]

        for color_group, expected in similar_colors:
            existing_colors = [
                (var, defined_variables.get(var, "NOT_FOUND"))
                for var in color_group
                if var in defined_variables
            ]
            if len(existing_colors) > 1:
                values = [color[1] for color in existing_colors]
                if len(set(values)) == 1:  # Same values
                    color_redundancies.append(
                        f"Identical: {', '.join([c[0] for c in existing_colors])}"
                    )
                else:
                    color_redundancies.append(
                        f"Similar: {', '.join([f'{c[0]}({c[1]})' for c in existing_colors])}"
                    )

        if color_redundancies:
            issues.append(f"🎨 {len(color_redundancies)} color redundancies found")
            for redundancy in color_redundancies:
                print(f"   {redundancy}")

        # 4. Find variables that reference other variables inefficiently
        circular_refs = []
        for var_name, var_value in defined_variables.items():
            if "var(--" in var_value:
                referenced_vars = re.findall(r"var\((--[\w-]+)\)", var_value)
                for ref_var in referenced_vars:
                    if ref_var in defined_variables:
                        ref_value = defined_variables[ref_var]
                        if var_name in ref_value:
                            circular_refs.append(f"{var_name} ↔ {ref_var}")

        if circular_refs:
            issues.append(f"🔄 {len(circular_refs)} potential circular references")
            for ref in circular_refs[:3]:
                print(f"   {ref}")

        # 5. Check for naming inconsistencies
        naming_issues = []

        # Check for inconsistent naming patterns
        spacing_vars = [var for var in defined_variables.keys() if "space" in var]
        color_vars = [var for var in defined_variables.keys() if "color" in var]

        # Look for similar names that might be redundant
        name_groups = {}
        for var in defined_variables.keys():
            # Group by base name (remove modifiers like -light, -dark, etc.)
            base_name = re.sub(
                r"-(light|dark|medium|strong|muted|primary|secondary)$", "", var
            )
            if base_name not in name_groups:
                name_groups[base_name] = []
            name_groups[base_name].append(var)

        large_groups = {
            base: vars for base, vars in name_groups.items() if len(vars) > 4
        }
        if large_groups:
            issues.append(
                f"📝 {len(large_groups)} variable families with many variants"
            )
            for base, vars in list(large_groups.items())[:2]:
                print(f"   {base}: {len(vars)} variants ({', '.join(vars[:3])}...)")

        # Report results
        if not issues:
            self.test_results.append("✅ variables.css is well-optimized")
        else:
            self.test_results.append(
                f"⚠️  variables.css optimization opportunities: {len(issues)} areas identified"
            )
            print(
                f"   💡 Consider: consolidating duplicates, removing unused vars, simplifying naming"
            )

    def test_variables_css_structure(self):
        """Test variables.css for logical organization and documentation"""
        variables_content = self.read_file_content(self.css_files["variables"])

        if not variables_content:
            self.test_results.append(
                "❌ variables.css file not found - cannot analyze structure"
            )
            return

        issues = []

        # Check for proper section organization
        expected_sections = [
            "/* Color Palette */",
            "/* Spacing */",
            "/* Typography */",
            "/* Border Radius */",
            "/* Shadows */",
            "/* Transitions */",
            "/* Glassmorphism */",
        ]

        missing_sections = []
        for section in expected_sections:
            if section not in variables_content:
                missing_sections.append(section.replace("/* ", "").replace(" */", ""))

        if missing_sections:
            issues.append(
                f"📚 Missing organizational sections: {', '.join(missing_sections)}"
            )

        # Check for alphabetical order within sections
        lines = variables_content.split("\n")
        current_section = None
        section_vars = []

        for line in lines:
            line = line.strip()
            if line.startswith("/*") and line.endswith("*/"):
                # Process previous section
                if current_section and section_vars:
                    sorted_vars = sorted(section_vars)
                    if section_vars != sorted_vars:
                        issues.append(
                            f"🔤 {current_section} variables not alphabetically ordered"
                        )

                current_section = line.replace("/*", "").replace("*/", "").strip()
                section_vars = []
            elif line.startswith("--") and ":" in line:
                var_name = line.split(":")[0].strip()
                section_vars.append(var_name)

        # Check documentation coverage
        var_count = len(re.findall(r"--[\w-]+\s*:", variables_content))
        comment_count = len(re.findall(r"/\*.*?\*/", variables_content, re.DOTALL))

        if comment_count < (var_count / 10):  # Less than 1 comment per 10 variables
            issues.append(
                f"📝 Low documentation coverage: {comment_count} comments for {var_count} variables"
            )

        # Report results
        if not issues:
            self.test_results.append(
                "✅ variables.css has good structure and organization"
            )
        else:
            self.test_results.append(
                f"⚠️  variables.css structure improvements needed: {len(issues)} issues"
            )
            for issue in issues[:3]:
                print(f"   {issue}")

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
            self.test_undefined_css_variables,
            self.test_variables_css_optimization,
            self.test_variables_css_structure,
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
            self.test_text_visibility_on_white_backgrounds,
            self.test_css_semantic_color_usage,
            self.test_equal_height_card_layouts,
            # Home Pages Specific Tests
            self.test_home_pages_css_hardcoded_values,
            self.test_home_pages_css_variable_usage,
            # Messaging Pages Specific Tests
            self.test_messaging_pages_css_hardcoded_values,
            # Profile Pages Specific Tests
            self.test_profile_pages_css_hardcoded_values,
            self.test_profile_pages_css_optimization_analysis,
            # Search Pages Specific Tests
            self.test_search_pages_css_hardcoded_values,
            self.test_search_pages_css_optimization_analysis,
            self.test_search_pages_css_variable_usage,
            self.test_search_pages_css_structure_organization,
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
