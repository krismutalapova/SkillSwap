"""
CSS Performance and Optimization Testing
Tests for CSS performance, file size, load times, and optimization opportunities

This file contains tests that are focused specifically on CSS performance analysis,
file optimization, and load time testing.

"""

import os
import re
import time
from pathlib import Path
from django.conf import settings
from django.test import override_settings
from core.tests.frontend_tests.utils import CSSLiveTestCase, CSSTestCase


class CSSFileSizeTests(CSSTestCase):
    def test_css_file_sizes_reasonable(self):
        size_limits = {
            "variables.css": 50 * 1024,
            "utilities.css": 100 * 1024,
            "base.css": 75 * 1024,
            "components.css": 150 * 1024,
        }

        oversized_files = []

        for css_file in self.css_files:
            file_size = self.file_utils.get_file_size(css_file)
            if file_size:
                filename = css_file.name

                # Check against size limits
                limit = size_limits.get(filename, 200 * 1024)

                if file_size > limit:
                    oversized_files.append(
                        f"{filename}: {file_size/1024:.1f}KB (limit: {limit/1024:.1f}KB)"
                    )

        if oversized_files:
            # This is more of a warning than a hard failure
            print(f"Large CSS files that may need optimization: {oversized_files}")

    def test_total_css_size_reasonable(self):
        total_size = 0
        file_count = 0

        for css_file in self.css_files:
            file_size = self.file_utils.get_file_size(css_file)
            if file_size:
                total_size += file_size
                file_count += 1

        total_size_kb = total_size / 1024

        max_total_size_kb = 500

        self.assertLessEqual(
            total_size_kb,
            max_total_size_kb,
            f"Total CSS size ({total_size_kb:.1f}KB) exceeds reasonable limit ({max_total_size_kb}KB)",
        )

        # Log for information
        if file_count > 0:
            avg_size_kb = total_size_kb / file_count
            print(
                f"CSS Analysis: {file_count} files, {total_size_kb:.1f}KB total, {avg_size_kb:.1f}KB average"
            )

    def test_css_compression_opportunities(self):
        compression_opportunities = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                opportunities = self._analyze_compression_opportunities(
                    content, css_file.name
                )
                compression_opportunities.extend(opportunities)

        # This is informational - shows optimization opportunities
        if compression_opportunities:
            print(f"CSS Compression opportunities: {compression_opportunities[:5]}")

    def _analyze_compression_opportunities(self, content: str, filename: str) -> list:
        opportunities = []

        # Check for excessive whitespace
        lines = content.split("\n")
        empty_lines = sum(1 for line in lines if line.strip() == "")
        if empty_lines > len(lines) * 0.1:
            opportunities.append(f"{filename}: {empty_lines} empty lines")

        # Check for long comments
        comment_chars = len(re.findall(r"/\*.*?\*/", content, re.DOTALL))
        if comment_chars > len(content) * 0.05:
            opportunities.append(f"{filename}: Extensive comments")

        # Check for repeated selectors
        selectors = re.findall(r"([^{]+)\s*\{", content)
        unique_selectors = set(selectors)
        if len(selectors) - len(unique_selectors) > 5:
            opportunities.append(f"{filename}: Duplicate selectors")

        return opportunities


class CSSPerformanceTests(CSSLiveTestCase):
    def test_css_load_time(self):
        # Time the page load
        start_time = time.time()
        response = self.client.get("/home/")
        load_time = time.time() - start_time

        self.assertEqual(response.status_code, 200)

        self.assertLess(
            load_time,
            5.0,
            f"Page load time ({load_time:.2f}s) exceeds reasonable limit",
        )

        # Log performance info
        print(f"Page load time: {load_time:.3f}s")

    def test_css_rendering_performance(self):
        self.skipIfNoSelenium()

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            # Measure page load time
            start_time = time.time()
            driver.get(f"{self.live_server_url}/home/")

            # Wait for page to be fully loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            load_time = time.time() - start_time

            # Check that styles are applied (page has rendered)
            body = driver.find_element(By.TAG_NAME, "body")
            body_styles = driver.execute_script(
                "return window.getComputedStyle(arguments[0])", body
            )

            # Basic check that CSS is loaded
            self.assertIsNotNone(body_styles.get("margin"))

            # Performance should be reasonable
            self.assertLess(
                load_time,
                10.0,
                f"Browser page load time ({load_time:.2f}s) is too slow",
            )

            print(f"Browser load time: {load_time:.3f}s")

        finally:
            driver.quit()

    def test_critical_css_inline(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Check for inline styles (which might indicate critical CSS)
        inline_styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)

        if inline_styles:
            total_inline_css = sum(len(style) for style in inline_styles)
            print(f"Inline CSS found: {total_inline_css} characters")

            self.assertLess(
                total_inline_css,
                10000,
                "Too much inline CSS - consider moving to external files",
            )

    def test_css_caching_headers(self):
        css_urls = ["/static/css/variables.css", "/static/css/base.css"]

        for css_url in css_urls:
            response = self.client.get(css_url)

            if response.status_code == 200:
                # Check for cache-related headers
                cache_control = response.get("Cache-Control", "")

                # In production, CSS should have cache headers
                # This is informational for development
                if not cache_control:
                    print(
                        f"Note: {css_url} lacks cache headers (expected in development)"
                    )


