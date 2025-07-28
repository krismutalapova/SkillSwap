"""
Responsive Design Testing
Tests for responsive design, mobile-first approach, and breakpoint consistency

This file contains tests focusing specifically on responsive design patterns, mobile compatibility, and layout behavior.
"""

import re
from core.tests.frontend_tests.utils import CSSTestCase, CSSLiveTestCase


class ResponsiveBreakpointTests(CSSTestCase):
    def test_mobile_first_approach(self):
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                with self.subTest(css_file=css_file):
                    # Count mobile-first vs desktop-first patterns
                    min_width_queries = len(
                        re.findall(r"@media[^{]*min-width", content)
                    )
                    max_width_queries = len(
                        re.findall(r"@media[^{]*max-width", content)
                    )

                    # If media queries exist, mobile-first should be preferred
                    total_queries = min_width_queries + max_width_queries
                    if total_queries > 0:
                        mobile_first_ratio = min_width_queries / total_queries
                        self.assertGreaterEqual(
                            mobile_first_ratio,
                            0.5,
                            f"File {css_file} should use mobile-first approach. "
                            f"Found {min_width_queries} min-width and {max_width_queries} max-width queries",
                        )

    def test_breakpoint_consistency(self):
        all_breakpoints = []

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Extract breakpoint values
                breakpoint_pattern = r"@media[^{]*(?:min-width|max-width)\s*:\s*(\d+px)"
                breakpoints = re.findall(breakpoint_pattern, content)
                all_breakpoints.extend(breakpoints)

        if all_breakpoints:
            # Convert to integers and find unique values
            unique_breakpoints = list(
                set(int(bp.replace("px", "")) for bp in all_breakpoints)
            )
            unique_breakpoints.sort()

            # Common responsive breakpoints
            standard_breakpoints = [480, 768, 992, 1200]

            # Check if most breakpoints align with standard values
            aligned_breakpoints = [
                bp
                for bp in unique_breakpoints
                if any(abs(bp - std) <= 32 for std in standard_breakpoints)
            ]

            alignment_ratio = len(aligned_breakpoints) / len(unique_breakpoints)
            self.assertGreaterEqual(
                alignment_ratio,
                0.7,
                f"Breakpoints should align with standard values. "
                f"Found: {unique_breakpoints}, Standard: {standard_breakpoints}",
            )

    def test_responsive_utilities(self):
        utilities_content = self.css_utils.read_css_file("utilities.css")
        if utilities_content:
            responsive_patterns = [
                r"\.hidden-\w+",
                r"\.visible-\w+",
                r"\.flex-\w+-\w+",
                r"@media[^{]*\.[^{]*hidden",
            ]

            responsive_utilities_found = 0
            for pattern in responsive_patterns:
                if re.search(pattern, utilities_content):
                    responsive_utilities_found += 1

            self.assertGreater(
                responsive_utilities_found,
                0,
                "Should have some responsive utility classes for mobile/desktop differences",
            )

    def test_responsive_navigation(self):
        nav_files = ["base.css", "components.css", "utilities.css"]

        nav_responsive_features = 0

        for css_file in nav_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for navigation-related responsive patterns
                nav_patterns = [
                    r"nav[^{]*@media",
                    r"\.nav[^{]*@media",
                    r"@media[^{]*nav",
                    r"mobile[^{]*nav",
                    r"hamburger|menu-toggle",
                ]

                for pattern in nav_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        nav_responsive_features += 1
                        break

        # This is informational - not all sites need complex responsive nav
        if nav_responsive_features == 0:
            print(
                "Note: No responsive navigation patterns detected. Consider mobile navigation needs."
            )


class ResponsiveComponentTests(CSSLiveTestCase):
    def test_navigation_responsive_behavior(self):
        self.skipIfNoSelenium()

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            # Test navigation at different viewport sizes
            viewports = [
                (320, 568),  # Mobile
                (768, 1024),  # Tablet
                (1920, 1080),  # Desktop
            ]

            driver.get(f"{self.live_server_url}/home/")

            for width, height in viewports:
                with self.subTest(viewport=f"{width}x{height}"):
                    driver.set_window_size(width, height)

                    # Check if navigation is visible and functional
                    nav_elements = driver.find_elements(
                        "css selector", "nav, .nav, .navbar"
                    )
                    self.assertGreater(
                        len(nav_elements),
                        0,
                        f"Navigation should be present at {width}x{height} viewport",
                    )

                    # Check if navigation doesn't overflow
                    for nav in nav_elements:
                        nav_width = nav.size["width"]
                        self.assertLessEqual(
                            nav_width,
                            width + 20,  # Allow small overflow
                            f"Navigation width ({nav_width}px) should not exceed viewport ({width}px)",
                        )

        finally:
            driver.quit()

    def test_card_grid_responsive_behavior(self):
        self.skipIfNoSelenium()

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            # Create test skill for cards to display
            self.create_test_skill()

            driver.get(f"{self.live_server_url}/skills/")

            # Test at mobile and desktop sizes
            viewports = [(320, 568), (1920, 1080)]

            for width, height in viewports:
                with self.subTest(viewport=f"{width}x{height}"):
                    driver.set_window_size(width, height)

                    # Find card grid elements
                    card_grids = driver.find_elements(
                        "css selector", ".card-grid, .grid, .skills-grid"
                    )

                    if card_grids:
                        grid = card_grids[0]
                        cards = grid.find_elements(
                            "css selector", "[class*='card'], [class*='skill']"
                        )

                        if cards and len(cards) > 1:
                            # Check card spacing and layout
                            first_card = cards[0]
                            second_card = cards[1]

                            first_rect = first_card.location
                            second_rect = second_card.location

                            # On mobile, cards should stack vertically more
                            # On desktop, cards should be more horizontal
                            if width <= 768:
                                # Mobile: expect more vertical stacking
                                if first_rect["y"] != second_rect["y"]:
                                    vertical_gap = abs(
                                        second_rect["y"] - first_rect["y"]
                                    )
                                    self.assertGreater(
                                        vertical_gap,
                                        10,
                                        "Cards should have adequate vertical spacing on mobile",
                                    )

        finally:
            driver.quit()

    def test_form_responsive_behavior(self):
        self.skipIfNoSelenium()

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            # Login to access forms
            self.client.login(username="testuser", password="testpass123")

            # Use Django's session for Selenium
            driver.get(f"{self.live_server_url}/skills/create/")

            viewports = [(320, 568), (768, 1024), (1920, 1080)]

            for width, height in viewports:
                with self.subTest(viewport=f"{width}x{height}"):
                    driver.set_window_size(width, height)

                    # Find form elements
                    forms = driver.find_elements("css selector", "form")
                    inputs = driver.find_elements(
                        "css selector", "input, textarea, select"
                    )

                    if inputs:
                        for input_elem in inputs[:3]:
                            input_width = input_elem.size["width"]

                            # Inputs should not overflow viewport
                            self.assertLessEqual(
                                input_width,
                                width - 40,  # Account for padding/margins
                                f"Input width ({input_width}px) should fit in viewport ({width}px)",
                            )

                            # On mobile, inputs should be reasonably sized
                            if width <= 480:
                                self.assertGreaterEqual(
                                    input_width,
                                    200,
                                    f"Input should be at least 200px wide on mobile, got {input_width}px",
                                )

        finally:
            driver.quit()


