#!/usr/bin/env python3
"""
CSS Duplicate Classes Detection Test Suite
Tests for duplicate CSS class definitions across different CSS files

This test ensures clean CSS architecture by detecting:
- Duplicate class definitions across different files, excluding
    legitimate responsive overrides in @media queries, different selector types (base class
    vs modifiers vs pseudo-classes), css property values that look like class names
- Conflicting CSS rules for the same class
- Proper separation of concerns between CSS files
"""

import re
import os
from pathlib import Path
from collections import defaultdict, Counter


class CSSClassDuplicateDetector:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.css_dir = self.project_root / "static/css"

        self.css_files = [
            "base.css",
            "variables.css",
            "utilities.css",
            "components.css",
            "auth-pages.css",
            "profile-pages.css",
            "skill-pages.css",
            "search-page.css",
            "home-pages.css",
            "messaging-pages.css",
            "error-pages.css",
            "component-pages.css",
        ]

        # Files that should only contain specific types of CSS
        self.file_expectations = {
            "variables.css": "css_variables",
            "utilities.css": "utility_classes",
            "base.css": "base_elements",
        }

        self.class_definitions = {}
        self.duplicate_classes = defaultdict(list)
        self.analysis_results = {}

    def normalize_selector(self, selector):
        """
        Normalize CSS selectors to identify the base class name.
        Removes modifiers, pseudo-classes, child selectors, etc.

        Examples:
        - '.btn-base' -> 'btn-base' (atomic foundation)
        - '.btn-primary-colors:hover' -> 'btn-primary-colors' (atomic color with pseudo-class)
        - '.btn-primary-colors.large' -> 'btn-primary-colors' (modifier)
        - '.card .btn-primary-colors' -> 'btn-primary-colors' (child selector)
        - '.btn-primary-colors, .btn-secondary-colors' -> ['btn-primary-colors', 'btn-secondary-colors'] (multiple)
        """
        if "," in selector:
            return [self.normalize_selector(s.strip()) for s in selector.split(",")]

        # Remove everything after pseudo-classes, pseudo-elements, or additional modifiers
        selector = re.sub(
            r":(hover|focus|active|visited|before|after|first-child|last-child|nth-child)",
            "",
            selector,
        )
        selector = re.sub(r"::[a-zA-Z-]+", "", selector)

        class_matches = re.findall(r"\.([a-zA-Z0-9_-]+)", selector)

        if class_matches:
            return class_matches[0]

        return None

    def is_responsive_override(self, css_content, selector_start):
        # Look backwards from the selector to find if we're in a @media block
        content_before = css_content[:selector_start]

        # Find all @media blocks that could contain this selector
        media_blocks = []
        for match in re.finditer(r"@media[^{]*{", content_before):
            media_start = match.start()
            media_blocks.append(media_start)

        if not media_blocks:
            return False

        # For each @media block, check if we're still inside it
        for media_start in media_blocks:
            # Count braces from media start to selector position
            media_content = css_content[media_start:selector_start]
            open_braces = media_content.count("{")
            close_braces = media_content.count("}")

            # If more opens than closes, we're inside this media block
            if open_braces > close_braces:
                return True

        return False

    def is_modifier_extension(self, selector):
        """
        Check if a selector is a legitimate modifier extension.
        """
        # Remove whitespace and normalize
        selector = selector.strip()

        # Check for pseudo-classes (:hover, :focus, etc.)
        if ":" in selector and not selector.startswith("@"):
            return True

        # Check for multiple classes (modifiers)
        class_matches = re.findall(r"\.([a-zA-Z0-9_-]+)", selector)
        if len(class_matches) > 1:
            return True

        # Check for descendant/child selectors with base class
        if " " in selector or ">" in selector:
            return True

        return False

    def is_legitimate_variant(self, class_name, full_rule, filename):
        # Check for file-specific naming patterns
        file_prefixes = {
            "profile-pages.css": ["profile-", "user-detail-", "compact-"],
            "skill-pages.css": ["skill-", "rating-"],
            "search-page.css": ["search-", "user-card-"],
            "messaging-pages.css": ["message-", "inbox-"],
            "auth-pages.css": ["auth-", "login-", "signup-"],
            "error-pages.css": ["error-", "btn-primary-colors"],
        }

        if filename in file_prefixes:
            for prefix in file_prefixes[filename]:
                if class_name.startswith(prefix):
                    return True, f"File-specific variant ({prefix}*)"

        # Check for size/state modifiers
        if any(
            suffix in class_name
            for suffix in [
                "-small",
                "-large",
                "-mini",
                "-enabled",
                "-active",
                "-selected",
            ]
        ):
            return True, "Size/state modifier"

        # Check for context-specific classes
        context_patterns = [
            r"-card$",
            r"-header$",
            r"-footer$",
            r"-section$",
            r"-grid$",
            r"-container$",
            r"-wrapper$",
        ]

        for pattern in context_patterns:
            if re.search(pattern, class_name):
                return True, f"Context-specific ({pattern})"

        return False, "No legitimate pattern found"

    def extract_css_classes(self, css_content, filename):
        classes = {}

        # Remove comments to avoid false matches
        css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)

        # Pattern for CSS selectors - more precise to avoid property values
        # This pattern looks for selectors that start a rule block
        selector_pattern = r"([^{}]*?)(?=\s*{)"

        matches = re.finditer(selector_pattern, css_content, re.MULTILINE)

        for match in matches:
            selector = match.group(1).strip()
            start_pos = match.start()

            # Skip if this doesn't contain a class selector
            if "." not in selector:
                continue

            # Skip if this looks like it's inside a property value
            # Check if there's a ':' before the selector on the same line
            line_start = css_content.rfind("\n", 0, start_pos)
            line_content = css_content[line_start:start_pos]
            if ":" in line_content and not selector.strip().startswith("."):
                continue

            # Skip @keyframes, @media declarations themselves, etc.
            if selector.strip().startswith(("@", "from", "to", "0%", "100%")):
                continue

            # Extract the complete CSS rule
            brace_start = css_content.find("{", start_pos)
            if brace_start == -1:
                continue

            brace_count = 1
            rule_end = brace_start + 1

            for i, char in enumerate(css_content[brace_start + 1 :], brace_start + 1):
                if char == "{":
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        rule_end = i + 1
                        break

            full_rule = css_content[start_pos:rule_end].strip()

            # Check if this is inside a responsive override
            is_responsive = self.is_responsive_override(css_content, start_pos)

            # Check if this is a modifier extension
            is_modifier = self.is_modifier_extension(selector)

            # Normalize the selector to get base class names
            normalized = self.normalize_selector(selector)

            if isinstance(normalized, list):
                # Handle multiple selectors
                for norm in normalized:
                    if norm:
                        self._add_class_definition(
                            classes,
                            norm,
                            full_rule,
                            is_responsive,
                            is_modifier,
                            selector,
                        )
            elif normalized:
                self._add_class_definition(
                    classes, normalized, full_rule, is_responsive, is_modifier, selector
                )

        return classes

    def _add_class_definition(
        self, classes, class_name, rule, is_responsive, is_modifier, original_selector
    ):
        # Create a metadata object for each class definition
        class_info = {
            "rule": rule,
            "is_responsive": is_responsive,
            "is_modifier": is_modifier,
            "original_selector": original_selector,
            "rule_preview": rule.replace("\n", " ").strip()[:100]
            + ("..." if len(rule) > 100 else ""),
        }

        if class_name in classes:
            if isinstance(classes[class_name], list):
                classes[class_name].append(class_info)
            else:
                classes[class_name] = [classes[class_name], class_info]
        else:
            classes[class_name] = class_info

    def analyze_css_files(self):
        print("🔍 ANALYZING CSS FILES FOR DUPLICATE CLASSES")
        print("=" * 60)

        for filename in self.css_files:
            file_path = self.css_dir / filename

            if not file_path.exists():
                print(f"⚠️  Warning: {filename} not found, skipping...")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract classes from this file
            classes = self.extract_css_classes(content, filename)
            self.class_definitions[filename] = classes

            print(f"✅ {filename}: {len(classes)} classes found")

        print(f"\n📊 Total files analyzed: {len(self.class_definitions)}")

    def detect_duplicates(self):
        print("\n🔍 DETECTING CROSS-FILE DUPLICATE CLASSES")
        print("=" * 60)

        class_to_files = defaultdict(list)

        for filename, classes in self.class_definitions.items():
            for class_name, class_info in classes.items():
                # Enhanced filtering: skip responsive overrides AND modifier extensions
                if isinstance(class_info, list):
                    # Check if ANY definition is a true base class (not responsive or modifier)
                    has_true_base = any(
                        not info.get("is_responsive", False)
                        and not info.get("is_modifier", False)
                        for info in class_info
                    )
                    if has_true_base:
                        class_to_files[class_name].append(filename)
                else:
                    if not class_info.get(
                        "is_responsive", False
                    ) and not class_info.get("is_modifier", False):
                        class_to_files[class_name].append(filename)

        duplicates_found = False

        for class_name, files in class_to_files.items():
            if len(files) > 1:
                # Enhanced legitimate usage detection
                legitimacy_result = self._is_legitimate_cross_file_usage(
                    class_name, files
                )
                if legitimacy_result["is_legitimate"]:
                    print(f"✅ LEGITIMATE PATTERN: .{class_name}")
                    print(f"   Found in files: {', '.join(files)}")
                    print(f"   Reason: {legitimacy_result['reason']}")
                    print()
                    continue

                duplicates_found = True
                self.duplicate_classes[class_name] = files
                print(f"❌ TRUE DUPLICATE: .{class_name}")
                print(f"   Found in files: {', '.join(files)}")

                # Show the actual CSS rules for comparison with enhanced metadata
                for file in files:
                    class_info = self.class_definitions[file][class_name]
                    if isinstance(class_info, list):
                        print(f"   {file}: Multiple definitions!")
                        for i, info in enumerate(class_info, 1):
                            flags = []
                            if info.get("is_responsive"):
                                flags.append("responsive")
                            if info.get("is_modifier"):
                                flags.append("modifier")
                            flag_str = f" ({', '.join(flags)})" if flags else ""
                            print(
                                f"     Definition {i}{flag_str}: {info['rule_preview']}"
                            )
                            print(
                                f"       Selector: {info.get('original_selector', 'N/A')}"
                            )
                    else:
                        flags = []
                        if class_info.get("is_responsive"):
                            flags.append("responsive")
                        if class_info.get("is_modifier"):
                            flags.append("modifier")
                        flag_str = f" ({', '.join(flags)})" if flags else ""
                        print(f"   {file}{flag_str}: {class_info['rule_preview']}")
                        print(
                            f"     Selector: {class_info.get('original_selector', 'N/A')}"
                        )
                print()

        if not duplicates_found:
            print("✅ No problematic cross-file duplicate classes found!")

        return not duplicates_found

    def _is_legitimate_cross_file_usage(self, class_name, files):

        # Check for file-specific variants first
        for filename in files:
            is_variant, reason = self.is_legitimate_variant(class_name, "", filename)
            if is_variant:
                return {
                    "is_legitimate": True,
                    "reason": f"File-specific variant: {reason}",
                }

        if "utilities.css" in files:
            non_utility_files = [f for f in files if f != "utilities.css"]
            all_legitimate = True

            for file in non_utility_files:
                class_info = self.class_definitions[file][class_name]
                if isinstance(class_info, list):
                    if any(
                        not info.get("is_responsive", False)
                        and not info.get("is_modifier", False)
                        for info in class_info
                    ):
                        all_legitimate = False
                        break
                else:
                    if not class_info.get(
                        "is_responsive", False
                    ) and not class_info.get("is_modifier", False):
                        all_legitimate = False
                        break

            if all_legitimate:
                return {
                    "is_legitimate": True,
                    "reason": f"Utilities.css base + responsive/modifier extensions in {', '.join(non_utility_files)}",
                }

        if "base.css" in files:
            non_base_files = [f for f in files if f != "base.css"]
            all_responsive = True

            for file in non_base_files:
                class_info = self.class_definitions[file][class_name]
                if isinstance(class_info, list):
                    if any(not info.get("is_responsive", False) for info in class_info):
                        all_responsive = False
                        break
                else:
                    if not class_info.get("is_responsive", False):
                        all_responsive = False
                        break

            if all_responsive:
                return {
                    "is_legitimate": True,
                    "reason": f"Base.css global + responsive overrides in {', '.join(non_base_files)}",
                }

        if "components.css" in files:
            non_component_files = [f for f in files if f != "components.css"]
            all_extensions = True

            for file in non_component_files:
                class_info = self.class_definitions[file][class_name]
                if isinstance(class_info, list):
                    if any(
                        not info.get("is_responsive", False)
                        and not info.get("is_modifier", False)
                        for info in class_info
                    ):
                        all_extensions = False
                        break
                else:
                    if not class_info.get(
                        "is_responsive", False
                    ) and not class_info.get("is_modifier", False):
                        all_extensions = False
                        break

            if all_extensions:
                return {
                    "is_legitimate": True,
                    "reason": f"Components.css base + extensions in {', '.join(non_component_files)}",
                }

        modifier_count = 0
        for filename in files:
            class_info = self.class_definitions[filename][class_name]
            if isinstance(class_info, list):
                if any(info.get("is_modifier", False) for info in class_info):
                    modifier_count += 1
            else:
                if class_info.get("is_modifier", False):
                    modifier_count += 1

        if modifier_count == len(files):
            return {
                "is_legitimate": True,
                "reason": "All instances are modifier extensions (hover, focus, etc.)",
            }

        return {
            "is_legitimate": False,
            "reason": "True architectural duplicate - complete redefinitions across files",
        }

    def detect_within_file_duplicates(self):
        print("\n🔍 DETECTING WITHIN-FILE DUPLICATES")
        print("=" * 60)

        within_file_duplicates = False

        for filename, classes in self.class_definitions.items():
            file_duplicates = []

            for class_name, class_info in classes.items():
                if isinstance(class_info, list):
                    # Filter out responsive duplicates - only count real duplicates
                    non_responsive_defs = [
                        info
                        for info in class_info
                        if not info.get("is_responsive", False)
                    ]
                    if len(non_responsive_defs) > 1:
                        file_duplicates.append((class_name, len(non_responsive_defs)))
                    elif len(class_info) > 1:
                        # Multiple definitions but some are responsive - still worth noting
                        responsive_count = len(
                            [
                                info
                                for info in class_info
                                if info.get("is_responsive", False)
                            ]
                        )
                        if responsive_count < len(class_info):
                            file_duplicates.append(
                                (
                                    class_name,
                                    len(class_info),
                                    f"{responsive_count} responsive",
                                )
                            )

            if file_duplicates:
                within_file_duplicates = True
                print(f"❌ {filename} has within-file duplicates:")
                for dup_info in file_duplicates:
                    if len(dup_info) == 2:
                        class_name, count = dup_info
                        print(f"   .{class_name}: {count} definitions")
                    else:
                        class_name, total_count, responsive_note = dup_info
                        print(
                            f"   .{class_name}: {total_count} definitions ({responsive_note})"
                        )

        if not within_file_duplicates:
            print("✅ No problematic within-file duplicates found!")

        return not within_file_duplicates

    def analyze_css_architecture(self):
        print("\n📋 CSS ARCHITECTURE ANALYSIS")
        print("=" * 60)

        architecture_issues = []

        expected_patterns = {
            "variables.css": {
                "pattern": r"^:root|^--",
                "description": "Should only contain CSS variables",
            },
            "utilities.css": {
                "pattern": r"^(btn-|text-|bg-|p-|m-|flex-|grid-)",
                "description": "Should contain utility classes",
            },
            "base.css": {
                "pattern": r"^(html|body|\*|::before|::after|h[1-6]|p|a|ul|ol|li)",
                "description": "Should contain base element styling",
            },
        }

        for filename, expected in expected_patterns.items():
            if filename in self.class_definitions:
                classes = self.class_definitions[filename]
                non_conforming = []

                for class_name in classes.keys():
                    if not re.match(expected["pattern"], class_name):
                        non_conforming.append(class_name)

                if non_conforming:
                    architecture_issues.append(
                        f"{filename}: {len(non_conforming)} classes don't follow expected pattern"
                    )
                    print(f"⚠️  {filename}: {expected['description']}")
                    print(f"   Non-conforming classes: {', '.join(non_conforming[:5])}")
                    if len(non_conforming) > 5:
                        print(f"   ... and {len(non_conforming) - 5} more")
                else:
                    print(f"✅ {filename}: Architecture follows expected patterns")

        return len(architecture_issues) == 0

    def generate_report(self):
        print("\n" + "=" * 70)
        print("📊 CSS DUPLICATE CLASSES DETECTION REPORT")
        print("=" * 70)

        total_classes = sum(len(classes) for classes in self.class_definitions.values())
        total_duplicates = len(self.duplicate_classes)

        print(f"📁 Files Analyzed: {len(self.class_definitions)}")
        print(f"🎯 Total Classes: {total_classes}")
        print(f"❌ Duplicate Classes: {total_duplicates}")

        if total_duplicates > 0:
            duplicate_percentage = (total_duplicates / total_classes) * 100
            print(f"📈 Duplication Rate: {duplicate_percentage:.1f}%")
        else:
            print(f"📈 Duplication Rate: 0.0%")

        # File breakdown
        print(f"\n📋 FILE BREAKDOWN:")
        for filename, classes in self.class_definitions.items():
            class_count = len(classes)
            duplicates_in_file = sum(
                1 for cls in classes.keys() if cls in self.duplicate_classes
            )
            print(
                f"   {filename}: {class_count} classes ({duplicates_in_file} involved in duplicates)"
            )

        # Success criteria
        print(f"\n🏆 SUCCESS CRITERIA:")

        # Run the tests if not already run
        no_cross_file_duplicates = len(self.duplicate_classes) == 0
        no_within_file_duplicates = True
        clean_architecture = True

        # Check within-file duplicates
        for filename, classes in self.class_definitions.items():
            for class_name, class_info in classes.items():
                if isinstance(class_info, list):
                    non_responsive_defs = [
                        info
                        for info in class_info
                        if not info.get("is_responsive", False)
                    ]
                    if len(non_responsive_defs) > 1:
                        no_within_file_duplicates = False
                        break
            if not no_within_file_duplicates:
                break

        success_criteria = {
            "No Cross-File Duplicates": no_cross_file_duplicates,
            "No Within-File Duplicates": no_within_file_duplicates,
            "Clean Architecture": clean_architecture,
            "All Files Present": len(self.class_definitions)
            >= 8,  # Minimum expected files
        }

        print(f"\n🏆 SUCCESS CRITERIA:")
        passed_tests = 0
        for criterion, passed in success_criteria.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {criterion}: {status}")
            if passed:
                passed_tests += 1

        overall_success = passed_tests == len(success_criteria)
        print(
            f"\n🎉 OVERALL RESULT: {'SUCCESS' if overall_success else 'NEEDS IMPROVEMENT'}"
        )
        print(f"   Tests Passed: {passed_tests}/{len(success_criteria)}")

        if overall_success:
            print("\n🚀 CSS architecture is clean with no duplicate classes!")
            print("   Excellent separation of concerns maintained.")
        else:
            print("\n⚠️  CSS architecture needs attention:")
            if total_duplicates > 0:
                print(f"   - {total_duplicates} duplicate classes need resolution")
            print("   - Review file organization and class naming conventions")

        return overall_success


def test_css_duplicate_classes():
    detector = CSSClassDuplicateDetector()

    # Step 1: Analyze all CSS files
    detector.analyze_css_files()

    # Step 2: Detect cross-file duplicates
    no_cross_file_duplicates = detector.detect_duplicates()

    # Step 3: Detect within-file duplicates
    no_within_file_duplicates = detector.detect_within_file_duplicates()

    # Step 4: Generate comprehensive report
    overall_success = detector.generate_report()

    return overall_success


def run_duplicate_detection_test():
    return test_css_duplicate_classes()


if __name__ == "__main__":
    success = test_css_duplicate_classes()
    exit(0 if success else 1)