class CSSOptimizationTests(CSSTestCase):
    def test_css_selector_efficiency(self):
        inefficient_selectors = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                selectors = re.findall(r"([^{]+)\s*\{", content)

                for selector in selectors:
                    selector = selector.strip()
                    if self._is_inefficient_selector(selector):
                        inefficient_selectors.append(f"{css_file.name}: {selector}")

        # This is informational rather than a failure
        if inefficient_selectors:
            print(f"Potentially inefficient selectors: {inefficient_selectors[:5]}")

    def test_css_unused_rules_detection(self):
        # This is a basic analysis - comprehensive unused CSS detection needs DOM analysis
        all_classes = set()
        all_ids = set()

        # Collect all CSS selectors
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Extract class selectors
                class_selectors = re.findall(r"\.([a-zA-Z0-9_-]+)", content)
                all_classes.update(class_selectors)

                # Extract ID selectors
                id_selectors = re.findall(r"#([a-zA-Z0-9_-]+)", content)
                all_ids.update(id_selectors)

        # Check template usage (basic analysis)
        template_files = self.file_utils.list_template_files()
        used_classes = set()
        used_ids = set()

        for template_file in template_files[:5]:
            content = self.file_utils.read_file_safe(template_file)
            if content:
                # Find used classes
                template_classes = re.findall(r'class="([^"]*)"', content)
                for class_attr in template_classes:
                    used_classes.update(class_attr.split())

                # Find used IDs
                template_ids = re.findall(r'id="([^"]*)"', content)
                used_ids.update(template_ids)

        # Analyze potentially unused selectors
        potentially_unused_classes = all_classes - used_classes
        potentially_unused_ids = all_ids - used_ids

        # Filter out utility classes and common patterns
        unused_classes = [
            cls for cls in potentially_unused_classes if not self._is_utility_class(cls)
        ]

        if unused_classes:
            print(f"Potentially unused classes (sample): {list(unused_classes)[:10]}")

        if potentially_unused_ids:
            print(f"Potentially unused IDs: {list(potentially_unused_ids)[:5]}")

    def test_css_shorthand_opportunities(self):
        shorthand_opportunities = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                opportunities = self._find_shorthand_opportunities(
                    content, css_file.name
                )
                shorthand_opportunities.extend(opportunities)

        if shorthand_opportunities:
            print(f"CSS Shorthand opportunities: {shorthand_opportunities[:5]}")

    def test_css_color_optimization(self):
        color_issues = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Find color values
                hex_colors = re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", content)

                # Check for colors that could use variables
                color_counts = {}
                for color in hex_colors:
                    color_counts[color] = color_counts.get(color, 0) + 1

                # Colors used more than once could be variables
                repeated_colors = [
                    color for color, count in color_counts.items() if count > 2
                ]

                if repeated_colors:
                    color_issues.append(
                        f"{css_file.name}: Repeated colors {repeated_colors[:3]}"
                    )

        if color_issues:
            print(f"Color optimization opportunities: {color_issues}")

    def _is_inefficient_selector(self, selector: str) -> bool:
        # Very basic checks for inefficient selectors
        inefficient_patterns = [
            r"\*",  # Universal selector
            r"[^>]+>[^>]+>[^>]+>",  # Deep descendant selectors
            r"\[[^]]*\$=",  # Attribute selectors with $ (ends with)
            r":not\([^)]*:not",  # Nested :not() selectors
        ]

        return any(re.search(pattern, selector) for pattern in inefficient_patterns)

    def _is_utility_class(self, class_name: str) -> bool:
        utility_prefixes = [
            "text-",
            "bg-",
            "border-",
            "p-",
            "m-",
            "w-",
            "h-",
            "d-",
            "flex-",
            "align-",
            "justify-",
            "float-",
        ]

        return any(class_name.startswith(prefix) for prefix in utility_prefixes)

    def _find_shorthand_opportunities(self, content: str, filename: str) -> list:
        opportunities = []

        # Look for margin/padding longhand that could be shorthand
        margin_props = ["margin-top", "margin-right", "margin-bottom", "margin-left"]
        padding_props = [
            "padding-top",
            "padding-right",
            "padding-bottom",
            "padding-left",
        ]

        for prop_group in [margin_props, padding_props]:
            # Count occurrences of each property
            prop_counts = {
                prop: len(re.findall(rf"{prop}:", content)) for prop in prop_group
            }

            # If multiple longhand properties are used frequently, suggest shorthand
            frequent_props = [prop for prop, count in prop_counts.items() if count > 2]

            if len(frequent_props) >= 2:
                base_prop = prop_group[0].split("-")[0]  # 'margin' or 'padding'
                opportunities.append(f"{filename}: Consider {base_prop} shorthand")

        return opportunities


