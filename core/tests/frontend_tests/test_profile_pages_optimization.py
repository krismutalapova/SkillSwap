#!/usr/bin/env python3
"""
Profile-pages.css Optimization Test Suite
Tests the success of Phase 7.1: Profile-Pages.css Targeted Optimization

This test is part of the comprehensive CSS refactoring validation suite.
It specifically validates the profile-pages.css optimization achievements.
"""

import re
import os
from pathlib import Path


def test_profile_pages_optimization():
    """Test profile-pages.css optimization results"""

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    css_file = project_root / "static/css/profile-pages.css"

    if not css_file.exists():
        print(f"❌ ERROR: {css_file} not found")
        return False

    with open(css_file, "r") as f:
        content = f.read()

    print("🧪 PROFILE-PAGES.CSS OPTIMIZATION TEST RESULTS")
    print("=" * 60)

    # Test 1: Count CSS variables usage
    css_var_pattern = r"var\(--[a-zA-Z0-9-]+\)"
    css_variables = re.findall(css_var_pattern, content)
    print(f"✅ CSS Variables Found: {len(css_variables)}")

    # Test 2: Count hardcoded pixel/rem/em values (excluding legitimate ones)
    hardcoded_pattern = r"\b\d+(?:\.\d+)?(?:px|rem|em)\b"
    hardcoded_values = re.findall(hardcoded_pattern, content)

    # Filter out legitimate hardcoded values
    legitimate_values = ["1px"]  # calc() function uses
    actual_hardcoded = [val for val in hardcoded_values if val not in legitimate_values]

    print(f"⚠️  Hardcoded Values Found: {len(actual_hardcoded)}")
    if actual_hardcoded:
        print(f"   Remaining hardcoded values: {list(set(actual_hardcoded))}")

    # Test 3: Check for specific targeted optimizations
    print("\n📊 TARGETED OPTIMIZATION CHECKS:")

    # Check for profile picture size variable
    profile_pic_usage = content.count("var(--profile-pic-size)")
    print(f"✅ Profile Picture Size Variable Usage: {profile_pic_usage} times")

    # Check for profile card min width variable
    profile_card_usage = content.count("var(--profile-card-min-width)")
    print(f"✅ Profile Card Min Width Variable Usage: {profile_card_usage} times")

    # Check for border width variables
    border_thin_usage = content.count("var(--border-width-thin)")
    border_medium_usage = content.count("var(--border-width-medium)")
    border_thick_usage = content.count("var(--border-width-thick)")
    total_border_vars = border_thin_usage + border_medium_usage + border_thick_usage
    print(f"✅ Border Width Variables Usage: {total_border_vars} times")
    print(
        f"   - thin: {border_thin_usage}, medium: {border_medium_usage}, thick: {border_thick_usage}"
    )

    # Check for transform hover variables
    transform_usage = content.count("var(--transform-hover-up)")
    print(f"✅ Transform Hover Variable Usage: {transform_usage} times")

    # Check for section organization
    section_headers = re.findall(r"/\* ===== .+ ===== \*/", content)
    print(f"✅ Section Headers Found: {len(section_headers)}")
    if section_headers:
        clean_headers = []
        for header in section_headers:
            # Clean up the header by removing /* ===== and ===== */
            clean_header = header.replace("/* ===== ", "").replace(" ===== */", "")
            clean_headers.append(clean_header)
        print(f"   Sections: {clean_headers}")

    # Test 4: Calculate optimization percentage
    total_values = len(css_variables) + len(actual_hardcoded)
    if total_values > 0:
        optimization_percentage = (len(css_variables) / total_values) * 100
        print(f"\n🎯 OPTIMIZATION PERCENTAGE: {optimization_percentage:.1f}%")

    # Test 5: Font size optimization check
    font_size_vars = content.count("font-size: var(--font-size-")
    hardcoded_font_sizes = len(
        [val for val in hardcoded_values if "rem" in val or "em" in val]
    )
    print(f"✅ Font Size Variables Usage: {font_size_vars} times")
    print(f"⚠️  Hardcoded Font Sizes: {hardcoded_font_sizes}")

    # Test 6: Overall file health
    print(f"\n📋 FILE STATISTICS:")
    print(f"   Total Lines: {len(content.splitlines())}")
    print(f"   File Size: {len(content)} characters")
    print(f"   CSS Variables: {len(css_variables)}")
    print(f"   Hardcoded Values: {len(actual_hardcoded)}")

    # Success criteria
    success_criteria = {
        "High CSS Variable Usage": len(css_variables) > 150,
        "Low Hardcoded Values": len(actual_hardcoded) < 5,
        "Profile Optimizations": profile_pic_usage > 0 and profile_card_usage > 0,
        "Border Variables": total_border_vars > 5,
        "Section Organization": len(section_headers) > 0,
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
        print("\n🚀 Profile-pages.css optimization is COMPLETE!")
        print("   Ready for production with excellent variable usage.")

    return overall_success


def run_profile_pages_test():
    """Wrapper function for integration with other test suites"""
    return test_profile_pages_optimization()


if __name__ == "__main__":
    success = test_profile_pages_optimization()
    exit(0 if success else 1)
