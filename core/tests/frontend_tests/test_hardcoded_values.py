"""
Hardcoded Values Detection Testing
Consolidated tests for detecting and validating hardcoded values across CSS files

This file consolidates hardcoded value detection that was previously scattered across:
- test_css_refactoring.py -> Various hardcoded value tests
- test_css_refactoring_suite.py -> Hardcoded value detection
- test_css_integration.py -> Hardcoded validation
- test_profile_pages_optimization.py -> Hardcoded value counting
"""

import re
from core.tests.frontend_tests.utils import CSSTestCase


class HardcodedValueDetectionTests(CSSTestCase):
    """Detect and validate hardcoded values across CSS files"""

    def test_no_hardcoded_colors(self):
        # Skip variables.css as it's allowed to define hardcoded values
        test_files = [f for f in self.css_files if f != "variables.css"]

        for css_file in test_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    hardcoded_values = self.css_utils.find_hardcoded_values(content)

                    if "colors" in hardcoded_values:
                        # Filter out legitimate hardcoded colors
                        legitimate_colors = [
                            "transparent",
                            "inherit",
                            "initial",
                            "unset",
                            "currentColor",
                            "white",
                            "black",
                        ]

                        problematic_colors = []
                        for color in hardcoded_values["colors"]:
                            if not any(
                                legit.lower() in color.lower()
                                for legit in legitimate_colors
                            ):
                                problematic_colors.append(color)

                        self.assertEqual(
                            len(problematic_colors),
                            0,
                            f"File {css_file} contains hardcoded colors that should use CSS variables: {problematic_colors}",
                        )

    def test_no_hardcoded_spacing(self):
        test_files = [f for f in self.css_files if f != "variables.css"]

        for css_file in test_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Allow common legitimate hardcoded spacing values
                    legitimate_spacing = [
                        "0px",
                        "1px",
                        "2px",
                        "100%",
                        "0%",
                        "50%",
                        "calc(",
                    ]

                    hardcoded_values = self.css_utils.find_hardcoded_values(
                        content, exclude_patterns=legitimate_spacing
                    )

                    # Count variables vs hardcoded spacing
                    variables_count = self.css_utils.count_css_variables(content)
                    hardcoded_spacing_count = (
                        len(hardcoded_values.get("pixels", []))
                        + len(hardcoded_values.get("rems", []))
                        + len(hardcoded_values.get("ems", []))
                    )

                    # If file uses variables, hardcoded spacing should be minimal
                    if variables_count > 5:
                        self.assertLessEqual(
                            hardcoded_spacing_count,
                            variables_count // 2,
                            f"File {css_file} has too many hardcoded spacing values ({hardcoded_spacing_count}) "
                            f"compared to CSS variables ({variables_count}). Consider using more spacing variables.",
                        )

    def test_no_hardcoded_border_radius(self):
        test_files = [f for f in self.css_files if f != "variables.css"]

        for css_file in test_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Find hardcoded border-radius values
                    border_radius_pattern = (
                        r"border-radius:\s*(\d+(?:\.\d+)?(?:px|rem|em|%))"
                    )
                    hardcoded_radius = re.findall(border_radius_pattern, content)

                    # Filter out legitimate values
                    legitimate_radius = ["0px", "50%", "100%"]
                    problematic_radius = [
                        radius
                        for radius in hardcoded_radius
                        if radius not in legitimate_radius
                    ]

                    if problematic_radius:
                        # Check if CSS variables are used for border-radius
                        variable_radius = re.findall(
                            r"border-radius:\s*var\(--[^)]+\)", content
                        )

                        self.assertGreaterEqual(
                            len(variable_radius),
                            len(problematic_radius),
                            f"File {css_file} should use CSS variables for border-radius instead of hardcoded values: {problematic_radius}",
                        )

    def test_no_hardcoded_font_sizes(self):
        test_files = [f for f in self.css_files if f != "variables.css"]

        for css_file in test_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Find hardcoded font-size values
                    font_size_pattern = r"font-size:\s*(\d+(?:\.\d+)?px)"
                    hardcoded_fonts = re.findall(font_size_pattern, content)

                    # Check for CSS variable usage in font-size
                    variable_fonts = re.findall(r"font-size:\s*var\(--[^)]+\)", content)
                    relative_fonts = re.findall(
                        r"font-size:\s*\d+(?:\.\d+)?(?:rem|em|%)", content
                    )

                    total_good_fonts = len(variable_fonts) + len(relative_fonts)

                    if hardcoded_fonts:
                        self.assertGreaterEqual(
                            total_good_fonts,
                            len(hardcoded_fonts),
                            f"File {css_file} should prefer CSS variables or relative units for font-size over hardcoded pixels: {hardcoded_fonts}",
                        )

    def test_legitimate_hardcoded_exceptions(self):
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # These should be allowed everywhere
                    legitimate_patterns = [
                        r":\s*0(?:px)?",  # Zero values
                        r":\s*1px",  # 1px borders/outlines
                        r":\s*100%",  # Full width/height
                        r":\s*transparent",  # Transparent colors
                        r"calc\([^)]+\)",  # Calc expressions
                    ]

                    found_legitimate = False
                    for pattern in legitimate_patterns:
                        if re.search(pattern, content):
                            found_legitimate = True
                            break

                    # This is just a validation that our detection isn't too strict
                    # Most CSS files should have at least some legitimate hardcoded values
                    if css_file in ["base.css", "utilities.css", "components.css"]:
                        self.assertTrue(
                            found_legitimate,
                            f"File {css_file} should contain some legitimate hardcoded values (0, 1px, 100%, etc.)",
                        )