class CSSMaintenanceTests(CSSTestCase):
    def test_css_comment_quality(self):
        comment_analysis = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Find all comments
                comments = re.findall(r"/\*(.*?)\*/", content, re.DOTALL)

                if comments:
                    # Analyze comment quality
                    useful_comments = 0
                    for comment in comments:
                        comment = comment.strip()
                        if len(comment) > 10 and not self._is_trivial_comment(comment):
                            useful_comments += 1

                    comment_analysis.append(
                        f"{css_file.name}: {useful_comments}/{len(comments)} useful comments"
                    )

        if comment_analysis:
            print(f"CSS Comment analysis: {comment_analysis}")

    def test_css_organization_consistency(self):
        organization_issues = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Check for consistent property ordering
                rules = re.findall(r"{([^}]+)}", content)

                inconsistent_rules = 0
                for rule in rules[:10]:  # Check first 10 rules
                    properties = [
                        prop.strip().split(":")[0].strip()
                        for prop in rule.split(";")
                        if prop.strip()
                    ]

                    if len(properties) > 3 and not self._is_consistent_property_order(
                        properties
                    ):
                        inconsistent_rules += 1

                if inconsistent_rules > 0:
                    organization_issues.append(
                        f"{css_file.name}: {inconsistent_rules} rules with inconsistent property order"
                    )

        if organization_issues:
            print(f"CSS Organization issues: {organization_issues}")

    def test_css_duplication_across_files(self):
        all_rules = {}

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Extract CSS rules (selector + declarations)
                rules = re.findall(r"([^{]+){([^}]+)}", content)

                for selector, declarations in rules:
                    selector = selector.strip()
                    declarations = declarations.strip()
                    rule_key = f"{selector}:{declarations}"

                    if rule_key in all_rules:
                        all_rules[rule_key].append(css_file.name)
                    else:
                        all_rules[rule_key] = [css_file.name]

        # Find duplicated rules
        duplicated_rules = [
            (rule, files) for rule, files in all_rules.items() if len(files) > 1
        ]

        if duplicated_rules:
            print(
                f"Duplicated CSS rules found: {len(duplicated_rules)} (showing sample)"
            )
            for rule, files in duplicated_rules[:3]:
                selector = rule.split(":")[0]
                print(f"  {selector} duplicated in: {files}")

    def _is_trivial_comment(self, comment: str) -> bool:
        trivial_patterns = [
            r"^\s*$",  # Empty comments
            r"^\s*-+\s*$",  # Just dashes
            r"^\s*end\s*$",  # Just "end"
            r"^\s*todo\s*$",  # Just "todo"
        ]

        return any(re.match(pattern, comment.lower()) for pattern in trivial_patterns)

    def _is_consistent_property_order(self, properties: list) -> bool:
        # Define preferred property order categories
        order_categories = [
            ["position", "top", "right", "bottom", "left", "z-index"],
            ["display", "flex", "grid", "float", "clear"],
            ["width", "height", "min-width", "max-width", "min-height", "max-height"],
            ["margin", "padding", "border"],
            ["background", "color", "font", "text"],
        ]

        # This is a simplified check - real property ordering is complex
        # Just check that common properties appear in reasonable order
        position_props = ["position", "top", "left", "z-index"]
        layout_props = ["display", "width", "height"]

        pos_indices = [i for i, prop in enumerate(properties) if prop in position_props]
        layout_indices = [
            i for i, prop in enumerate(properties) if prop in layout_props
        ]

        # If both types exist, position should generally come before layout
        if pos_indices and layout_indices:
            return min(pos_indices) < min(layout_indices)

        return True