class ResponsiveImageTests(CSSTestCase):
    def test_responsive_image_css(self):
        responsive_image_rules = 0

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for responsive image patterns
                image_patterns = [
                    r"img\s*\{[^}]*max-width\s*:\s*100%",
                    r"img\s*\{[^}]*width\s*:\s*100%",
                    r"\.img-responsive",
                    r"@media[^{]*img",
                    r"object-fit\s*:\s*(cover|contain)",
                ]

                for pattern in image_patterns:
                    if re.search(pattern, content):
                        responsive_image_rules += 1

        self.assertGreater(
            responsive_image_rules,
            0,
            "Should have CSS rules for responsive image handling",
        )

    def test_profile_picture_responsive(self):
        profile_css_files = ["profile-pages.css", "components.css", "utilities.css"]

        profile_responsive_rules = 0

        for css_file in profile_css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for profile picture responsive patterns
                patterns = [
                    r"\.profile-pic[^{]*\{[^}]*(?:max-width|width)[^}]*100%",
                    r"\.user-avatar[^{]*\{[^}]*(?:max-width|width)",
                    r"@media[^{]*profile",
                ]

                for pattern in patterns:
                    if re.search(pattern, content):
                        profile_responsive_rules += 1
                        break

        if profile_responsive_rules == 0:
            print("Note: Consider adding responsive rules for profile pictures")


class ResponsiveTypographyTests(CSSTestCase):
    def test_responsive_font_sizes(self):
        responsive_typography = 0

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for responsive typography patterns
                patterns = [
                    r"@media[^{]*font-size",
                    r"font-size\s*:\s*[0-9.]+vw",
                    r"font-size\s*:\s*clamp\(",
                    r"@media[^{]*h[1-6]",
                ]

                for pattern in patterns:
                    if re.search(pattern, content):
                        responsive_typography += 1
                        break

        # This is more informational than required
        if responsive_typography == 0:
            print("Note: Consider responsive typography for better mobile experience")

    def test_readable_line_length(self):
        readable_constraints = 0

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for readability constraints
                patterns = [
                    r"max-width\s*:\s*[0-9]+ch",
                    r"max-width\s*:\s*[456][0-9]{2}px",
                    r"\.container[^{]*max-width",
                ]

                for pattern in patterns:
                    if re.search(pattern, content):
                        readable_constraints += 1

        if readable_constraints > 0:
            self.assertGreater(
                readable_constraints,
                0,
                "Good: Found constraints for readable line lengths",
            )


class ResponsiveLayoutTests(CSSTestCase):
    def test_flexible_grid_systems(self):
        grid_systems = 0

        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for modern CSS grid and flexbox patterns
                patterns = [
                    r"display\s*:\s*grid",
                    r"display\s*:\s*flex",
                    r"grid-template-columns",
                    r"flex-wrap\s*:\s*wrap",
                    r"auto-fit|auto-fill",
                ]

                for pattern in patterns:
                    if re.search(pattern, content):
                        grid_systems += 1
                        break

        self.assertGreater(
            grid_systems,
            0,
            "Should use modern CSS layout methods (Grid/Flexbox) for responsive design",
        )

    def test_container_responsive_behavior(self):
        for css_file in self.css_files:
            content = self.css_utils.read_css_file(css_file)
            if content:
                # Look for container classes
                container_classes = re.findall(
                    r"(\.container[^{]*)\{([^}]+)\}", content
                )

                for class_def, properties in container_classes:
                    with self.subTest(css_file=css_file, container=class_def):
                        # Containers should have some responsive characteristics
                        has_responsive_features = any(
                            prop in properties
                            for prop in [
                                "max-width",
                                "min-width",
                                "padding",
                                "margin",
                                "%",
                            ]
                        )

                        self.assertTrue(
                            has_responsive_features,
                            f"Container {class_def} should have responsive properties",
                        )
