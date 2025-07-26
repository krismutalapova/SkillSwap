#!/usr/bin/env python3
"""
CSS Duplicate Classes Detection Test Suite
Tests for duplicate CSS class definitions across different CSS files

This test ensures clean CSS architecture by detecting:
- Duplicate class definitions across different files
- Conflicting CSS rules for the same class
- Proper separation of concerns between CSS files
"""

import re
import os
from pathlib import Path
from collections import defaultdict, Counter


class CSSClassDuplicateDetector:
    def __init__(self):
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent.parent
        self.css_dir = self.project_root / "static/css"

        # CSS files to analyze
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

        self.allowed_overlaps = {
            "variables.css": [],  # Should only contain :root and variables
            "utilities.css": [],  # Should only contain utility classes
            "base.css": ["body", "html", "*", "::before", "::after"],  # Base elements
        }

        self.class_definitions = {}
        self.duplicate_classes = defaultdict(list)
        self.analysis_results = {}

    def extract_css_classes(self, css_content, filename):
        classes = {}

        class_pattern = r"\.([a-zA-Z0-9_-]+)(?:[^{]*)?{"

        matches = re.finditer(class_pattern, css_content, re.MULTILINE)

        for match in matches:
            class_name = match.group(1)
            start_pos = match.start()

            brace_count = 0
            rule_end = start_pos
            in_rule = False

            for i, char in enumerate(css_content[start_pos:], start_pos):
                if char == "{":
                    brace_count += 1
                    in_rule = True
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0 and in_rule:
                        rule_end = i + 1
                        break

            # Extract the complete rule
            full_rule = css_content[start_pos:rule_end].strip()

            if class_name in classes:
                if isinstance(classes[class_name], list):
                    classes[class_name].append(full_rule)
                else:
                    classes[class_name] = [classes[class_name], full_rule]
            else:
                classes[class_name] = full_rule

        return classes

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
        print("\n🔍 DETECTING DUPLICATE CLASSES")
        print("=" * 60)

        class_to_files = defaultdict(list)

        for filename, classes in self.class_definitions.items():
            for class_name in classes.keys():
                class_to_files[class_name].append(filename)

        duplicates_found = False

        for class_name, files in class_to_files.items():
            if len(files) > 1:
                is_allowed = False
                for allowed_file, allowed_classes in self.allowed_overlaps.items():
                    if allowed_file in files and class_name in allowed_classes:
                        is_allowed = True
                        break

                if not is_allowed:
                    duplicates_found = True
                    self.duplicate_classes[class_name] = files
                    print(f"❌ DUPLICATE: .{class_name}")
                    print(f"   Found in files: {', '.join(files)}")

                    # Show the actual CSS rules for comparison
                    for file in files:
                        rule = self.class_definitions[file][class_name]
                        if isinstance(rule, list):
                            print(f"   {file}: Multiple definitions!")
                            for i, r in enumerate(rule, 1):
                                preview = r.replace("\n", " ").strip()[:100]
                                print(f"     Definition {i}: {preview}...")
                        else:
                            preview = rule.replace("\n", " ").strip()[:100]
                            print(f"   {file}: {preview}...")
                    print()

        if not duplicates_found:
            print("✅ No duplicate classes found across files!")

        return not duplicates_found

    def detect_within_file_duplicates(self):
        print("\n🔍 DETECTING WITHIN-FILE DUPLICATES")
        print("=" * 60)

        within_file_duplicates = False

        for filename, classes in self.class_definitions.items():
            file_duplicates = []

            for class_name, rule in classes.items():
                if isinstance(rule, list):
                    file_duplicates.append((class_name, len(rule)))

            if file_duplicates:
                within_file_duplicates = True
                print(f"❌ {filename} has within-file duplicates:")
                for class_name, count in file_duplicates:
                    print(f"   .{class_name}: {count} definitions")

        if not within_file_duplicates:
            print("✅ No within-file duplicates found!")

        return not within_file_duplicates

    def analyze_css_architecture(self):
        print("\n📋 CSS ARCHITECTURE ANALYSIS")
        print("=" * 60)

        architecture_issues = []

        # Check file-specific concerns
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
        success_criteria = {
            "No Cross-File Duplicates": total_duplicates == 0,
            "No Within-File Duplicates": self.detect_within_file_duplicates(),
            "Clean Architecture": self.analyze_css_architecture(),
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
