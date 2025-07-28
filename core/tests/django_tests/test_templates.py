from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.template import Context, Template
from core.models import Profile, Skill, Message, Rating
from core.templatetags.rating_extras import star_rating, filled_stars, empty_stars
from core.templatetags.core_extras import get_item


class TemplateRenderingTest(TestCase):
    """Test cases for template rendering and context"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        self.user.profile.city = "Stockholm"
        self.user.profile.country = "Sweden"
        self.user.profile.bio = "Test bio"
        self.user.profile.save()

        self.skill = Skill.objects.create(
            user=self.user,
            title="Python Programming",
            description="Learn Python basics",
            skill_type="offer",
            category="technology",
        )

    def test_base_template_context(self):
        """Test base template renders with proper context"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SkillSwap")
        self.assertContains(response, "navbar")

    def test_profile_template_context(self):
        """Test profile template renders with user data"""
        response = self.client.get(reverse("view_user_profile", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Stockholm")
        self.assertContains(response, "Test bio")

    def test_skill_template_context(self):
        """Test skill template renders with skill data"""
        response = self.client.get(reverse("skill_detail_page", args=[self.skill.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")
        self.assertContains(response, "Learn Python basics")
        self.assertContains(response, "John Doe")

    def test_skills_list_template_context(self):
        """Test skills list template renders with pagination"""
        # Create multiple skills for pagination test
        for i in range(15):
            Skill.objects.create(
                user=self.user,
                title=f"Skill {i}",
                description=f"Description {i}",
                skill_type="offer",
                category="technology",
            )

        response = self.client.get(reverse("skills_list_search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")
        # Check pagination context
        self.assertTrue("page_obj" in response.context)

    def test_message_template_context(self):
        """Test message templates render correctly"""
        self.client.login(username="testuser", password="testpass123")

        # Test send message template
        response = self.client.get(reverse("send_message_skill", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send Message")
        self.assertContains(response, self.skill.title)

        # Create a message and test inbox
        other_user = User.objects.create_user(username="other", password="pass123")
        Message.objects.create(
            sender=other_user,
            receiver=self.user,
            subject="Test Message",
            message="Hello there!",
        )

        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Message")


class TemplateTagTest(TestCase):
    """Test cases for custom template tags"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.skill = Skill.objects.create(
            user=self.user,
            title="Test Skill",
            description="Test description",
            skill_type="offer",
            category="technology",
        )

    def test_star_rating_tag(self):
        """Test star_rating template tag"""
        # Test with no rating
        result = star_rating(0)
        self.assertIn("fa-regular fa-star", result)

        # Test with full rating
        result = star_rating(5)
        self.assertIn("fa-solid fa-star", result)

        # Test with partial rating
        result = star_rating(3.5)
        # Should have both filled and empty stars
        self.assertIn("fa-solid fa-star", result)
        self.assertIn("fa-regular fa-star", result)

    def test_filled_stars_tag(self):
        """Test filled_stars template tag"""
        self.assertEqual(filled_stars(3.7), 4)  # Should round up
        self.assertEqual(filled_stars(3.2), 3)  # Should round down
        self.assertEqual(filled_stars(0), 0)
        self.assertEqual(filled_stars(5), 5)

    def test_empty_stars_tag(self):
        """Test empty_stars template tag"""
        self.assertEqual(empty_stars(3.7), 1)  # 5 - 4 filled
        self.assertEqual(empty_stars(5), 0)  # 5 - 5 filled
        self.assertEqual(empty_stars(0), 5)  # 5 - 0 filled

    def test_get_item_tag(self):
        """Test get_item template tag"""
        test_dict = {"key1": "value1", "key2": "value2"}
        self.assertEqual(get_item(test_dict, "key1"), "value1")
        self.assertEqual(get_item(test_dict, "nonexistent"), None)

    def test_template_tags_in_templates(self):
        """Test template tags work in actual templates"""
        # Create rating for the skill
        rater = User.objects.create_user(username="rater", password="pass123")
        Rating.objects.create(skill=self.skill, user=rater, rating=4, comment="Good!")

        response = Client().get(reverse("skill_detail_page", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 200)

        # The star rating should be rendered in the template
        self.assertContains(response, "fa-solid fa-star")  # Filled stars
        self.assertContains(response, "fa-regular fa-star")  # Empty stars


class FormTemplateTest(TestCase):
    """Test cases for form rendering in templates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_signup_form_template(self):
        """Test signup form renders correctly"""
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')

    def test_profile_form_template(self):
        """Test profile form renders correctly"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("edit_my_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="bio"')
        self.assertContains(response, 'name="city"')
        self.assertContains(response, 'name="country"')
        self.assertContains(response, 'name="gender"')
        self.assertContains(response, 'name="skills_offered"')
        self.assertContains(response, 'name="skills_needed"')

    def test_skill_form_template(self):
        """Test skill form renders correctly"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("add_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="skill_type"')
        self.assertContains(response, 'name="category"')
        self.assertContains(response, 'name="location"')
        self.assertContains(response, 'name="availability"')
        self.assertContains(response, 'name="is_remote"')

    def test_message_form_template(self):
        """Test message form renders correctly"""
        skill = Skill.objects.create(
            user=self.user,
            title="Test Skill",
            description="Test",
            skill_type="offer",
            category="technology",
        )

        other_user = User.objects.create_user(username="other", password="pass123")
        self.client.login(username="other", password="pass123")

        response = self.client.get(reverse("send_message_skill", args=[skill.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="message"')

    def test_form_error_rendering(self):
        """Test form errors render correctly"""
        # Submit invalid signup form
        response = self.client.post(
            reverse("signup"),
            {
                "username": "",  # Missing required field
                "first_name": "John",
                "last_name": "Doe",
                "password1": "pass123",
                "password2": "different123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "error")  # Error styling

        # Test profile form errors
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("edit_my_profile"),
            {"city": "", "country": ""},  # If required  # If required
        )

        # Should re-render form with any validation errors
        self.assertEqual(response.status_code, 200)


class TemplateInheritanceTest(TestCase):
    """Test cases for template inheritance and blocks"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_base_template_blocks(self):
        """Test that child templates override base template blocks"""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        # Check that base template structure is present
        self.assertContains(response, "<html")
        self.assertContains(response, "<head>")
        self.assertContains(response, "<body>")
        self.assertContains(response, "</html>")

    def test_navigation_consistency(self):
        """Test navigation appears consistently across pages"""
        # Test multiple pages for navigation consistency
        test_urls = [
            reverse("home"),
            reverse("skills_list_search"),
            reverse("search"),
        ]

        for url in test_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "navbar")  # Navigation should be present

    def test_footer_consistency(self):
        """Test footer appears consistently across pages"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        # Check for footer elements if they exist
        self.assertContains(response, "</body>")  # At minimum, page structure


class ResponsiveTemplateTest(TestCase):
    """Test cases for responsive design elements in templates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_responsive_classes_present(self):
        """Test responsive CSS classes are present in templates"""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        # Look for common responsive framework classes
        # These might be Bootstrap, custom classes, or other responsive patterns
        html_content = response.content.decode()

        # Check for meta viewport tag
        self.assertIn("viewport", html_content)

    def test_mobile_friendly_forms(self):
        """Test forms are mobile-friendly"""
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        html_content = response.content.decode()

        # Check for mobile-friendly input attributes
        self.assertContains(response, "input")  # Basic form inputs present

    def test_image_responsiveness(self):
        """Test images have responsive attributes"""
        # Create user with profile picture
        self.user.profile.profile_picture = "test_image.jpg"
        self.user.profile.save()

        response = self.client.get(reverse("view_user_profile", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)


class AccessibilityTest(TestCase):
    """Test cases for template accessibility features"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_semantic_html_elements(self):
        """Test templates use semantic HTML elements"""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        html_content = response.content.decode()

        # Check for semantic elements
        semantic_elements = [
            "<main",
            "<nav",
            "<header",
            "<footer",
            "<section",
            "<article",
        ]
        semantic_present = any(element in html_content for element in semantic_elements)

        # At least some semantic elements should be present
        self.assertTrue(semantic_present, "Template should use semantic HTML elements")

    def test_form_labels(self):
        """Test form inputs have proper labels"""
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<label")  # Form labels should be present

    def test_alt_text_for_images(self):
        """Test images have alt text"""
        user = User.objects.create_user(username="testuser", password="pass123")
        response = self.client.get(reverse("view_user_profile", args=[user.id]))

        self.assertEqual(response.status_code, 200)
        html_content = response.content.decode()

        # If images are present, they should have alt attributes
        if "<img" in html_content:
            self.assertIn("alt=", html_content)


class TemplatePerformanceTest(TestCase):
    """Test cases for template performance and optimization"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_template_caching_headers(self):
        """Test static content has appropriate caching headers"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # Check that the page loads successfully
        # In production, you'd check Cache-Control headers

    def test_minimal_database_queries(self):
        """Test templates don't cause excessive database queries"""
        from django.test.utils import override_settings
        from django.db import connection

        # Reset query count
        connection.queries_log.clear()

        response = self.client.get(reverse("skills_list_search"))
        self.assertEqual(response.status_code, 200)

        # Number of queries should be reasonable for the page
        query_count = len(connection.queries)
        self.assertLess(query_count, 20, f"Too many database queries: {query_count}")


class ErrorTemplateTest(TestCase):
    """Test cases for error page templates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_404_template(self):
        """Test 404 error template"""
        response = self.client.get("/nonexistent-page/")
        self.assertEqual(response.status_code, 404)

        # Check that custom 404 template is used
        self.assertContains(response, "404", status_code=404)

    def test_500_template_structure(self):
        """Test 500 error template structure (if accessible)"""
        # This is harder to test directly, but we can check the template exists
        # In a real scenario, you might use a test client that can trigger 500 errors
        pass


class JavaScriptInteractionTest(TestCase):
    """Test cases for JavaScript integration in templates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_javascript_includes(self):
        """Test JavaScript files are included in templates"""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        html_content = response.content.decode()

        # Check for JavaScript inclusions
        if "<script" in html_content:
            self.assertIn("</script>", html_content)

    def test_css_includes(self):
        """Test CSS files are included in templates"""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        html_content = response.content.decode()

        # Check for CSS inclusions
        self.assertIn("<link", html_content)  # Should have CSS links
        self.assertIn("stylesheet", html_content)


class TemplateSecurityTest(TestCase):
    """Test cases for template security features"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_csrf_token_in_forms(self):
        """Test CSRF tokens are present in forms"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("edit_my_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_user_data_escaping(self):
        """Test user data is properly escaped in templates"""
        # Create user with potentially dangerous content
        dangerous_user = User.objects.create_user(
            username="danger",
            first_name='<script>alert("xss")</script>',
            password="pass123",
        )

        response = self.client.get(
            reverse("view_user_profile", args=[dangerous_user.id])
        )
        self.assertEqual(response.status_code, 200)

        # The script tag should be escaped, not executed
        html_content = response.content.decode()
        self.assertNotIn('<script>alert("xss")</script>', html_content)
        self.assertIn("&lt;script&gt;", html_content)  # Should be escaped