class HardcodedValueAnalysisTests(CSSTestCase):
    def test_hardcoded_value_distribution(self):
        distribution = {}

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                hardcoded_values = self.css_utils.find_hardcoded_values(content)
                total_hardcoded = sum(
                    len(values) for values in hardcoded_values.values()
                )
                variables_count = self.css_utils.count_css_variables(content)

                distribution[css_file] = {
                    "hardcoded": total_hardcoded,
                    "variables": variables_count,
                    "ratio": variables_count / max(total_hardcoded, 1),
                }

        if "variables.css" in distribution:
            self.assertGreater(
                distribution["variables.css"]["hardcoded"],
                10,
                "variables.css should define many hardcoded values",
            )

        # Other files should have good variable-to-hardcoded ratios
        for css_file, stats in distribution.items():
            if css_file != "variables.css" and stats["variables"] > 0:
                with self.subTest(css_file=css_file):
                    self.assertGreaterEqual(
                        stats["ratio"],
                        0.5,
                        f"File {css_file} should have a good variable-to-hardcoded ratio. "
                        f"Variables: {stats['variables']}, Hardcoded: {stats['hardcoded']}",
                    )

    def test_most_common_hardcoded_values(self):
        all_hardcoded = {}

        for css_file in self.css_files:
            if css_file == "variables.css":
                continue

            content = self.css_utils.read_css_file(css_file)
            if content:
                hardcoded_values = self.css_utils.find_hardcoded_values(content)

                for category, values in hardcoded_values.items():
                    for value in values:
                        key = f"{category}:{value}"
                        all_hardcoded[key] = all_hardcoded.get(key, 0) + 1

        # Find values that appear in multiple files (candidates for variables)
        repeated_values = {k: v for k, v in all_hardcoded.items() if v > 1}

        if repeated_values:
            # This is informational - we don't fail the test, just warn
            most_repeated = sorted(
                repeated_values.items(), key=lambda x: x[1], reverse=True
            )[:5]
            print(f"\nMost repeated hardcoded values (candidates for CSS variables):")
            for value, count in most_repeated:
                print(f"  {value} appears in {count} files")

    def test_hardcoded_value_complexity(self):
        complex_patterns = [
            r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)",
            r"hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)",
            r"calc\([^)]*[+\-*/][^)]*[+\-*/][^)]*\)",
            r"linear-gradient\([^)]{30,}\)",
        ]

        for css_file in self.css_files:
            if css_file == "variables.css":
                continue
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    for pattern in complex_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            # Allow some complexity, but encourage moving to variables
                            self.assertLessEqual(
                                len(matches),
                                2,
                                f"File {css_file} has complex hardcoded values that should be moved to variables.css: {matches}",
                            )


class HardcodedValueMigrationTests(CSSTestCase):
    def test_gradual_migration_progress(self):
        # This test helps track migration progress over time
        total_variables = 0
        total_hardcoded = 0

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                variables_count = self.css_utils.count_css_variables(content)
                hardcoded_values = self.css_utils.find_hardcoded_values(content)
                hardcoded_count = sum(
                    len(values) for values in hardcoded_values.values()
                )

                total_variables += variables_count
                total_hardcoded += hardcoded_count

        # Overall, variables should be more common than hardcoded values
        if total_variables > 0:
            variable_percentage = (
                total_variables / (total_variables + total_hardcoded) * 100
            )
            self.assertGreaterEqual(
                variable_percentage,
                30,
                f"Design system should use CSS variables for at least 30% of values. "
                f"Current: {variable_percentage:.1f}% ({total_variables} variables, {total_hardcoded} hardcoded)",
            )

    def test_critical_files_use_variables(self):
        critical_files = ["base.css", "components.css", "utilities.css"]

        for css_file in critical_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    variables_count = self.css_utils.count_css_variables(content)

                    self.assertGreater(
                        variables_count,
                        5,
                        f"Critical file {css_file} should use CSS variables extensively. Found only {variables_count}",
                    )
